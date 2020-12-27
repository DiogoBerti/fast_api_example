from sqlalchemy.orm import Session

from . import models, schemas


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

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_data: schemas.ItemCreate,  item_id: int):
    '''
        Rota para fazer o update dos itens... funciona mas achei horrível
    '''
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        # Tinha que ter outro jeito de fazer isso...
        item.title = item_data.title or item.title
        item.description = item_data.description or item.description
        db.commit()
        db.refresh(item)
        return item
    return False

def update_user(db: Session,user_id: int,values: schemas.UpdateUserSchema):
    '''
        Essa sim, é uma boa forma de fazer o update por conta do
        exclude_unset, que ignora tudo o que não é obrigatório
        no dicionário
    '''
    user = get_user(db, user_id)
    if user:
        db.query(models.User).filter(
            models.User.id == user_id
        ).update(values.dict(exclude_unset=True))
        db.commit()
        db.refresh(user)

        return user