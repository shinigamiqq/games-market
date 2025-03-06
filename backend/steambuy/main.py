import json
from typing import Optional, get_overloads
from fastapi import APIRouter, HTTPException
import requests
from starlette.types import StatefulLifespan

app = APIRouter()

@app.get('/get_min_steambuy/{name}')
async def get_min_steam_buy(name: str):
    request = requests.get(url=f"https://steammachine.ru/api/search/?q={name}&v=1&format=json")
    if request.json()["response"]["data"] != None:
        goods = request.json()["response"]["data"]["goods"]
        #return(goods)
        min_price = 10000000
        good_id = None
        good_url = None
        good_name = None
        for i in range(len(goods)):
            if isinstance(goods[i]["price"], dict):
                price = int(goods[i]["price"]["rub"])
                if price < min_price:
                    min_price = price
                    good_id = goods[i]["id_good"]
                    good_url = goods[i]["url"]+"?partner=1345858"
                    good_name = goods[i]["name"]

        return {
            "name": good_name,
            "id": good_id,
            "url": good_url,
            "price": min_price
        }
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/get_max_steambuy/{name}')
async def get_max_steam_buy(name: str):
    request = requests.get(url=f"https://steammachine.ru/api/search/?q={name}&v=1&format=json")
    if request.json()["response"]["data"] is not None:
        goods = request.json()["response"]["data"]["goods"]

        max_price = -1
        good_id, good_url, good_name = None, None, None

        for good in goods:
            if isinstance(good["price"], dict):
                price = int(good["price"]["rub"])
                if price > max_price:
                    max_price = price
                    good_id = good["id_good"]
                    good_url = good["url"]+"?partner=1345858"
                    good_name = good["name"]

        if max_price == -1:
            return {"message": "No valid prices found"}

        return {
            "name": good_name,
            "id": good_id,
            "url": good_url,
            "price": max_price
        }
    else:
        raise HTTPException(status_code=404, detail="No products found")

@app.get('/get_range_steambuy/{name}&min={min}&max={max}')
async def get_range_steam_buy(name: str, min: int, max: int, direction: Optional[bool] = None):
    request = requests.get(url=f"https://steammachine.ru/api/search/?q={name}&v=1&format=json")
    if request.json()["response"]["data"] is not None:
         goods = request.json()["response"]["data"]["goods"]
         new_goods = []
         for good in goods:
             if isinstance(good["price"], dict):
                 price = int(good["price"]["rub"])
                 if price < max and price > min:
                     good["price"]["rub"] = price
                     good["url"] = good["url"]+"?partner=1345858"
                     new_goods.append(good)
         for good in new_goods:
             good['id'] = good.pop('id_good')
             good["price"] = good["price"]["rub"]
         if direction == True:
             new_goods = sorted(new_goods, key= lambda x: x["price"])
             return new_goods
         if direction == False:
             new_goods = sorted(new_goods, key= lambda x: x["price"], reverse=True)
             return new_goods
         return new_goods
    else:
         raise HTTPException(status_code=404, detail="No products found")
