from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from request_logging import init_logging

# Create the Flask application
app = Flask(__name__)
app.config['DEBUG'] = True


# Initialize SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localuser:localpassword@db/user_api_db'
db = SQLAlchemy(app)
init_logging(app)

'''
NOTE: This is based directly on the tutorial from flask-rest-jsonapi:
    https://flask-rest-jsonapi.readthedocs.io/en/latest/quickstart.html
'''

################################################################################
#
#   For explanation of the below 3 layers, see flask-rest-jsonapi docs here:
#       https://flask-rest-jsonapi.readthedocs.io/en/latest/index.html
#
#   DATABASE LAYER  <==  DATA ABSTRACTION LAYER  <==  REST API LAYER
#
################################################################################


################################################################################
# DATABASE LAYER
################################################################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email_address = db.Column(db.String)
    zip_code = db.Column(db.String)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_date = db.Column(db.Date)
    notes = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('exams'))

db.create_all()


################################################################################
# DATA ABSTRACTION LAYER
################################################################################
class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'user_list'

    id = fields.Integer(as_string=True, dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    # Change "email_address" to this to make it read-only (won't be exposed in GET responses).
    # email_address = fields.Email(required=True, load_only=True)
    email_address = fields.Email(required=True)
    zip_code = fields.Str(required=True)
    exams = Relationship(self_view='user_exams',
                             self_view_kwargs={'id': '<id>'},
                             related_view='exam_list',
                             related_view_kwargs={'id': '<id>'},
                             many=True,
                             schema='ExamSchema',
                             type_='exam')


class ExamSchema(Schema):
    class Meta:
        type_ = 'exam'
        self_view = 'exam_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    exam_date = fields.Date()
    notes = fields.Str(required=True)
    user_id = fields.Integer(required=True)
    patient = Relationship(attribute='user',
                         self_view='exam_user',
                         self_view_kwargs={'id': '<id>'},
                         related_view='user_detail',
                         related_view_kwargs={'exam_id': '<id>'},
                         schema='UserSchema',
                         type_='user')


################################################################################
# REST API LAYER
################################################################################
class UserList(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class UserDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('exam_id') is not None:
            try:
                exam = self.session.query(Exam).filter_by(id=view_kwargs['exam_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'exam_id'},
                                     "Exam: {} not found".format(view_kwargs['exam_id']))
            else:
                if exam.user is not None:
                    view_kwargs['id'] = exam.user.id
                else:
                    view_kwargs['id'] = None

    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User,
                  'methods': {'before_get_object': before_get_object}}


class UserRelationship(ResourceRelationship):
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}


class ExamList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Exam)
        if view_kwargs.get('id') is not None:
            try:
                self.session.query(User).filter_by(id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "User: {} not found".format(view_kwargs['id']))
            else:
                query_ = query_.join(User).filter(User.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get('id') is not None:
            user = self.session.query(User).filter_by(id=view_kwargs['id']).one()
            data['user_id'] = user.id

    schema = ExamSchema
    data_layer = {'session': db.session,
                  'model': Exam,
                  'methods': {'query': query,
                              'before_create_object': before_create_object}}


class ExamDetail(ResourceDetail):
    schema = ExamSchema
    data_layer = {'session': db.session,
                  'model': Exam}


class ExamRelationship(ResourceRelationship):
    schema = ExamSchema
    data_layer = {'session': db.session,
                  'model': Exam}


# Create endpoints
api = Api(app)
api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>', '/exams/<int:exam_id>/patient')
api.route(UserRelationship, 'user_exams', '/users/<int:id>/relationships/exams')
api.route(ExamList, 'exam_list', '/exams', '/users/<int:id>/exams')
api.route(ExamDetail, 'exam_detail', '/exams/<int:id>')
api.route(ExamRelationship, 'exam_user', '/exams/<int:id>/relationships/patient')

if __name__ == '__main__':
    # Start application
    app.run(debug=True)
