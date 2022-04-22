from graphene import ObjectType, Schema, Field
import gateway.schema_user as schema_user
import gateway.schema_group as schema_group
import gateway.schema_nginx as schema_nginx


class Query(ObjectType):
    user = Field(schema_user.QueryUser)
    resolve_user = schema_user.resolve_user


class Mutations(ObjectType):
    user_register = schema_user.RegisterUser.Field()
    group_register = schema_group.RegisterGroup.Field()
    app_nginx_create = schema_nginx.CreateAppNginx.Field()


schema = Schema(query=Query, mutation=Mutations)
