import graphene


class App(graphene.Interface):
    name = graphene.String(required=True)
    org = graphene.String(required=True)
