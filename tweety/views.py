from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from markov_bot import Tweet_Generator
from twython import Twython

import random
import settings


def get_tweet_history(screen_name):
    twt = Twython(settings.API_KEY,settings.API_SECRET)
    time_line = twt.get_user_timeline(screen_name = screen_name,count = 200) # at max retrieves 200 tweets
    tweets_list = [ tweet['text'] for tweet in time_line ]
    twt_gen = Tweet_Generator(tweets_list)
    next_tweets = []
    for i in xrange(10): # generates 10 tweets at a time
        next_tweets.append(twt_gen.generate_tweet(size = random.randint(5,20)))
    return next_tweets

def index(request):
    context = Context({})
    return render_to_response('index.html',context)

def get_tweets(request):
    if request.method == "GET":
        context = Context({})
        # getting the screen_name of the user from the query parameter
        screen_name = request.GET.get('screen_name','')
        # js will do the job of checking if screen name exists on twitter or not
        if not screen_name:
            context['errors']  = 'No username supplied'
            return render_to_response('index.html',context)
        next_tweets = get_tweet_history(screen_name)
        context['tweets'] = next_tweets # passing a list parameter
        return render_to_response('index.html',context)
 