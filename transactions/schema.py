from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import graphene
from graphene_django import DjangoObjectType

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


class DepositMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        amount           =   graphene.Int(required=True)
        trnx_hash        =   graphene.String(required=True)


    # The class attributes define the response of the mutation
    deposit = graphene.Field(DepositType)

    @classmethod
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


# class UserUpdateMutation(graphene.Mutation):
#     class Arguments:
#          # The input arguments for this mutation

#         email = graphene.String(required=False)
#         first_name = graphene.String(required=False)
#         last_name = graphene.String(required=False)
#         profile_photo = Upload(required=False)
#         wallet_address = graphene.String(required=False) 

#     user = graphene.Field(UserType)

#     def mutate(self, info, **kwargs):
#         request_user = info.context.user
#         user_queryset = User.objects.filter(id=request_user.id, email=request_user.email)
#         user_queryset.update(**kwargs)
#         user = user_queryset.first()
        
#         return UserUpdateMutation(user=user)
     
    



class TransactionsMutations(graphene.ObjectType):

    new_deposit = DepositMutation.Field()
    new_withdrawal = WithdrawalMutation.Field()
    



