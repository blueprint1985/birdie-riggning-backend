from run import db
from flask import request
from flask_restful import Resource
from models.Crew import CrewModel
from schemas.Crew import CrewSchema
from re import search
from sqlalchemy.exc import IntegrityError

crews_schema = CrewSchema(many=True)
crew_schema = CrewSchema()

class Crew(Resource):
    def get(self, crew_id):
        crew = CrewModel.query.filter_by(id=crew_id).first()

        if not crew:
            return {'status': 'error',
                'message': 'Crew does not exist',
                'code': 'ERROR_CREW_NOT_EXISTS'}, 404

        result = crew_schema.dump(crew).data
        return {'status': 'success', 'data': result, 'code': 'SUCCESS_CREW_LIST_FETCHED'}, 200
    
    def delete(self, crew_id):
        crew = CrewModel.query.filter_by(id=crew_id).first()

        if not crew:
            return {'status': 'error',
                'message': 'Crew does not exist',
                'code': 'ERROR_CREW_NOT_EXISTS'}, 404

        crew = CrewModel.query.filter_by(id=crew_id).delete()
        db.session.commit()

        result = crew_schema.dump(crew).data
        return {'status': 'success', 'data': result, 'code': 'SUCCESS_CREW_LIST_FETCHED'}, 200

class CrewList(Resource):
    def get(self):
        crew = CrewModel.query.all()
        result = crews_schema.dump(crew).data
        return {'status': 'success', 'data': result, 'code': 'SUCCESS_CREW_FETCHED'}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
                return {'status': 'error',
                    'message': 'No input data provided',
                    'code': 'ERROR_NO_DATA_PROVIDED'}, 400

        # Validate and deserialize input
        data, errors = crew_schema.load(json_data)
        if errors:
            return {'status': 'error',
                'errors': errors,
                'code': 'ERROR_INPUT_VALIDATION'}, 422

        crew = CrewModel(
            nickname=data['nickname'],
            email=data['email'],
            phone=data['phone'],
            is_admin=data['is_admin'])

        try:
            db.session.add(crew)
            db.session.commit()
        # IntegrityError has an 'orig' attr that says "Duplicate entry 'foo' for key 'column'"
        #  It also does Foreign Keys, haven't checked what they look like
        # NOTE: This is very MySQL specific and probably won't work with other database engines.
        except IntegrityError as err:
            # Find the column, \w+ (non-whitespace) is what we're looking for
            # err.orig doesn't have a __str__ method, so use `repr()` to get a string representation
            res = search("(?<=key ')\w+", repr(err.orig))
            if res == None: # Unknown error... Probably a FK constraint...
                return {'status': 'error', 'message': 'Unknown integrity error', 'code': 'ERROR_UNKNOWN_ERROR'}, 409
            return {'status': 'error', 'message': "{} already exists".format(res[0].title()), 'code': "ERROR_EXISTING_{}".format(res[0].upper())}, 409

        result = crew_schema.dump(crew).data
        return { 'status': 'success', 'data': result, 'code': 'SUCCESS_CREW_CREATED' }, 201
