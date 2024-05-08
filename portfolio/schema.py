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

    def resolve_prev_close(self, info):
        return str(self.prev_close)

    def resolve_volume(self, info):
        return str(self.volume)

    def resolve_market_cap(self, info):
        return str(self.market_cap)
    
class PositionType(DjangoObjectType):
    class Meta:
        model = Position
        fields = "__all__"


class StocksQuery(graphene.ObjectType):
    all_stocks =  graphene.List(StockType)

    
    def resolve_all_stocks(root, info):
        """
        This returns the list of stocks
        """
        
        data = Stock.objects.all()
        
        return reversed(list(data))
    
class PositionQuery(graphene.ObjectType):
    open_positions =  graphene.List(PositionType)

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
        volume   =   graphene.Decimal(required=True)
        direction   =   graphene.String(required=True)  #should be long or short
        ticker   =   graphene.String(required=True)  #should be name of stock
        price   =   graphene.Decimal(required=True)


    # The class attributes define the response of the mutation
    position = graphene.Field(PositionType)

    @classmethod
    @login_required
    def mutate(cls, root, info, price, volume, direction, ticker):

        user = info.context.user

        if user.balance >= price: 

            try:
                stock = Stock.objects.get(ticker=ticker)
                position = Position.objects.create(user=user, price=price, volume=volume, direction=direction, stock=stock)
                position.save()



            except Exception as e:
                raise e
        else:
            raise GraphQLError("Insufficient balance")

        # Notice we return an instance of this mutation
        return PositionMutation(position=position)




class PortfolioQuery(StocksQuery, PositionQuery, graphene.ObjectType):
    pass

class PortfolioMutations(graphene.ObjectType):
    pass

    new_position = PositionMutation.Field()
    # new_withdrawal = WithdrawalMutation.Field()
    



