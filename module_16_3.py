from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
async def all_users():
    return users

@app.post('/user/{username}/{age}')
async def add_users(username: Annotated[str, Path(min_length=3, max_length=15)],
                    age: Annotated[int, Path(ge=18, le=120)]):
    keys = [user for user in users]
    users[str(int(max(keys)) + 1)] = f'Имя: {username}, возраст: {age}'
    return f'User {max([user for user in users])} is registered'

@app.put('/user/{user_id}/{username}/{age}')
async def update_users(user_id: str,
                       username: Annotated[str, Path(min_length=3, max_length=15)],
                       age: Annotated[int, Path(ge=18, le=120)]):
    users[str(user_id)] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'

@app.delete('/user/{user_id}')
async def del_users(user_id: Annotated[int, Path(ge=1)]):
    if user_id in users:
        users.pop(str(user_id))
        return f'The user {user_id} is delete'
    return 'The user not found'