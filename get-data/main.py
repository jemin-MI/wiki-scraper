from fastapi import FastAPI
import service
from typing import Optional
import uvicorn

app = FastAPI()

@app.post("/get-data/{domain}")
async def create_user(domain,  sheet: Optional[bool] = False):
    """
    Greet the user with their name and email.
    """
    return service.get_data(domain, sheet)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)