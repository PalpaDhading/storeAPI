from flask_restful import Resource, reqparse
from models.site import SiteModel

class Site(Resource):
    def get(self, sitename):
        site = SiteModel.find_by_name(sitename)
        if site:
            return site.json()
        return {'message': "Site {} not found".format(sitename)}, 404

    def post(self, sitename):
        if SiteModel.find_by_name(sitename):
            return {'message': "A cell site with name '{}' already exists.".format(sitename)}, 400

        site = SiteModel(sitename)
        try:
            site.save_to_db()
        except:
            return {"message": "An error occurred creating the {} site.".format(sitename)}, 500

        return site.json(), 201

    def delete(self, sitename):
        site = SiteModel.find_by_name(sitename)
        if site:
            site.delete_from_db()

        return {'message': "Site {} deleted".format(sitename)}

class SiteList(Resource):
    def get(self):
        return {'SiteList': list(map(lambda x: x.json(), SiteModel.query.all()))}
