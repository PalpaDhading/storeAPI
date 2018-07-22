from db import db
import datetime


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    dateandtime =db.Column(db.String(100))

    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,dateandtime, price, store_id):
        self.dateandtime = format(datetime.datetime.now().strftime("%B %d, %Y %H:%M"))
        self.name = name
        self.price = price
        self.store_id = store_id
        print (self.dateandtime)

    def json(self):
        return {'Name': self.name, 'Date&Time':self.dateandtime,'Price': self.price,'Store_ID' :self.store_id}

    def get_date(cls):
        return format(datetime.datetime.now().strftime("%B %d, %Y %H:%M"))


    @classmethod
    def find_by_store_id(cls, store_id):
        return cls.query.filter_by(store_id=store_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_itemname_storeID(cls,name,store_id):
        return cls.query.filter_by(name=name,store_id=store_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
