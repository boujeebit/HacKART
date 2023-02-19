import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from identity.validator import validate_user_is_authenticated

class Identity(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name')

class Query(object):
    identity = graphene.Field(Identity)

    def resolve_identity(self, info):
        validate_user_is_authenticated(info.context.user)

        return info.context.user