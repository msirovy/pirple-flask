#from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    group = db.Column(db.String(100), unique=False, default="users")
    enabled = db.Column(db.Integer, default=1)

    def __repr__(self):
        return self.email

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, **kw):
        try:
            obj = cls(**kw)
            db.session.add(obj)
            db.session.commit()
            return True
            
        except IntegrityError as err:
            print(err)
            return False

    @classmethod
    def delete(cls, **kw):
        try:
            obj = cls(**kw)
            db.session.delete(obj)
            db.session.commit()
            return True
            
        except IntegrityError as err:
            print(err)
            return False

    @classmethod
    def verify_user(self, email, password):
        print(email)
        # TODO
        try:
            User.query.filter_by(email=email, password=password).first()

            print("Result of auth: ", usr)
            print("END RESULT")
        except IOError as err:
            print(err)

        return True


class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(30), default=str(datetime.datetime.now()), unique=False)
    email = db.Column(db.String(120), unique=False)
    activity = db.Column(db.String(100))
    status = db.Column(db.String(10))
    message = db.Column(db.String(350))

    def __repr__(self):
        return dict(email=self.email, activity=self.activity, time=self.time, status=self.status)

    def __str__(self):
        return self.time, " - ", self.activity

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()


class Pages(db.Model):
    __tablename__ = "pages"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(160), unique=False)
    text = db.Column(db.Text)
    author = db.Column(db.String(120), unique=False)


    def __repr__(self):
        return '<Page %r>' % self.slug
    
    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()
