import graphene, datetime
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from node.models import Node, Network, Heartbeat

class NodeType(DjangoObjectType):
    class Meta:
        model = Node

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

class HeartbeatMutation(graphene.Mutation):
    message = graphene.String()
    node = graphene.Field(NodeType)

    class Arguments:
        id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, id):
        auth_header = info.context.META.get('HTTP_KEY')

        if not auth_header:
            return HeartbeatMutation(message="ERROR: No Auth key provided.")

        try:
            Heartbeat.objects.get(key=auth_header)
        except:
            return HeartbeatMutation(message="ERROR: BAD KEY")

        try:
            node = Node.objects.get(id=id)
        except:
            return HeartbeatMutation(message="ERROR: Node not found with provided ID")

        node.heartbeat = datetime.datetime.now()
        node.save()

        return HeartbeatMutation(message="Heartbeat Successful", node=node)


class Mutation(graphene.ObjectType):
    heartbeat = HeartbeatMutation.Field()
