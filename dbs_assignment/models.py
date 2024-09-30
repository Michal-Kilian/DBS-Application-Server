import datetime
import uuid

from sqlalchemy.orm import relationship
from dbs_assignment.database import Base
from sqlalchemy import Column, UUID, String, Date, Enum, Integer, ForeignKey, Table, DateTime


publication_authors = Table(
    'publication_authors',
    Base.metadata,
    Column('publication_id', ForeignKey('publications.id')),
    Column('author_id', ForeignKey('authors.id'))
)


publication_categories = Table(
    'publication_categories',
    Base.metadata,
    Column('publication_id', ForeignKey('publications.id')),
    Column('category_id', ForeignKey('categories.id'))
)


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    name = Column(String(255))
    surname = Column(String(255))
    email = Column(String(50))
    birth_date = Column(Date)
    personal_identificator = Column(String(50))
    # child = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    rentals = relationship("Rental", back_populates='users')
    reservations = relationship("Reservation", back_populates='users')


class Card(Base):
    __tablename__ = 'cards'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    magstripe = Column(String(255))
    status = Column(Enum('active', 'inactive', 'expired', name='CardStatusEnum'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class Publication(Base):
    __tablename__ = 'publications'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    authors = relationship('Author', secondary=publication_authors, back_populates='publications')
    categories = relationship('Category', secondary=publication_categories, back_populates='publications')


class Instance(Base):
    __tablename__ = 'instances'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    type = Column(Enum('physical', 'ebook', 'audiobook', name='InstanceTypeEnum'))
    publisher = Column(String(255))
    year = Column(Integer())
    status = Column(Enum('available', 'reserved', name='InstanceStatusEnum'), default='available')
    publication_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class Author(Base):
    __tablename__ = 'authors'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    name = Column(String(255))
    surname = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    publications = relationship('Publication', secondary=publication_authors, back_populates='authors')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    name = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    publications = relationship('Publication', secondary=publication_categories, back_populates='categories')


class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    publication_instance_id = Column(UUID(as_uuid=True))
    duration = Column(Integer())
    start_date = Column(DateTime, default=datetime.datetime.utcnow())
    end_date = Column(DateTime)
    status = Column(Enum('active', 'overdue', 'returned', name="RentalStatusEnum"), default='active')

    users = relationship("User", back_populates='rentals')


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    publication_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    users = relationship("User", back_populates='reservations')


class BadReturn(Base):
    __tablename__ = 'bad_returns'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    rental_id = Column(UUID(as_uuid=True))
    user_id = Column(UUID(as_uuid=True))
    price = Column(Integer)
    reason = Column(String(255), nullable=True)


class Extension(Base):
    __tablename__ = 'extensions'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    rental_id = Column(UUID(as_uuid=True))
    previous_date = Column(DateTime)
    new_date = Column(DateTime)


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    publication_id = Column(UUID(as_uuid=True))
    rating = Column(Integer, nullable=True)
    comment = Column(String(255), nullable=True)


class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True,
                autoincrement=False)
    publication_id = Column(UUID(as_uuid=True))
    type = Column(Enum('wishlist', 'read', 'favorite', name="WishlistTypeEnum"))
