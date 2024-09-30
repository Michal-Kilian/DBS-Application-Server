from fastapi import APIRouter, HTTPException
from starlette import status
from dbs_assignment.models import Publication, Instance, Author, Category
from dbs_assignment.endpoints.assignment5.base_models import PublicationModel, InstanceModel
from dbs_assignment.endpoints.assignment5.users_cards import DB

router = APIRouter()


def check_authors(authors: list):
    for author in authors:
        if not DB.query(Author).filter(Author.name == author.get('name') and Author.surname == author.get('surname')).first():
            return False
    return True


def check_categories(categories):
    for category in categories:
        if not DB.query(Category).filter(Category.name == category).first():
            return False
    return True


def adjust_authors(authors):
    authors_list = []
    for author in authors:
        a = DB.query(Author).filter(Author.name == author.get('name') and Author.get('surname')).first()
        authors_list.append(a)
    return authors_list


def adjust_categories(categories):
    category_list = []
    for category in categories:
        c = DB.query(Category).filter(Category.name == category).first()
        category_list.append(c)
    return category_list


@router.post('/publications', response_model=PublicationModel, status_code=status.HTTP_201_CREATED,
             description='Created')
def create_publication(request: PublicationModel):
    if not hasattr(request, 'title') or not hasattr(request, 'authors') or not hasattr(request, 'categories'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif DB.query(Publication).filter(Publication.id == request.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='UUID already exists')
    elif not check_authors(request.authors) or not check_categories(request.categories):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    else:
        publication = Publication()
        if hasattr(request, 'id'):
            publication.id = request.id
        publication.title = request.title
        publication.authors = adjust_authors(request.authors)
        publication.categories = adjust_categories(request.categories)
        DB.add(publication)
        DB.commit()
        return publication


@router.get('/publications/{publicationId}', response_model=PublicationModel, status_code=status.HTTP_200_OK,
            description='OK')
def get_publication(publicationId: str):
    if not DB.query(Publication).filter(Publication.id == publicationId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        publication = DB.query(Publication).filter(Publication.id == publicationId).first()
        return publication


@router.patch('/publications/{publicationId}', response_model=PublicationModel, status_code=status.HTTP_200_OK,
              description='OK')
def update_publication(publicationId: str, request: PublicationModel):
    if not hasattr(request, 'title') or not hasattr(request, 'authors') or not hasattr(request, 'categories'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif not DB.query(Publication).filter(Publication.id == publicationId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    elif not check_authors(request.authors) or not check_categories(request.categories):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    else:
        publication = DB.query(Publication).filter(Publication.id == publicationId).first()
        if hasattr(request, 'id'):
            publication.id = request.id
        publication.title = request.title
        publication.authors = adjust_authors(request.authors)
        publication.categories = adjust_categories(request.categories)
        DB.commit()
        return publication


@router.delete('/publications/{publicationId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_publication(publicationId: str):
    if not DB.query(Publication).filter(Publication.id == publicationId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        publication = DB.query(Publication).filter(Publication.id == publicationId).first()
        DB.delete(publication)
        DB.commit()
        return


@router.post('/instances', response_model=InstanceModel, status_code=status.HTTP_201_CREATED, description='Created')
def create_instance(request: InstanceModel):
    if not hasattr(request, 'type') or not hasattr(request, 'publisher') or not hasattr(request,
                                                                                        'year') or not hasattr(request,
                                                                                                               'publication_id'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif hasattr(request, 'status') and request.status not in ['available', 'reserved']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    elif request.type not in ['physical', 'ebook', 'audiobook']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    else:
        instance = Instance()
        instance.id = request.id
        instance.type = request.type
        instance.publisher = request.publisher
        instance.year = request.year
        instance.status = request.status
        instance.publication_id = request.publication_id
        DB.add(instance)
        DB.commit()
        return instance


@router.get('/instances/{instanceId}', response_model=InstanceModel, status_code=status.HTTP_200_OK, description='OK')
def get_instance(instanceId: str):
    if not DB.query(Instance).filter(Instance.id == instanceId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        instance = DB.query(Instance).filter(Instance.id == instanceId).first()
        return instance


@router.patch('/instances/{instanceId}', response_model=InstanceModel, status_code=status.HTTP_200_OK,
              description='OK')
def update_instance(instanceId: str, request: InstanceModel):
    if not hasattr(request, 'type') or not hasattr(request, 'publisher') or not hasattr(request,
                                                                                        'year') or not hasattr(request,
                                                                                                               'publication_id'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif not DB.query(Instance).filter(Instance.id == instanceId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    elif hasattr(request, 'status') and request.status not in ['available', 'reserved']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    elif request.type not in ['physical', 'ebook', 'audiobook']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad Request')
    else:
        instance = DB.query(Instance).filter(Instance.id == instanceId).first()
        instance.id = instanceId
        instance.type = request.type
        instance.publisher = request.publisher
        instance.year = request.year
        if hasattr(request, 'status'):
            instance.status = request.status
        instance.publication_id = request.publication_id
        DB.add(instance)
        DB.commit()
        return instance


@router.delete('/instances/{instanceId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_instance(instanceId: str):
    if not DB.query(Instance).filter(Instance.id == instanceId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        instance = DB.query(Instance).filter(Instance.id == instanceId).first()
        DB.delete(instance)
        DB.commit()
        return
