from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True
