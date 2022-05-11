import graphene


class Git(graphene.Interface):
    repo = graphene.String(required=True)
    branch = graphene.String(required=False)


class GitInput(graphene.InputObjectType):
    repo = graphene.String(required=True)
    branch = graphene.String(required=False)
