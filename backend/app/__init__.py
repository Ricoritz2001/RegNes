import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Load default config
    config_class = os.getenv('FLASK_CONFIG', 'app.config.DevelopmentConfig')
    app.config.from_object(config_class)

    # Optional override from instance/config.py
    app.config.from_pyfile('config.py', silent=True)

    # Optional test override
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Ensure instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Fallback SQLite path if none set
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        db_file = os.path.join(app.instance_path, 'flaskr.sqlite')
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.status import bp as status_bp
    from app.routes.trends import bp as trends_bp
    from app.routes.geojson_region import bp as geojson_bp
    from app.routes.regional_data import bp as regional_bp
    from app.routes.heatmap import bp as heatmap_bp

    app.register_blueprint(status_bp)
    app.register_blueprint(trends_bp)
    app.register_blueprint(geojson_bp)
    app.register_blueprint(regional_bp)
    app.register_blueprint(heatmap_bp)

    # CLI: Ingest data command
    @app.cli.command("ingest-data")
    @click.argument("data_folder", type=click.Path(exists=True))
    @with_appcontext
    def ingest_data_cli(data_folder):
        from app.services.data_ingestion import ingest
        ingest(data_folder)
        click.secho("CSV/TSV ingestion complete!", fg="green")

    return app
