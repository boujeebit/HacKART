import graphene, datetime
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from team.models import Team

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class Query(graphene.ObjectType):
    teams = graphene.List(TeamType)
    team_count = graphene.Int()

    def resolve_teams(self, info):
        validate_user_is_authenticated(info.context.user)

        return Team.objects.all()

    def resolve_team_count(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Team.objects.all().count()