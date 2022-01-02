from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from gateway.schema import schema


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

    CORS(app)
    return app
