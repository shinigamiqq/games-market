from typing import Optional
from fastapi import APIRouter, HTTPException
import requests


app = APIRouter()

@app.get('/min_plati/{name}')
async def get_plati_min(name: str):
    request = requests.get(url=f"https://plati.io/api/search.ashx?query={name}&pagesize=40&visibleOnly=true&response=json")
    #print(request.json())
    if request.json()["total"] > 0:
        items = request.json()["items"]
        min_price = 10000000
        for i in range(len(items)):
            if items[i]["price_rur"] < min_price:
                min_price = items[i]["price_rur"]
                game_id = items[i]["id"]
                game_name = items[i]["name"]
                game_url = items[i]["url"]+"?ai=1345858"
                image = items[i]["image"]
        return {"price": min_price, "id": game_id,
                "name": game_name, "url": game_url, "image": image}
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/max_plati/{name}')
async def get_plati_max(name: str):
    request = requests.get(url=f"https://plati.io/api/search.ashx?query={name}&pagesize=40&visibleOnly=true&response=json")
    #print(request.json())
    if request.json()["total"] > 0:
        items = request.json()["items"]
        max_price = -1
        for i in range(len(items)):
            if items[i]["price_rur"] > max_price:
                max_price = items[i]["price_rur"]
                game_id = items[i]["id"]
                game_name = items[i]["name"]
                game_url = items[i]["url"]+"?ai=1345858"
                image = items[i]["image"]
        return {"price": max_price, "id": game_id,
                "name": game_name, "url": game_url, "image": image}
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/most_popular_plati/{name}')
async def get_plati_popular(name: str):
    request = requests.get(url=f"https://plati.io/api/search.ashx?query={name}&pagesize=40&visibleOnly=true&response=json")
    print(request.json())
    if request.json()["total"] > 0:
        items = request.json()["items"]
        numsold = -1
        for i in range(len(items)):
            if items[i]["numsold"] > numsold:
                numsold = items[i]["numsold"]
                game_id = items[i]["id"]
                game_name = items[i]["name"]
                game_url = items[i]["url"]+"?ai=1345858"
                price = items[i]["price_rur"]
                image = items[i]["image"]
        return { "numsold": numsold, "price": price, "id": game_id,
                "name": game_name, "url": game_url, "image": image }
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/get_range_plati/{name}&min={min}&max={max}')
async def get_plati_range(name: str, min: int, max: int, direction: Optional[bool] = None):
    request = requests.get(url=f"https://plati.io/api/search.ashx?query={name}&pagesize=40&visibleOnly=true&response=json")
    if request.json()["total"] > 0:
        sorted_items = []
        items = request.json()["items"]
        for i in range(len(items)):
            if items[i]["price_rur"] > min and items[i]["price_rur"] < max:
                items[i]["url"] = items[i]["url"]+"?ai=1345858"
                sorted_items.append(items[i])
        for item in sorted_items:
            item['price'] = item.pop('price_rur')
        if direction == True:
            sorted_items = sorted(sorted_items, key=lambda x: x["price"])
            return sorted_items
        if direction == False:
            sorted_items = sorted(sorted_items, key=lambda x: x["price"], reverse=True)
            return sorted_items
        return sorted_items
    else:
        raise HTTPException(status_code=404, detail="No products found")

