from django.contrib import admin
from django.http import  HttpResponce
from .models import *
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order_table)
admin.site.register(Account)