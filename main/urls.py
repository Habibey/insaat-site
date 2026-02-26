from django.urls import path
from . import views

#app_name = 'main' # ayrıca bir namespace tanımlayarak URL'leri daha düzenli hale getirebiliriz

urlpatterns = [
    path('', views.home, name='home'), # Anasayfa URL'si
    path('hakkimda/', views.hakkimda, name='hakkimda'), # Hakkımda sayfası URL'si
    path('egitim/', views.egitim, name='egitim'), # Eğitim sayfası URL'si
    path('uyedetay/<int:pk>/', views.uyedetay, name='uyedetay'), # Üye detay sayfası URL'si
    path('sosyal/',views.sosyal,name='sosyal'), # Sosyal sayfası URL'si
    path('uygulamalar/',views.uygulamalar,name='uygulamalar'), # Uygulamalar sayfası URL'si
    path('geodezik/', views.geodezik_uygulama, name='geodezik_uygulama'),
  
]


