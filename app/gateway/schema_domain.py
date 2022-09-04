import requests
from graphene import ObjectType, String, Field, Mutation, List
from flask import g, current_app
from .helpers import prepare_common_headers


class Domain(ObjectType):
    class Meta:
        description = 'domain'
    name = String()
    org = String()


class QueryDomain(ObjectType):
    domains = List(Domain)
    error = String()


def resolve_domain(root, info, org, name=None):
    headers = prepare_common_headers(g)
    url = current_app.config['domainsservice_endpoint']+"/v1/domains?org="+org
    if name:
        url += "&name="+name
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code == 401:
        return {"error": "Unauthenticated", "domains": []}
    if response.status_code == 403:
        return {"error": "Unauthorized", "domains": []}
    response_json = response.json()
    return {'domains': [Domain(
                name=dom.get('name'),
                org=dom.get('org'),
                ) for dom in response_json]}


class RegisterDomain(Mutation):
    class Arguments:
        name = String(required=True)
        org = String(required=True)
    domain = Field(Domain)
    error = String()

    def mutate(root, info, name, org):
        print("Creating domain:",
              name,
              org)
        headers = prepare_common_headers(g)
        response = requests.post(
                current_app.config['domainsservice_endpoint']+"/v1/domains",
                json={
                    "name": name,
                    "org": org,
                    },
                headers=headers,
        )
        if response.status_code == 409:
            return {'error': "Domain already exists: " +
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
        domain = Domain(
            name=j['name'],
            org=j['org'])
        return {'domain': domain}
