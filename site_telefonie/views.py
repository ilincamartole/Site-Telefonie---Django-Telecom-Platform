from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime, date
import logging

logger = logging.getLogger('django')


import locale
import os
import time
import json
from django.conf import settings
from urllib.parse import urlparse
from collections import Counter
from site_telefonie.models import Serviciu, Telefon,Produs,CategoriePachet,Pachet, Vizualizare
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from site_telefonie.forms import FiltruProduseForm, FiltruPacheteForm, ContactForm, ServiciuForm, TelefonForm, CreareUtilizatorForm,CustomLoginForm, CrearePromotieForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
import uuid
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash



try:
    locale.setlocale(locale.LC_TIME, 'Romanian_Romania.1250')
except locale.Error:
	try:
		locale.setlocale(locale.LC_TIME, 'ro_RO.UTF-8')
	except locale.Error:
		pass  

moment_start_server = datetime.now()


fisier_accesari="loguri.txt"
class Accesare:
    id_counter = 0
    istoric = []

    def __init__(self, ip_client=None, url=None, data=None, salvare=True):
        Accesare.id_counter += 1
        self.id = Accesare.id_counter
        self.ip_client = ip_client
        self.url = url
        # daca nu primim data, setam data curenta
        self.data = data or datetime.now()
        Accesare.istoric.append(self)

        if salvare:
            with open(fisier_accesari, "a") as f:
# Scriem datele separate prin virgula
                data_text = self.data.strftime('%Y-%m-%d %H:%M:%S')
                linie = f"{self.ip_client},{self.url},{data_text}\n"
                f.write(linie)

    def lista_parametri(self):
        return [("id", self.id), ("ip_client", self.ip_client), ("url", self.url), ("data", self.data)]
    def get_url(self):
        return self.url

    def pagina(self):
        if not self.url:
            return None
        parsed = urlparse(self.url)
        return parsed.path or "/"



if os.path.exists(fisier_accesari):
    # Deschidem fisierul sa il citim ("r" = read)
    with open(fisier_accesari, "r") as f:
        for linie in f:

            linie = linie.strip() # Scoatem spatiile goale si \n
            if len(linie) > 0:
                parti = linie.split(",")

                
                # Extragem bucatile
                ip_vechi, rest = linie.split(",", 1)
                url_vechi, data_text = rest.rsplit(",", 1)  
                data_veche = datetime.strptime(data_text, '%Y-%m-%d %H:%M:%S')

                # Recream obiectul in memorie, dar ii zicem salvare=False
                # ca sa NU il scrie din nou in fisier
                Accesare(ip_vechi, url_vechi, data_veche, salvare=False)


def afis_data(param_data):
	acum = datetime.now()

	if param_data is None:
		return ""
	elif param_data == 'zi':
		data_formatata = acum.strftime("%A, %d %B %Y")
		return f"<p>{data_formatata}</p>"
	elif param_data == 'timp':
		data_formatata = acum.strftime("%H:%M:%S")
		return f"<p>{data_formatata}</p>"
	else:
		data_formatata = acum.strftime("%A, %d %B %Y, %H:%M:%S")
		return f"<p>{data_formatata}</p>"


def index(request):
	Accesare(request.META.get('REMOTE_ADDR'), request.build_absolute_uri())
	return HttpResponse("""
		<html>
		<body>
		 <b>Primul răspuns</b>
		 <p>
		 Site-ul reprezintă o platformă comercială pentru o companie de telecomunicații care oferă servicii de internet și telefonie. Proiectul va include o pagină principală de prezentare, o secțiune dedicată pachetelor de internet fibră optică cu diverse viteze și prețuri, o pagină pentru serviciile de telefonie fixă și mobilă, precum și o secțiune de oferte speciale. Utilizatorii vor putea vizualiza detaliile fiecărui pachet, compara opțiunile disponibile și completa un formular de contact pentru a solicita abonamente sau informații suplimentare.
		 </p>
		 </body>
		 </html>
	""")


def info(request):
    if not request.user.groups.filter(name="Administratori_site").exists():
        return eroare_403_view(
            request,
            titlu="Eroare 403",
            mesaj="Nu ai acces la pagina /info"
        )

    Accesare(get_client_ip(request), request.build_absolute_uri())

    param_data = request.GET.get('data', None)
    sectiune_data = afis_data(param_data)
    return HttpResponse(f"""
        <html>
        <body>
         <title> Informații despre server </title>
         <h1>Informații despre server</h1>
        <h2>Data si ora:</h2>
         {sectiune_data}
         </body>
         </html>
    """)


def afis_template(request):
	return render(request, "site_telefonie/exemplu.html",
				  {
					  "titlu_tab": "Titlu fereastra",
					  "titlu_articol": "Titlu afisat",
					  "continut_articol": "Continut text"
				  })


def afis_template1(request):
	return render(request, "site_telefonie/simplu.html")

def log(request):
    if not request.user.groups.filter(name="Administratori_site").exists():
        return eroare_403_view(
            request,
            titlu="Eroare 403",
            mesaj="Nu ai acces la pagina /log"
        )
    # Inregistram accesul curent
    Accesare(get_client_ip(request), request.build_absolute_uri())

    accesari = Accesare.istoric
    k = len(accesari)
    accesari_de_afisat = accesari[:]
    mesaj = ""
    mod_afisare="lista"
    coloane_tabel=[]

    nr_params= len(request.GET)
    nume_params = list(request.GET.keys())



        # --- filtrare dupa ID-uri ---
    iduri_param = request.GET.getlist("iduri")
    if iduri_param:
            # Construim lista de id-uri in ordinea primita in query (ex: [2,3,5,4,2,1])
            iduri_lista = []
            for x in iduri_param:
                for y in x.split(","):
                    if y.strip().isdigit():
                        iduri_lista.append(int(y.strip()))

            # Verificam flag-ul pentru dubluri (default: false)
            dubluri_flag = request.GET.get("dubluri", "false").lower() == "true"

            if not dubluri_flag:
                # Eliminam duplicatele, pastrand prima aparitie (in ordinea ceruta)
                seen = set()
                uniq = []
                for x in iduri_lista:
                    if x not in seen:
                        uniq.append(x)
                        seen.add(x)
                iduri_lista = uniq
            
            else:
                # Daca dubluri_flag==True, nu eliminam duplicatele.
                pass

            # Construim lista de accesari respectand ordinea din iduri_lista.
            # (noi iteram pur si simplu lista 'iduri_lista' si adaugam obiectele gasite).
            id_map = {a.id: a for a in accesari}  
            accesari_de_afisat = []
            for ident in iduri_lista:
                a = id_map.get(ident)
                if a:
                    accesari_de_afisat.append(a)

            mesaj = f"Accesările selectate după ID-uri: {', '.join(map(str, iduri_lista))}"




    # --- filtrare ultimele n accesari ---
    ultimele = request.GET.get('ultimele')
    if ultimele:
        if ultimele.isdigit():
            n = int(ultimele)
            if n > k:
                accesari_de_afisat = accesari
                mesaj += f"<br><span style='color:red'>Exista doar {k} accesari fata de {n} cerute.</span>"
            else:
                accesari_de_afisat = accesari[-n:]
                mesaj += f"Ultimele {n} accesări:"
        else:
            return HttpResponse("Parametrul 'n' este obligatoriu cifra.")
        
    
    # --- filtrare dupa parametru "accesari" ---
    accesari_param = request.GET.get("accesari")
    info_accesari_nr=None
    
    if accesari_param == "nr":
        accesari_de_afisat = [a for a in accesari if a.data >= moment_start_server]
        mesaj = f"Total accesări de la pornirea serverului: {len(accesari_de_afisat)}"





    # --- tabel fix cu toate coloanele ---
    param_tabel = request.GET.get("tabel")
    date_tabel = [] # Lista de dictionare pentru template
    
    if param_tabel:
        mod_afisare = "tabel"
        if param_tabel == "tot":
            coloane_tabel = ["id", "ip_client", "url", "data"]
        else:
            # ex: tabel=id,url
            coloane_tabel = [c.strip() for c in param_tabel.split(",") if c.strip()]
        
        # Construim datele doar pentru coloanele cerute
        for a in accesari_de_afisat:
            rand = {}
            if "id" in coloane_tabel: rand["id"] = a.id
            if "ip_client" in coloane_tabel: rand["ip_client"] = a.ip_client
            if "url" in coloane_tabel: rand["url"] = a.url
            if "data" in coloane_tabel: rand["data"] = a.data.strftime('%Y-%m-%d %H:%M:%S')
            date_tabel.append(rand)


    # --- statistici pagini ---
    pagina_max = pagina_min = None
    if k > 0:
        pagini = [a.pagina() for a in accesari]
        counter = Counter(pagini)
        pagina_max = counter.most_common(1)[0][0]
        pagina_min = counter.most_common()[-1][0]
    
    categorii = CategoriePachet.objects.all()

    context = {
        "accesari": accesari_de_afisat,
        "mesaj": mesaj,
        "mod_afisare": mod_afisare,
        "coloane_tabel": coloane_tabel,
        "accesari_tabel": date_tabel,
        "nr_params": nr_params,
        "nume_params": nume_params,
        "accesari_nr": info_accesari_nr,
        "accesari_param": accesari_param,

        "pagina_max": pagina_max,
        "pagina_min": pagina_min,
        'categorii': categorii
    }

    return render(request, "site_telefonie/log.html", context)


def index(request):
    return render(request, "site_telefonie/index.html", {"ip": get_client_ip(request)})

def despre(request):
    return render(request, "site_telefonie/despre.html", {"ip": get_client_ip(request)})

def in_lucru(request):
    return render(request, "site_telefonie/in_lucru.html", {"ip": get_client_ip(request)})

# Functie ajutatoare pentru IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Serviciu, Telefon, CategoriePachet
from .forms import FiltruProduseForm


def lista_produse(request):
    Accesare(get_client_ip(request), request.build_absolute_uri())

    servicii = Serviciu.objects.all()
    telefoane = Telefon.objects.all()
    toate_produsele = list(servicii) + list(telefoane)

    form = FiltruProduseForm(request.GET or None)
    mesaj_paginare = None
    if form.is_valid():
        nume = form.cleaned_data.get('nume')
        tip = form.cleaned_data.get('tip')
        pret_min = form.cleaned_data.get('pret_min')
        pret_max = form.cleaned_data.get('pret_max')
        items_per_page = form.cleaned_data.get('items_per_page') or 5  # valoare default

        if nume:
            toate_produsele = [p for p in toate_produsele if nume.lower() in p.nume.lower()]

        if tip:
            if tip == 'serviciu':
                toate_produsele = [p for p in toate_produsele if isinstance(p, Serviciu)]
            elif tip == 'telefon':
                toate_produsele = [p for p in toate_produsele if isinstance(p, Telefon)]

        if pret_min is not None:
            toate_produsele = [p for p in toate_produsele if p.pret >= pret_min]
        if pret_max is not None:
            toate_produsele = [p for p in toate_produsele if p.pret <= pret_max]
        
        # Mesaj DOAR daca utilizatorul a schimbat items_per_page si navigheaza intre pagini
        if 'items_per_page' in request.GET and 'page' in request.GET:
            if int(request.GET.get('page', 1)) > 1:
                mesaj_paginare = "Atenție! În urma schimbării numărului de produse pe pagină, este posibil să fi sărit peste unele produse sau să le vedeți din nou pe cele deja vizualizate."

    else:
        items_per_page = 5  # valoare default

    # Sortare
    sortare = request.GET.get('sort')
    if sortare == 'a':
        toate_produsele.sort(key=lambda x: x.nume.lower())
    elif sortare == 'd':
        toate_produsele.sort(key=lambda x: x.nume.lower(), reverse=True)

    if settings.DEBUG:
        messages.debug(request, f"Filtru produse: rezultate={len(toate_produsele)}, items_per_page={items_per_page}, sort={sortare}")

    # Paginare
    paginator = Paginator(toate_produsele, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context={'form': form,
        'page_obj': page_obj,
        'sortare': sortare,
        'mesaj_paginare': mesaj_paginare
    }
    return render(request, 'site_telefonie/lista_produse.html', context)

def detalii_produs(request, pk):
    """
    Afisează pagina de detalii pentru un produs. 
    ID-ul este pasat ca 'pk' (primary key).
    
    """
    Accesare(get_client_ip(request), request.build_absolute_uri())

    produs = get_object_or_404(Produs, id_produs=pk)


    
    detalii_specifice = None
    tip_produs = None
    
    # Incercam sa accesam obiectul "copil" specific (Serviciu sau Telefon)
    try:
        detalii_specifice = Serviciu.objects.get(id_produs=pk)
        tip_produs = 'serviciu'
    except Serviciu.DoesNotExist:
        try:
            detalii_specifice = Telefon.objects.get(id_produs=pk)
            tip_produs = 'telefon'
        except Telefon.DoesNotExist:

            pass

    categorii = CategoriePachet.objects.all()
    context = {
        'produs': produs,            # Obiectul Produs (cu nume, pret)
        'detalii': detalii_specifice, # Obiectul Serviciu SAU Telefon (cu descriere, imagine, etc.)
        'tip_produs': tip_produs
        ,'categorii': categorii
    }

    return render(request, 'site_telefonie/detalii_produs.html', context)

from site_telefonie.models import Pachet, CategoriePachet
from django.core.paginator import Paginator
from django.shortcuts import render

def lista_pachete(request):
    Accesare(get_client_ip(request), request.build_absolute_uri())

    form = FiltruPacheteForm(request.GET or None)
    pachete = Pachet.objects.all()
    items_per_page = 5  # valoare implicita
    mesaj_paginare = None
    
    if form.is_valid():
        nume = form.cleaned_data.get('nume_pachet')
        categorie = form.cleaned_data.get('categorie')
        items_per_page = form.cleaned_data.get('items_per_page') or 5 

        pret_min = form.cleaned_data.get('pret_min')
        pret_max = form.cleaned_data.get('pret_max')

        if nume:
            pachete = pachete.filter(nume_pachet__icontains=nume)
        if categorie:
            pachete = pachete.filter(apartine=categorie)
        if pret_min is not None:
            pachete = pachete.filter(contine__pret__gte=pret_min)
        if pret_max is not None:
            pachete = pachete.filter(contine__pret__lte=pret_max)
        
        # Mesaj DOAR daca utilizatorul a schimbat items_per_page si navigheaza intre pagini
        if 'items_per_page' in request.GET and 'page' in request.GET:
            if int(request.GET.get('page', 1)) > 1:
                mesaj_paginare = "Atenție! În urma schimbării numărului de produse pe pagină, este posibil să fi sărit peste unele produse sau să le vedeți din nou pe cele deja vizualizate."
    else:
        items_per_page = 5  # valoare implicita

    # Paginare
    paginator = Paginator(pachete, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    context = {
        'form': form,
        'page_obj': page_obj,
        'mesaj_paginare': mesaj_paginare
    }
    return render(request, 'site_telefonie/lista_pachete.html', context)
from django.contrib import messages

def pachete_categorie(request, nume_categorie):
    Accesare(get_client_ip(request), request.build_absolute_uri())
    categorie = get_object_or_404(CategoriePachet, nume_categorie=nume_categorie)

    # Blocheaza accesul daca parametrul 'categorie' din GET nu corespunde categoriei din URL
    categorie_param = request.GET.get('categorie')
    if categorie_param and str(categorie.id_categorie) != str(categorie_param):
        messages.error(request, "Acces interzis: nu poți schimba categoria din URL.")
        # return redirect('lista_categorii')  # Comentează această linie!

    form = FiltruPacheteForm(
        request.GET or None,
        initial={'categorie': categorie}
    )

    pachete = Pachet.objects.filter(apartine=categorie)

    if form.is_valid():
        nume = form.cleaned_data.get('nume_pachet')
        pret_min = form.cleaned_data.get('pret_min')
        pret_max = form.cleaned_data.get('pret_max')

        if nume:
            pachete = pachete.filter(nume_pachet__icontains=nume)
        if pret_min:
            pachete = pachete.filter(contine__pret__gte=pret_min)
        if pret_max:
            pachete = pachete.filter(contine__pret__lte=pret_max)

    paginator = Paginator(pachete.distinct(), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    messages.info(request, f"Afișăm pachetele din categoria: {nume_categorie}")
    return render(request, 'site_telefonie/lista_pachete.html', {
        'form': form,
        'page_obj': page_obj,
        'categorie_selectata': categorie,
    })

def lista_categorii(request):
    Accesare(get_client_ip(request), request.build_absolute_uri())
    categorii = CategoriePachet.objects.all()
    return render(request, 'site_telefonie/lista_categorii.html', {'categorii': categorii})

categorii = CategoriePachet.objects.all()



def contact(request):
    Accesare(get_client_ip(request), request.build_absolute_uri())

    mesaj_trim = False
    mesaj_salvat = False
    mesaj_path = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if 'submit' in request.POST and form.is_valid():
            # --- Preprocesare date ---
            data = form.cleaned_data.copy()
            
            # Calcul varsta in ani si luni
            data_nasterii = data.get("data_nasterii")
            azi = date.today()
            ani = azi.year - data_nasterii.year
            luni = azi.month - data_nasterii.month
            if luni < 0:
                ani -= 1
                luni += 12
            data["varsta"] = f"{ani} ani și {luni} luni"
            del data["data_nasterii"]  # stergem campul original
            
            import re
            mesaj = data.get("mesaj", "") 
            # Curatare mesaj: \n -> spatiu, multiple spatii -> unul singur
            mesaj = re.sub(r'\s+', ' ', mesaj.strip())
            # Majuscule dupa terminatori de fraza
            mesaj = re.sub(r'(?<=[\.\?\!]\s)([a-zăâîșț])', lambda m: m.group(1).upper(), mesaj)
            data["mesaj"] = mesaj
            

            
            # Stabilim flag urgent
            tip = data.get("tip_mesaj")
            min_zile = data.get("minim_zile_asteptare")
            urgent = False
            if (tip in ["review", "cerere"] and min_zile == 4) or (tip in ["intrebare", "cerere"] and min_zile == 2):
                urgent = True
            data["urgent"] = urgent
            
            # Adauga informatii despre utilizator
            ip = request.META.get("REMOTE_ADDR", "unknown")
            data["ip_utilizator"] = ip
            data["data_ora_trimitere"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Nu salva confirmare_email
            if "confirmare_email" in data:
                del data["confirmare_email"]
            
            # --- Salvare JSON ---
            folder = os.path.join(settings.BASE_DIR, "site_telefonie", "Mesaje")
            os.makedirs(folder, exist_ok=True)
            timestamp = int(time.time())
            filename = f"mesaj_{timestamp}"
            if urgent:
                filename += "_urgent"
            filename += ".json"
            filepath = os.path.join(folder, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            mesaj_trim = True
            mesaj_salvat = True
            mesaj_path = filepath
    else:
        form = ContactForm()
    
    return render(request, 'site_telefonie/contact.html', {
        'form': form,
        'mesaj_trim': mesaj_trim,
        'mesaj_salvat': mesaj_salvat,
        'mesaj_path': mesaj_path
    })


def adauga_produs(request):


    if not request.user.has_perm("site_telefonie.add_produs"):
        return eroare_403_view(
            request,
            titlu="Eroare adaugare produse",
            mesaj="Nu ai voie sa adaugi produse"  
        )
    Accesare(get_client_ip(request), request.build_absolute_uri())
    tip_produs = request.GET.get('tip')  # luam tipul din URL sau din select
    form = None

    if request.method == "POST":
        tip_produs = request.POST.get('tip_produs')
        if tip_produs == 'serviciu':
            form = ServiciuForm(request.POST, request.FILES)
        elif tip_produs == 'telefon':
            form = TelefonForm(request.POST, request.FILES)


        if form and form.is_valid():

            telfon_nou=form.save(commit=False)

            pret_calculat=form.cleaned_data.get('pret_calculat')

            if pret_calculat is not None:
                telfon_nou.pret = pret_calculat

            form.save()
            messages.success(request, "Produsul a fost adăugat cu succes!")
            return redirect('pagina_succes')  # redirect dupa salvare
    else:
        # GET: cream un formular gol pentru tipul selectat
        if tip_produs == 'serviciu':
            form = ServiciuForm()
        elif tip_produs == 'telefon':
            form = TelefonForm()

    return render(request, 'site_telefonie/adauga_produs.html', {
        'form': form,
        'tip_produs': tip_produs
    })


def pagina_succes(request):

    # Aceasta pagina ar putea afisa un mesaj de confirmare
    context = {
        'mesaj': 'Produsul a fost adăugat cu succes!'
    }
    return render(request, 'site_telefonie/pagina_succes.html', context)

from django.core.mail import mail_admins # <--- IMPORT OBLIGATORIU

def pagina_inregistrare(request):
    if request.method == "POST":
        
        # 1. Luam datele brute din request, inainte de validarea formularului
        username_ales = request.POST.get('username', '').strip().lower()
        email_folosit = request.POST.get('email', 'Nespecificat')

        # 2. Verificam daca userul vrea sa fie "admin"
        if username_ales == 'admin':
            subiect = "cineva incearca sa ne preia site-ul"
            mesaj_text = f"Tentativă de înregistrare cu user 'admin'.\nEmail atacator: {email_folosit}"
            
            mesaj_html = f"""
                <h1 style="color: red;">{subiect}</h1>
                <p>O persoană a încercat să își facă cont cu numele interzis <strong>admin</strong>.</p>
                <p>Adresa de e-mail folosită: <strong>{email_folosit}</strong></p>
            """
            
            # 3. Trimitem mail catre administratorii din settings.py
            mail_admins(
                subject=subiect,
                message=mesaj_text,
                html_message=mesaj_html
            )
            
            # Reafisam formularul cu datele introduse, dar cu o eroare manuala
            form = CreareUtilizatorForm(request.POST)
            return render(request, 'site_telefonie/pagina_inregistrare.html', {
                'form': form,
                'eroare_custom': 'Nu aveți permisiunea să folosiți username-ul "admin"!'
            })

        form = CreareUtilizatorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_confirmat = False
            user.cod = str(uuid.uuid4())

            
            user.save()
            

            
            subject = 'Confirmare înregistrare cont'
            link_confirmare = request.build_absolute_uri(f"/confirmare_email/{user.cod}/")
            
            mesaj_html = render_to_string('site_telefonie/email_confirmare.html', {
                'nume': user.last_name,
                'prenume': user.first_name,
                'username': user.username,
                'link_confirmare': link_confirmare
            })
            mesaj_text = strip_tags(mesaj_html)
            
            send_mail(
                subject,
                mesaj_text,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=mesaj_html,
                fail_silently=False,
            )

            return render(request, 'site_telefonie/confirmare_inregistrare.html') 
    else:
        form = CreareUtilizatorForm()
    
    return render(request, 'site_telefonie/pagina_inregistrare.html', {'form': form})
def confirmare_email(request, cod):
    try:
        user = CreareUtilizatorForm.Meta.model.objects.get(cod=cod)
        user.email_confirmat = True
        user.cod=None
        user.save()
        mesaj = "Emailul a fost confirmat cu succes! Acum vă puteți autentifica."
    except CreareUtilizatorForm.Meta.model.DoesNotExist:
        messages.error(request, "Codul de confirmare este invalid sau a expirat.")
    return render(request, 'site_telefonie/mail_confirmat.html', {'mesaj': mesaj})

import django.utils.timezone as timezone

mail_admins('Test direct', 'Daca vezi asta, setarile sunt bune!')



def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            print("DEBUG: Login REUSIT. Stergem istoricul de erori.")
            if 'login_failed_attempts' in request.session:
                messages.warning(request, "Autentificare eșuată. Verifică datele și încearcă din nou.")
                del request.session['login_failed_attempts']

            user = form.get_user()

            #  1) verificare BLOCAT (inainte de login)
            if getattr(user, "blocat", False):
                messages.error(request, "Ți-a fost contul blocat. Contactează un administrator.")
                return render(request, 'site_telefonie/login.html', {'form': form})

            # 2) verificare email confirmat (cum aveai)
            if not user.email_confirmat:
                return render(request, 'site_telefonie/login.html', {
                    'form': form,
                    'eroare': 'Confirmă emailul!'
                })

            # 3) login efectiv
            login(request, user)
            messages.success(request, f"Bun venit, {user.username}! Te-ai autentificat cu succes.")


            if not form.cleaned_data.get('ramane_logat'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(24 * 60 * 60)

            return redirect('profil_utilizator')

        else:
            print("DEBUG: Login ESUAT. Incepem numaratoarea...")
            

            username_incercat = request.POST.get('username', 'Necunoscut')
            ip_adresa = get_client_ip(request)
            acum = timezone.now().timestamp()

            attempts = request.session.get('login_failed_attempts', [])
            print(f"DEBUG: Lista inainte de curatare: {attempts}")

            attempts = [t for t in attempts if acum - t < 120]
            attempts.append(acum)
            if settings.DEBUG:
                messages.debug(request, f"Login eșuat pentru '{username_incercat}' de la IP {ip_adresa}. Încercări în 2 min: {len(attempts)}")

            print(f"DEBUG: Lista dupa adaugare: {attempts}")
            print(f"DEBUG: Numar incercari curente: {len(attempts)}")

            if len(attempts) >= 3:
                print("DEBUG: !!! ALERTA !!! S-a atins pragul de 3. Trimit mail...")

                subiect = "Logari suspecte"
                mesaj_text = f"User: {username_incercat}, IP: {ip_adresa}"
                mesaj_html = f"<h1 style='color:red;'>{subiect}</h1><p>User: {username_incercat}</p>"

                try:
                    mail_admins(subject=subiect, message=mesaj_text, html_message=mesaj_html)
                    print("DEBUG: Mail trimis cu succes.")
                except Exception as e:
                    print(f"DEBUG: Eroare la trimiterea mailului: {e}")

                attempts = []

            request.session['login_failed_attempts'] = attempts
            request.session.modified = True

    else:
        form = CustomLoginForm()

    return render(request, 'site_telefonie/login.html', {'form': form})

def profil_utilizator(request):
    if request.user.is_authenticated:
        return render(request, 'site_telefonie/profil.html')
    else:
        return redirect('login')
    
def logout_view(request):
    logout(request)
    messages.info(request, "Te-ai delogat.")
    return redirect('index')

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def schimbare_parola(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Parola a fost actualizata')
            return redirect('profil_utilizator')
        else:
            messages.error(request, 'Exista erori.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'site_telefonie/schimbare_parola.html', {'form': form})

import traceback

def detalii_pachet(request, pk):
    pachet_ales = get_object_or_404(Pachet, id_pachet=pk)
    Accesare(get_client_ip(request), request.build_absolute_uri())
    if request.user.is_authenticated:
        N = 5
        vizualizari_user = Vizualizare.objects.filter(user=request.user).order_by('data')
        if vizualizari_user.count() >= N:
            cea_mai_veche = vizualizari_user.first()
            cea_mai_veche.delete()
        Vizualizare.objects.create(user=request.user, pachet=pachet_ales)
    context = {
        'pachet': pachet_ales,
        'produse_incluse': pachet_ales.contine.all(),
        'categorii': CategoriePachet.objects.all()
    }
    messages.debug(request, f"Template-ul randează pachetul cu ID: {pk}")
    return render(request, 'site_telefonie/detalii_pachet.html', context)

from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
# Importeaza modelele tale
from .models import Promotie, Vizualizare, Pachet, CategoriePachet

def creare_promotie(request):
    categorii = CategoriePachet.objects.all()
    if request.method == 'POST':
        form = CrearePromotieForm(request.POST)
        if form.is_valid():
            promotie_noua = form.save(commit=False)
            promotie_noua.save()
            form.save_m2m()  # salveaza relatia ManyToMany
            K = 3  # pragul de vizualizari
            lista_mesaje = []
            for categorie in form.cleaned_data['categorii']:
                # selecteaza utilizatorii cu minim K vizualizari la pachete din aceasta categorie
                useri_eligibili = set()
                for user in get_user_model().objects.all():
                    nr_viz = Vizualizare.objects.filter(
                        user=user,
                        pachet__apartine=categorie
                    ).count()
                    if nr_viz >= K:
                        useri_eligibili.add(user)
                # alegem template-ul potrivit pentru categorie
                if categorie.nume_categorie == 'Business':
                    template_mail = 'emails/promo_alt.txt'
                else:
                    template_mail = 'emails/promo.txt'
                for user in useri_eligibili:
                    txt_mail = render_to_string(template_mail, {
                        'nume_categorie': categorie.nume_categorie,
                        'subiect': form.cleaned_data['subiect_email'],
                        'mesaj': form.cleaned_data['mesaj_email'],
                        'discount': form.cleaned_data['discount'],
                        'data_expirare': form.cleaned_data['data_sfarsit']
                    })
                    lista_mesaje.append((form.cleaned_data['subiect_email'], txt_mail, None, [user.email]))
            if lista_mesaje:
                send_mass_mail(tuple(lista_mesaje), fail_silently=False)
            return render(request, 'site_telefonie/promotie_succes.html')
    else:
        form = CrearePromotieForm()
    return render(request, 'site_telefonie/creare_promotie.html', {'form': form, 'categorii': categorii})


import traceback
from django.core.mail import mail_admins


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


from django.http import HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

def eroare_403_view(request, mesaj="Nu aveți acces la această resursă", titlu=""):
    current_user_key = request.user.pk if request.user.is_authenticated else None
    last_user_key = request.session.get("last_user_key")

    # daca s-a schimbat userul (anonim -> logat, logat -> alt user, logat -> anonim) resetam
    if last_user_key != current_user_key:
        request.session["nr_403"] = 0
        request.session["last_user_key"] = current_user_key

    request.session["nr_403"] = request.session.get("nr_403", 0) + 1

    context = {
        "titlu": titlu,
        "mesaj_personalizat": mesaj,
        "nr_403": request.session["nr_403"],
        "N_MAX_403": settings.N_MAX_403,
    }
    return render(request, "site_telefonie/403.html", context, status=403)


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import Permission
from django.views.decorators.csrf import csrf_exempt

@login_required
def claim_oferta(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    perm = Permission.objects.get(codename="vizualizeaza_oferta")
    request.user.user_permissions.add(perm)
    return redirect("oferta_speciala")

def oferta_view(request):
    if not request.user.has_perm("site_telefonie.vizualizeaza_oferta"):
        return eroare_403_view(
            request,
            titlu="Eroare afisare oferta",
            mesaj="Nu ai voie să vizualizezi oferta"
        )

    return render(request, "site_telefonie/oferta.html")

@login_required
def logout_custom(request):
    # stergem permisiunea (daca exista)
    try:
        perm = Permission.objects.get(codename="vizualizeaza_oferta")
        request.user.user_permissions.remove(perm)
    except Permission.DoesNotExist:
        pass

    logout(request)  # logout real
    return redirect("login")