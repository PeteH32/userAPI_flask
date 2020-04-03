from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

# Create the Flask application
app = Flask(__name__)
app.config['DEBUG'] = True


# Initialize SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://localuser:localpassword@db/user_api_db'
db = SQLAlchemy(app)

'''
NOTE: This is based directly on the tutorial from flask-rest-jsonapi:
    https://flask-rest-jsonapi.readthedocs.io/en/latest/quickstart.html
'''

# Create data storage
class Bmduser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    birth_date = db.Column(db.Date)
    password = db.Column(db.String)


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String)
    bmduser_id = db.Column(db.Integer, db.ForeignKey('bmduser.id'))
    bmduser = db.relationship('Bmduser', backref=db.backref('exams'))

db.create_all()


# Create logical data abstraction (same as data storage for this first example)
class BmduserSchema(Schema):
    class Meta:
        type_ = 'bmduser'
        self_view = 'bmduser_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'bmduser_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(load_only=True)
    birth_date = fields.Date()
    # Change "password" to this to make it read-only (won't be exposed in GET responses).
    # password = fields.Str(required=True, load_only=True)
    password = fields.Str(required=True)
    exams = Relationship(self_view='bmduser_exams',
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
    serial = fields.Str(required=True)
    bmduser_id = fields.Integer(required=True)
    owner = Relationship(attribute='bmduser',
                         self_view='exam_bmduser',
                         self_view_kwargs={'id': '<id>'},
                         related_view='bmduser_detail',
                         related_view_kwargs={'exam_id': '<id>'},
                         schema='BmduserSchema',
                         type_='bmduser')


# Create resource managers
class BmduserList(ResourceList):
    schema = BmduserSchema
    data_layer = {'session': db.session,
                  'model': Bmduser}


class BmduserDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('exam_id') is not None:
            try:
                exam = self.session.query(Exam).filter_by(id=view_kwargs['exam_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'exam_id'},
                                     "Exam: {} not found".format(view_kwargs['exam_id']))
            else:
                if exam.bmduser is not None:
                    view_kwargs['id'] = exam.bmduser.id
                else:
                    view_kwargs['id'] = None

    schema = BmduserSchema
    data_layer = {'session': db.session,
                  'model': Bmduser,
                  'methods': {'before_get_object': before_get_object}}


class BmduserRelationship(ResourceRelationship):
    schema = BmduserSchema
    data_layer = {'session': db.session,
                  'model': Bmduser}


class ExamList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Exam)
        if view_kwargs.get('id') is not None:
            try:
                self.session.query(Bmduser).filter_by(id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'id'}, "Bmduser: {} not found".format(view_kwargs['id']))
            else:
                query_ = query_.join(Bmduser).filter(Bmduser.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get('id') is not None:
            bmduser = self.session.query(Bmduser).filter_by(id=view_kwargs['id']).one()
            data['bmduser_id'] = bmduser.id

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
api.route(BmduserList, 'bmduser_list', '/bmdusers')
api.route(BmduserDetail, 'bmduser_detail', '/bmdusers/<int:id>', '/exams/<int:exam_id>/owner')
api.route(BmduserRelationship, 'bmduser_exams', '/bmdusers/<int:id>/relationships/exams')
api.route(ExamList, 'exam_list', '/exams', '/bmdusers/<int:id>/exams')
api.route(ExamDetail, 'exam_detail', '/exams/<int:id>')
api.route(ExamRelationship, 'exam_bmduser', '/exams/<int:id>/relationships/owner')

if __name__ == '__main__':
    # Start application
    app.run(debug=True)
