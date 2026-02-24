from django.shortcuts import render
from .models import researchMember,hakkimizda
from django.shortcuts import get_object_or_404

# Create your views here.
def egitim(request):
    members = researchMember.objects.filter(anasayfa=True) # anasayfa alanı True olan üyeleri çekiyoruz
    return render(request, 'egitim.html', {'members': members}) # home.html şablonuna üyeleri gönderiyoruz
def home(request):
    return render(request,'home.html')

def hakkimda(request):
    hakkimizda_obj = hakkimizda.objects.first() # Hakkımızda nesnesini al
    return render(request,'hakkimda.html', {'hakkimizda': hakkimizda_obj}) # Hakkımızda nesnesini şablona gönder

def uyedetay(request, pk):
    member=get_object_or_404(researchMember, pk=pk) # Belirli bir üye nesnesini al
    return render(request,'uyedetay.html', {'member': member}) # Üye nesnesini şablona gönder

def sosyal(request):
    return render(request,'sosyal.html')