import graphene, datetime
from graphene_django import DjangoObjectType
from identity.validator import validate_user_is_authenticated

from node.models import Node, Heartbeat

class NodeType(DjangoObjectType):
    class Meta:
        model = Node

class Query(graphene.ObjectType):
    nodes = graphene.List(NodeType)

    def resolve_nodes(self, info):
        validate_user_is_authenticated(info.context.user)
        
        return Node.objects.all()

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
