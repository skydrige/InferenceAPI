from django.contrib import admin
from .models import test_session, Chat_Session, Chat_Messages
from django.contrib.auth.models import User


# Register your models here.
# admin.site.register(User)
admin.site.register(test_session)
admin.site.register(Chat_Session)
admin.site.register(Chat_Messages)
