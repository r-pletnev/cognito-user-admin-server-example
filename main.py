from cognito import cognito_client

from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from cognito.validation import is_valid_token

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class User(BaseModel):
    Username: str
    UserCreateDate: datetime
    Enabled: bool
    UserStatus: str
    Attributes: list
    Email: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        attrs = self.Attributes
        self.Email = attrs[-1].get("Value")


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("public/index.html") as index_file:
        return "".join(index_file.readlines())


@app.get("/users/")
def read_users(email: Optional[str] = None):
    result = cognito_client.get_user_list(email)
    users = [User(**u) for u in result["Users"]]
    return users


@app.post("/users/")
def create_user(email: str, authorization: Optional[str] = Header(None)):
    is_valid, err = is_valid_token(authorization)
    if not is_valid:
        return {"error": err}
    cognito_client.create_user(email)
    return {"ok": True}


@app.get("/user-exist/")
def find_user(email: str, authorization: Optional[str] = Header(None)):
    is_valid, err = is_valid_token(authorization)
    if not is_valid:
        return {"error": err}
    result = cognito_client.get_user_list(email)
    users = [User(**u) for u in result["Users"]]
    return {"exists": len(users) > 0}
