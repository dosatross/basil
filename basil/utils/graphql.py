import graphene
from graphene import Int, Field, List

class Connection(graphene.Connection):
    class Meta:
      abstract = True

    total_count = Int()

    @staticmethod
    def resolve_total_count(root, info, **kwargs):
      return root.length

    # @classmethod
    # def __init_subclass_with_meta__(cls, node=None, name=None, **options):
    #   super(Connection, cls).__init_subclass_with_meta__(node=node, name=name, **options)
    #   cls._meta.fields["all"] = DjangoListField(node)

    