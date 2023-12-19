from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel,Field
from typing import Optional
from datetime import date



user_db = {
    'Shreyas' : {'usrename':'Shreyas', 'dob':'06-10-2000', 'age':23, 'location':'Bangalore'},
    'Akshay' : {'usrename':'Akshay', 'dob':'27-04-2000', 'age':23, 'location':'Bangalore'},
    'Karthik': {'usrename':'Karthik', 'dob':'23-11-2000', 'age':23, 'location':'Bangalore'}
}

class User(BaseModel):
    username:str = Field(min_length=2,max_length=10)
    dob:date
    age:int = Field(None,gt=18,lt=30)
    location: Optional[str] = None


class UserUpdate(User):
    dob : Optional[date] = None
    age : int = Field(None, gt=10,lt=100)

def ensure_username_in_db(username):
       if username not in user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{username} not found')

app = FastAPI()

@app.get("/users/querry")
def get_users_query(limit: int):    
    user_list = list(user_db.values())
    return user_list[: limit]

@app.get("/users")
def get_users():
    user_list = list(user_db.values())
    return user_list


@app.get('/users/{username}')
def get_users_path(username:str): 
    ensure_username_in_db(username)
    return user_db[username]

@app.post('/user/')
def create_user(user:User):
    username = user.username
    if username in user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f'Cannot create user. Username {username} already exists')
    user_db[username] = user.model_dump()
    return {'message':f'Successfully created user: {username}'}

@app.delete('/users/{username}')
def delete_user(username:str):
    ensure_username_in_db(username)
    del user_db[username]
    return {'message':f'Successfully deleted user: {username}'}

@app.put('/users')
def update_user(user:User):
    username = user.username
    ensure_username_in_db(username)
    user_db[username] = user.model_dump()
    return {'message' : f'successfully updated user : {username}'}

@app.patch('/users')
def upadte_user_partial(user:UserUpdate):
    username = user.username
    ensure_username_in_db(username)
    user_db[username].update(user.model_dump(exclude_unset=True))   
    return {'message': f'Successfully udated user : {username}'}