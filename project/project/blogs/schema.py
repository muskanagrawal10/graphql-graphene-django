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

class BlogInput(graphene.InputObjectType):
    title = graphene.String()
    author = graphene.String()
    body = graphene.String()
    likes = graphene.Int()
    dislikes = graphene.Int()
    
class CreateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInput(required=True)

    blog = graphene.Field(BlogType)
    
    @classmethod
    def mutate(cls, root, info, input):
        blog = Blog()
        blog.title = input.title
        blog.author = input.author
        blog.body = input.body
        blog.likes = input.likes
        blog.dislikes = input.dislikes
        blog.save()
        return CreateBlog(blog=blog)

class UpdateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInput(required=True)
        id = graphene.ID()

    blog = graphene.Field(BlogType)
    
    @classmethod
    def mutate(cls, root, info, input, id):
        blog = Blog.objects.get(pk=id)
        # blog.title = input.title
        blog.author = input.author
        blog.body = input.body
        # blog.likes = input.likes
        # blog.dislikes = input.dislikes
        blog.save()
        return UpdateBlog(blog=blog)

class Mutation(graphene.ObjectType):

    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)