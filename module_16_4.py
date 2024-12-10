from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, List

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []


@app.get('/users', response_model=List[User])
async def all_users():
    return users


@app.post('/user/{username}/{age}', response_model=User)
async def add_users(
        username: Annotated[str, Path(..., min_length=3, max_length=15)],
        age: Annotated[int, Path(..., ge=18, le=120)]
):
    new_user = User(id=max([user.id for user in users, default=0]) + 1, 
                    username=username, 
                    age=age)
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
