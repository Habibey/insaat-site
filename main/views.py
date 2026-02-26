from django.shortcuts import render
from .models import researchMember,hakkimizda
from django.shortcuts import get_object_or_404
from .utils import generate_dome_geometry, grpdet, define_supports, create_dome_plot

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

def geodezik_uygulama(request):
    context = {}
    
    # Sayfa ilk açıldığında kutucuklarda görünecek varsayılan değerler
    default_params = {'type': 5, 'span': 31.78, 'height': 7.0, 'freq': 5}
    context['params'] = default_params

    if request.method == 'POST':
        try:
            # 1. HTML formundan gelen verileri alıyoruz
            params = {
                'type': int(request.POST.get('type')),
                'span': float(request.POST.get('span')),
                'height': float(request.POST.get('height')),
                'freq': int(request.POST.get('freq'))
            }
            
            # Formda girilen son değerleri ekranda tutmak için güncelliyoruz
            context['params'] = params
            
            # 2. utils.py'daki matematiksel işlemleri çalıştırıyoruz
            dome = generate_dome_geometry(params)
            dome = grpdet(dome)
            dome = define_supports(dome)
            
            # 3. 3D Grafiği oluşturuyoruz
            fig = create_dome_plot(dome)
            
            # 4. Grafiği HTML sayfasına gömülebilir bir metne (string) çeviriyoruz
            # include_plotlyjs='cdn' kısmı grafiğin tarayıcıda interaktif çalışmasını sağlar
            plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
            context['plot_div'] = plot_div
            
        except Exception as e:
            context['error'] = f"Hesaplama sırasında bir hata oluştu: {str(e)}"
            
    # Sonuçları geodezik.html sayfasına gönderiyoruz
    return render(request, 'geodezik.html', context)  

def uygulamalar(request):
    return render(request,'uygulamalar.html')  