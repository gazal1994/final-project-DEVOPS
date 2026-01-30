from flask import Flask, Blueprint, jsonify
from flask_restplus import Api
from ma import ma
from db import db

from resources.store import Store, StoreList, store_ns, stores_ns
from resources.item import Item, ItemList, items_ns, item_ns
from marshmallow import ValidationError

app = Flask(__name__)
bluePrint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    bluePrint, 
    doc='/doc', 
    title='DevOps Final Project - REST API',
    version='1.0.0',
    description='''
    🚀 Professional REST API for Store and Item Management
    
    Built with Flask-RESTPlus and deployed using modern DevOps practices:
    • Containerized with Docker
    • CI/CD with GitHub Actions  
    • Deployed on AWS EC2
    • Automated deployment pipeline
    
    This API provides complete CRUD operations for managing stores and items.
    ''',
    contact='Gazal',
    contact_email='your-email@example.com',
    license='MIT',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY'
        }
    }
)
app.register_blueprint(bluePrint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api.add_namespace(item_ns)
api.add_namespace(items_ns)
api.add_namespace(store_ns)
api.add_namespace(stores_ns)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


item_ns.add_resource(Item, '/<int:id>')
items_ns.add_resource(ItemList, "")
store_ns.add_resource(Store, '/<int:id>')
stores_ns.add_resource(StoreList, "")

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True,host='0.0.0.0')
