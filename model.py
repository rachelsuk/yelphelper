from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/
# https://hackersandslackers.com/flask-sqlalchemy-database-models/
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html

app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.Text, nullable=False)
    lname = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.fname} {self.lname}>"


class YelpHelperSession(db.Model):
    __tablename__ = 'yelphelper_sessions'

    session_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    term = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer)

    users = db.relationship("User",
                            secondary="users_yelphelper_sessions",
                            backref="yelphelper_sessions")

    def __repr__(self):
        return f"<Session {self.date}>"


class UserYelpHelperSession(db.Model):
    __tablename__ = 'users_yelphelper_sessions'

    user_session_id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey(
        'yelphelper_sessions.session_id'))

    def __repr__(self):
        return f"<User {self.user_id} Session {self.session_id}>"


class Business(db.Model):
    __tablename__ = 'businesses'

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alias = db.Column(db.Text)
    name = db.Column(db.Text)
    image_url = db.Column(db.Text)
    url = db.Column(db.Text)
    review_count = db.Column(db.Integer)
    yelp_rating = db.Column(db.Integer)
    price = db.Column(db.Integer)
    address = db.Column(db.Text)
    distance = db.Column(db.Integer)

    def __repr__(self):
        return f"<Business {self.name}>"


class Score(db.Model):
    __tablename__ = 'scores'

    score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(
        db.Integer, db.ForeignKey('businesses.business_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey(
        'yelphelper_sessions.session_id'))
    score = db.Column(db.Integer)

    business = db.relationship('Business', backref='scores')
    user = db.relationship('User', backref='scores')
    session = db.relationship('YelpHelperSession', backref='scores')

    def __repr__(self):
        return f"<Rating by user {self.user_id} for business {self.business_id} during session {self.session_id}>"


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///yelphelper'
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    db.create_all()
