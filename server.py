from fastapi import FastAPI
from pydantic import BaseModel
import random
import datetime

app = FastAPI()


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

class VINRequest(BaseModel):
    vin: str

@app.post("/get-acceleration-data")
def get_acceleration_data(request: VINRequest):
    vin = request.vin.upper()
    
    if vin not in mock_data:
        return {"error": "VIN not found"}
    
    return {"vin": vin, "data": mock_data[vin]}


