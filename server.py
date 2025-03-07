from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import datetime

app = FastAPI()

# Allow frontend (localhost:4200) to access the API
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Allow all origins (or specify frontend domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generate mock acceleration data for multiple VINs
def generate_mock_data():
    data = {}
    vin_numbers = [f"VIN{1000 + i}" for i in range(10)]  # Mock VINs
    
    for vin in vin_numbers:
        records = []
        for days_ago in range(180):  
            date = datetime.date.today() - datetime.timedelta(days=days_ago)
            records.append({
                "date": str(date),
                "G-Force": round(random.uniform(0.5, 2.5), 2),
                "X-acc": round(random.uniform(-3.0, 3.0), 2),
                "Y-acc": round(random.uniform(-3.0, 3.0), 2)
            })
        data[vin] = records
    return data

mock_data = generate_mock_data()

# Define VIN request model
class VINRequest(BaseModel):
    vin: str

@app.post("/get-acceleration-data")
def get_acceleration_data(request: VINRequest):
    vin = request.vin.upper()
    
    if vin not in mock_data:
        return {"error": "VIN not found"}
    
    return {"vin": vin, "data": mock_data[vin]}

# Run the server only in local development (not needed for Render)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
