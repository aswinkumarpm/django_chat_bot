from django.db.models import F, Sum
from django.http import Http404
from django.shortcuts import render, redirect
import random
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from .models import Call
from .forms import UserRegistrationForm
from django import forms


def home(request):
    query = Call.objects.all()

    context = {
        "query": query,
    }

    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

        else:
            return HttpResponse("Correct Your forms")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def index(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")
        return redirect(
            '/play/%s?&choice=%s'
            % (room_code, char_choice)
        )
    return render(request, "index.html", {})


def game(request, room_code):
    choice = request.GET.get("choice")
    if choice not in ['X', 'O']:
        raise Http404("Choice does not exists")
    context = {
        "char_choice": choice,
        "room_code": room_code
    }
    return render(request, "game.html", context)


def test(request, message):
    print("aswonkajkdskjhjkhd")
    print(message)

    print(request.user)

    call = Call(message=message, user=request.user)
    call.save()

    # choice = request.GET.get("choice")
    # if choice not in ['X', 'O']:
    #     raise Http404("Choice does not exists")
    # context = {
    #     "char_choice": message,
    # }
    return redirect('new_chat')


def new_chat(request):
    query = Call.objects.all()
    from django.db.models import Count


    categories = Call.objects.all().order_by('message').values('user__username', 'message').annotate(count=Count('user'))
    print(categories)

    res = User.objects.all()
    print(res)

    test = Call.objects.values('user__username').order_by('user__username').annotate(count=Count('message'))
    print(test)



    context = {
        "query": query,
        "categories": categories,
        "test": test,
    }




    return render(request, 'chatbot_tutorial/new_chat_bot.html', context)


class ChatView(TemplateView):
    template_name = 'chatbot_tutorial/new_chatbot.html'


def respond_to_websockets(message):
    jokes = {
        'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                   """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
        'fat': ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
        'dumb': [
            """Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
            """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
    }

    # result_message = {
    #     'type': 'text'
    # }
    if message == 'fat':
        # if 'fat' in message['text']:
        result_message = random.choice(jokes['fat'])

    elif message == 'stupid':

        # elif 'stupid' in message['text']:
        result_message = random.choice(jokes['stupid'])

    elif message == 'dumb':

        # elif 'dumb' in message['text']:
        result_message = random.choice(jokes['dumb'])

    elif message in ['hi', 'hey', 'hello']:
        result_message = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
