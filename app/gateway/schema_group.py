import requests
from graphene import ObjectType, String, Field, Mutation, List
from flask import g, current_app


def resolve_group(root, info):
    return Group()


def resolve_groups(root, info):
    return [Group(cn="g2")]


class Group(ObjectType):
    class Meta:
        description = 'a group'
    name = String()
    owner = String()
    members = List(String)


class RegisterGroup(Mutation):
    class Arguments:
        cn = String(required=True)
        members = List(String, required=False)
    group = Field(Group)
    error = String()

    def mutate(root, info, cn, members):
        headers = {}
        if g.get('user', None):
            headers['X-User'] = g.user
        print("Creating group:",
              cn,
              members)
        response = requests.post(
            current_app.config['usersservice_endpoint']+"/groups/",
            json={
                "name": cn,
                "members": members,
            },
            headers=headers,
        )
        if response.status_code == 409:
            return {'error': "Group already exists: " +
                    str(response.content)}
        if response.status_code == 400:
            return {'error': "Bad request. TODO better messaging: " +
                    str(response.content)}

        j = response.json()
        group = RegisterGroup(Group(**j))
        return group
