# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.models import Meal, MealCreate
from typing import List, Optional

# Hardcoded meals data (no database)
meals_data = [
        {
            "id": "1",
            "title": "Whole Milk and Cottage Cheese",
            "description": "High-protein dairy combination for muscle building",
            "calories": "850 cal",
            "protein": "45g protein",
            "image": "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "bulking"
        },
        {
            "id": "2",
            "title": "Nuts and Nut Butters",
            "description": "Calorie-dense healthy fats and proteins",
            "calories": "720 cal",
            "protein": "25g protein",
            "image": "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "bulking"
        },
        {
            "id": "3",
            "title": "Whole Eggs",
            "description": "Complete protein with essential amino acids",
            "calories": "680 cal",
            "protein": "42g protein",
            "image": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "bulking"
        },
        {
            "id": "4",
            "title": "Rice",
            "description": "Complex carbohydrates for energy and recovery",
            "calories": "450 cal",
            "protein": "8g protein",
            "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "bulking"
        },
        {
            "id": "5",
            "title": "Chicken and Mutton",
            "description": "Lean protein sources for muscle development",
            "calories": "650 cal",
            "protein": "65g protein",
            "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "bulking"
        },
    # Add more meal items here as needed
    {
            "id": "6",
            "title": "Carbohydrates",
            "description": "Complex carbs for sustained energy during cuts",
            "calories": "320 cal",
            "protein": "12g protein",
            "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        },
        {
            "id": "7",
            "title": "Lean Fish",
            "description": "Low-calorie, high-protein white fish",
            "calories": "280 cal",
            "protein": "45g protein",
            "image": "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        },
        {
            "id": "8",
            "title": "Eggs",
            "description": "High-quality protein with essential nutrients",
            "calories": "180 cal",
            "protein": "24g protein",
            "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        },
        {
            "id": "9",
            "title": "Dairy",
            "description": "Low-fat dairy products for protein",
            "calories": "250 cal",
            "protein": "28g protein",
            "image": "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        },
        {
            "id": "10",
            "title": "Pulses (Lentils, Beans, Peas)",
            "description": "Plant-based protein and fiber",
            "calories": "200 cal",
            "protein": "18g protein",
            "image": "https://images.unsplash.com/photo-1586795158095-e891c9e1a42b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        },
        {
            "id": "11",
            "title": "Tofu, Seeds & Nuts",
            "description": "Plant-based proteins and healthy fats",
            "calories": "290 cal",
            "protein": "22g protein",
            "image": "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
            "category": "cutting"
        }
]

# FastAPI app setup
app = FastAPI(title="The Gym by Johnson API")

# API Routes
@app.get("/")
async def read_root():
    with open("static/index.html", "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/api/meals", response_model=List[Meal])
async def get_meals(category: Optional[str] = None):
    """
    Endpoint to fetch meals. Optionally, filter by category.
    """
    if category:
        meals = [meal for meal in meals_data if meal["category"] == category]
    else:
        meals = meals_data
    return meals

@app.get("/api/meals/{meal_id}", response_model=Meal)
async def get_meal(meal_id: str):
    """
    Endpoint to fetch a single meal by its ID.
    """
    meal = next((m for m in meals_data if m["id"] == meal_id), None)
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    return meal

@app.post("/api/meals", response_model=Meal)
async def create_meal(meal: MealCreate):
    """
    Create a new meal (this is optional if you just need a GET endpoint).
    """
    new_id = str(len(meals_data) + 1)  # Generate a new ID based on the length
    meal_dict = meal.dict()
    meal_dict["id"] = new_id
    meals_data.append(meal_dict)  # Append to the in-memory meals data
    return meal_dict

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
























# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
# from pymongo import MongoClient
# from pydantic import BaseModel
# from typing import List, Optional
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# app = FastAPI(title="The Gym by Johnson API")

# # MongoDB connection with fallback to in-memory storage
# MONGO_URL = os.getenv("MONGO_URL")
# meals_data = []

# def get_meals_storage():
#     """Get meals storage - MongoDB if available, otherwise in-memory"""
#     global meals_data
#     if MONGO_URL:
#         try:
#             client = MongoClient(MONGO_URL)
#             db = client.gym_johnson
#             return db.meals
#         except Exception as e:
#             print(f"MongoDB connection failed: {e}")
#             print("Using in-memory storage instead")
#     return None

# # Pydantic models
# class Meal(BaseModel):
#     id: str
#     title: str
#     description: str
#     calories: str
#     protein: str
#     image: str
#     category: str  # "bulking" or "cutting"

# class MealCreate(BaseModel):
#     title: str
#     description: str
#     calories: str
#     protein: str
#     image: str
#     category: str

# # Initialize default meals data
# def init_db():
#     global meals_data
#     storage = get_meals_storage()
    
#     # Check if data already exists
#     if storage and storage.count_documents({}) > 0:
#         return
#     elif not storage and meals_data:
#         return
    
#     bulking_meals = [
#         {
#             "id": "1",
#             "title": "Whole Milk and Cottage Cheese",
#             "description": "High-protein dairy combination for muscle building",
#             "calories": "850 cal",
#             "protein": "45g protein",
#             "image": "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "bulking"
#         },
#         {
#             "id": "2",
#             "title": "Nuts and Nut Butters",
#             "description": "Calorie-dense healthy fats and proteins",
#             "calories": "720 cal",
#             "protein": "25g protein",
#             "image": "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "bulking"
#         },
#         {
#             "id": "3",
#             "title": "Whole Eggs",
#             "description": "Complete protein with essential amino acids",
#             "calories": "680 cal",
#             "protein": "42g protein",
#             "image": "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "bulking"
#         },
#         {
#             "id": "4",
#             "title": "Rice",
#             "description": "Complex carbohydrates for energy and recovery",
#             "calories": "450 cal",
#             "protein": "8g protein",
#             "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "bulking"
#         },
#         {
#             "id": "5",
#             "title": "Chicken and Mutton",
#             "description": "Lean protein sources for muscle development",
#             "calories": "650 cal",
#             "protein": "65g protein",
#             "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "bulking"
#         }
#     ]
    
#     cutting_meals = [
#         {
#             "id": "6",
#             "title": "Carbohydrates",
#             "description": "Complex carbs for sustained energy during cuts",
#             "calories": "320 cal",
#             "protein": "12g protein",
#             "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         },
#         {
#             "id": "7",
#             "title": "Lean Fish",
#             "description": "Low-calorie, high-protein white fish",
#             "calories": "280 cal",
#             "protein": "45g protein",
#             "image": "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         },
#         {
#             "id": "8",
#             "title": "Eggs",
#             "description": "High-quality protein with essential nutrients",
#             "calories": "180 cal",
#             "protein": "24g protein",
#             "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         },
#         {
#             "id": "9",
#             "title": "Dairy",
#             "description": "Low-fat dairy products for protein",
#             "calories": "250 cal",
#             "protein": "28g protein",
#             "image": "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         },
#         {
#             "id": "10",
#             "title": "Pulses (Lentils, Beans, Peas)",
#             "description": "Plant-based protein and fiber",
#             "calories": "200 cal",
#             "protein": "18g protein",
#             "image": "https://images.unsplash.com/photo-1586795158095-e891c9e1a42b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         },
#         {
#             "id": "11",
#             "title": "Tofu, Seeds & Nuts",
#             "description": "Plant-based proteins and healthy fats",
#             "calories": "290 cal",
#             "protein": "22g protein",
#             "image": "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&h=600",
#             "category": "cutting"
#         }
#     ]
    
#     all_meals = bulking_meals + cutting_meals
    
#     if storage:
#         storage.insert_many(all_meals)
#     else:
#         meals_data.extend(all_meals)

# # API Routes
# @app.get("/")
# async def read_root():
#     with open("static/index.html", "r") as file:
#         content = file.read()
#     return HTMLResponse(content=content)

# @app.get("/api/meals", response_model=List[Meal])
# async def get_meals(category: Optional[str] = None):
#     global meals_data
#     storage = get_meals_storage()
    
#     if storage:
#         query = {"category": category} if category else {}
#         meals = list(storage.find(query, {"_id": 0}))
#     else:
#         if category:
#             meals = [meal for meal in meals_data if meal.get("category") == category]
#         else:
#             meals = meals_data
    
#     return meals

# @app.get("/api/meals/{meal_id}", response_model=Meal)
# async def get_meal(meal_id: str):
#     global meals_data
#     storage = get_meals_storage()
    
#     if storage:
#         meal = storage.find_one({"id": meal_id}, {"_id": 0})
#     else:
#         meal = next((m for m in meals_data if m.get("id") == meal_id), None)
    
#     if not meal:
#         raise HTTPException(status_code=404, detail="Meal not found")
#     return meal

# @app.post("/api/meals", response_model=Meal)
# async def create_meal(meal: MealCreate):
#     global meals_data
#     storage = get_meals_storage()
    
#     if storage:
#         # Generate a new ID
#         last_meal = storage.find_one(sort=[("id", -1)])
#         new_id = str(int(last_meal["id"]) + 1) if last_meal else "1"
        
#         meal_dict = meal.dict()
#         meal_dict["id"] = new_id
        
#         storage.insert_one(meal_dict)
#     else:
#         # Generate a new ID for in-memory storage
#         max_id = max([int(m.get("id", "0")) for m in meals_data], default=0)
#         new_id = str(max_id + 1)
        
#         meal_dict = meal.dict()
#         meal_dict["id"] = new_id
        
#         meals_data.append(meal_dict)
    
#     return meal_dict

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Initialize database on startup
# @app.on_event("startup")
# async def startup_event():
#     init_db()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)