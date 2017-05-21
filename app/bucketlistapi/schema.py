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
email = data['email']
email = User.query.filter_by(email=email).first()
if email:
    response = {'error': 'Email already in use'}
    return response, 400
        # try:
        #     first_name = data['first_name']
        #     last_name = data['last_name']
        #     email = data['email']
        #     password = data['password']
        #     verify_password = data['verify_password']
        #     new_user =User(first_name,last_name,email,password,verify_password)
        #     db.add(new_user)

        # try:
        #     #register user
        #     new_user = User(first_name,last_name,email,password)
        #     # new_user.first_name = first_name
        #     # new_user.last_name = last_name
        #     # username= first_name + last_name
        #     # new_user.email = email
        #     # new_user.password = password
        #     db.session.add(new_user)
        #     db.session.commit()
        #     return {'message': '{} added successfully'.format(username)}, 201
        # except Exception as error:
        #     db.session.rollback()
        #     return {'error': '{} try again'.format(username)}, 400
