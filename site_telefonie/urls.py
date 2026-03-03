from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views
urlpatterns = [
	path("", views.index, name="index"),
	path("info/", views.info, name="info"),
    path("exemplu_template/", views.afis_template, name="afis_template"),
    path("afis_template1/", views.afis_template1, name="afis_template1"),
    path("log/", views.log, name="log"),
    path('despre/', views.despre, name='despre'),
    path('contact/', views.contact, name='contact'),
    path('cos_virtual/', views.in_lucru, name='cos_virtual'),
    path('produse/', views.lista_produse, name='lista_produse'),
    path('produs/<int:pk>/', views.detalii_produs, name='detalii_produs'),
    path('pachete/', views.lista_pachete, name='lista_pachete'),
    
    path('categorii/', views.lista_categorii, name='lista_categorii'),
    path('categorii/<str:nume_categorie>/', views.pachete_categorie, name='pachete_categorie'),
    path("produse/adauga/", views.adauga_produs, name="adauga_produs"),
    path("pagina_succes/", views.pagina_succes, name="pagina_succes"),
    path('inregistrare/', views.pagina_inregistrare, name='inregistrare'),
    path('login/', views.custom_login_view, name='login'),
    path('profil_utilizator/', views.profil_utilizator, name='profil_utilizator'),
    path('logout/', views.logout_view, name='logout'),
    path('schimbare_parola/', views.schimbare_parola, name='schimbare_parola'),
    path('confirmare_email/<str:cod>/', views.confirmare_email, name='confirmare_email'),
    path('creare-promotie/', views.creare_promotie, name='creare_promotie'),
    path('detalii-pachet/<int:pk>/', views.detalii_pachet, name='detalii_pachet'),
    path('interzis/', views.eroare_403_view, name='interzis'),
    path('oferta/', views.oferta_view, name='oferta_speciala'),
    path('logout-custom/', views.logout_custom, name='logout_custom'),
    path('claim-oferta/', views.claim_oferta, name='claim_oferta'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler403 = 'proiect1.views.eroare_403_view'