from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

templates = Jinja2Templates(directory="module_16/templates")

class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/users/{user_id}', response_class=HTMLResponse)
async def all_users(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            get_user = user
            return templates.TemplateResponse('users.html', {'request': request, 'users': get_user})
    raise HTTPException(status_code=404, detail="User not found")


@app.post('/user/{username}/{age}', response_model=User)
async def add_users(
        username: Annotated[str, Path(..., min_length=3, max_length=15)],
        age: Annotated[int, Path(..., ge=18, le=120)]
):
    new_user = User(id=max([user.id for user in users], default=0) + 1, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_users(
        user_id: int,
        username: Annotated[str, Path(..., min_length=3, max_length=15)],
        age: Annotated[int, Path(..., ge=18, le=120)]
):
    for user in users:
        if user_id == user.id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}', response_model=User)
async def del_users(user_id: int):
    for index, akk in enumerate(users):
        if user_id == akk.id:
            users.pop(index)
            return akk
    raise HTTPException(status_code=404, detail='User was not found')
