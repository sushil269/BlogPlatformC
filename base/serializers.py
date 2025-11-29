from rest_framework import serializers
from .models import User, Category, Tag, Post, Comment


# ======================================================
# User Serializer
# ======================================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# ======================================================
# Category Serializer
# ======================================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False}
        }


# ======================================================
# Tag Serializer
# ======================================================
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


# ======================================================
# Post Serializer
# ======================================================
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ['author', 'publication_date']


# ======================================================
# Comment Serializer (Threaded)
# ======================================================
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ['id','posts','parent_coment','author', 'created_at']