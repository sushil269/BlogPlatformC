"""
URL configuration for blog_platform project.
"""

from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

# Frontend Views
from base.views import (
    home,
    post_detail,
    dashboard,
    post_create,
    post_edit,
    post_delete,
    login_view,
    register_view,
    logout_view,
    profile_edit_view, 
    comment_edit_view,   
    comment_delete_view     
)


# ----------------------------
# URL PATTERNS
# ----------------------------

urlpatterns = [

    # ----------------------------
    #  ADMIN
    # ----------------------------
    path('admin/', admin.site.urls),

    # ----------------------------
    # INCLIUDE api_urls
    # ----------------------------
    path('api/', include("base.api_urls")),

    # ----------------------------
    # FRONTEND
    # ----------------------------
    path('', home, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('dashboard/', dashboard, name='dashboard'),
    path('post/create/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    
    # ----------------------------
    #  AUTHENTICATION
    # ----------------------------
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # ----------------------------
    #  NEW PROFILE EDIT PAGE
    # ----------------------------
    path('profile/edit/', profile_edit_view, name='profile_edit'),

    # ----------------------------
    # COMMENT EDIT & DELETE
    # ----------------------------
    path('comment/<int:pk>/edit/', comment_edit_view, name='comment_edit'),
    path('comment/<int:pk>/delete/', comment_delete_view, name='comment_delete'),

]


# ----------------------------
# STATIC MEDIA FOR PROFILE
# ----------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
