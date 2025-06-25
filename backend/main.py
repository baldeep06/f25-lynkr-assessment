from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import requests
import uuid

app = FastAPI(title="Weather Data System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = "113812a21debdd91e363d58a3878d629"

# In-memory storage for weather data
weather_storage: Dict[str, Dict[str, Any]] = {}

class WeatherRequest(BaseModel):
    date: str
    location: str
    notes: Optional[str] = ""

class WeatherResponse(BaseModel):
    id: str

@app.post("/weather", response_model=WeatherResponse)
async def create_weather_request(request: WeatherRequest):
    """
    You need to implement this endpoint to handle the following:
    1. Receive form data (date, location, notes)
    2. Calls WeatherStack API for the location
    3. Stores combined data with unique ID in memory
    4. Returns the ID to frontend
    """
    token_parameters = {
        "access_key": api_key,
        "query": request.location
    }

    try:
        request_response = requests.get("http://api.weatherstack.com/current", params=token_parameters)
        weather_data = request_response.json()

        if "error" in weather_data:
            raise HTTPException(status_code=400, detail="WeatherStack API error or Location is not valid")

        # a unique key for weather to be created
        weather_unique_key = str(uuid.uuid4())

        weather_storage[weather_unique_key] = {
            "date": request.date,
            "location": request.location,
            "notes": request.notes,
            "weather": weather_data["current"]
        }

        return {"id": weather_unique_key}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Could not connect to WeatherStack API: {e}")


@app.get("/weather/{weather_id}")
async def get_weather_data(weather_id: str):
    """
    Retrieve stored weather data by ID.
    This endpoint is already implemented for the assessment.
    """
    if weather_id not in weather_storage:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    return weather_storage[weather_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)