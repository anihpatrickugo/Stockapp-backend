import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Stock, Position

# Create your views here.

class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = "__all__"

    def resolve_image(self, info):
        """Resolve product image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

    def resolve_open(self, info):
        return str(self.open)

    def resolve_direction(self, info):
        return str(self.direction)


    def resolve_prev_close(self, info):
        return str(self.prev_close)

    def resolve_price(self, info):
        return str(self.price)

    def resolve_market_cap(self, info):
        return str(self.market_cap)
    
class PositionType(DjangoObjectType):


    class Meta:
        model = Position
        fields = "__all__"

    current_percent = graphene.Int(required=False)

    def resolve_current_percent(self, info):
        return  int(self.current_percent())


class StocksQuery(graphene.ObjectType):
    all_stocks = graphene.List(StockType)

    
    def resolve_all_stocks(root, info):
        """
        This returns the list of stocks
        """
        
        data = Stock.objects.all()
        
        return reversed(list(data))
    
class PositionQuery(graphene.ObjectType):
    open_positions = graphene.List(PositionType)

    @login_required
    def resolve_open_positions(root, info):
        """
        This returns the list of positions
        """
        user = info.context.user
        
        data = Position.objects.select_related("user").filter(user=user)        
        return reversed(list(data))
    


class PositionMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        volume   =   graphene.Int(required=True)
        direction   =   graphene.String(required=True)  #should be long or short
        ticker   =   graphene.String(required=True)  #should be name of stock
        pin = graphene.Int(required=True)


    # The class attributes define the response of the mutation
    position = graphene.Field(PositionType)

    @classmethod
    @login_required
    def mutate(cls, root, info, volume, direction, ticker, pin):

        user = info.context.user
        stock = Stock.objects.get(ticker=ticker)
        price = volume * stock.price


        # first check if pin is correct
        if user.pin == pin:

            # then check if the user balance is enough for the transaction.
            if user.balance >= price:

                try:
                    position = Position.objects.create(user=user, price=price, volume=volume, direction=direction,
                                                       stock=stock)
                    position.save()
                except Exception as e:
                    raise e
            else:

                # user balance is not enough
                raise GraphQLError("Insufficient balance")

        else:
            # pin is incorrect
            raise GraphQLError("Incorrect pin")

        # Notice we return an instance of this mutation
        return PositionMutation(position=position)



class ClosePositionMutation(graphene.Mutation):

    class Arguments:
        # The input arguments for this mutation
        id = graphene.Int(required=True)

    # The class attributes define the response of the mutation
    Success = graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):

        user = info.context.user

        try:
            position = Position.objects.get(id=id)
            if position.user == user:
                user.balance += (position.price + ((position.current_percent()/ 100 )* position.price))
                user.save()
                position.delete()
                return ClosePositionMutation(Success=True)
            else:
                raise GraphQLError("You are not authorized to close this position")

        except Position.DoesNotExist:
            raise GraphQLError("Position does not exist")

        except Exception as e:
            raise e



class PortfolioQuery(StocksQuery, PositionQuery, graphene.ObjectType):
    pass

class PortfolioMutations(graphene.ObjectType):
    new_position = PositionMutation.Field()
    close_position = ClosePositionMutation.Field()

    



