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
    🚀 **Professional REST API for Store and Item Management**
    
    ### Built with Modern DevOps Stack:
    
    | Technology | Purpose |
    |------------|---------|
    | 🐳 Docker | Containerization |
    | ⚙️ GitHub Actions | CI/CD Pipeline |
    | ☁️ AWS EC2 | Cloud Hosting |
    | 🔄 Automated Deployment | Zero-downtime updates |
    
    ### Features:
    - ✅ Complete CRUD operations for stores and items
    - ✅ RESTful API design
    - ✅ Automated testing and deployment
    - ✅ Scalable architecture
    - ✅ Production-ready configuration
    
    ### Deployment Info:
    - **Platform:** AWS EC2 (eu-north-1)
    - **Container:** Docker
    - **CI/CD:** GitHub Actions
    - **Image:** Available on Docker Hub
    
    ---
    
    **Repository:** [GitHub](https://github.com/gazal1994/final-project-DEVOPS) | 
    **Docker Hub:** [gazal94/final-python-app](https://hub.docker.com/r/gazal94/final-python-app)
    ''',
    contact='Gazal - DevOps Engineer',
    contact_url='https://github.com/gazal1994/final-project-DEVOPS',
    license='MIT License',
    license_url='https://opensource.org/licenses/MIT',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-KEY',
            'description': 'API Key for authentication (Future implementation)'
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
