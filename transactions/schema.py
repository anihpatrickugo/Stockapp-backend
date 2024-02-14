from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Deposit, Withdrawal

User = get_user_model()


class DepositType(DjangoObjectType):
    class Meta:
        model = Deposit
        fields = "__all__"

class WithdrawalType(DjangoObjectType):
    class Meta:
        model = Withdrawal
        fields = "__all__"

class DepositQuery(graphene.ObjectType):
      all_deposits = graphene.List(DepositType)
      deposits = graphene.List(DepositType, verified=graphene.Boolean())

      @login_required
      def resolve_all_deposits(root, info):
          """
          This returns all deposits
          """
          user = info.context.user
          return Deposit.objects.select_related('user').filter(user=user).reverse()
      
      @login_required
      def resolve_deposits(root, info, verified):
          """
          This return list of only verified deposits or unverified deposits.
          """
          user = info.context.user
          return Deposit.objects.select_related('user').filter(user=user, verified=verified).reverse()
         

class WithdrawalQuery(graphene.ObjectType):
    all_withdrawals = graphene.List(WithdrawalType)
    withdrawals =  graphene.List(WithdrawalType, verified=graphene.Boolean())

    
    @login_required
    def resolve_all_withdrawals(root, info):
        """
        This returns all withdrawals
        """
        user = info.context.user
        print(user.id)
        return Withdrawal.objects.select_related('user').filter(user=user).reverse()
    
    @login_required
    def resolve_withdrawals(root, info, verified):
        """
        This return list of only verified withdrawals or unverified withdrawals.
        """
        user = info.context.user
        print(user.id)
        return Withdrawal.objects.select_related('user').filter(user=user, verified=verified).reverse()






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
            deposit.verified_ = False
            deposit.save()

            # try to create transaction object  here later
            

            # send the deposit email here later
            # send_mail(
            #   'Activate Your Account',
            #    'Here is the activation code: %s' % code.code,
            #   'from@example.com',
            #   [user.email]
            # )

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

        try:
            withdrawal = Withdrawal.objects.create(user=user, amount=amount)
            withdrawal.verified_ = False
            withdrawal.save()

            # try to create transaction object  here later
            

            # send the deposit email here later
            # send_mail(
            #   'Activate Your Account',
            #    'Here is the activation code: %s' % code.code,
            #   'from@example.com',
            #   [user.email]
            # )

        except Exception as e:
            raise e

        # Notice we return an instance of this mutation
        return WithdrawalMutation(withdrawal=withdrawal)

     
    
class TransactionsQuery(DepositQuery,WithdrawalQuery,graphene.ObjectType):
    pass

class TransactionsMutations(graphene.ObjectType):

    new_deposit = DepositMutation.Field()
    new_withdrawal = WithdrawalMutation.Field()
    



