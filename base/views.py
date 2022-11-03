from django.shortcuts import render , redirect
from .forms import NewUserForm, ImageForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Friend, Message
from django.db.models import Q
from django.http import JsonResponse

#-----------------------------------------------------------------------

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated == False:
        return redirect('login')
    
    user = request.user.profile

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    
    result = Q(profile__name__icontains=q)
    try:
        friends = user.friends.filter(result)
    except:
        friends = user.friends.all()


    context = {
        'friends':friends,
         'user':user
         }

    return render(request, 'index.html', context)

#-----------------------------------------------------------------------

def signUp_Page(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'form': form
        }
    return render(request, 'sign-up.html', context)

#-----------------------------------------------------------------------

def login_Page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'login.html')

#-----------------------------------------------------------------------

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

#-----------------------------------------------------------------------

@login_required(login_url='login')
def chat(request, slug):
    form = MessageForm()
    user = request.user.profile
    receiver_profile = Profile.objects.get(slug=slug)
    friend = user.friends.get(slug=slug)
    messages = Message.objects.all()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.receiver = receiver_profile
            message.save()


            return redirect('chat',slug)



    context = {
        'user':user,
        'friend':friend,
        'form': form,
        'messages':messages,
        }
    
    
    return render(request, 'chat.html', context) 

#-----------------------------------------------------------------------

def messages(request):
    messages = Message.objects.all()

    return JsonResponse({'messages':list(messages.values())})

#-----------------------------------------------------------------------

@login_required(login_url='login')
def add_friend(request ):
    users_friends = request.user.profile.friends.all()
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    
    result = Q(profile__name__icontains=q)
    try:
        friends = Friend.objects.filter(result)
    except:
        friends = Friend.objects.all()

    user = request.user.profile
    context = {
        'friends': friends,
         'user':user,
         'usersfriends': users_friends
         }
    
    return render(request, 'search.html', context)

#-----------------------------------------------------------------------

def profile(request, slug):
    form = ImageForm()
    user = request.user.profile
    user_as_friend = Friend.objects.get(slug=user.slug)
    users_friends = request.user.profile.friends.all()
    friend = Friend.objects.get(slug=slug)
    
    if request.method == 'POST':
        if 'add-btn' in request.POST:
            user.friends.add(friend)
            friend.profile.friends.add(user_as_friend)
            return redirect('/')
        elif 'remove-btn' in request.POST: 
            user.friends.remove(friend)
            friend.profile.friends.remove(user_as_friend)
            return redirect('/')

        else:
            form = ImageForm(request.POST, request.FILES , instance=user)
            if form.is_valid():
                form.save()
    

    context = {
        'user':user,
        'friend':friend,
        'userfriends': users_friends,
        'form':form,
        'slug':slug,
        
        }
    
    return render(request, 'profile.html', context)   
