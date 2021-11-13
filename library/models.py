from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from datetime import datetime,timedelta
# Create your models here.
# class UserExtend(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     isAdmin = models.BooleanField(default = False)
#     isActive = models.BooleanField(default = True)
#     def __str__(self):
#        return self.user.username

class Book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bookname = CharField(max_length=50)
    author = CharField(max_length=20)
    isActive = models.BooleanField(default = True)
    def __str__(self):
        return str(self.bookname)+"["+str(self.id)+']'

class Burrow(models.Model):
        burrower = models.ManyToManyField(User,related_name="burrower")
        issuer = models.ManyToManyField(User,related_name="issuer")
        book = models.ManyToManyField(Book,related_name="book")
        isActive = models.BooleanField(default = True)
        def __str__(self):
            return str(self.burrower.username)+"["+str(self.book.bookname)+']'
