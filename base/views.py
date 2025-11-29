from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import User, Post, Comment, Category, Tag
# Create your views here.


# ======================================================
# REGISTER USER (Author or Reader)
# ======================================================
def register_view(request):
    """
    Handle user registration.
    Allows creating a new account as an Author or Reader.
    Validates required fields, email format, and uniqueness.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        role = request.POST.get("role") or "reader"
        image = request.FILES.get("profile_picture")

        error_message = ""

        # Required field checks
        if not username:
            error_message += "Username required. "
        if not password:
            error_message += "Password required. "
        if not email:
            error_message += "Email required. "

        # Ensure  username is unique
        if username and User.objects.filter(username=username).exists():
            error_message += "Username already exists. "

        # Email format
        if email and '@' not in email:
            error_message += "Invalid email format. "

        # Ensure email is unique
        if email and User.objects.filter(email=email).exists():
            error_message += "Email already exists. "

        # Create user if no validation errors
        if not error_message:
            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role,
                profile_picture=image
            )
            return render(request, "register.html", {"success": "Registered successfully!"})

        # Show validation errors
        return render(request, "register.html", {"error": error_message})

    return render(request, "register.html")




# ======================================================
# LOGIN VIEW
# ======================================================
def login_view(request):
    """"
    Authenticate a user using username and password.
    Redirects to home page upon success.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        error_message = ""
        
        # Required fiels checks
        if not username: error_message += "Username required. "
        if not password: error_message += "Password required. "
        
        # Try authenticating the user
        user = authenticate(username=username, password=password)
        
        # Invalid credentials
        if user is None and not error_message:
            error_message = "Invalid credentials!"
        
        #Successful login
        if not error_message:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {"error": error_message})

    return render(request, "login.html")



# ======================================================
# LOGOUT VIEW
# ======================================================
@login_required(login_url='login')
def logout_view(request):
    """
    Log out the currently authenticated user.
    Redirects to login page.
    """
    logout(request)
    return redirect('login')



# ======================================================
# HOME VIEW — LIST OF PUBLISHED POSTS WITH SEARCH & PAGINATION
# ======================================================
@login_required(login_url="login")
def home(request):
    """
    Display all published blog posts.
    Supports search by title, content, or author.
    Includes pagination (5 posts per page).
    """
    posts = Post.objects.filter(status="published").order_by("-publication_date")
    
    # Search filter
    search = request.GET.get("search")
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(author__username__icontains=search)
        )
    
    # Paginate results
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {
        "posts": posts,
        "page_obj": page_obj,
        "search": search,
    })



# ======================================================
# POST DETAIL VIEW + COMMENTS
# ======================================================

@login_required(login_url='login')
def post_detail(request, pk):
    """
    Show a single post with its comments.
    Allows adding new top-level comments and replies .
    Includes comment pagination.
    """
    post = get_object_or_404(Post, id=pk)

    # Get comments (only top-level)
    comments_list = Comment.objects.filter(
        post=post,
        parent_comment=None
    ).order_by("-created_date")

    # Pagination for comments (5 per page)
    paginator = Paginator(comments_list, 5)
    page_number = request.GET.get("cpage")
    comments = paginator.get_page(page_number)

    # Add new comment and reply
    if request.method == "POST":
        content = request.POST.get("comment")
        parent_id = request.POST.get("parent_id")

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent_comment_id=parent_id
            )
            return redirect("post_detail", pk=pk)

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,   # Paginated comments
    })




# ======================================================
# DASHBOARD — AUTHOR POSTS ONLY
# ======================================================
@login_required(login_url="login")
def dashboard(request):
    """
    Display all posts created by the logged-in author.
    Readers cannot access this page.
    """
    if request.user.role != "author":
        return redirect("home")

    posts = Post.objects.filter(author=request.user).order_by("-publication_date")
    
    #paginate author post 
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "dashboard.html", {
        "posts": posts,
        "page_obj": page_obj,
    })



# ======================================================
# CREATE POST (AUTHOR ONLY)
# ======================================================
@login_required(login_url="login")
def post_create(request):
    """
    Allow authors to create a new blog post.
    Supports adding categories and tags there .
    """
    if request.user.role != "author":
        return redirect("home")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        status_value = request.POST.get("status") or "draft"
        
        # Create post
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            status=status_value,
        )

        # Optional: Set Categories and Tags
        categories = request.POST.getlist("categories")
        tags = request.POST.getlist("tags")

        if categories:
            post.categories.set(categories)
        if tags:
            post.tags.set(tags)

        return redirect("dashboard")
    
    # Data for form
    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, "post_create.html", {
        "categories": categories,
        "tags": tags,
    })



# ======================================================
# EDIT POST
# ======================================================
@login_required(login_url="login")
def post_edit(request, pk):
    """
    Allow an author to edit their own post.
    Supports updating title, content, status, categories, and tags.
    """
    post = get_object_or_404(Post, id=pk)

    # Ensure only the author can edit this post
    if request.user != post.author:
        return redirect("dashboard")

    # Handle from submission
    if request.method == "POST":
        # Update basic post fields
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.status = request.POST.get("status") or "draft"
        
        # Update many-to-many relationships
        post.categories.set(request.POST.getlist("categories"))
        post.tags.set(request.POST.getlist("tags"))
        
        # Save updated post back to the database
        post.save()
        return redirect("dashboard")

    # Get categories and tags for the edit forms
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # Render the edit page with the existing post data
    return render(request, "post_edit.html", {
        "post": post,
        "categories": categories,
        "tags": tags,
    })


# ======================================================
# DELETE POST
# ======================================================
@login_required(login_url='login')
def post_delete(request, pk):
    """
    Delete a post belonging to the logged-in author.
    Prevents unauthorized deletions attempts .
    """
    post = get_object_or_404(Post, id=pk)
   
   # Ensure only the author can delete the post
    if request.user != post.author:
        return HttpResponseForbidden("You cannot delete this post.")

    post.delete()
    return redirect("dashboard")





# ======================================================
# CATEGORY PAGE
# ======================================================
@login_required(login_url="login")
def category_list_view(request):
    """
    Display all categories in the system.
    """
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})



# ======================================================
# TAG PAGE
# ======================================================
@login_required(login_url="login")
def tag_list_view(request):
    """
    Display all tags available in the system.
    """
    tags = Tag.objects.all()
    return render(request, "tag_list.html", {"tags": tags})

# ======================================================
# EDIT COMMENT VIEW
# ======================================================
@login_required(login_url='login')
def comment_edit_view(request, pk):
    """
    Edit an existing comment.
    Only the original author is allowed to modify their own comment.
    """
    # Get comment
    comment = get_object_or_404(Comment, pk=pk)

    # Only the author can edit
    if request.user != comment.author:
        return HttpResponseForbidden("You cannot edit this comment")

    #Handled from submission
    if request.method == "POST":
        new_text = request.POST.get("content")   #get edited comment text

        # Prevent empty update
        if not new_text.strip():
            return render(request, "comment_edit.html", {
                "comment": comment,
                "error": "Comment cannot be empty."
            })

        # Save updated comment
        comment.content = new_text   # update comment text
        comment.save()
        
        # Redirect back to the post where the comments belongs
        return redirect("post_detail", pk=comment.post.pk)

    return render(request, "comment_edit.html", {"comment": comment})


# ======================================================
# DELETE COMMENT VIEW
# ======================================================
@login_required(login_url='login')
def comment_delete_view(request, pk):
    """
    Delete a specific comment.
    Only the comment author can delete their own comment.
    """

    comment = get_object_or_404(Comment, id=pk)

    #  Disallow others from deleting the comment
    if request.user != comment.author:
        return HttpResponseForbidden("You cannot delete this comment.")

    post_id = comment.post.id

    #  Delete the comment
    comment.delete()

    return redirect("post_detail", pk=post_id)


# ======================================================
# PROFILE EDIT VIEW
# ======================================================

@login_required(login_url='login')
def profile_edit_view(request):
    """
    Handle profile editing for the logged-in user.
    Allows updating username, email, bio, and profile picture.
    """
    user = request.user

    #Process for the submission
    if request.method == "POST":
        #update basic profile informations
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")

        #update profile picture if a new one is uploaded 
        if request.FILES.get("profile_picture"):
            user.profile_picture = request.FILES.get("profile_picture")

        user.save()
        #Render the page with a success message
        return render(request, "profile_edit.html", {"user": user, "success": "Profile updated!"})

    return render(request, "profile_edit.html", {"user": user})

