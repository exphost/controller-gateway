import requests
from graphene import ObjectType, String, Field, Mutation, List
from .schema_app import App
from .schema_git import GitInput
from flask import g, current_app


class AppNginx(ObjectType):
    class Meta:
        interfaces = (App,)

    class GitRepo(ObjectType):
        repo = String(required=True)
        branch = String(required=False)

    fqdns = List(String, required=False)
    git = Field(GitRepo, required=False)


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
        return [AppNginx(name=x['name'],
                         org=org,
                         git=x.get('git', None),
                         fqdns=x.get('fqdns', None)
                         ) for x in response.json()['nginx']]


class CreateAppNginx(Mutation):
    class Arguments:
        name = String(required=True)
        org = String(required=True)
        git = GitInput(required=False)
        fqdns = List(String, required=False)

    error = String()
    nginx = Field(lambda: AppNginx)

    def mutate(root, info, name, org, git=None, fqdns=None):
        headers = {}
        if g.get('user', None):
            headers['X-User'] = g.user
        if g.get('user_full', None):
            headers['X-User-Full'] = g.user_full
        print("Creating nginx app:",
              name,
              org,
              git,
              fqdns)

        response = requests.post(
            current_app.config['appsservice_endpoint']+"/nginx/",
            json={
                "name": name,
                "org": org,
                "git": git,
                "fqdns": fqdns
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

        nginx = AppNginx(name=name,
                         org=org,
                         git=git,
                         fqdns=fqdns)
        # j = response.json()
        # nginx = AppNginx(name=j['name'], org=j['org']) #TODO #257
        return CreateAppNginx(nginx=nginx)
