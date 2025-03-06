from typing import Optional
from fastapi import APIRouter, HTTPException
import xml.etree.ElementTree as ET
import cloudscraper
import redis
import json

app = APIRouter()

# Подключение к Redis
redis_client = redis.Redis(host='redis', port=6379, db=0)

async def fetch_data_from_api():
    scraper = cloudscraper.create_scraper()
    response = scraper.get("https://steam-account.ru/partner/products.xml")
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            products = []
            for product in root.findall("product"):
                product_data = {
                    "id": product.find("id").text if product.find("id") is not None else None,
                    "name": product.find("name").text if product.find("name") is not None else None,
                    "url": product.find("url").text if product.find("url") is not None else None,
                    "price": product.find("price").text if product.find("price") is not None else None,
                    "activation": product.find("activation").text if product.find("activation") is not None else None,
                    "region": product.find("region").text if product.find("region") is not None else None,
                    "view": product.find("view").text if product.find("view") is not None else None,
                }
                if product_data["url"]:
                    product_data["url"] = product_data["url"] + "?ai=1345858"
                products.append(product_data)
            return products
        except ET.ParseError as e:
            raise HTTPException(status_code=500, detail="Failed to parse XML")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

async def get_cached_or_fetch_data():
    cached_data = redis_client.get("steam_products")
    if cached_data:
        return json.loads(cached_data)
    else:
        data = await fetch_data_from_api()
        redis_client.set("steam_products", json.dumps(data), ex=3600)  # Устанавливаем TTL 60 минут
        return data

@app.get('/get_min_steam_account/{name}')
async def get_min_steam_account(name: str):
    products = await get_cached_or_fetch_data()
    filtered_products = [product for product in products if name.lower() in product['name'].lower()]
    if filtered_products:
        sorted_products = sorted(filtered_products, key=lambda x: x['price'])
        cheapest_product = sorted_products[0]
        return cheapest_product
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/get_max_steam_account/{name}')
async def get_max_steam_account(name: str):
    products = await get_cached_or_fetch_data()
    filtered_products = [product for product in products if name.lower() in product['name'].lower()]
    if filtered_products:
        sorted_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
        most_expensive_product = sorted_products[0]
        return most_expensive_product
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/get_range_steam_accounts/{name}&min={min}&max={max}')
async def get_range_steam_accounts(
    name: str,
    min: int,
    max: int,
    direction: Optional[bool] = None
):
    products = await get_cached_or_fetch_data()
    filtered_products = [product for product in products if name.lower() in product['name'].lower()]
    if min is not None:
        filtered_products = [product for product in filtered_products if int(product['price']) >= min]
    if max is not None:
        filtered_products = [product for product in filtered_products if int(product['price']) <= max]
    if direction is not None:
        filtered_products = sorted(
            filtered_products,
            key=lambda x: x['price'],
            reverse=not direction
        )
    if filtered_products:
        return filtered_products
    else:
        raise HTTPException(status_code=404, detail="No products found")
