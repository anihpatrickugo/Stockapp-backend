from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
import graphql_social_auth
import graphql_jwt
from graphene_file_upload.scalars import Upload

from .models import ActivationCode


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


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
            send_mail(
              'Activate Your Account',
               'Here is the activation code: %s' % code.code,
              'from@example.com',
              [user.email]
            )

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
        profile_photo = Upload(required=False)
        wallet_address = graphene.String(required=False) 

    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        request_user = info.context.user
        user_queryset = User.objects.filter(id=request_user.id, email=request_user.email)
        user_queryset.update(**kwargs)
        user = user_queryset.first()
        
        return UserUpdateMutation(user=user)
     
    



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



