from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify
import base64

db_connect = create_engine("sqlite:///sqlite.db")
app = Flask(__name__)
api = Api(app)

class Data(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from test_mic")
        result = {'results': [dict(zip(tuple(query.keys()),i)) for i in query.cursor]}
        return result, 200, {"Access-Control-Allow-Origin":"*"}

    def post(self):
        data = request.get_json()
        conn = db_connect.connect()
        command = data["command"]
        position = data["position"]
        id_mic = data["id_mic"]
        ts = data["ts"]
        #decode string containing the wav data
        audio_data = "data:audio/wav;base64," + data["audio_data"]
        query = conn.execute("insert into test_mic values (?,?,?,?,?)", id_mic , ts , position , command, audio_data)

api.add_resource(Data, '/data')

if __name__ == '__main__':
	app.run(host= '0.0.0.0',port='8080' )
