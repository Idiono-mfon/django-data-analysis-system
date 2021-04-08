from django.shortcuts import render, redirect
# import default user model already created by django
from .models import CustomUser
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from account.validations import validate_input,validate_login_form

# Create your views here.


def logoutuser(request):
    logout(request)
    return redirect('/')

def home(request):

    if not request.user.is_authenticated:
        return redirect('login')
    else:
        username = request.user.username
        return render(request,'analyse.html',{'name':username,'active':True})

def loginUser(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        result = validate_login_form({"name":username,"password":password})
        result = list(x for x in result if x not in {"false"})
        if len(result) != 0:

            for i in result:
                messages.info(request, i)
            
            return redirect("login")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # then get the user_id using the user logged in name
            return redirect('home')
        else:
            messages.info(request,'invalid login credentials')
            return redirect('login')


    else:
        return render(request, 'login.html')

def register(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('name',False)
        email = request.POST.get('email',False)
        password1= request.POST.get('password1',False)
        password2 = request.POST.get('password2',False)
        username = request.POST.get('username',False)

        # validation goes in here
        result = validate_input({"name":first_name, "email": email, "password1":password1, "password2":password2, "username":username})
        result = list(x for x in result if x not in {"false"})
        if len(result) != 0:

            for msg in result:
                messages.info(request, msg)
            return redirect("register")

     # check if password and confirm password field matches
        if password1 == password2:
            # check if user already exists in the table
            if CustomUser.objects.filter(username=username).exists():
                # check if the email list
                messages.info(request, 'Username already exist')
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                # check if user email is already in the database
                messages.info(request, 'Email already exist')
                #  this holds messages  which will be printed on the same page
                return redirect('register')
                # redirect user
            else:
                # insert user
                user = CustomUser.objects.create_user(username = username, password = password1, first_name = first_name,email = email)
                user.save()
                messages.info(request, 'Registration sucessfull!! Login In now')
                return redirect('login')
        else:
            messages.info(request, 'password fields are not uniform')
            return redirect('register')
    else:
        return render(request, 'register.html')

        

    