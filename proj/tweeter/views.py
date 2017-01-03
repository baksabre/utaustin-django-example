from __future__ import print_function

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from tweeter.models import Tweet, Profile
from tweeter.forms import TweetForm, UserProfileForm


@require_http_methods(["GET", "POST"])
def home_page(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet_text = form.cleaned_data["tweet"]
            tweet = Tweet(content=tweet_text, creator=request.user)
            tweet.save()
            return HttpResponseRedirect("/")
    else:
        form = TweetForm()
    recent_tweets = Tweet.objects.order_by('-created_at').all()[:5]
    context = {
        "recent_tweets": recent_tweets,
        "form": form,
    }
    return render(request, "home_page.html", context)


@require_http_methods(["GET", "POST"])
def view_user(request, username):
    try:
        user = User.objects.filter(username=username).get()
    except User.DoesNotExist:
        raise Http404("User {username} not found".format(username=username))

    if user == request.user:
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
        else:
            form = UserProfileForm()
    else:
        form = None

    user_tweets = (
        Tweet.objects.filter(creator=user)
        .order_by('-created_at').all()
    )
    context = {
        "viewed_user": user,
        "tweets": user_tweets,
        "form": form,
    }
    return render(request, "view_user.html", context)
