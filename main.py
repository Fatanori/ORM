import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
from models import create_tables, Publisher, Shop, Book, Stock, Sale

SQLsystem = 'postgresql'
login = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432
db_name = "BD"

DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)


def insert_data_into_tables():
    with open('tests_data.json', 'r') as f:
        data = json.load(f)

        publishers = ({'id': i['pk'], 'fields': i['fields']} for i in data if i['model'] == 'publisher')
        books = ({'id': i['pk'], 'fields': i['fields']} for i in data if i['model'] == 'book')
        shops = ({'id': i['pk'], 'fields': i['fields']} for i in data if i['model'] == 'shop')
        stocks = ({'id': i['pk'], 'fields': i['fields']} for i in data if i['model'] == 'stock')
        sales = ({'id': i['pk'], 'fields': i['fields']} for i in data if i['model'] == 'sale')

    for publisher in publishers:
        add_record = Publisher(id=publisher['id'],
                               name=publisher['fields']['name']
                               )
        session.add(add_record)
        session.commit()

    for book in books:
        add_record = Book(id=book['id'],
                          title=book['fields']['title'],
                          publisher_id=book['fields']['publisher']
                          )
        session.add(add_record)
        session.commit()

    for shop in shops:
        add_record = Shop(id=shop['id'],
                          name=shop['fields']['name']
                          )
        session.add(add_record)
        session.commit()

    for stock in stocks:
        add_record = Stock(id=stock['id'],
                           book_id=stock['fields']['book'],
                           shop_id=stock['fields']['shop'],
                           count=stock['fields']['count']
                           )
        session.add(add_record)
        session.commit()

    for sale in sales:
        add_record = Sale(id=sale['id'],
                          price=sale['fields']['price'],
                          date_sale=sale['fields']['date_sale'],
                          stock_id=sale['fields']['stock'],
                          count=sale['fields']['count']
                          )
        session.add(add_record)
        session.commit()


insert_data_into_tables()

publ_name = input('Введите имя писателя или id для вывода: ')

result_id = session.query(
    Publisher.id,
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale
).join(Book, Book.publisher_id == Publisher.id).join(Stock, Stock.book_id == Book.id).\
    join(Shop, Shop.id == Stock.shop_id).join(Sale, Sale.stock_id == Stock.id).\
    filter(Publisher.id == publ_name)

result_name = session.query(
    Publisher.id,
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale
).join(Book, Book.publisher_id == Publisher.id).join(Stock, Stock.book_id == Book.id).\
    join(Shop, Shop.id == Stock.shop_id).join(Sale, Sale.stock_id == Stock.id).\
    filter(Publisher.name.like(f"%{publ_name}%"))

if publ_name.isnumeric():
    for r in result_id:
        print(r.title, "|", r.name, "|", r.price, "|", r.date_sale)
else:
    for r in result_name:
        print(r.title, "|", r.name, "|", r.price, "|", r.date_sale)

session.close()