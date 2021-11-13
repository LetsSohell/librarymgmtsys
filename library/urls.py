from django.urls import path

from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("login",views.login,name="login"),
    path("authenticateuser",views.authenticateuser,name="authenticateuser"),
    path("signupuser",views.signupuser,name="signupuser"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("books",views.books,name="books"),
    path("addbook",views.addbook,name="addbook"),
    path("deletebook/<int:bookid>",views.deletebook,name="deletebook"),
    path("getupdate/<int:bookid>",views.getupdate,name="getupdate"),
    path("updatebook",views.updatebook,name="updatebook"),
    path("logout",views.HandleLogout,name="logout")



]
