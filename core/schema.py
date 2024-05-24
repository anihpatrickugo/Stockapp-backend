import graphene
from users.schema import AuthMutations, AuthQuery
from transactions.schema import TransactionsMutations, TransactionsQuery
from portfolio.schema import PortfolioQuery, PortfolioMutations

class Query(AuthQuery, TransactionsQuery, PortfolioQuery, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class Mutation(AuthMutations, TransactionsMutations, PortfolioMutations, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation)