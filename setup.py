import os
from app import create_app, db
from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv
from app.models import Penerbangan, Maskapai, User, Role

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv("FLASK_ENV"))
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, db=db, Maskapai=Maskapai, Penerbangan=Penerbangan, User=User, Role=Role
    )


@app.cli.command()
def deploy():
    upgrade()
