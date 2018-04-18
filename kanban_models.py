__author__ = 'roiman'
#Kanban Models
from uuid import uuid4
from sqlalchemy import Integer, String, Text, Binary, Column, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, as_declarative

#for form creation
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Length

# for user creation and managemnet
from flask_login import UserMixin
import os


# connecting to the database
engine = create_engine('sqlite:///'+os.getcwd()+'/kanban.db')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
# I am very sure I am not handling this correctly,
# the connection is not lost when the app is stopped

# defining our tables
Base = declarative_base()

class Task(Base):
	"defines a Task"
	__tablename__ = "tasks"
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	text = Column(String)
	statusID = Column(Integer, nullable=False)	
	user_id = Column(String, ForeignKey('users.id'),
        nullable=False)

class User(Base, UserMixin):
	"defines users"
	__tablename__ = "users"
	id = Column(String, default=lambda: str(uuid4()), primary_key=True, nullable=False)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)

# creating tables
Base.metadata.create_all(engine)


# check for uniqueness of data (from https://github.com/rpicard/explore-flask/blob/fa361d505f6716007a237afd6bf1d1bebb570ebf/source/forms.rst)
class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = session.query(self.model).filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


# form for logging in
class LoginForm(FlaskForm):
	"""
	A class to handle login
	"""
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		rv = FlaskForm.validate(self)
		if not rv:
			return False

		# there is room for error handling and logging
		self.username = str(self.username)
		user = session.query(User).filter_by(username=self.username).first()
		if user is None:
			# self.username.errors.append('Unknown username')
			return False

		if not user.check_password(self.password.data):
			# self.password.errors.append('Invalid password')
			return False

		self.user = user
		return True

# name was just kept since I originally thought to ask for an email
# but that's too much typing for quick test ^^"
class EmailPasswordForm(FlaskForm):
	"""Form for registering"""
	username = StringField('Username', validators=[DataRequired(),
		Length(min=4, max=25),
		Unique(
            User,
            User.username,
            # TODO: one of these days,
            # this message will be shown somewhere
            message=u'Username Exists.')])
	password = PasswordField('Password', validators=[DataRequired(),
		Length(min=4, max=25)])


if __name__ == '__main__':
	app.run(debug=True)