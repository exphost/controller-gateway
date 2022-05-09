import traceback
import jwt
from jwt import PyJWKClient
from flask import g, current_app
import json
import base64


def get_userinfo(token):
    print(f"CURRENT APP: {current_app}")
    g.user = "qweqwe"


def validate_token(token):
    try:
        jwks_uri = current_app.config['auth_config']['jwks_uri']
        current_app.logger.debug("jwks_uri: {uri}".format(uri=jwks_uri))
        jwks_client = PyJWKClient(jwks_uri)
        print(jwks_client)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="exphost-controller",
        )
        print("validate_token")
        print(data)
        print("validate_token after")
        g.user = data['name']
        g.user_full = base64.b64encode(json.dumps(data).encode()).decode()
        return True
    except (jwt.exceptions.PyJWKClientError,
            jwt.exceptions.InvalidAudienceError,
            jwt.exceptions.InvalidSignatureError) as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return False
