from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    street = db.Column(db.String(1000))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))

    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self,name,street,city,state):
        self.name = name
        self.street =street
        self.city =city
        self.state =state

    def json(self):
        return {'name': self.name,'Adrress':{'Street':self.street,'City':self.city,'State':self.state},'Items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
