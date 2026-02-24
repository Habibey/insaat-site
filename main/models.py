from django.db import models

# Create your models here.
class researchMember(models.Model):
    name = models.CharField(max_length=150)
    aktifmi=models.BooleanField(default=True)
    title=models.CharField(max_length=150,null=True,blank=True)
    email=models.EmailField()
    unvan=models.CharField(max_length=150,null=True,blank=True) #üye unvanı (örneğin: Doç. Dr., Prof. Dr. gibi)
    uzmanlikAlani=models.CharField(max_length=150,null=True,blank=True) #üye uzmanlık alanı (örneğin: Yapı Malzemeleri, Geoteknik gibi)
    seo_title=models.CharField(max_length=155,null=True,blank=True) #arama motorlarında görünecek başlık
    seo_description=models.TextField(max_length=155,null=True,blank=True)#arama motorlarında görünecek açıklama
    slug=models.SlugField(max_length=150,unique=True,null=True,blank=True) #url'de görünecek benzersiz tanımlayıcı
    resim=models.ImageField(upload_to="uyeresimleri",null=True,blank=True) #üye resimleri için medya klasöründe "uye_resimleri" adlı bir alt klasör oluşturulur
    anasayfa=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Araştırma Üyesi'
        verbose_name_plural = 'Araştırma Üyeleri'
  
    def __str__ (self): #Admin panelinde isim ile listelenir yazmazsan object olarak listelenir
        return self.name
    

class hakkimizda(models.Model):
    description=models.TextField(max_length=500,null=True,blank=True) #hakkımızda sayfasında görünecek açıklama
    metin=models.CharField(max_length=150,null=True,blank=True) #hakkımızda sayfasında görünecek başlık
    resim=models.ImageField(upload_to="arkaplan",null=True,blank=True) #hakkımızda sayfasında görünecek arkaplan resmi için medya klasöründe "arkaplan" adlı bir alt klasör oluşturulur

    class Meta:
        verbose_name = 'Hakkımızda'
        verbose_name_plural = 'Hakkımızda'

    def __str__(self):
        return self.metin