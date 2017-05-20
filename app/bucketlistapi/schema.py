from marshmallow import Schema, fields,validate


class UserResigrationSchema(Schema):


    first_name = fields.String(required = True, load_only=True, validate=[validate.Length(max=12)],error_message = 'First name required')

    last_name = fields.String(required = True, load_only=True, validate=[validate.Length(max=12)],error_message ='Last name required')

    email = fields.String(required = True, load_only=True, validate=[validate.Length(max=12)],error_message = 'Email required')

    password = fields.String(required = True, load_only=True, validate=[validate.Length(min=6)],error_message = 'Password required')

    verify_password = fields.String(required = True, load_only=True, validate=[validate.Length(min=6)],error_message= 'Password required')
