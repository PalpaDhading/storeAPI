from db import db

class ItemModel(db.Model):
    __tablename__ = 'itemsdata'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    sitename = db.Column(db.Integer, db.ForeignKey('sitesdata.sitename'))
    site = db.relationship('SiteModel')

    def __init__(self, name, price, sitename):
        self.name = name
        self.price = price
        self.sitename = sitename

    def json(self):
        return {'ITEMNAME': self.name, 'price': self.price}

    @classmethod
    def find_by_site_name(cls,sitename):
        return cls.query.filter_by(sitename=sitename).first()

    @classmethod
    def find_by_itemname_sitename(cls,name,sitename):
        return cls.query.filter_by(name=name,sitename=sitename).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
