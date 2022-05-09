import requests
from graphene import ObjectType, String, Field, Mutation, List
from flask import g, current_app


def resolve_user(root, info):
    headers = {}
    if g.get('user', None):
        headers['X-User'] = g.user
    if g.get('user_full', None):
        headers['X-User-Full'] = g.user_full
    response = requests.get(
        current_app.config['usersservice_endpoint']+"/userinfo",
        headers=headers,
    )
    if response.status_code == 401:
        return {"error": "Not authorized"}
    response_json = response.json()
    return {"user": User(
        sn=response_json.get('sn'),
        gn=response_json.get('gn'),
        mail=response_json.get('mail'),
        groups=response_json.get('groups'),
        login=response_json.get('username')
        )}


class User(ObjectType):
    class Meta:
        description = 'a user'
    sn = String()
    gn = String()
    mail = String()
    login = String()
    groups = List(String)


class QueryUser(ObjectType):
    user = Field(User)
    error = String()


class RegisterUser(Mutation):
    class Arguments:
        sn = String(required=True)
        gn = String(required=True)
        mail = String(required=True)
        login = String(required=True)
        password = String(required=True)
    user = Field(User)
    error = String()

    def mutate(root, info, sn, gn, mail, login, password):
        print("Creating user:",
              sn,
              gn,
              login,
              mail)
        headers = {}
        if g.get('user', None):
            headers['X-User'] = g.user
        if g.get('user_full', None):
            headers['X-User-Full'] = g.user_full
        response = requests.post(
                current_app.config['usersservice_endpoint']+"/users",
                json={
                    "sn": sn,
                    "gn": gn,
                    "login": login,
                    "password": password,
                    "mail": mail,
                    },
                headers=headers,
        )
        if response.status_code == 409:
            return {'error': "User already exists: " +
                    str(response.content)}
        if response.status_code == 400:
            return {'error': "Bad request. TODO better messaging: " +
                    str(response.content)}

        j = response.json()
        del(j['password'])
        user = RegisterUser(User(**j))
#            sn = j['sn'],
#            gn = j['gn'],
#            login = j['login'],
#            mail = j['mail']
#        ))
        return user
