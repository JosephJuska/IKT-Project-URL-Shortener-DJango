from django.shortcuts import render, redirect, reverse
from .models import UserModel, UrlModel
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .email import verification_email
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import pyshorteners
import secrets


def convert(url):
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(url)
    return short_url.split('/')[-1]

# Create your views here.
def index_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('account'))
    
    return render(request, "index.html")

def login_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('account'))
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and UserModel.objects.filter(username=username, verified=True):
            login(request, user)
            return redirect(reverse('account'))
        
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, "login.html")

def register_page(request):
    if request.user.is_authenticated:
        return redirect(reverse('account'))
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            verification_token = secrets.token_urlsafe()
            UserModel.objects.create_user(username=username, email=email, password=password, verification_token=verification_token)
            verification_email(username=username, email=email, verification_token=verification_token)
            messages.success(request, 'Account has been created successfully. Please verify your account via the email')
            return redirect(reverse('login'))
    
    else:
        form = RegisterForm()

    return render(request, "register.html", {'form' : form})

def account_page(request):
    if not request.user.is_authenticated:
        return redirect(reverse('index'))
    
    validator = URLValidator()
    if request.method == 'POST':
        if 'url_id' in request.POST:
            try:
                url_id = request.POST['url_id']
                url = UrlModel.objects.get(id=url_id)
                url.delete()
                messages.success(request, 'Short URL has been deleted successfully')
            
            except UrlModel.DoesNotExist:
                messages.error(request, 'Error occurred while deleting the Short URL')

        else:
            url = request.POST['url']
            if type(url) != str:
                print(type(url) != str)
                print(type(url))
                print('1')
                messages.error(request, 'Invalid URL')

            elif len(url) > 1000:
                print('2')
                messages.error(request, 'URL is too long')

            else:
                try:
                    validator(url)
                    short_url = convert(url + request.user.username)
                    print(short_url)
                    if not UrlModel.objects.filter(short_url=short_url).exists():
                        new_url_model = UrlModel.objects.create(url=url, short_url=short_url, user=request.user)
                        new_url_model.save()

                    else:
                        print('4')
                        messages.error(request, 'URL already exists')

                except ValidationError:
                    print('3')
                    messages.error(request, 'Invalid URL')

    url_objects = UrlModel.objects.filter(user=request.user)

    if not url_objects.exists():
        content = False
        click_amount = "No URLs"

    else:
        content = url_objects.all()
        click_amount = 0
        for item in content:
            click_amount += item.use_amount

    return render(request, "account.html", {'content': content, 'click_amount': click_amount})

def logout_page(request):
    if not request.user.is_authenticated:
        return redirect(reverse('index'))
    
    logout(request)
    return redirect(reverse('index'))

def verification_page(request, token):
    if request.user.is_authenticated:
        return redirect(reverse('account'))
    
    try:
        user = UserModel.objects.get(verification_token=token, verified=False)
        user.verified = True
        user.save()
        return render(request, 'verification.html')
    
    except UserModel.DoesNotExist:
        return redirect(reverse('index'))

def short_page(request, short_url):
    try:
        real_url = UrlModel.objects.get(short_url=short_url)

        content = {'real_url' : real_url.url, 'short_url' : real_url.short_url}
        return render(request, "short.html", content)
    
    except:
        return redirect(reverse('index'))
    
def redirect_page(request, short_url):
    try:
        real_url = UrlModel.objects.get(short_url=short_url)
        real_url.use_amount += 1
        real_url.save()

        return redirect(real_url.url)
    
    except:
        return redirect(reverse('index'))