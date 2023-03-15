import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from identity.models import Integration, Broker

from identity.validator import validate_user_is_authenticated
import requests

class IdentityObj(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'username', 'is_superuser', 'first_name', 'last_name')

class IntegrationObj(DjangoObjectType):
    class Meta:
        model = Integration
        exclude_fields = ('key',)

class Query(object):
    identity = graphene.Field(IdentityObj)
    integrations = graphene.List(IntegrationObj)
    blinky = graphene.Boolean()

    def resolve_identity(self, info):
        validate_user_is_authenticated(info.context.user)

        return info.context.user
    
    def resolve_integrations(self, info):
        validate_user_is_authenticated(info.context.user)

        return Integration.objects.all()

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

'''
mutation($action: String!, $id: String, $type: String, $name: String ) {
	integration(action: $action, id: $id, type: $type, name: $name) {
		message
        key
  }
}
'''
class IntegrationMutation(graphene.Mutation):
    message = graphene.String()
    integration = graphene.Field(IntegrationObj)
    key = graphene.String() 

    class Arguments:
        action = graphene.String(required=True)
        id = graphene.String()
        type = graphene.String()
        name = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, action, id=None, type=None, name=None):
        validate_user_is_authenticated(info.context.user)

        if not info.context.user.is_superuser:
            raise Exception("Insufficient permissions.")
        
        action = action.lower()
        if action in ['create', 'delete']:

            # CREATE METHOD
            if action == 'create':
                if name and type:
                    if type == 'PF' or type == 'HB':
                        integration = Integration(name=name, type=type, created_by=info.context.user)
                        integration.hint = '*'*32 + str(integration.key)[-4:]
                        integration.save()

                        message = "success"
                        key = integration.key
                    else:
                        raise Exception("Unknown integration type.")
                else:
                    raise Exception("Type and name required to create integration.")

                return IntegrationMutation(message=message, integration=integration, key=key)

            # DELETE METHOD
            elif action == 'delete':
                if not id:
                    raise Exception("ID required.")
                
                try:
                    integration = Integration.objects.get(id=id)
                except:
                    raise Exception("Integration ID not found.")
                
                try:
                    integration.delete()
                except:
                    raise Exception("Could not delete integration")
                
                return IntegrationMutation(message='success', integration=None, key=None)
        # Unknown Type
        else:
            raise Exception("Unknown action of: ", action)

class Mutation(object):
    login  = LogIn.Field()
    logout = LogOut.Field()
    integration = IntegrationMutation.Field()