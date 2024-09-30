from fastapi import APIRouter

from dbs_assignment.endpoints.assignment5 import users_cards, publications_instances, rentals_reservations, \
    authors_categories

router = APIRouter()
router.include_router(users_cards.router, tags=["users_cards"])
router.include_router(publications_instances.router, tags=["publication_instances"])
router.include_router(rentals_reservations.router, tags=["rentals_reservations"])
router.include_router(authors_categories.router, tags=["authors_categories"])
