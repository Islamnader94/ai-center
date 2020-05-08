from flask import request
from flask_restful import Resource
from Model import db, DataScanned, DataScannedSchema
import json

all_scanned_schema = DataScannedSchema(many=True)
scanned_schema = DataScannedSchema()


class ScannedDataResource(Resource):
    @staticmethod
    def get():
        scanned = DataScanned.query.all()
        scanned = all_scanned_schema.dump(scanned)
        return {'status': 'success', 'data': scanned}, 200


    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = scanned_schema.loads(response)
        scanned_data = DataScanned.query.filter_by(email=data[0]['email']).first()
        if scanned_data:
            return {'message': 'Data already exists'}, 400
        scanned_data = DataScanned(
            email=data[0]['email'],
            phone=data[0]['phone']
        )

        db.session.add(scanned_data)
        db.session.commit()

        result = scanned_schema.dump(scanned_data)

        return {"status": 'success', 'data': result}, 201