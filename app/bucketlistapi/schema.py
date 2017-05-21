from marshmallow import Schema, fields,validate




class UserRegistrationSchema(Schema):

    """Schema class to validate user during registration"""
    first_name = fields.String(required = True, load_only=True, validate=[validate.Length(min=3, max=12)],error_messages = {'required':'First name required'})
    last_name = fields.String(required = True, load_only=True, validate=[validate.Length(min=3, max=12)],error_messages ={'required': 'Last name required'})
    email = fields.Email(required = True, load_only=True, validate=[validate.Length(min=20)],error_messages = {'required': 'Email required'})
    password = fields.String(required = True, load_only=True, validate=[validate.Length(min=6)],error_messages = {'required': 'Password required'})
    verify_password = fields.String(required = True, load_only=True, validate=[validate.Length(min=6)],error_messages = {'required': 'Password required'})


class UserLoginSchema(Schema):
    """Schema class to validate user during login"""
    email = fields.String(required = True, load_only=True, validate=[validate.Length(max=12)],error_messages = {'required': 'Email required'})
    password = fields.String(required = True, load_only=True, validate=[validate.Length(min=6)],error_messages = {'required':'Password required'})

class BucketListItemSchema(Schema):
    """Schema class for adding bucketlist item"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,error_messages={'required': 'Provide bucketlist item name'})
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    done = fields.Boolean()

class BucketListSchema(Schema):
    """Schema class to validate bucketlist"""
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,error_messages={'required': 'Provide bucketlist name'})
    items = fields.Nested(BucketListItemSchema, dump_only=True, many=True)
    created_by = fields.Integer(attribute='user.user_id', dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
