from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .models import User, Post, Comment, Category, Tag
from .serializers import (
    UserSerializer,
    PostSerializer,
    CommentSerializer,
    CategorySerializer,
    TagSerializer
)


# ======================================================
# User Registration / Profile
# ======================================================
class UserViewSet(ModelViewSet):
    """
    API endpoint for managing user accounts.
    Allows open registration and viewing user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handle user registration.
        Validates serializer data, hashes the password,
        and creates a new user.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])  # Hash the password for secure storage
            user.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ======================================================
# Login API (username & password)
# ======================================================
class LoginViewSet(GenericViewSet):
    """API endpoint for user login.
    Authenticates using username and password
    and returns an authentication token.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # Login via POST
    def create(self, request):
        """
        Authenticate the user and return auth token
        """
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            # Generate or retrieve authentication token
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "Login successful",
                    "token": token.key
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )


# ======================================================
# Post API - CRUD for Blog Posts
# ======================================================
class PostViewSet(ModelViewSet):
    """
    API endpoint for managing blog posts.
    - Authors can create, update, and delete posts.
    - Readers can only view published posts.
    """
    queryset = Post.objects.all().order_by("-publication_date")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "content", "author__username", "categories__name"]
    filterset_fields = ["tags", "publication_date"]
    
    # list
    def list(self, request):
        """
        List posts for the user.
        - Readers see only published posts.
        - Authors see only their own posts.
        """
        posts = Post.objects.filter(status="published")

        # authors can see their own drafts
        if request.user.is_authenticated and request.user.role == "author":
            posts = Post.objects.filter(author=request.user)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    # Create
    def create(self, request, *args, **kwargs):
        """
        Allow authors to create new posts.
        Readers are blocked from creating posts.
        """
        if request.user.role != "author":
            return Response({"error": "Only authors can create posts"}, status=403)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    #Retrieve
    def retrieve(self, request, pk=None):
        """
        Retrieve a single post by its ID.
        """
        post = Post.objects.get(pk=pk)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    #Update
    def update(self, request, pk=None):
        """
        Update a post.
        Only the original author is allowed to edit.
        """
        post = Post.objects.get(pk=pk)

        if request.user != post.author:
            return Response({"error": "You can edit only your own posts"}, status=403)

        serializer = self.get_serializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    
    # Destroy
    def destroy(self, request, pk=None):
        """
        Delete a post.
        Only the author is allowed to delete their post.
        """
        post = Post.objects.get(pk=pk)

        if request.user != post.author:
            return Response({"error": "You can delete only your own posts"}, status=403)

        post.delete()
        return Response({"message": "Post deleted successfully"})


# ======================================================
# Comment API - Threaded Comments
# Readers can comment
# ======================================================
class CommentViewSet(GenericViewSet):
    """
    API endpoint for managing comments.
    Users can create, edit, delete, and view their own comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    # LIST comments for logged-in user
    def list(self, request):
        """
        List comments authored by the logged-in user.
        """
        comments = Comment.objects.filter(author=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    # CREATE comment
    def create(self, request):
        """
        Create a new comment under a post.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    # GET comment detail
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific comment by ID.
        """
        comment = Comment.objects.get(pk=pk)
        serializer = self.get_serializer(comment)
        return Response(serializer.data)

    # UPDATE
    def update(self, request, pk=None):
        """
        Edit an existing comment.
        Only the original author is allowed to update it.
        """
        comment = Comment.objects.get(pk=pk)

        if comment.author != request.user:
            return Response({"error": "You can update only your own comments"}, status=403)

        serializer = self.get_serializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE
    def destroy(self, request, pk=None):
        """
        Delete a comment.
        Only the author is allowed to delete their comments.
        """
        comment = Comment.objects.get(pk=pk)

        if comment.author != request.user:
            return Response({"error": "You can delete only your own comments"}, status=403)

        comment.delete()
        return Response({"message": "Comment deleted"})


# ======================================================
# Category API
# ======================================================
class CategoryViewSet(ModelViewSet):
    """
    API endpoint for listing and managing categories.
    Open access because categories do not contain sensitive data.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# ======================================================
# Tag API
# ======================================================
class TagViewSet(ModelViewSet):
    """
    API endpoint for listing and managing tags.
    Open access for viewing and creating tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]