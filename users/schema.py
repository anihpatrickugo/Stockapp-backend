from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphql_social_auth
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload

from .models import ActivationCode
from .mails import send_user_verify_otp, send_new_pin_mail
from .utils import generate_random_4_digit_number


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password", "is_superuser", "is_staff", "is_active", "date_joined",
                   "groups", "user_permissions", "last_login", "pin")

    # serializing the decimal field to avoid serialization error by
    # [ApolloError: Received not compatible Decimal "0"]
    def resolve_balance(self, info):
        return str(self.balance)



class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.String())

    @login_required
    def resolve_user(root, info):
        """
        This returns all current user
        """
        user = info.context.user
        user_obj = User.objects.get(id=user.id)
        return user_obj




class RegisterUserMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)


    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, email, first_name, last_name, password):

        try:
            user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_active = False
            user.save()

            # try to create activation code
            code = ActivationCode.objects.create(user=user)

            # send the ativation code to user email    
            send_user_verify_otp(user=user, code=code.code)

        except IntegrityError as e:
            raise GraphQLError("A user with this email already exists")

        except Exception as e:
            raise e



        # Notice we return an instance of this mutation
        return RegisterUserMutation(user=user)


    
class VerifyUserMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        token = graphene.String(required=True)
   

    # The class attributes define the response of the mutation
    # user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, *args, **kwargs):
        activation_code = kwargs.get("token")

        try:
            code = ActivationCode.objects.get(code=activation_code)
            user = code.user
            user.is_active = True
            user.save()
            code.delete()

        except Exception as e:
            raise e

        # Notice we return an instance of this mutation
        # return RegisterUserMutation(user=user)
        return VerifyUserMutation(success=True)



class UserUpdateMutation(graphene.Mutation):
    class Arguments:
         # The input arguments for this mutation

        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        photo = Upload(required=False)
        wallet_address = graphene.String(required=False) 

    user = graphene.Field(UserType)
    
    @login_required
    def mutate(self, info, **kwargs):
        request_user = info.context.user
        user = User.objects.get(id=request_user.id, email=request_user.email)

        # photo = kwargs.get("photo")
        # if photo:
        #     kwargs["photo"] = photo

        try:
            user.first_name = kwargs.get("first_name")
            user.last_name = kwargs.get("last_name")
            user.email = kwargs.get("email")
            user.wallet_address = kwargs.get("wallet_address")
            user.photo = kwargs.get("photo")

            user.save()
            # user = user_queryset.first()
            return UserUpdateMutation(user=user)

        except IntegrityError as e:
            raise GraphQLError("A user with this email already exists")

        except Exception as e:
            raise


class PinUpdateMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        old_pin = graphene.Int(required=True)
        new_pin = graphene.Int(required=True)

    user = graphene.Field(UserType)


    @login_required
    def mutate(self, info, **kwargs):
        request_user = info.context.user
        user = User.objects.get(id=request_user.id, email=request_user.email)
        print(user.pin)

        old_pin = kwargs.get("old_pin")
        new_pin = kwargs.get("new_pin")

        if user.pin == old_pin:
            user.pin = new_pin
            user.save()
            return PinUpdateMutation(user=user)
        else:
            raise GraphQLError("Incorrect pin")


class RequestNewPinMutation(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        """
              This do a transaction pin reset
        """
        user = info.context.user
        user_obj = User.objects.get(id=user.id)
        new_pin = generate_random_4_digit_number()
        user_obj.pin = new_pin
        user_obj.save()

        # send pin to email
        send_new_pin_mail(user=user_obj, code=new_pin)
        return RequestNewPinMutation(success=True)



class AuthQuery(UserQuery, graphene.ObjectType):
    pass

class AuthMutations(graphene.ObjectType):

    # social auth
    social_auth = graphql_social_auth.SocialAuthJWT.Field()

    # token auth
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


    # custom auth
    register_user = RegisterUserMutation.Field()
    verify_user = VerifyUserMutation.Field()
    update_user = UserUpdateMutation.Field()
    change_pin = PinUpdateMutation.Field()
    request_new_pin = RequestNewPinMutation.Field()



