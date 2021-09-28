import bcrypt

from datetime import datetime
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session

import models
import schemas


def passwd_encypt(passwd):
    salt = bcrypt.gensalt()
    
    return bcrypt.hashpw(passwd.encode('utf-8'), salt)


def validate_user(db: Session, user_id: int, password: str):
    user = get_user(db, user_id)
    if user != None:
      return bcrypt.checkpw(user.passwd.encode('utf-8'), password)

    return false


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def add_temperature(db: Session, data):
    table = models.Temperature
    items_max_number = 69120 # 4 days off 5 sec data frequency
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db_data = table(value=data, time=datetime.strptime(now, '%Y-%m-%d %H:%M:%S'))

    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    print('montecarlo add_temperature db_data : ', db_data.id)
    if db_data.id != None and db_data.id > items_max_number:
        db_data_delete =  db.query(table).filter(table.id == db_data.id-items_max_number).delete()
        print('montecarlo add_temperature db_data_delete : ', db_data_delete)
        db.commit()


def get_temperature_list(db: Session, limit: int):
    table = models.Temperature
    # db_data_list = db.query(models.Temperature).filter().order_by(User.age.desc()).limit(10)
    # db_data_list =  db.query(models.Temperature).filter(models.Temperature.id==db_data.id-10)
    db_data_list = db.query(table).order_by(table.id.desc()).limit(limit)

    # for item in db_data_list:
    #     print('montecarlo get_temperature_list item : ', item.value)

    return db_data_list     
