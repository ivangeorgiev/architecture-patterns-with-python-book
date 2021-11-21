import datetime
import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import config
from ..domain import model
from ..adapters import orm
from ..service_layer import services
from ..service_layer.unit_of_work import SqlAlchemyUnitOfWork

orm.start_mappers()

def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

def create_app(test_config=None):
    app = Flask(__name__)

    default_database = os.path.join(app.instance_path, "learning.sqlite")
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE_URL=f'sqlite:///{default_database}',
    )

    app.config.from_pyfile("config.py", silent=True)
    if test_config is not None:
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- print(f"Initialize DB with url: {app.config['DATABASE_URL']}")
    engine = create_engine(app.config['DATABASE_URL'])
    app.db = engine
    orm.metadata.create_all(engine)
    get_sesion = sessionmaker(bind=engine)

    @app.route("/hello")
    def hello():
        return "Hello, World!"


    @app.route("/")
    def hello_world():
        from pathlib import Path
        (Path(__file__).parent / "flask_app.py").touch()
        return "<p>Hello, World!</p>"

    @app.route('/allocate', methods=['POST'])
    def allocate_endpoint():
        line = (
            request.json['orderid'],
            request.json['sku'],
            request.json['qty']
        )

        try:
            with SqlAlchemyUnitOfWork(get_sesion) as uow:
                batchref = services.allocate(*line, uow)
        except (model.OutOfStock, services.InvalidSku) as e:
            return jsonify({"message": str(e)}), 400

        return jsonify({'batchref':batchref}), 201

    @app.route("/add_batch", methods=['POST'])
    def add_batch():
        eta = request.json['eta']
        if eta is not None:
            eta = datetime.datetime.fromisoformat(eta).date()
        batch = (
            request.json['ref'],
            request.json['sku'],
            request.json['qty'],
            eta,
        )
        with SqlAlchemyUnitOfWork(get_sesion) as uow:
            services.add_batch(*batch, uow)
        return 'OK', 201

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
