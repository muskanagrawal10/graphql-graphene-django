import graphene
from graphene_django import DjangoObjectType
from .models import Blog

class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = (
            'id',
            'author',
            'title',
            'body',
            'likes',
            'dislikes',
            'date_created',
        )

class Query(graphene.ObjectType):
    blogs = graphene.List(BlogType)

    def resolve_blogs(root, info, **kwargs):
        return Blog.objects.all()

schema= graphene.Schema(query = Query)
