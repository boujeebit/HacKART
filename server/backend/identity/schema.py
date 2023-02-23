import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from identity.models import Platform, Heartbeat, Broker

from identity.validator import validate_user_is_authenticated
import requests

class Identity(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name')

class PlatformType(DjangoObjectType):
    class Meta:
        model = Platform
        only_fields = ('id', 'key', 'name', 'hint')

class HeartbeatType(DjangoObjectType):
    class Meta:
        model = Heartbeat
        only_fields = ('id', 'key', 'name', 'hint')

class Query(object):
    identity = graphene.Field(Identity)
    platforms = graphene.List(PlatformType)
    heartbeats = graphene.List(HeartbeatType)
    blinky = graphene.Boolean()

    def resolve_identity(self, info):
        validate_user_is_authenticated(info.context.user)

        return info.context.user
    
    def resolve_platforms(self, info):
        validate_user_is_authenticated(info.context.user)

        return Platform.objects.all()
    
    def resolve_heartbeats(self, info):
        validate_user_is_authenticated(info.context.user)

        return Heartbeat.objects.all()

    # Test blink of ESP 
    def resolve_blinky(self, info):
        validate_user_is_authenticated(info.context.user)

        try:
            broker = Broker.objects.all().first()
        except:
            return False
        publish_url = 'https://%s:%i/topics/hackart/init?qos=1' % (broker.endpoint, broker.port)
        publish_msg = "Hello from HacKART terminal"

        publish = requests.request('POST',
            publish_url,
            data=publish_msg,
            cert=['', ''])

        if publish.status_code == 200:
            return True
        else:
            return False

class LogIn(graphene.Mutation):
    id = graphene.Int()
    isAuthenticated = graphene.Int()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)

        if not user:
            raise Exception('Invalid username or password')

        login(info.context, user)

        return LogIn(id=user.id, isAuthenticated=True)
    
class LogOut(graphene.Mutation):
    status = graphene.String()

    def mutate(self, info):
        user = info.context.user
        validate_user_is_authenticated(user)
        logout(info.context) 
        return LogOut(status='Logged Out')

class Mutation(object):
    login  = LogIn.Field()
    logout = LogOut.Field()