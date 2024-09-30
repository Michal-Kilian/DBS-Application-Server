from fastapi import APIRouter, HTTPException
from starlette import status
from dbs_assignment.models import Author, Category
from dbs_assignment.endpoints.assignment5.base_models import AuthorModel, CategoryModel
from dbs_assignment.endpoints.assignment5.users_cards import DB


router = APIRouter()


@router.post('/authors', response_model=AuthorModel, status_code=status.HTTP_201_CREATED, description='Created')
def create_author(request: AuthorModel):
    if not hasattr(request, 'name') or not hasattr(request, 'surname'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif DB.query(Author).filter(Author.id == request.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Conflict')
    else:
        author = Author(
            id=request.id,
            name=request.name,
            surname=request.surname
        )
        DB.add(author)
        DB.commit()
        return author


@router.get('/authors/{authorId}', response_model=AuthorModel, status_code=status.HTTP_200_OK, description='OK')
def get_author(authorId: str):
    if not DB.query(Author).filter(Author.id == authorId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        author = DB.query(Author).filter(Author.id == authorId).first()
        return author


@router.patch('/authors/{authorId}', response_model=AuthorModel, status_code=status.HTTP_200_OK, description='OK')
def update_author(authorId: str, request: AuthorModel):
    if not DB.query(Author).filter(Author.id == authorId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        author = DB.query(Author).filter(Author.id == authorId).first()
        if hasattr(request, 'name'):
            author.name = request.name
        if hasattr(request, 'surname'):
            author.surname = request.surname
        DB.commit()
        return author


@router.delete('/authors/{authorId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_author(authorId: str):
    if not DB.query(Author).filter(Author.id == authorId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        author = DB.query(Author).filter(Author.id == authorId).first()
        DB.delete(author)
        DB.commit()
        return


@router.post('/categories', response_model=CategoryModel, status_code=status.HTTP_201_CREATED, description='Created')
def create_category(request: CategoryModel):
    if not hasattr(request, 'name'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing Required Information')
    elif DB.query(Category).filter(Category.id == request.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Conflict')
    else:
        category = Category()
        category.id = request.id
        category.name = request.name
        DB.add(category)
        DB.commit()
        return category


@router.get('/categories/{categoryId}', response_model=CategoryModel, status_code=status.HTTP_200_OK, description='OK')
def get_category(categoryId: str):
    if not DB.query(Category).filter(Category.id == categoryId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    else:
        category = DB.query(Category).filter(Category.id == categoryId).first()
        return category


@router.patch('/categories/{categoryId}', response_model=CategoryModel, status_code=status.HTTP_200_OK, description='OK')
def update_category(categoryId: str, request: CategoryModel):
    if not DB.query(Category).filter(Category.id == categoryId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        category = DB.query(Category).filter(Category.id == categoryId).first()
        if hasattr(request, 'name'):
            category.name = request.name
        DB.commit()
        return category


@router.delete('/categories/{categoryId}', status_code=status.HTTP_204_NO_CONTENT, description='No Content')
def delete_category(categoryId: str):
    if not DB.query(Category).filter(Category.id == categoryId).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    else:
        category = DB.query(Category).filter(Category.id == categoryId).first()
        DB.delete(category)
        DB.commit()
        return
