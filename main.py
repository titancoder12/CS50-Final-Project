from flask import Flask
from flask_restful import Api, Resource, marshal, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#db = SQLAlchemy(app)

# class VideoModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     views = db.Column(db.Integer, nullable=False)
#     likes = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"
People = [{"name":"Joe", "age":"30", "id": 0},
          {"name":"Bob", "age":"15", "id": 1},
          {"name":"Alice", "age":"10", "id": 2}]

person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Name of person is required", required=True)
person_put_args.add_argument("age", type=int, help="Age of person is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of person is required")
video_update_args.add_argument("age", type=int, help="Age of person is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer
}

# db.create_all() # Eugene

class Person(Resource):
    # @marshal_with(resource_fields)
    def get(self, person_id):
        result = People[person_id]
        if not result:
            abort(404, message="Person not found")
        return result
    
    # @marshal_with(resource_fields)
    def put(self, person_id):
        args = person_put_args.parse_args()
        result = People[person_id]
        if result:
            abort(409, message="Person ID taken")
        People[person_id] = args
        
        return People[person_id], 201
    
    # @marshal_with(resource_fields)
    # def patch(self, video_id):
    #     args = video_update_args.parse_args()
    #     result = VideoModel.query.filter_by(id=video_id).first()
    #     if not result:
    #         abort(404, message="Video doesn't exist")
    #     if args['name']:
    #         result.name = args['name']
    #     if args['views']:
    #         result.views = args['views']
    #     if args['likes']:
    #         result.likes = args['likes']
        
        #db.session.commit()

        # return result

        
api.add_resource(Person, "/person/<int:person_id>")

if __name__ == "__main__":
    app.run(debug=True)