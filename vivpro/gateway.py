import json
from typing import Union
from repo import DataStore
from fastapi import Request, FastAPI, HTTPException, Query
app = FastAPI()

ds = DataStore()


@app.get("/get_data")
async def get_data(request: Request, title: str = Query(None), page: int = Query(1, gt=0), size: int = Query(10, gt=0)):
    query_params = dict(request.query_params)
    filters = {key: query_params[key] for key in query_params if key not in ["page", "size"]}
    result = ds.get_info_by_filter(**filters)

    total_items = len(result)
    start = (page - 1) * size
    end = start + size
    paginated_result = result.iloc[start:end]
    
    return {
        "page": page,
        "size": size,
        "total_items": total_items,
        "total_pages": (total_items // size) + (1 if total_items % size != 0 else 0),
        "data": paginated_result.to_dict(orient='records')
    }

@app.post("/process_and_save_data")
async def process_and_save_data(request: Request):
    try:
        body = await request.json()
        ds.process_and_save_data(body)
        return {"message": "Data processed and saved successfully"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/rate_song/{song_title}/{rating}")
async def rate_song(request: Request, song_title: str, rating: int):
    try:
        filter = {"title": song_title}
        ds.update_field('rating', rating, **filter)
        return {"message": "Song rated successfully"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

