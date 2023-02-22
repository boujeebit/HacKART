import graphene

import identity.schema
import node.schema
import team.schema
import game.schema

class Query(identity.schema.Query, node.schema.Query, team.schema.Query, game.schema.Query, graphene.ObjectType):
    pass

class Mutation(identity.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)