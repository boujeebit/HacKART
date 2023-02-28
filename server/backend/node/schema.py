import graphene, datetime
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from node.models import Node, Network
from team.models import Team

class NodeType(DjangoObjectType):
    class Meta:
        model = Node

    balloons = graphene.JSONString()
    def resolve_balloons(self, info):
        balloons = {'b1': False, 'b2': False, 'b3': False}
        for solve in self.solves.all():
            if solve.challenge.balloon == 1:
                balloons['b1'] = True
            elif solve.challenge.balloon == 2:
                balloons['b2'] = True
            elif solve.challenge.balloon == 3:
                balloons['b3'] = True
        return balloons

class NetworkType(DjangoObjectType):
    class Meta:
        model = Network

class Query(graphene.ObjectType):
    node = graphene.Field(NodeType, id=graphene.String(required=True))
    nodes = graphene.List(NodeType)
    node_count = graphene.Int()

    def resolve_node(self, info, id):
        validate_user_is_authenticated(info.context.user)

        return Node.objects.get(id=id)

    def resolve_nodes(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Node.objects.all()

    def resolve_node_count(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Node.objects.all().count()

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
