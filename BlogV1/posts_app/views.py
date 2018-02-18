from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from models import Post, Category, Comment, Tag, Reply ,Like
from django.contrib.auth.models import User
from .forms import  UserRegForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import Post, Category, Comment, Tag, Reply, Like, Dislike, Forbidden
from forms import ReplyForm, CommentForm
import csv

# Create your views here.

def post(request, post_id):
    comment_form = CommentForm()
    reply_form = ReplyForm()
    post = Post.objects.get(id = post_id)
    tags = Tag.objects.filter(tag_posts__id = post_id)
    categories = Category.objects.all()
    comments = Comment.objects.filter(comment_post__id = post_id)
    reg_form = UserRegForm()

    comments_replies = []

    for comment in comments:
        replies = Reply.objects.filter(reply_comment__id = comment.id)
        comments_replies.append(replies)
    context = {'post': post, 'categories': categories, 'comments':comments, 'replies':comments_replies, 'reg_form':reg_form}
    return render(request, 'post.html', context)


def register_view(request):
    title="Register"
    form = UserRegForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

    context={
        "form":form,
        "title":title
     }
    return render(request, 'register.html', context)



def login_view(request):

    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return HttpResponse("logged in")
        else :
            return HttpResponse("you don`t exsit")

    return render(request , "login.html")

@login_required
def logged_in_only(request):
    return HttpResponse("you are authenticated")
    context = {'post': post, 'categories': categories,
               'comments':comments, 'replies':comments_replies,
               'comment_form':comment_form,
               'reply_form':reply_form,
               'tags':tags}

    return render(request, 'post.html', context)

def home(request):
    categories = Category.objects.all()
    posts_all = Post.objects.all()
    context = {'categories': categories, 'posts_all': posts_all, 'Post':Post,'Like': Like, 'Dislike': Dislike}
    return render(request, 'home.html', context)

def category(request, cat_id):
    categories = Category.objects.all()
    category = Category.objects.get(id = cat_id)
    context = {'category': category , 'categories': categories}
    # return HttpResponse(category)
    return render(request, 'category.html', context)

def comment_reply(request):
    if request.method == 'GET':
        comment_id = request.GET['comment_id']
        comment = Comment.objects.get(pk=comment_id)
        text = request.GET['reply_text']
        print text
        reply = Reply(reply_comment=comment, reply_text=text, reply_user=request.user)
        reply.save()
        return HttpResponse("Success!")
    else:
        return HttpResponse("Request method is not a GET")
    cat_posts = Post.objects.filter(post_category__id = cat_id)

    #cat_post = map(lambda x : x, cat_posts)

    context = {'category': category, 'categories': categories, 'cat_posts':cat_posts }

    return render(request, 'category.html', context)


def like_view(request,post_id):
    pid=Post.objects.get(id=post_id)
    Like.objects.create(like_post=pid,like_user=request.user)
    return JsonResponse({"state":True,"safe":False})


def unlike_view(request,post_id):
    pid=Post.objects.get(id=post_id)
    Like.objects.filter(like_post=pid,like_user=request.user).delete()
    return JsonResponse({"state": True, "safe": False})



def dislike_view(request,post_id):
    pid=Post.objects.get(id=post_id)
    Dislike.objects.create(dislike_user=request.user,dislike_post=pid)
    count = Dislike.objects.all().count()
    print count
    if count == 10:
        Post.objects.get(id=post_id).delete()
    return JsonResponse({"state": True, "safe": False})



def undislike_view(request,post_id):
    pid=Post.objects.get(id=post_id)
    Dislike.objects.filter(dislike_user_id=request.user,dislike_post_id=pid).delete()
    return JsonResponse({"state": True, "safe": False})



# def search(file_path):
#    reader = csv.DictReader(open(file_path))
#         for row in reader:
#             srch = Post()
#             srch.save()


# def search(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         posts = Post.objects.filter(post_title = q )[:20]
#         results = []
#         for post in posts:
#             post_json = {}
#             post_json['id'] = post.rxcui
#             post_json['label'] = drug.short_name
#             post_json['value'] = drug.short_name
#             results.append(post_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)


