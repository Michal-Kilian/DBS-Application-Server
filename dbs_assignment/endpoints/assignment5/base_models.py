from pydantic import BaseModel
import uuid
import datetime


class UserModel(BaseModel):
    id: uuid.UUID = None
    name: str
    surname: str
    email: str
    birth_date: datetime.date
    personal_identificator: str
    rentals: list = None
    reservations: list = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class CardModel(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID
    magstripe: str = None
    status: str
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class PublicationModel(BaseModel):
    id: uuid.UUID = None
    title: str
    authors: list
    categories: list
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class InstanceModel(BaseModel):
    id: uuid.UUID = None
    type: str
    publisher: str
    year: int
    status: str = None
    publication_id: uuid.UUID
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed: True
        orm_mode = True


class AuthorModel(BaseModel):
    id: uuid.UUID = None
    name: str
    surname: str
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class CategoryModel(BaseModel):
    id: uuid.UUID = None
    name: str
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class RentalRequestModel(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID = None
    publication_id: uuid.UUID = None
    duration: int
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    status: str = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class RentalResponseModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    publication_instance_id: uuid.UUID
    duration: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    status: str

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class ReservationModel(BaseModel):
    id: uuid.UUID = None
    user_id: uuid.UUID
    publication_id: uuid.UUID
    updated_at: datetime.datetime = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
