from django.contrib import admin
from .models import Contact, TemporaryBlockedContact, File

admin.site.register(Contact)
admin.site.register(TemporaryBlockedContact)
admin.site.register(File)
