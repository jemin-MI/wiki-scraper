from fastapi import FastAPI
import service
from typing import Optional


app = FastAPI()

@app.post("/get-data/{domain}")
async def create_user(domain,  sheet: Optional[bool] = False):
    """
    Greet the user with their name and email.
    """
    return service.get_data(domain, sheet)
