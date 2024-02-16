import graphene
# import graphql_jwt
from users.schema import AuthMutations
from transactions.schema import TransactionsMutations, TransactionsQuery
from portfolio.schema import PortfolioQuery, PortfolioMutations

class Query(TransactionsQuery, PortfolioQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(AuthMutations, TransactionsMutations, PortfolioMutations, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation)