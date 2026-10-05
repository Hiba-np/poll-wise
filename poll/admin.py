from django.contrib import admin

# Register your models here.
from poll.models import CustomeUser,poll,choice

admin.site.register(CustomeUser)
admin.site.register(poll)
admin.site.register(choice)