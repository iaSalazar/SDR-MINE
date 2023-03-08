from ..models.user_model import User, user_schema, users_schema
from flask_restful import Resource
from ..app.extensions import db, api, guard
from flask import request
from flask_restful import Resource


class ResourceAuthSignIn(Resource):

    def post(self):
        try:
            requestRoles = request.json['roles']
            requestRoles.append('user')
            print(requestRoles)
            new_user = User(

                username=request.json['username'],
                hashed_password=guard.hash_password(request.json['password']),
                roles=requestRoles

            )

            user = User.query.filter(
                User.username == new_user.username).first()
            if user == None:
                db.session.add(new_user)
                db.session.commit()
                return user_schema.dump(new_user)
            elif user != None:
                return {"error_msg": "Username already registered"}, 409

        except KeyError:

            new_user = User(

                username=request.json['username'],
                hashed_password=guard.hash_password(request.json['password']),
                roles=['user']

            )

            user = User.query.filter(
                User.username == new_user.username).first()
            if user == None:
                db.session.add(new_user)
                db.session.commit()
                return user_schema.dump(new_user)
            elif user != None:
                return {"error_msg": "Username already registered"}, 409


class ResourceAuthLogIn(Resource):

    def post(self):
        """ username = request.json.get("username", None)
        password = request.json.get("password", None)

        if username != "test" or password != "test" or username =='':
        return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token) """
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        usert = guard.authenticate(username, password)
        user = User.query.filter_by(username=username).first()
        ret = {'access_token': guard.encode_jwt_token(usert),
               'id': user.id, 'roles': user.roles, 'username': user.username}
        return ret, 200


class ResourceRefreshAuth(Resource):

    def post(self):
        """
        Refreshes an existing JWT by creating a new one that is a copy of the old
        except that it has a refrehsed access expiration.
          .. example::
        $ curl http://localhost:5000/api/refresh -X GET \
          -H "Authorization: Bearer <your_token>"
         """
        print("refresh request")
        # old_token = request.get_data()
        old_token = request.json.get("acces_token", None)
        new_token = guard.refresh_jwt_token(old_token)
        ret = {'access_token': new_token}
        return ret, 200


api.add_resource(ResourceAuthSignIn, '/api/auth/signIn')
api.add_resource(ResourceAuthLogIn, '/api/auth/logIn')
api.add_resource(ResourceRefreshAuth, '/api/auth/refreshAuth')
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')


# @app.route('/api/members', methods=["GET"])
# @flask_praetorian.auth_required
# def members():
#     # Access the identity of the current user with get_jwt_identity

#     # return jsonify(logged_in_as=current_user), 200
#     return jsonify(
#         message="protected endpoint (allowed user {})".format(
#             flask_praetorian.current_user().username,
#         )
#     )
#     return {"members": ["member1", "Member2", "Member3"]}, 200


# # Create a route to authenticate your users and return JWTs. The
# # create_access_token() function is used to actually generate the JWT.


# @app.route("/api/users/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     """
#     get user
#     """
#     user = User.query.get_or_404(user_id)
#     print(user.roles)
#     return user_schema.dump(user)
