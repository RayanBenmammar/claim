import datetime
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

load_dotenv()

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class File(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[str] = mapped_column(String(50), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(50), nullable=False)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "Hello, Claim!"


@app.route("/documents", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify(error="No file uploaded"), 400
    file = request.files["file"]
    document = File(
        filename=file.filename,
        document_type=None,
        status="pending",
        created_at= datetime.datetime.now().isoformat(),
        updated_at= datetime.datetime.now().isoformat(),
    )
    db.session.add(document)
    db.session.commit()
    return jsonify(message="Document uploaded successfully!"), 201