import requests
from graphene import ObjectType, String, Field, Mutation
from .schema_app import App
from flask import g, current_app


class AppNginx(ObjectType):
    class Meta:
        interfaces = (App,)


def resolve_nginx(root, info, org):
    headers = {}
    if g.get('user', None):
        headers['X-User'] = g.user
    if g.get('user_full', None):
        headers['X-User-Full'] = g.user_full
    response = requests.get(
        current_app.config['appsservice_endpoint']+"/nginx/?org="+org,
        headers=headers,
    )
    if response.status_code == 200:
        return [AppNginx(x['name'], org) for x in response.json()['nginx']]


class CreateAppNginx(Mutation):
    class Arguments:
        name = String(required=True)
        org = String(required=True)

    error = String()
    nginx = Field(lambda: AppNginx)

    def mutate(root, info, name, org):
        headers = {}
        if g.get('user', None):
            headers['X-User'] = g.user
        if g.get('user_full', None):
            headers['X-User-Full'] = g.user_full
        print("Creating nginx app:",
              name,
              org)

        response = requests.post(
            current_app.config['appsservice_endpoint']+"/nginx/",
            json={
                "name": name,
                "org": org,
            },
            headers=headers,
        )
        if response.status_code == 409:
            return {'error': "Application already exists: " +
                    str(response.content)}
        if response.status_code == 400:
            return {'error': "Bad request. TODO better messaging: " +
                    str(response.content)}
        if response.status_code == 401:
            return {'error': "Unauthorized: " +
                    str(response.content)}

        nginx = AppNginx(name, org)
        # j = response.json()
        # nginx = AppNginx(name=j['name'], org=j['org']) #TODO #257
        return CreateAppNginx(nginx=nginx)
