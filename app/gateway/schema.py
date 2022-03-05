from graphene import ObjectType, Schema, Field
import gateway.schema_user as schema_user
import gateway.schema_group as schema_group


class Query(ObjectType):
    user = Field(schema_user.QueryUser)
    resolve_user = schema_user.resolve_user


class Mutations(ObjectType):
    user_register = schema_user.RegisterUser.Field()
    group_register = schema_group.RegisterGroup.Field()


schema = Schema(query=Query, mutation=Mutations)
