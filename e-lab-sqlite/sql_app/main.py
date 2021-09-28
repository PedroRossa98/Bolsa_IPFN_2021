import os
import sys
import uvicorn

from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

home_dir = os.path.dirname(__file__)
modules_dir = os.path.join(home_dir, 'sql_app')
sys.path.append(modules_dir)

from database import SessionLocal, engine
import crud
import models
import schemas
from montecarlo import ConfigExperimentModel, config_experiment_data, resultpoint_data, resultlist_data



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/config")
def config_experiment(user: ConfigExperimentModel):
    return config_experiment_data(user)


@app.get("/resultpoint")
def get_point(db: Session = Depends(get_db)):
    return resultpoint_data(db)


@app.get("/resultlist/{limit}",  response_model=List[schemas.Temperature])
def get_point_list(limit: int, db: Session = Depends(get_db)):
    items = resultlist_data(db, limit=limit)
    for item in items:
        
        print('montecarlo get_point_list item : ', type(item.value), item.value) 

    print('montecarlo get_point_list type : ', type(item), type(schemas.Temperature))    
    return list(items)


if __name__ == "__main__":
    print('Load Main Stuff')
    print('Encrypted : ', crud.passwd_encypt('Test'))
    # https://www.uvicorn.org/settings/
    # https://fastapi.tiangolo.com/advanced/websockets/
    # uvicorn.run("main:app", host='127.0.0.1', port=8001, workers=4, access_log=False)  
    # uvicorn.run("main:app", host='127.0.0.1', port=8001)  