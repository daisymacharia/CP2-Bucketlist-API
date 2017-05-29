from marshmallow import Schema, fields,validate
from flask import url_for

class UserRegistrationSchema(Schema):
    """Schema class to validate user during registration"""
    first_name = fields.String(validate=[validate.Length(min=2),
                validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                error="Invalid characters")],
                required=True,error_messages={'required': 'Enter first name'})
    last_name = fields.String(validate=[validate.Length(min=2),
                validate.Regexp(r"[a-zA-Z0-9_\- ]*$",
                                error="Invalid characters")],
                required=True,error_messages={'required': 'Enter last name'})
    email = fields.Email(validate=[validate.Length(max=50)],
                    required=True,error_messages={'required': 'Enter email'})
    password = fields.String(validate=[validate.Length(min=5)],
                    required=True,error_messages={'required': 'Enter password'})
    verify_password = fields.String(validate=[validate.Length(min=5)],
                   required=True,error_messages={'required': 'Enter password'})


class UserLoginSchema(Schema):
    """Schema class to validate user during login"""
    email = fields.Email(validate=[validate.Length(max=50)],
                    required=True,error_messages={'required': 'Enter email'})
    password = fields.String(validate=[validate.Length(min=5)],
                required=True,error_messages={'required': 'Enter password'})
class BucketListItemSchema(Schema):
    """Schema class for adding bucketlist item"""
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=[validate.Length(min=2),
             validate.Regexp(r"[a-zA-Z0-9_\- ]*$", error="Invalid characters")],
                required=True,error_messages={'required': 'Enter name'})
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    done = fields.Boolean()
    url = fields.Method('get_url')

    @staticmethod
    def get_url(obj):
        return url_for('bucketlistitem', id=obj.bucketlist_id, item_id=obj.id,
                                                      _external=True)


class BucketListSchema(Schema):
    """Schema class to validate bucketlist"""
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=[validate.Length(min=2),
             validate.Regexp(r"[a-zA-Z0-9_\- ]*$", error="Invalid characters")],
                required=True,error_messages={'required': 'Enter name'})
    items = fields.Nested(BucketListItemSchema, dump_only=True, many=True)
    created_by = fields.Integer(attribute='user.user_id', dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)

    url = fields.Method('get_url')

    @staticmethod
    def get_url(obj):
        return url_for('bucketlist', id=obj.id, _external=True)
