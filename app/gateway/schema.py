from graphene import ObjectType, Schema, Field, List, String
import gateway.schema_user as schema_user
import gateway.schema_group as schema_group
import gateway.schema_nginx as schema_nginx
import gateway.schema_domain as schema_domain
import gateway.schema_email as schema_email


class Query(ObjectType):
    user = Field(schema_user.QueryUser)
    resolve_user = schema_user.resolve_user

    nginx = List(schema_nginx.AppNginx, org=String())
    resolve_nginx = schema_nginx.resolve_nginx

    domain = Field(schema_domain.QueryDomain, org=String())
    resolve_domain = schema_domain.resolve_domain

    email = Field(schema_email.QueryEmail, org=String())
    resolve_email = schema_email.resolve_email


class Mutations(ObjectType):
    user_register = schema_user.RegisterUser.Field()
    group_register = schema_group.RegisterGroup.Field()
    app_nginx_create = schema_nginx.CreateAppNginx.Field()
    domain_register = schema_domain.RegisterDomain.Field()
    email_create = schema_email.RegisterEmail.Field()


schema = Schema(query=Query, mutation=Mutations)
