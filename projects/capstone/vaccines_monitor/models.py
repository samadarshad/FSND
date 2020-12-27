import os
from sqlalchemy import Column, String, create_engine, Integer, Boolean, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import config
from flask_migrate import Migrate

database_path = os.getenv('DATABASE_URL')
print(database_path)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    db.create_all()

class Patient(db.Model):
  __tablename__ = 'patients'

  id = Column(Integer, primary_key=True)
  user_id = Column(String) # foreign key to Auth0 database
  
  name = Column(String)
  age = Column(Integer)
  had_covid = Column(Boolean)
  tests = db.relationship('Test', backref=__tablename__, lazy='dynamic', cascade="all, delete", passive_deletes=True)

  def __init__(self, user_id, name, age, had_covid):
    self.user_id = user_id
    self.name = name
    self.age = age
    self.had_covid = had_covid

  def format(self):
    return {
        'id': self.id,
        'user_id': self.user_id,
        'name': self.name,
        'age': self.age,
        'had_covid': self.had_covid
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

class Vaccine(db.Model):
  __tablename__ = 'vaccines'

  id = Column(Integer, primary_key=True)

  name = Column(String)
  tests = db.relationship('Test', backref=__tablename__, lazy='dynamic')

  def __init__(self, name):
    self.name = name

  def format(self):
    return {
        'id': self.id,
        'name': self.name
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


class Test(db.Model):
  __tablename__ = 'tests'

  id = Column(Integer, primary_key=True)
  effective = Column(Boolean)
  patient_id = Column(Integer, ForeignKey('patients.id', ondelete="CASCADE"), nullable=False)
  vaccine_id = Column(Integer, ForeignKey('vaccines.id'), nullable=False)

  def __init__(self, effective, patient_id, vaccine_id):
    self.effective = effective
    self.patient_id = patient_id
    self.vaccine_id = vaccine_id

  def format(self):
    return {
        'id': self.id,
        'effective': self.effective,
        'patient_id': self.patient_id,
        'patient_age': self.patients.age,
        'patient_had_covid': self.patients.had_covid,
        'vaccine_id': self.vaccine_id
    }

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
 
