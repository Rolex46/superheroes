#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import Hero, HeroPower, Power, db

fake = Faker()

with app.app_context():
    Hero.query.delete()
    HeroPower.query.delete()
    Power.query.delete()

    heros = []
    for i in range(50):
        h = Hero(
            name=fake.name(),
            super_name=fake.sentence(),
        )
        heros.append(h)

    db.session.add_all(heros)

    powers = []
    for i in range(50):
        p = Power(
            name=fake.name(),
            description=fake.sentence(),
        )
        powers.append(p)
    db.session.add_all(powers)

    hero_powers = []
    for h in heros:
        for i in range(randint(1, 10)):
            hp = HeroPower(
                strength=fake.sentence(),
                hero=h,
                power=rc(powers),
            )
            hero_powers.append(hp)

    db.session.add_all(hero_powers)

    for p in powers:
        hp = rc(hero_powers)
        p.hero_power = hp
        hero_powers.remove(hp)

    db.session.commit()
