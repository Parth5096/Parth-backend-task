from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models import User
from ..schemas import RegisterSchema, LoginSchema

auth_bp = Blueprint("auth", __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    errors = register_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"message": "Email already registered"}, 400

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role=data.get("role", "user"),
    )
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "email": user.email, "role": user.role}, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    errors = login_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(
    identity=str(user.id),                   
    additional_claims={"role": user.role}    
    )
    return {"access_token": access_token}