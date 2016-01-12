from django.contrib import admin
from .models import Post, Info, BitcoinAddress

admin.site.register(Post)
admin.site.register(Info)
admin.site.register(BitcoinAddress)
# Register your models here.
