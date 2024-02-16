import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Stock

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
    

class StocksQuery(graphene.ObjectType):
    all_stocks =  graphene.List(StockType)

    
    def resolve_all_stocks(root, info):
        """
        This returns the list of stocks
        """
        
        data = Stock.objects.all()
        
        return reversed(list(data))
    



class PortfolioQuery(StocksQuery, graphene.ObjectType):
    pass

class PortfolioMutations(graphene.ObjectType):
    pass

    # new_deposit = DepositMutation.Field()
    # new_withdrawal = WithdrawalMutation.Field()
    



