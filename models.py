import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "Publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=120), unique=True)

    # book = relationship("Book", backref="Publisher")

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Book(Base):
    __tablename__ = "Book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=120), unique=True)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("Publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="Book")
    # stock = relationship("Stock", backref="Book")

    def __str__(self):
        return f'Book {self.id}: {self.title}, Publisher: {self.publisher_id}'


class Shop(Base):
    __tablename__ = "Shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=120), unique=True)

    # stock = relationship("Stock", backref="Shop")

    def __str__(self):
        return f'Shop {self.id}: {self.name}'


class Stock(Base):
    __tablename__ = "Stock"
    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("Book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("Shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    shop = relationship(Shop, backref="Stock")
    book = relationship(Book, backref="Stock")
    # sale = relationship("Sale", backref="Stock")

    def __str__(self):
        return f'Stock {self.id}: Book: {self.book_id}, Shop: {self.shop_id}, Count: {self.count}'


class Sale(Base):
    __tablename__ = "Sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String(length=120), nullable=False)
    date_sale = sq.Column(sq.String(length=120), nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("Stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="Sale")

    def __str__(self):
        return f'Sale {self.id}: Price: {self.price}, ' \
               f'Date: {self.date_sale}, Stock: {self.stock_id}, Count: {self.count}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)