from typing import Optional
from fastapi import APIRouter, HTTPException
from FunPayAPI import Account, Runner, types, enums
import asyncio

app = APIRouter()

TOKEN = "82eldrke1yvymsgm71gg82qy7jjinb44"
acc = Account(TOKEN).get()
runner = Runner(acc)

async def get_items():
    result = []
    items = acc.get_sorted_categories()
    if not items:
        raise HTTPException(status_code=404, detail="Товары не найдены")

    for cat in items.values():
        subcats = cat.get_subcategories()
        result.append({
            "id": cat.id,
            "name": cat.name,
            "subs": [subcats[i].id for i in range(len(subcats))],
            "subs_type": [subcats[i].type for i in range(len(subcats))]
        }
        )

    return result

@app.get("/get_min_funpay/{name}")
async def get_funpay_min(name: str):
    result = await get_items()

    lot_fields = []
    for i in range(len(result)):
        if result[i]["name"].lower() == name.lower():
            for j in range(len(result[i]["subs"])):
                try:
                    #print("call lot: ", result[i]["subs"][j])
                    lot_field = acc.get_subcategory_public_lots(result[i]["subs_type"][j], result[i]["subs"][j])
                    #print(lot_field[1].subcategory.name)
                    if lot_field:
                        for k in range(len(lot_field)):
                            if lot_field[k].subcategory.name == "Аккаунты" or lot_field[k].subcategory.name == "Ключи":
                                lot_fields.append([lot_field[k].price, lot_field[k].id, lot_field[k].title, lot_field[k].public_link])
                                #print(lot_fields)

                except Exception as e:
                    print(f"Error getting lot fields for subcat {result[i]['subs'][j]}: {e}")
    minimum = float('inf')
    min_item = []
    for i in range(len(lot_fields)):
        if lot_fields[i][0] < minimum:
            min_item = lot_fields[i]
            minimum = lot_fields[i][0]

    return { "price": min_item[0], "id": min_item[1], "name": min_item[2], "url": min_item[3] }

@app.get("/get_max_funpay/{name}")
async def get_funpay_max(name: str):
    result = await get_items()

    lot_fields = []
    for i in range(len(result)):
        if result[i]["name"].lower() == name.lower():
            for j in range(len(result[i]["subs"])):
                try:
                    #print("call lot: ", result[i]["subs"][j])
                    lot_field = acc.get_subcategory_public_lots(result[i]["subs_type"][j], result[i]["subs"][j])
                    #print(lot_field[1].subcategory.name)
                    if lot_field:
                        for k in range(len(lot_field)):
                            if lot_field[k].subcategory.name == "Аккаунты" or lot_field[k].subcategory.name == "Ключи":
                                lot_fields.append([lot_field[k].price, lot_field[k].id, lot_field[k].title, lot_field[k].public_link])
                                #print(lot_fields)

                except Exception as e:
                    print(f"Error getting lot fields for subcat {result[i]['subs'][j]}: {e}")
    maximum = float('-inf')
    max_item = []
    for i in range(len(lot_fields)):
        if lot_fields[i][0] > maximum:
            max_item = lot_fields[i]
            maximum = lot_fields[i][0]

    return { "price": max_item[0], "id": max_item[1], "name": max_item[2], "url": max_item[3] }

@app.get("/get_range_funpay/{name}&min={min}&max={max}")
async def get_range_funpay(name: str, min: int, max: int):
    result = await get_items()

    lot_fields = []
    for i in range(len(result)):
        if result[i]["name"].lower() == name.lower():
            for j in range(len(result[i]["subs"])):
                try:
                    #print("call lot: ", result[i]["subs"][j])
                    lot_field = acc.get_subcategory_public_lots(result[i]["subs_type"][j], result[i]["subs"][j])
                    #print(lot_field[1].subcategory.name)
                    if lot_field:
                        for k in range(len(lot_field)):
                            if (lot_field[k].subcategory.name == "Аккаунты" or lot_field[k].subcategory.name == "Ключи"):
                                lot_fields.append({"price": lot_field[k].price,
                                                   "id": lot_field[k].id,
                                                   "name": lot_field[k].title,
                                                   "url": lot_field[k].public_link})
                                #print(lot_fields)

                except Exception as e:
                    print(f"Error getting lot fields for subcat {result[i]['subs'][j]}: {e}")

    sorted_items = []
    for item in lot_fields:
        if min <= item["price"] <= max:
            sorted_items.append(item)
    return sorted_items
