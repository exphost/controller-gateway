from graphene import ObjectType, Schema, Field, List
import gateway.schema_user as schema_user


class Query(ObjectType):
    user = Field(schema_user.User)
    users = List(schema_user.User)

    resolve_user = schema_user.resolve_user
    resolve_users = schema_user.resolve_users


class Mutations(ObjectType):
    user_register = schema_user.RegisterUser.Field()


schema = Schema(query=Query, mutation=Mutations)
