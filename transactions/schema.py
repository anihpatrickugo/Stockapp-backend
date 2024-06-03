from django.contrib.auth import get_user_model
import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Deposit, Withdrawal, RecentTransaction

User = get_user_model()


class DepositType(DjangoObjectType):
    class Meta:
        model = Deposit
        fields = "__all__"

class WithdrawalType(DjangoObjectType):
    class Meta:
        model = Withdrawal
        fields = "__all__"

class RecentTransactionType(DjangoObjectType):
    class Meta:
        model = RecentTransaction
        fields = "__all__"


    def resolve_logo(self, info):
        """Resolve product image absolute path"""
        if self.logo:
            self.logo = info.context.build_absolute_uri(self.logo.url)
        return self.logo


class DepositQuery(graphene.ObjectType):
      all_deposits = graphene.List(DepositType)
      deposits = graphene.List(DepositType, verified=graphene.Boolean())

      @login_required
      def resolve_all_deposits(root, info):
          """
          This returns all deposits
          """
          user = info.context.user
          qs = Deposit.objects.select_related('user').filter(user=user)
          return reversed(list(qs))
      
      @login_required
      def resolve_deposits(root, info, verified):
          """
          This return list of only verified deposits or unverified deposits.
          """
          user = info.context.user
          qs = Deposit.objects.select_related('user').filter(user=user, verified=verified)
          return reversed(list(qs))
         

class WithdrawalQuery(graphene.ObjectType):
    all_withdrawals = graphene.List(WithdrawalType)
    withdrawals =  graphene.List(WithdrawalType, verified=graphene.Boolean())

    
    @login_required
    def resolve_all_withdrawals(root, info):
        """
        This returns all withdrawals
        """
        user = info.context.user
        qs = Withdrawal.objects.select_related('user').filter(user=user)
        return reversed(list(qs))
    
    @login_required
    def resolve_withdrawals(root, info, verified):
        """
        This return list of only verified withdrawals or unverified withdrawals.
        """
        user = info.context.user
        qs = Withdrawal.objects.select_related('user').filter(user=user, verified=verified)
        return reversed(list(qs))
    

class RecentTransactionsQuery(graphene.ObjectType):

    recent_transactions =  graphene.List(RecentTransactionType)

    @login_required
    def resolve_recent_transactions(root, info):
        """
        This returns the last ten recent transactions
        """
        user = info.context.user
        qs = RecentTransaction.objects.select_related('user').filter(user=user)
        return reversed(list(qs))






class DepositMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        amount           =   graphene.Int(required=True)
        trnx_hash        =   graphene.String(required=True)

    # The class attributes define the response of the mutation
    deposit = graphene.Field(DepositType)

    @classmethod
    @login_required
    def mutate(cls, root, info, amount, trnx_hash):

        user = info.context.user

        try:
            deposit = Deposit.objects.create(user=user, amount=amount, trnx_hash=trnx_hash)
            deposit.verified = False
            deposit.save()
        

        except Exception as e:
            raise e

        # Notice we return an instance of this mutation
        return DepositMutation(deposit=deposit)


    
class WithdrawalMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        amount   =   graphene.Int(required=True)


    # The class attributes define the response of the mutation
    withdrawal = graphene.Field(WithdrawalType)

    @classmethod
    @login_required
    def mutate(cls, root, info, amount):

        user = info.context.user

        if user.balance >= amount: 

            try:
                withdrawal = Withdrawal.objects.create(user=user, amount=amount)
                withdrawal.verified = False
                withdrawal.save()


            except Exception as e:
                raise e
        else:
            raise GraphQLError("Insufficient balance")

        # Notice we return an instance of this mutation
        return WithdrawalMutation(withdrawal=withdrawal)

     
    
class TransactionsQuery(DepositQuery, WithdrawalQuery, 
                        RecentTransactionsQuery, graphene.ObjectType):
    pass

class TransactionsMutations(graphene.ObjectType):

    new_deposit = DepositMutation.Field()
    new_withdrawal = WithdrawalMutation.Field()
    



