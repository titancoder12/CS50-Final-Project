from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields
app = Flask(__name__)
api = Api(app)

# test comment
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#db = SQLAlchemy(app)

# class VideoModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     views = db.Column(db.Integer, nullable=False)
#     likes = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"
People = [{"firstname":"Joe", "lastname":"Lee", "age":30, "role":"player", "team_id":1, "id": 0},
          {"firstname":"Bob", "lastname":"Lao", "age":35, "role":"coach", "team_id":1, "id": 1},
          {"firstname":"Foo", "lastname":"Lin", "age":10, "role":"player", "team_id":1, "id": 2}]

person_put_args = reqparse.RequestParser()
person_put_args.add_argument("firstname", type=str, help="First name of person is required", required=True)
person_put_args.add_argument("lastname", type=str, help="Last name of person is required", required=True)
person_put_args.add_argument("age", type=int, help="Age of person is required", required=True)
person_put_args.add_argument("role", type=str, help="Role of person is required", required=True)
person_put_args.add_argument("team_id", type=int, required=False)

person_update_args = reqparse.RequestParser()
person_update_args.add_argument("firstname", type=str)
person_update_args.add_argument("lastname", type=str)
person_update_args.add_argument("age", type=int)
person_update_args.add_argument("role", type=str)
person_update_args.add_argument("team_id", type=int)

people_resource_fields = {
    'id': fields.Integer,
    'team_id': fields.Integer,
    'firstname': fields.String,
    'lastname': fields.String,
    'age': fields.Integer,
    'role': fields.String,
}


Teams = [{}, {"name":"ND Athletics", "id": 1}]

team_put_args = reqparse.RequestParser()
team_put_args.add_argument("name", type=str, help="Name of team is required", required=True)

team_update_args = reqparse.RequestParser()
team_update_args.add_argument("name", type=str)

team_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

# db.create_all() # Eugene

class Person(Resource):

    # @marshal_with(people_resource_fields)
    def get(self, firstname, lastname):
        for i in range(len(People)):
            if (People[i]["firstname"] == firstname) and (People[i]["lastname"] == lastname):
                return People[i]
        print(People[i])
        return {"error": 404}
    
    # @marshal_with(people_resource_fields)
    def put(self):
        args = person_put_args.parse_args()
        args["team_id"] = 0
        args["id"] = len(People)
        args_copy = args.copy()
        print(args_copy)
        People.append(args_copy)
        print(People)
        return args, 201
    
    def patch(self, person_id):
        args = person_update_args.parse_args()
        if args["firstname"]:
            People[person_id]["firstname"] = args["firstname"]
        if args["lastname"]:
            People[person_id]["lastname"] = args["lastname"]
        if args["role"]:
            People[person_id]["role"] = args["role"]
        if args["age"]:
            People[person_id]["age"] = args["age"]
        if args["team_id"]:
            People[person_id]["team_id"] = args["team_id"]
        print(args["role"])
        print(People[person_id]["role"])


    
class Team(Resource):

    # @marshal_with(team_resource_fields)
    def get(self, team_id):
        team = {}
        if len(Teams) < int(team_id):
            return {"message": 404}
        team["name"] = Teams[team_id]["name"]
        team["id"] = Teams[team_id]["id"]
        for person in People:
            if person["team_id"] == team_id:
                team[person["firstname"]+" "+person["lastname"]] = person["role"]
        return team
    
    # @marshal_with(team_resource_fields)
    def put(self):
        args = team_put_args.parse_args()
        args["id"] = len(Teams)
        args_copy = args.copy()
        Teams.append(args_copy)
        print(Teams)
        return len(Teams)-1

    def patch(self, team_id):
        args = team_update_args.parse_args()
        if args["name"]:
            Teams[team_id]["name"] = args["name"]
        return Teams[team_id]
        
api.add_resource(Person, "/person","/person/", "/person/<int:person_id>", "/person/<string:firstname>_<string:lastname>")
api.add_resource(Team, "/team", "/team/", "/team/<int:team_id>")



if __name__ == "__main__":
    app.run(debug=True)