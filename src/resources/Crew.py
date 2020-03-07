from run import db
from flask import request
from flask_restful import Resource
from models.Crew import CrewModel
from schemas.Crew import CrewSchema

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

        # Check if nickname already exists
        crew_nick_exists_test = CrewModel.query.filter_by(nickname=json_data['nickname']).first()
        if crew_nick_exists_test:
            return {'status': 'error',
                'message': 'Nickname already exists',
                'code': 'ERROR_EXISTING_NICKNAME'}, 409

        # Check if email already exists
        crew_email_exists_test = CrewModel.query.filter_by(email=json_data['email']).first()
        if crew_email_exists_test:
            return {'status': 'error',
                'message': 'Email already exists',
                'code': 'ERROR_EXISTING_EMAIL'}, 409

        # Check if phone already exists
        crew_phone_exists_test = CrewModel.query.filter_by(phone=json_data['phone']).first()
        if crew_phone_exists_test:
            return {'status': 'error',
                'message': 'Phone already exists',
                'code': 'ERROR_EXISTING_PHONE'}, 409

        crew = CrewModel(
            nickname=data['nickname'],
            email=data['email'],
            phone=data['phone'],
            is_admin=data['is_admin'])

        db.session.add(crew)
        db.session.commit()

        result = crew_schema.dump(crew).data
        return { 'status': 'success', 'data': result, 'code': 'SUCCESS_CREW_CREATED' }, 201