import graphene, datetime
from datetime import timedelta
from django.utils import timezone
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from node.models import Node, Network
from team.models import Team

import identity.aws as aws

class NodeType(DjangoObjectType):
    class Meta:
        model = Node

    zombie = graphene.Boolean()

    def resolve_zombie(self, info):
        expected = self.heartbeat + timedelta(seconds=(self.internval*5))
        if timezone.now() > expected:
            return True
        else:
            return False
        

class NetworkType(DjangoObjectType):
    class Meta:
        model = Network

class Query(graphene.ObjectType):
    node = graphene.Field(NodeType, id=graphene.String(required=True))
    nodes = graphene.List(NodeType)
    node_count = graphene.Int()
    sync = graphene.Boolean(id=graphene.String(required=True), action=graphene.String(required=True), enforce=graphene.Boolean(), a=graphene.Boolean(), b=graphene.Boolean(), c=graphene.Boolean())

    def resolve_node(self, info, id):
        validate_user_is_authenticated(info.context.user)

        return Node.objects.get(id=id)

    def resolve_nodes(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Node.objects.all()

    def resolve_node_count(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Node.objects.all().count()
    
    def resolve_sync(self, info, id, action, enforce=False, a=None, b=None, c=None):
        # action: ['reset' (resets the board to state to all false), 'team' (sync board to team state), 'custom' (pass in ['a','b','c'] to sync state)]
        # enforce: Bool. If try, pop the balloons that go from false to true. Only avaliable when action is custom
        validate_user_is_authenticated(info.context.user)
        try:
            node = Node.objects.get(id=id)
        except:
            raise Exception("Node with ID does not exist.")
        
        if action not in ['reset', 'team', 'custom']:
            raise Exception("Sync action not valid.")

        sync_state = {'A': False, 'B': False, 'C': False}
        if action == 'reset':
            pass

        elif action == 'custom':
            if a is None or b is None or c is None:
                raise Exception("a, b, and c flags must be explicitly defined..")
            sync_state = {'A': a, 'B': b, 'C': c}

        elif action == 'team':
            if not node.team:
                raise Exception("No team to sync with.")
            if node.team.solves.all():
                for solve in node.team.solves.all():
                    sync_state[solve.challenge.balloon] = True

        print(enforce)
        if action == 'custom' and enforce:
            aws.publish(id, 'pop', sync_state)
        else:
            aws.publish(id, 'sync', sync_state)

        print(sync_state)
        return True

class NodeMutation(graphene.Mutation):
    message = graphene.String()
    node = graphene.Field(NodeType)

    class Arguments:
        type = graphene.String(required=True)
        id = graphene.String()
        name = graphene.String()
        team = graphene.String()
    
    @classmethod
    def mutate(cls, root, info, type, id=None, name=None, team=None):
        validate_user_is_authenticated(info.context.user)

        if not info.context.user.is_superuser:
            raise Exception("Insufficient permissions.")
        
        type = type.lower()
        if type in ['create', 'update', 'delete']:

            # CREATE METHOD
            if type == 'create':
                try:
                    node = Node(name=name)
                    node.save()
                    message = 'created'
                except:
                    raise Exception("Failed to create new node.")
            
            # UPDATE METHOD
            elif type == 'update':
                if not id:
                    raise Exception("Failed to provide node ID.")
                try:
                    node = Node.objects.get(id=id)
                except:
                    raise Exception("Failed to lookup node.")
                if team:
                    try:
                        team = Team.objects.get(id=team)
                        node.team = team
                    except:
                        raise Exception("Failed to lookup team.")
                if name:
                    node.name = name
                node.save()
                message = 'updated'

            # DELETE METHOD
            elif type == 'delete':
                if not id:
                    raise Exception("Failed to provide node ID.")
                try:
                    node = Node.objects.get(id=id)
                except:
                    raise Exception("Failed to lookup node.")
                node.delete()
                node = None
                message = 'deleted'
        
        # Unknown Type
        else:
            raise Exception("Unknown type of: ", type)

        return NodeMutation(message=message, node=node)

class Mutation(graphene.ObjectType):
    node = NodeMutation.Field()




# class HeartbeatMutation(graphene.Mutation):
#     message = graphene.String()
#     node = graphene.Field(NodeType)

#     class Arguments:
#         id = graphene.String(required=True)

#     @classmethod
#     def mutate(cls, root, info, id):
#         auth_header = info.context.META.get('HTTP_KEY')

#         if not auth_header:
#             return HeartbeatMutation(message="ERROR: No Auth key provided.")

#         try:
#             Heartbeat.objects.get(key=auth_header)
#         except:
#             return HeartbeatMutation(message="ERROR: BAD KEY")

#         try:
#             node = Node.objects.get(id=id)
#         except:
#             return HeartbeatMutation(message="ERROR: Node not found with provided ID")

#         node.heartbeat = datetime.datetime.now()
#         node.save()

#         return HeartbeatMutation(message="Heartbeat Successful", node=node)


# class Mutation(graphene.ObjectType):
#     heartbeat = HeartbeatMutation.Field()
