import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from .models import Blog
class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        interfaces =(relay.Node,)
        fields = (
            'id',
            'author',
            'title',
            'body',
            'likes',
            'dislikes',
            'date_created',
        )
class BlogConnection(relay.Connection):
    class Meta:
        node = BlogType

class Query(graphene.ObjectType):
    blogs = graphene.List(BlogType)
    # blogsPag = graphene.DjangoPaginationConnectionField(BlogType)
    blogById = graphene.Field(BlogType, blog_id = graphene.Int())
    blogsCount = graphene.Int()
    blogsPag = relay.ConnectionField(BlogConnection)


    
    def resolve_blogsPag(root, info, **kwargs):
        return Blog.objects.all()

    def resolve_blogs(root, info, **kwargs):
        return Blog.objects.all()
 
    def resolve_blogById(self, info, blog_id):
        return Blog.objects.get(pk=blog_id)

    def resolve_blogsCount(self, info, **kwargs):
        return Blog.objects.count()

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