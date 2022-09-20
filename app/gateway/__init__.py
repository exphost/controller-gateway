from flask import Flask, request
from flask_cors import CORS
from flask_graphql import GraphQLView
from gateway.schema import schema
import requests
import os
from gateway import auth


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel("DEBUG")

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=schema,
            graphiql=True
        )
    )

    app.config['usersservice_endpoint'] = os.environ.get('USERSSERVICE_ENDPOINT', None)  # noqa: E501
    app.config['appsservice_endpoint'] = os.environ.get('APPSSERVICE_ENDPOINT', None)  # noqa: E501
    app.config['domainsservice_endpoint'] = os.environ.get('DOMAINSSERVICE_ENDPOINT', None)  # noqa: E501
    app.config['auth_endpoint'] = os.environ.get('AUTH_ENDPOINT', None)
    app.config['emailsservice_endpoint'] = os.environ.get('EMAILSSERVICE_ENDPOINT', None)  # noqa: E501

    if not app.config['usersservice_endpoint']:
        app.logger.error("USERSSERVICE_ENDPOINT not provided")
        return False

    if not app.config['appsservice_endpoint']:
        app.logger.error("APPSSERVICE_ENDPOINT not provided")
        return False

    if not app.config['domainsservice_endpoint']:
        app.logger.error("DOMAINSSERVICE_ENDPOINT not provided")
        return False

    if not app.config['auth_endpoint']:
        app.logger.error("AUTH_ENDPOINT not provided")
        return False

    auth_endpoint = app.config['auth_endpoint']
    auth_config_endpoint = auth_endpoint+"/.well-known/openid-configuration"
    app.logger.info(f"Getting auth config from: {auth_config_endpoint}")
    app.config['auth_config'] = requests.get(auth_config_endpoint).json()
    app.logger.debug("Dex config: {config}".format(config=app.config['auth_config']))  # noqa: E501

    CORS(app)

    @app.before_request
    def defore_request_func():
        token = request.cookies.get('accessToken', None)
        if token:
            if not auth.validate_token(token):
                return "Could not validate token", 401
    return app
