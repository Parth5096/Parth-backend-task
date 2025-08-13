from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models import Task
from ..schemas import TaskCreateSchema, TaskUpdateSchema, TaskOutSchema


tasks_bp = Blueprint("tasks", __name__)
create_schema = TaskCreateSchema()
update_schema = TaskUpdateSchema()
out_schema = TaskOutSchema()

def current_user_id() -> int | None:
    ident = get_jwt_identity() 
    return int(ident) if ident is not None else None


def is_admin() -> bool:
    try:
        claims = get_jwt() 
    except Exception:
        return False
    return claims.get("role") == "admin"

@tasks_bp.get("")
@jwt_required(optional=True)
def list_tasks():
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 10)), 100)
    completed_param = request.args.get("completed")

    uid = current_user_id()
    if uid is None:
        return {"items": [], "page": page, "per_page": per_page, "total": 0}

    query = Task.query
    if not is_admin():
        query = query.filter(Task.user_id == uid)
    if completed_param is not None:
        v = completed_param.lower()
        if v in ("true", "1"):
            query = query.filter(Task.completed.is_(True))
        elif v in ("false", "0"):
            query = query.filter(Task.completed.is_(False))

    page_obj = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return {
        "items": [out_schema.dump(t) for t in page_obj.items],
        "page": page_obj.page,
        "per_page": page_obj.per_page,
        "total": page_obj.total,
    }


@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id: int):
    uid = current_user_id()
    task = Task.query.get_or_404(task_id)

    if not is_admin() and task.user_id != uid:
        return {"message": "Not authorized"}, 403

    return out_schema.dump(task)


@tasks_bp.post("")
@jwt_required()
def create_task():
    uid = current_user_id()
    data = request.get_json() or {}
    errors = create_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    task = Task(**data, user_id=uid)
    db.session.add(task)
    db.session.commit()
    return out_schema.dump(task), 201


@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
    uid = current_user_id()
    task = Task.query.get_or_404(task_id)

    if not is_admin() and task.user_id != uid:
        return {"message": "Not authorized"}, 403

    data = request.get_json() or {}
    errors = update_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    for k, v in data.items():
        setattr(task, k, v)
    db.session.commit()
    return out_schema.dump(task)


@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
    uid = current_user_id()
    task = Task.query.get_or_404(task_id)

    if not is_admin() and task.user_id != uid:
        return {"message": "Not authorized"}, 403

    db.session.delete(task)
    db.session.commit()
    return "", 204