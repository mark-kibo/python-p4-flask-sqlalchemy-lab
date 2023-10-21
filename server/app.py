#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal=Animal.query.get(id)
    if animal:
        return f"""
    <ul>
        <li>ID: {animal.id}</li>
        <li>Name: {animal.name}</li>
        <li>Species: {animal.species}</li>
        <li>Zookeeper: {animal.zookeeper.name}</li>
        <li>Enclosure: {animal.enclosure.environment}</li>
        
    </ul>


"""
    return None

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper=Zookeeper.query.get(id)
    animals = ""
    if zookeeper:
        for animal in zookeeper.wild:
            animals += f"<li>Animal: {animal.name}</li>"

        return f"""
        <ul>
            <li>ID: {zookeeper.id}</li>
            <li>Name: {zookeeper.name}</li>
            <li>Birthday: {zookeeper.birthday}</li>
            <li>
                <ul>
                    {animals}
                </ul>
            </li>
        </ul>
        """
    return None

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure=Enclosure.query.get(id)
    animals=""
    if enclosure:
        for animal in enclosure.wild:
            animals += f"<li>Animal: {animal.name}</li>"
        return f"""
        <ul>
            <li>ID: {enclosure.id}</li>
            <li>Environment: {enclosure.environment}</li>
            <li>Open to Visitors: {enclosure.open_to_visitors}</li>
            <li>
                <ul>
                    {animals}
                </ul>
            </li>
        </ul>
        """
    return ''


if __name__ == '__main__':
    manager.run()
    app.run(port=5555, debug=True)
