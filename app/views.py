from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Post, PostLike, User, Follow
import json


@api_view(["POST"])
def create_user(request):
    data = request.data
    user = User.objects.create_user(data["user_name"], password=data["password"], )
    user.save()

    return HttpResponse(f"user_id: {user.id}", status=201)


@api_view(["POST"])
def create_post(request):
    data = request.data
    body = data["body"]
    post = Post(user=User(data["user_id"]), body=body)
    post.save()

    return HttpResponse(f"Success. post id: {post.id}")


@api_view(["GET"])
def get_top_users(request):
    users_posts = []
    users = User.objects.all()

    for _user in users:
        posts = Post.objects.filter(user=_user)
        if posts:
            users_posts.append(
                {"username": str(_user),
                 "posts": len(posts)
                 })

    return HttpResponse(json.dumps(sorted(users_posts, key=lambda i: i['posts'], reverse=True)))


@api_view(["POST"])
def follow_user(request):
    data = request.data
    who = User.objects.get(pk=data["user_id"])
    whom = User.objects.get(pk=data["following_user_id"])
    follow = Follow(who=who, whom=whom)
    follow.save()

    return HttpResponse(json.dumps({"message": "Followed successfully."}), status=201)


@api_view(["POST"])
def like_post(request, post_id):
    data = request.data
    user_id = data["user_id"]
    get_object_or_404(Post, id=post_id)
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=post_id)
    like_post = PostLike(user_id=user.id, post_id=post.id)
    like_post.save()

    return HttpResponse("Like post successfully", status=201)


@api_view(["GET"])
def get_list_of_posts(request, user_id):
    all_posts = []
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user_id)
    for post in posts:
        # here I will return posts created by given user id.
        all_posts.append({
            "id": post.id,
            "body": post.body,
            "author": str(user),
            "likes": len(post.liked_by.all()),
        })
    # i am assuming here reverse chronological order mean most like to least like.
    # if you meant by least likes to most like then you just have to pass reverse=True in sorted function
    reverse = sorted(all_posts, key=lambda i: i['likes'])
    return HttpResponse(json.dumps({"data": reverse}))
