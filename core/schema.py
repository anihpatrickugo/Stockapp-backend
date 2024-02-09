import graphene
# import graphql_jwt
from users.schema import AuthMutations
from transactions.schema import TransactionsMutations

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(AuthMutations, TransactionsMutations, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation)