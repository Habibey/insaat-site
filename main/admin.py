from django.contrib import admin
from .models import researchMember,hakkimizda

# Register your models here.
class researchMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email','aktifmi' ) # Admin panelinde görünecek alanlar
    search_fields = ('name', 'email') # Admin panelinde arama yapılacak alanlar
    list_filter = ('aktifmi',) # Admin panelinde filtreleme yapılacak alanlar
admin.site.register(researchMember, researchMemberAdmin)

class hakkimizdaAdmin(admin.ModelAdmin):
    list_display = ('metin',) # Admin panelinde görünecek alanlar
admin.site.register(hakkimizda, hakkimizdaAdmin)    
