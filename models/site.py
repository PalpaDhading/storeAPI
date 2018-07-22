from db import db

class SiteModel(db.Model):
    __tablename__ = 'sitesdata'

    #id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(80), primary_key=True)

    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self, sitename):
        self.sitename = sitename

    def json(self):
        return {'SITENAME': self.sitename, 'ITEM': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,sitename):
        return cls.query.filter_by(sitename=sitename).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
