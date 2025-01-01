from django.urls import path
from . import  views

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('',views.index,name='home'),
    path('acc',views.acc_creation,name='acc_creation'),
    path('otp',views.otp,name='otps'),
    path('pin_gen',views.pin,name='pin'),
    path('withdraw',views.withdraw,name='withdraw'),
    path('deposit',views.deposit,name='deposit'),
    path('transfer',views.transfer,name='transfer'),
    path('details',views.details,name='details')
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)