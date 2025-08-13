from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(load_default="user", validate=validate.OneOf(["user", "admin"]))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TaskCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(load_default="")
    completed = fields.Boolean(load_default=False)


class TaskUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String()
    completed = fields.Boolean()


class TaskOutSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    completed = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()