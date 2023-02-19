import graphene, datetime
from graphene_django import DjangoObjectType

from team.models import Team

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class Query(graphene.ObjectType):
    teams = graphene.List(TeamType)

    def resolve_teams(self, info):
        return Team.objects.all()