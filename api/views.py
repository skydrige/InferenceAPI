from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_protect

from .Preprocessor import Preprocessor
from .inference.summary import Summarizer
from .models import Session, Messages

summarizer = Summarizer()


@csrf_protect
def index(request):
    processor = Preprocessor()
    content = processor.clean(request.POST['content'])
    print(content)
    if len(content) <= 10 or len(content) >= 20000:
        return JsonResponse({"summary": "Can't summarize this!"})
    text = summarizer.summarize(content)
    return JsonResponse({"summary": processor.formater(text)})


def test(request):
    text = summarizer.summarize(summarizer.text)
    return HttpResponse(Preprocessor().formater(text))


@csrf_protect
def direct_summary(request):
    processor = Preprocessor()
    content = processor.clean(request.POST['content'])
    if len(content) <= 10 or len(content) >= 20000:
        return render(request, 'contextForm.html', {'userInput': content, 'summary': "Can't summarize this!"})

    print("Direct: ", content)
    text = summarizer.summarize(content)
    return render(request, 'contextForm.html', {'userInput': content, 'summary': processor.formater(text)})


def direct_form(request):
    return render(request, 'contextForm.html')


@login_required(login_url='login_view')
def chat(request):
    name = request.user.first_name
    session_id = request.session['session_id']
    if session_id is None:
        redirect(new_chat)
    data = Messages.objects.filter(username=request.user, session=session_id)
    processor = Preprocessor()
    for i in data:
        i.model = processor.formater(i.model)
    return render(request, 'test.html', {'username': name, 'data': data})


@login_required(login_url='login_view')
@csrf_protect
def user_query(request):
    username = request.user.username
    session_id = request.session['session_id']
    query = request.POST.get('query')
    if len(query) < 10:
        return redirect(chat)
    message_db = Messages.objects.filter(username=username, session=session_id).order_by('-timestamp')
    previous = message_db[:4]
    text = summarizer.reply(query, previous)
    conversation = Messages()
    conversation.session = session_id
    message_id = message_db.first()
    if message_id is not None:
        conversation.message_id = session_id + ".message." + str(int(str(message_id).split(".")[-1]) + 1)
    else:
        conversation.message_id = session_id + '.message.0'
    conversation.username = username
    conversation.user = query
    conversation.model = text
    conversation.save()
    return redirect(chat)


@login_required(login_url='login_view')
def new_chat(request):
    user = User.objects.get(username=request.user.username)
    session = Session()
    session.user = user
    session_id = Session.objects.filter(user=user).order_by('-timestamp').first()
    if session_id is not None:
        session.session_id = user.username + "." + str(int(str(session_id).split(".")[-1]) + 1)
    else:
        session.session_id = user.username + 'session.0'
    session.save()
    request.session['session_id'] = session.session_id
    return redirect(chat)


@csrf_protect
def signup(request):
    user = User()
    try:
        user.first_name = request.POST['name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.set_password(request.POST['password'])
        user.save()
        return render(request, 'login.html', {'message': 'Account created!', 'user': user})
    except IntegrityError:
        return render(request, 'signup.html', {'error': 'User already existed!', 'user': user})
    except MultiValueDictKeyError:
        return render(request, 'signup.html')
    except Exception as e:
        return render(request, 'signup.html', {'error': e})


@csrf_protect
def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html', {'error': e})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(chat)
    else:
        return render(request, 'login.html', {'error': 'Invalid username or password!', 'details': user})


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {'message': 'You have been logged out!'})


def test_html(request):
    return render(request, 'test.html')
