import requests
from graphene import ObjectType, String, Field, Mutation, List
from flask import g, current_app
from .helpers import prepare_common_headers


class Email(ObjectType):
    class Meta:
        description = 'email'
    mail = String()
    cn = String()
    sn = String()
    aliases = List(String)
    password = String()


class QueryEmail(ObjectType):
    emails = List(Email)
    error = String()


def resolve_email(root, info, org):
    headers = prepare_common_headers(g)
    url = current_app.config['emailsservice_endpoint']+"/v1/emails/?org="+org
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code == 401:
        return {"error": "Unauthenticated", "email": []}
    if response.status_code == 403:
        return {"error": "Unauthorized", "emails": []}
    response_json = response.json()
    return {'emails': [Email(
                mail=em.get('mail'),
                cn=em.get('cn'),
                sn=em.get('sn'),
                aliases=em.get('aliases'),
                ) for em in response_json]}


class RegisterEmail(Mutation):
    class Arguments:
        org = String(required=True)
        mail = String(required=True)
        cn = String(required=True)
        sn = String(required=True)
        password = String(required=False)
        aliases = List(String, required=False)
    email = Field(Email)
    error = String()

    def mutate(root, info, org, mail, cn, sn, password=None, aliases=None):
        headers = prepare_common_headers(g)
        email_json = {
            "mail": mail,
            "cn": cn,
            "sn": sn,
            }
        if aliases:
            email_json['aliases'] = aliases
        print("Creating domain:", org, email_json)
        if password:
            email_json['password'] = password
        response = requests.post(
            current_app.config['emailsservice_endpoint']+"/v1/emails/?org="+org,  # noqa 501
            json=email_json,
            headers=headers,
        )
        if response.status_code == 409:
            return {'error': "Email already exists: " +
                    str(response.content)}
        if response.status_code == 400:
            return {'error': "Bad request. TODO better messaging: " +
                    str(response.content)}
        if response.status_code == 401:
            return {'error': "Unauthenticated:" +
                    str(response.content)}
        if response.status_code == 403:
            return {'error': "Unauthorized:" +
                    str(response.content)}

        j = response.json()
        email = Email(
            mail=j['mail'],
            cn=j['cn'],
            sn=j['sn'],
            password=j['password'],
            aliases=j['aliases'],
        )
        return {'email': email}
