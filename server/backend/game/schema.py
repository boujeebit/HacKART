import graphene, datetime
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from game.models import Challenge, Solve

class ChallengeType(DjangoObjectType):
    class Meta:
        model = Challenge

class SolvesType(DjangoObjectType):
    class Meta:
        model = Solve

class Query(graphene.ObjectType):
    challenges = graphene.List(ChallengeType)
    solves = graphene.List(SolvesType)
    solve_count = graphene.Int()
    solve_graph = graphene.JSONString()

    def resolve_challenges(self, info):
        validate_user_is_authenticated(info.context.user)

        return Challenge.objects.all()
    
    def resolve_solves(self, info):
        validate_user_is_authenticated(info.context.user)

        return Solve.objects.all()
    
    def resolve_solve_count(self, info):
        validate_user_is_authenticated(info.context.user)

        return Solve.objects.all().count()
    
    def resolve_solve_graph(self, info):
        validate_user_is_authenticated(info.context.user)
        d = datetime.datetime.now()
        
        a = {}
        for x in range(24):
            a[(x+1+d.hour)%24] = 0

        for solve in Solve.objects.filter(time__gte=d-datetime.timedelta(days=1)):
            a[solve.time.hour] += 1

        data = {"labels": [], "datasets": [{ "label": "Solves", "backgroundColor": "#ff5555", "data": []}]}
        for key, value in a.items():
            data["labels"].append(key)
            data["datasets"][0]["data"].append(value)

        return data




class ChallengeMutation(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        action = graphene.String()
        # id = graphene.String()
        # externalid = graphene.String()
        # name = graphene.String()
        # balloon = graphene.String()
    
    @classmethod
    def mutate(self, info, action):
        # validate_user_is_authenticated(info.context.user)
        
        return ChallengeMutation(message='Challenge')

class Mutation(object):
    challenge = ChallengeMutation.Field()