from django.contrib import admin
from .models import Contact,User,Product,Wishlist,Cart
# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)