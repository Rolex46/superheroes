from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heros'

    serialize_rules = ('-hero_powers.hero',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='hero')


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('strength')
    def validate_strength(self,key,strength):
        valid_strength = ['Weak', 'Strong', 'Average']
        if strength not in valid_strength:
            raise ValueError('Invalid strength. Allowed values are "Weak", "Strong","Average"')

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    serialize_rules = ('hero_powers.power',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship('HeroPower', backref='power')

    @validates('description')
    def validate_description(self,key,description):
        if not description:
            raise ValueError("Description must be present")
        if len(description) < 20:
            raise ValueError("Description must be atleast 20 characters long")