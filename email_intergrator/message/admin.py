from django.contrib import admin
from message.models import EmailAccount, Message

admin.site.register(EmailAccount)
admin.site.register(Message)
