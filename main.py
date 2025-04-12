from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.census.gov/data/2021/acs/acs5"
VARIABLE = "B25064_001E"  # Median Gross Rent

@app.get("/search")
async def search_market(zip: str = Query(...)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params={
                "get": VARIABLE,
                "for": f"zip code tabulation area:{zip}"
            })

            if response.status_code != 200:
                return {"error": "Census API error", "status_code": response.status_code}

            data = response.json()
            median_rent = int(data[1][0])  # skip header
            return {
                "zip": zip,
                "median_rent": median_rent
            }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to fetch data from Census API."
        }
