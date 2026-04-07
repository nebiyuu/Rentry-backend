from fastapi import FastAPI, HTTPException
from database import get_db_products
from services.recommendation import calculate_similar_items
from services.pricing import predict_rental_price
from services.image_validator import validate_image_quality 

# Adding a title and version makes the /docs page look much better
app = FastAPI(title="Rentry AI Microservice", version="1.0.0")

# --- 0. Home Route (Health Check) ---
@app.get("/")
async def root():
    return {
        "message": "Rentry AI Engine is Online",
        "endpoints": ["/recommend/{id}", "/predict-price/{value}", "/validate-image/"]
    }

# --- 1. Recommendation Route ---
@app.get("/recommend/{product_uuid}")
async def recommend(product_uuid: str):
    data = get_db_products()
    if not data:
        raise HTTPException(status_code=404, detail="Product database is empty")
    recs = calculate_similar_items(product_uuid, data)
    return {"status": "success", "recommended_ids": recs}

# --- 2. Pricing Route ---
@app.get("/predict-price/{market_value}")
async def price(market_value: float):
    # The AI logic we fixed with the 5-tier fallback
    suggestion = predict_rental_price(market_value)
    return {"status": "success", "suggested_rent": suggestion}

# --- 3. Image Validation Route ---
@app.get("/validate-image/")
async def check_image(path: str):
    # Standard Computer Vision quality check
    result = validate_image_quality(path)
    return result

if __name__ == "__main__":
    import uvicorn
    # Using reload=True during development is helpful!
    uvicorn.run(app, host="0.0.0.0", port=8000)