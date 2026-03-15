import datetime
import os
import threading
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
    document_id = document.id
    file_content = file.read()
    # Start a new thread to parse the document asynchronously
    thread = threading.Thread(target=parse_document, args=(document_id, file_content))
    thread.daemon = True
    thread.start()
    return jsonify(message="Document uploaded successfully!"), 201

def parse_document(document_id, file_content: bytes):
    with app.app_context(): #mandatory to access the database outside of request context
        document = db.session.get(File, document_id)
        if not document:
            print(f"Document with ID {document_id} not found.")
            return
        # Simulate parsing logic
        print(f"Parsing document {document.filename} (ID: {document.id})...")
        # Update document status to "success" after parsing
        document.status = "success"
        document.updated_at = datetime.datetime.now().isoformat()
        db.session.commit()
        print(f"Document {document.filename} parsed successfully!")