import datetime
import uuid
from fastapi import APIRouter, HTTPException
from starlette import status
from dbs_assignment.models import Rental, Reservation, Instance
from dbs_assignment.endpoints.assignment5.base_models import RentalRequestModel, RentalResponseModel, ReservationModel
from dbs_assignment.endpoints.assignment5.users_cards import DB

router = APIRouter()


def queue_permission(user_id: uuid.UUID, publication_id: uuid.UUID):
    if DB.query(Reservation).filter(Reservation.publication_id == publication_id) \
        .order_by(Reservation.created_at).first() == DB.query(Reservation).filter(
        Reservation.publication_id == publication_id and
            Reservation.user_id == user_id).first():
        return True
    else:
        return False


def get_publication_instance_id(publication_id):
    return DB.query(Instance).filter(Instance.publication_id == publication_id and status == 'available').first()


def calculate_end_date(duration):
    return datetime.datetime.utcnow() + datetime.timedelta(days=duration)


@router.post('/rentals', response_model=RentalResponseModel, status_code=status.HTTP_201_CREATED,
             description='Created')
def create_rental(request: RentalRequestModel):
    if not hasattr(request, 'user_id') or not hasattr(request, 'publication_id') or not hasattr(request, 'duration') \
            or not DB.query(Instance).filter(Instance.publication_id == request.publication_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    else:
        if DB.query(Reservation).filter(Reservation.publication_id == request.publication_id):
            if not queue_permission(request.user_id, request.publication_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not the first in queue')

        if not get_publication_instance_id(request.publication_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='No publication instances available')

        publication_instance_id = get_publication_instance_id(request.publication_id).id,

        rental = Rental()
        if hasattr(request, 'id'):
            rental.id = request.id
        rental.user_id = request.user_id
        rental.publication_instance_id = publication_instance_id
        rental.duration = request.duration
        rental.end_date = calculate_end_date(request.duration)

        DB.add(rental)
        DB.commit()
        return rental


@router.get('/rentals/{rentalId}', response_model=RentalResponseModel, status_code=status.HTTP_200_OK,
            description='OK')
def get_rental(rentalId: str):
    if not DB.query(Rental).filter(Rental.id == rentalId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        rental = DB.query(Rental).filter(Rental.id == rentalId).first()
        return rental


@router.patch('/rentals/{rentalId}', response_model=RentalResponseModel, status_code=status.HTTP_200_OK,
              description='OK')
def update_rental(rentalId: str, request: RentalRequestModel):
    if not hasattr(request, 'duration') or request.duration < 0 or request.duration > 14:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    elif DB.query(Rental).filter(Rental.id == rentalId and Rental.status == 'active').first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
    else:
        rental = DB.query(Rental).filter(Rental.id == rentalId).first()
        rental.end_date = rental.end_date + request.duration
        DB.commit()
        return rental


@router.post('/reservations', response_model=ReservationModel, status_code=status.HTTP_201_CREATED,
             description='Created')
def create_reservation(request: ReservationModel):
    if not hasattr(request, 'user_id') or not hasattr(request, 'publication_id'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    else:
        reservation = Reservation()
        if hasattr(request, 'id'):
            reservation.id = request.id
        reservation.user_id = request.user_id
        reservation.publication_id = request.publication_id
        DB.add(reservation)
        DB.commit()
        return reservation


@router.get('/reservations/{reservationId}', response_model=ReservationModel, status_code=status.HTTP_200_OK,
            description='OK')
def get_reservation(reservationId: str):
    if not DB.query(Reservation).filter(Reservation.id == reservationId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        reservation = DB.query(Reservation).filter(Reservation.id == reservationId).first()
        return reservation


@router.delete('/reservations/{reservationId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_reservation(reservationId: str):
    if not DB.query(Reservation).filter(Reservation.id == reservationId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        reservation = DB.query(Reservation).filter(Reservation.id == reservationId).first()
        DB.delete(reservation)
        DB.commit()
        return
