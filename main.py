from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import itertools
from fastapi.openapi.utils import get_openapi

app = FastAPI()

class Car(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    color: str
    price_per_day: float
    available:  bool

id_gen = itertools.count(1)

cars_db = []

# получение всех автомобилей
@app.get("/cars", response_model = List[Car])
async def get_cars():
    return cars_db

# создание автомобиля
@app.post("/cars", response_model=Car)
async def create_car(car: Car):
    car.id = next(id_gen)  # Обновленный способ задания ID
    cars_db.append(car)  # Прямое добавление объекта car в базу данных
    return car

# получение автомобиля по конкретному id
@app.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int):
    for car in cars_db:
        if car.id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")

# обновление конкретного автомобиля по id
@app.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, updated_car: Car):
    for i, car in enumerate(cars_db):
        if car.id == car_id:
            cars_db[i] = updated_car  # Прямая замена объекта автомобиля в базе данных
            return updated_car
    raise HTTPException(status_code=404, detail="Car not found")

# удаление  конкретного автомобиля по id
@app.delete("/cars/{car_id}", response_model=Car)
async def delete_car(car_id: int):
    for i, car in enumerate(cars_db):
        if car.id == car_id:
            del_car = cars_db.pop(i)
            return del_car
    raise HTTPException(status_code=404, detail="Car not found")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Car Rental API",
        version="1.0.0",
        description="This is a simple API for managing car rentals.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if  __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port = 8000)