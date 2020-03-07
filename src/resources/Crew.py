from flask_restful import Resource
from models.Crew import CrewModel
from schemas.Crew import CrewSchema

crews_schema = CrewSchema(many=True)
crew_schema = CrewSchema()

class Crew(Resource):
    def get(self):
        crew = CrewModel.query.all()
        crew = crews_schema.dump(crew).data
        return {'status': 'success', 'data': crew}, 200