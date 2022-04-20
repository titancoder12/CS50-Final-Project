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
People = [{"firstName":"Joe", "lastName":"Lee", "age":30, "role":"player", "team_id":1, "id": 0},
          {"firstName":"Bob", "lastName":"Lao", "age":35, "role":"coach", "team_id":1, "id": 1},
          {"firstName":"Foo", "lastName":"Lin", "age":10, "role":"player", "team_id":1, "id": 2}]

Teams = [{"name":"ND Athletics", "id": 1}]

person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Name of person is required", required=True)
person_put_args.add_argument("age", type=int, help="Age of person is required", required=True)

# STILL NEED TO ADD MORE RESOURCES FOR PEOPLE
# people_resource_fields = {
#     'id': fields.Integer,
#     'name': fields.String,
#     'age': fields.Integer

# }

# db.create_all() # Eugene

class Person(Resource):

    # @marshal_with(resource_fields)
    def get(self, person_id):
        return People[person_id]
    
    # @marshal_with(resource_fields)
    def put(self):
        args = person_put_args.parse_args()
        args["id"] = len(People)
        People.append(args)
        
        
        return args, 201
    
class Team(Resource):

    # @marshal_with(resource_fields)
    def get(self, team_id):
        team_people = {}
        for person in People:
            if person["team_id"] == team_id:
                team_people[person["firstName"]+" "+person["lastName"]] = person["role"]
        return team_people
    
    # @marshal_with(resource_fields)
    def put(self):
        args = person_put_args.parse_args()
        args["id"] = len(People)
        People.append(args)
        print(People)
        
        return People, 201

api.add_resource(Person, "/person","/person/", "/person/<int:person_id>")
api.add_resource(Team, "/team", "/team/", "/team/<int:team_id>")



if __name__ == "__main__":
    app.run(debug=True)