from fastapi import APIRouter, HTTPException
from starlette import status
from dbs_assignment.database import Session
from dbs_assignment.models import User, Card, Rental, Reservation
from dbs_assignment.endpoints.assignment5.base_models import UserModel, CardModel

router = APIRouter()
DB = Session()


def check_if_empty_r_r(user):
    if not DB.query(Rental).filter(Rental.user_id == user.id).first() \
            and not DB.query(Reservation).filter(Reservation.user_id == user.id).first():
        return {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "birth_date": user.birth_date,
            "email": user.email,
            "personal_identificator": user.personal_identificator
        }
    else:
        return user


@router.get('/users/{userId}', status_code=status.HTTP_200_OK, description='User Found')
def get_user(userId: str):
    if not DB.query(User).filter(User.id == userId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    else:
        user = DB.query(User).filter(User.id == userId).first()
        return check_if_empty_r_r(user)


@router.patch('/users/{userId}', status_code=status.HTTP_200_OK, description='User updated')
def update_user(userId: str, request: UserModel):
    if not hasattr(request, 'name') or not hasattr(request, 'surname') or not hasattr(request, 'email') or not hasattr(
            request, 'birth_date') or not hasattr(request, 'personal_identificator'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif not DB.query(User).filter(User.id == userId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    elif DB.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email Already Taken')
    else:
        user = DB.query(User).filter(User.id == userId).first()
        if hasattr(request, 'id'):
            user.id = request.id
        else:
            user.id = userId
        user.name = request.name
        user.surname = request.surname
        user.email = request.email
        user.birth_date = request.birth_date
        user.personal_identificator = request.personal_identificator
        DB.commit()
        return check_if_empty_r_r(user)


@router.post('/users', status_code=status.HTTP_201_CREATED, description='Created')
def create_user(request: UserModel):
    if not hasattr(request, 'id') or not hasattr(request, 'name') or not hasattr(request, 'surname') or not hasattr(
            request, 'email') or not hasattr(request, 'birth_date') or not hasattr(request, 'personal_identificator'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif DB.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email Already Taken')
    elif DB.query(User).filter(User.id == request.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='UUID already exists')
    else:
        user = User()
        user.id = request.id
        user.name = request.name
        user.surname = request.surname
        user.email = request.email
        user.birth_date = request.birth_date
        user.personal_identificator = request.personal_identificator

        DB.add(user)
        DB.commit()

        return check_if_empty_r_r(user)


@router.post('/cards', response_model=CardModel, status_code=status.HTTP_201_CREATED, description='Created')
def create_card(request: CardModel):
    if not hasattr(request, 'user_id') or not hasattr(request, 'magstripe') or not hasattr(request, 'status'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif request.status not in ['active', 'inactive', 'expired']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    else:
        card = Card(
            id=request.id,
            user_id=request.user_id,
            magstripe=request.magstripe,
            status=request.status
        )
        DB.add(card)
        DB.commit()
        return card


@router.get('/cards/{cardId}', response_model=CardModel, status_code=status.HTTP_200_OK, description='OK')
def get_card(cardId: str):
    if not DB.query(Card).filter(Card.id == cardId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        card = DB.query(Card).filter(Card.id == cardId).first()
        return card


@router.patch('/cards/{cardId}', response_model=CardModel, status_code=status.HTTP_200_OK, description='OK')
def update_card(cardId: str, request: CardModel):
    if not hasattr(request, 'user_id') or not hasattr(request, 'status'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif request.status not in ['active', 'inactive', 'expired']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    elif not DB.query(Card).filter(Card.id == cardId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        card = DB.query(Card).filter(Card.id == cardId).first()
        card.status = request.status
        card.user_id = request.user_id
        DB.commit()
        return card


@router.delete('/cards/{cardId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_card(cardId: str):
    if not DB.query(Card).filter(Card.id == cardId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        card = DB.query(Card).filter(Card.id == cardId).first()
        DB.delete(card)
        DB.commit()
        return
