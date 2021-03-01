import dataclasses
import json
import logging
import os
from datetime import date

import orjson
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, abort, make_response, request
from flask_api import status
from flask_pymongo import PyMongo
from flask_restx import Api, Resource, fields
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        TESTING=True,
        LOGGER_NAME='TrailerPlanLog'
    )
    return app


application = create_app()
api = Api(application)
load_dotenv()
mongoServer = os.getenv('MONGO_HOSTNAME')
nameSpace = api.namespace('trailerplan/api/v1.2/users', description='TrailerPlan User API')
application.config['MONGO_URI'] = "mongodb://"+mongoServer+":27017/trailerplandb"
mongo = PyMongo(application)


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('TrailerPlanApiLogger')
logger.setLevel(logging.DEBUG)


def get_db(self):
    root_pswd = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
    client = MongoClient(mongoServer+':27017', username='root', password=root_pswd)
    db = client.trailerplandb
    return db


user_model = api.model('Resource', {
    'CIVILITE': fields.String,
    'FIRST_NAME': fields.String,
    'LAST_NAME': fields.String,
    'SEXE': fields.String,
    'BIRTHDAY': fields.String,
    'CITY': fields.String,
    'COUNTRY': fields.String
})


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@nameSpace.route("/")
class UserCollectionController(Resource):

    def get(self):
        """ Retrieve all users """
        dao = UserDao('p_user')
        users = dao.get_collection()
        logger.debug('List of users : %s', json.dumps(users, cls=JSONEncoder))
        return getResponseHttp(users)

    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    def post(self):
        """ Create a user """
        dao = UserDao('p_user')
        trailer_obj = orjson.loads(request.data) if request.data else abort(status.HTTP_400_BAD_REQUEST)
        dao.insert(trailer_obj)
        logger.debug('user to insert : %s', json.dumps(trailer_obj, cls=JSONEncoder))
        return getResponseHttp(trailer_obj)


@nameSpace.route("/<string:string_object_id>")
@api.response(404, 'User not found.')
class UserItemController(Resource):

    def get(self, string_object_id):
        """ Retrieve user by id """
        dao = UserDao('p_user')
        user = dao.get(ObjectId(string_object_id))
        logger.debug('user finded : %s', json.dumps(user, cls=JSONEncoder))
        return getResponseHttp(user)

    @api.expect(user_model)
    @api.response(204, 'User successfully updated.')
    def put(self, string_object_id):
        """ Update a user by id """
        dao = UserDao('p_user')
        trailer_obj = orjson.loads(request.data) if request.data else abort(status.HTTP_400_BAD_REQUEST)
        dao.update(ObjectId(string_object_id), trailer_obj)
        logger.debug("user to update : %s", json.dumps(trailer_obj, cls=JSONEncoder))
        return None, 204

    @api.response(204, 'User successfully deleted')
    def delete(self, string_object_id):
        """ Delete a user by id """
        dao = UserDao('p_user')
        logger.debug('user id to delete : %s', string_object_id)
        dao.delete_by_id(ObjectId(string_object_id))
        return None, 204


def getResponseHttp(obj2dump):
    response = make_response(json.dumps(obj2dump, cls=JSONEncoder))
    response.headers['Content-Type'] = 'application/json'
    return response


@dataclasses.dataclass
class UserDao(object):
    def __init__(self, table):
        self.db = get_db(self)
        self.collection = self.db[table]

    def get_collection(self):
        return [user for user in self.collection.find()]

    def get(self, idx):
        return self.collection.find_one({"_id": idx})

    def insert(self, user):
        self.collection.insert_one(user)

    def update(self, id, user):
        self.collection.replace_one({"_id": id}, user)

    def delete(self, user):
        self.collection.delete_one({"_id": user['_id']})

    def delete_by_id(self, id):
        self.collection.delete_one({"_id": id})

    def getLength(self):
        return self.users.__len__()


def default(obj):
    if isinstance(obj, ShortAddress):
        return obj.toJson()
    raise TypeError


@dataclasses.dataclass
class Object(object):
    """oject model"""
    def toJson(self):
        return orjson.dumps(self.__dict__, default=default).decode("utf-8")


@dataclasses.dataclass
class AbstractClass(Object):
    """abstract object model"""
    def __init__(self):
        self.creationDate = date.day, self.modificationDate = date.day


@dataclasses.dataclass
class ShortAddress(AbstractClass):
    """object model of an short address"""
    def __init__(self, pId=-1, city='Paris', country='France'):
        self.id, self.city, self.country = pId, city, country

    def toString(self):
        str2return = '' if self.city is None else "à {0} ".format(self.city)
        str2return += "en {0}".format(self.country)
        return str2return


@dataclasses.dataclass
class Address(ShortAddress):
    """object model of an address"""
    def __init__(self, pId=-1, num=1, typeVoie='rue', voie='de la Paix', zipCode='75009'):
        ShortAddress.__init__(self)
        self.id, self.num, self.typeVoie, self.libelleVoie, self.zipCode = pId, num, typeVoie, voie, zipCode

    def toString(self):
        return "{0} {1} {2} {3}".format(self.num, self.typeVoie, self.libelleVoie, self.zipCode)


@dataclasses.dataclass
class User(AbstractClass):
    """object model of an user"""
    def __init__(self, pId=-1, civility=None, firstName='', lastName='', sexe='', birthday=date.today(), city='', country=''):
        self.id, self.firstName, self.lastName, self.sexe, self.birthday = \
            pId, firstName, lastName, sexe, birthday
        self.address = ShortAddress(self.id, city, country)
        self.civility = 'Monsieur' if civility is None else civility

    def setAddress(self, adresse):
        self.address = adresse

    def toString(self):
        str2return = "{0} {1} {2} né le {3} {4}" \
            .format(self.firstName, self.lastName.upper(), self.sexe, self.birthday, self.address.toString())
        return str2return


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=int("5000"), debug=True)
