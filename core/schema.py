from django.conf import settings
import graphene
from users.schema import AuthMutations, AuthQuery
from transactions.schema import TransactionsMutations, TransactionsQuery
from portfolio.schema import PortfolioQuery, PortfolioMutations

class Query(AuthQuery, TransactionsQuery, PortfolioQuery, graphene.ObjectType):
    # These are Queries for the Site Details
    wallet_address = graphene.String(default_value=settings.SITE_USDT_WALLET_ADDRESS)
    minimum_deposit = graphene.Int(default_value=settings.SITE_MINIMUM_DEPOSIT_AMAOUNT)
    minimum_withdrawal = graphene.Int(default_value=settings.SITE_MINIMUM_WITHDRAWAL_AMAOUNT)


class Mutation(AuthMutations, TransactionsMutations, PortfolioMutations, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query, mutation=Mutation)