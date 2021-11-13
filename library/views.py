from django.shortcuts import render,HttpResponse,redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime,timedelta,date

from .models import Book, Burrow

from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
# Create your views here.
def home(request):
    return render(request, "index.html")

def dashboard(request):
    if request.session.has_key('is_logged'):
        return render(request,"dashboard.html")
    else:
        return render(request, "index.html")

def authenticateuser(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        RegisteredUser = authenticate(username=email, password=password)
        if RegisteredUser is not None:
            dj_login(request, RegisteredUser)
            request.session['is_logged'] = True
            RegisteredUser = request.user.id
            request.session["user_id"] = RegisteredUser
            request.session["isAdmin"] = User.objects.get(id = RegisteredUser).is_staff
            messages.success(request, " Successfully logged in")
            return redirect('dashboard')
        else:
            messages.error(request," Invalid Credentials, Please try again")
            return redirect("/")
    return HttpResponse('404-not found')

def HandleLogout(request):
        del request.session['is_logged']
        del request.session["user_id"]
        del request.session["isAdmin"]
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('home')

def signupuser(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        # userprofile = UserExtend(isAdmin=True)
        if request.method == 'POST':
            try:
                UserExists = User.objects.get(username=request.POST['email'])
                messages.error(request," Email already taken, Try something else!!!")
                return redirect("login")
            except User.DoesNotExist:
                # create the user
                user = User.objects.create_user(email, email, password)
                user.first_name=name
                user.last_name=name
                user.email = email
                user.is_staff = 1
                user.save()
                # userprofile.user = user
                # userprofile.save()
                messages.success(request," Your account has been successfully created")
                return redirect("login")
    else:
        return HttpResponse('404 - NOT FOUND ')

def login(request):
    return render(request,"login.html")


def books(request):
    if request.session.has_key('is_logged'):
        books = []
        if User.objects.get(id = request.session["user_id"]).is_staff:
            # try:
            books = Book.objects.filter(user_id = request.session["user_id"])
            # except Book.DoesNotExist:
            #     return render(request,"book.html",{"Books":books})
        else:
            books = Book.objects.all()
        return render(request,"book.html",{"Books":books})
    else:
        return redirect("login")


def addbook(request):
    if request.method == 'POST':
        if request.session.has_key('is_logged'):
            if request.session["isAdmin"] == 1:
                user1 = User.objects.get(id = request.session["user_id"])
                bookname = request.POST["bookname"]
                author = request.POST["author"]
                add = Book(user = user1,bookname=bookname,author=author)
                add.save()
                messages.success(request,"Book added!")
                return redirect("books")
            else:
                messages.error(request," Error while adding book")
                return redirect("books")
        else:
            return redirect("login")
    else:
        return HttpResponse('404 - NOT FOUND ')

def deletebook(request, bookid):
    if request.session.has_key('is_logged'):
        if request.session["isAdmin"] == 1:
            if bookid > 0:
                Book.objects.filter(id = bookid).delete()
                messages.error(request," Book deleted")
        else:
            messages.error(request," You are not authorized to delete")
        return redirect("books")
    else:
        return redirect("login")

def getupdate(request,bookid):
    if request.session.has_key('is_logged'):
        if request.session["isAdmin"] == 1:
            book = Book.objects.get(id = bookid)
            return render(request,"updateform.html",{"Book":book})
            # if books is not None:
            #     return render(request,"updateform.html",{"Book":books})
            # else:
            #     return HttpResponse('404 - Not Found ')
        else:
            return HttpResponse('401 - Unauthorized ')
    else:
        return redirect("login")


def updatebook(request):
    if request.session.has_key('is_logged'):
        if request.session["isAdmin"] == 1:
            booknameUpdate = request.POST["bookname"]
            authorUpdate = request.POST["author"]
            bookid = request.POST["bookid"]
            Book.objects.filter(id = bookid).update(bookname = booknameUpdate,author= authorUpdate)
            messages.success(request," Book updated")
            return redirect("books")
        else:
            messages.error(request," You are not authorized to delete")
            return redirect("books")
    else:
        return redirect("login")
