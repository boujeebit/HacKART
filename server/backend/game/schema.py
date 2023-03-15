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

    def resolve_challenges(self, info):
        validate_user_is_authenticated(info.context.user)

        return Challenge.objects.all()
    
    def resolve_solves(self, info):
        validate_user_is_authenticated(info.context.user)

        return Solve.objects.all()


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