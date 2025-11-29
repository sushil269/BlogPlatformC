from django.urls import path
from .api_views import (
    UserViewSet,
    LoginViewSet,
    PostViewSet,
    CommentViewSet,
    CategoryViewSet,
    TagViewSet
)

# ======USER AUTH ======
register_view = UserViewSet.as_view({
    "post": "create",
})

login_view = LoginViewSet.as_view({
    "post": "create",
})

# ====== POSTS ======
post_list = PostViewSet.as_view({
    "get": "list",
    "post": "create",
})
post_detail = PostViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "update",
    "delete": "destroy",
})

# ====== COMMENTS ======
comment_list = CommentViewSet.as_view({
    "get": "list",
    "post": "create",
})
comment_detail = CommentViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "update",
    "delete": "destroy",
})

# ====== CATEGORIES ======
category_list = CategoryViewSet.as_view({
    "get": "list",
    "post": "create",
})
category_detail = CategoryViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "update",
    "delete": "destroy",
})

# ====== TAGS ======
tag_list = TagViewSet.as_view({
    "get": "list",
    "post": "create",
})
tag_detail = TagViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "update",
    "delete": "destroy",
})


urlpatterns = [

    # ====== AUTH ======
    path("register/", register_view, name="api-register"),
    path("login/", login_view, name="api-login"),

    # ====== POSTS ======
    path("posts/", post_list, name="api-posts-list"),
    path("posts/<int:pk>/", post_detail, name="api-posts-detail"),

    # ====== COMMENTS ======
    path("comments/", comment_list, name="api-comments-list"),
    path("comments/<int:pk>/", comment_detail, name="api-comments-detail"),

    # ====== CATEGORIES ======
    path("categories/", category_list, name="api-categories-list"),
    path("categories/<int:pk>/", category_detail, name="api-categories-detail"),

    # ====== TAGS ======
    path("tags/", tag_list, name="api-tags-list"),
    path("tags/<int:pk>/", tag_detail, name="api-tags-detail"),
]