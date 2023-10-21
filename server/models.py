from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import enum

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Environment(enum.Enum):
    GRASS = "grass"
    SAND = "sand"
    WATER="water"

class Zookeeper(db.Model):
    __tablename__ = 'zookeepers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    birthday = db.Column(db.String(20))
    animals = db.relationship("Animal", backref="wild", lazy=True)

class Enclosure(db.Model):
    __tablename__ = 'enclosures'

    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(enum.Enum(Environment))
    open_to_visitors = db.Column(db.Boolean, default=False, nullable=False)
    animals = db.relationship("Animal", backref="wild", lazy=True)
class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    species = db.Column(db.String(20))
    zookeeper = db.Column(db.Integer(), db.ForeignKey("zookeeper.id"))
    enclosure = db.Column(db.Integer(), db.ForeignKey("enclosure.id"))
