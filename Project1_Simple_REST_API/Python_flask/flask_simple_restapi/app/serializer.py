from extensions.extension import ma,fields,validate,validates_schema
from app.models import Users,Todo
from app.utils import get_secret_hash

class UserSchema(ma.ModelSchema):

    first_name = fields.Str(required=True,validate=[validate.Length(min=2,max=250)])
    last_name = fields.Str(required=True,validate=[validate.Length(min=2,max=250)])
    user_name = fields.Str(required=True,validate=[validate.Length(min=2,max=250)])
    email = fields.Email(required=True)
    password = fields.Str(load_only=True,required=True,validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True)
    def hash_pass(self,data,**kwargs):
        hashed_pass =  get_secret_hash(data.get("password"))
        data.update({"password": hashed_pass})

    class Meta:
        model = Users

    todos = fields.Nested('TodoSchema', many=True)
        
class UpdateSchema(ma.Schema):

    first_name = fields.Str(validate=[validate.Length(min=2,max=250)])
    last_name = fields.Str(validate=[validate.Length(min=2,max=250)])
    user_name = fields.Str(validate=[validate.Length(min=2,max=250)])
    email = fields.Email()
    password = fields.Str(validate=[validate.Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?#&]{8,}$")])

    @validates_schema(skip_on_field_errors=True)
    def hash_pass(self,data,**kwargs):
        if data.get("password"):
            hashed_pass =  get_secret_hash(data.get("password"))
            data.update({"password": hashed_pass})



class TodoSchema(ma.ModelSchema):

    title = fields.Str(required=True,validate=[validate.Length(min=2,max=250)])
    description = fields.Str(validate=[validate.Length(min=2,max=250)])

    class Meta:
        model = Todo
        include_fk = True



class TodoUpdateSchema(ma.Schema):

    title = fields.Str(validate=[validate.Length(min=2,max=250)])
    description = fields.Str(validate=[validate.Length(min=2,max=250)])
    user_id  = fields.Int()