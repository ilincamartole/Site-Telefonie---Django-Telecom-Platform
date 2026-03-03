# site_telefonie/forms.py
from django import forms
from .models import Produs, CategoriePachet
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.core.validators import RegexValidator
from decimal import Decimal
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UtilizatorPersonalizat

TIPURI = [
    ('serviciu', 'Serviciu'),
    ('telefon', 'Telefon')
]

class FiltruProduseForm(forms.Form):
    nume = forms.CharField(
        label="Nume",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nume produs'}))

    pret_min = forms.DecimalField(
        label="Preț minim",
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={'placeholder': 'Minim', 'type': 'number', 'step': '0.01'}),
        error_messages={'min_value': 'Prețul minim nu poate fi negativ!'}
    )
    pret_max = forms.DecimalField(
        label="Preț maxim",
        required=False,
        min_value=0,
        widget=forms.TextInput(attrs={'placeholder': 'Maxim', 'type': 'number', 'step': '0.01'}),
        error_messages={'min_value': 'Prețul maxim nu poate fi negativ!'}
    )
    tip = forms.ChoiceField(
        label="Tip produs",
        required=False,
        choices=[('', 'Toate')] + TIPURI,
        widget=forms.Select()
    )
    items_per_page = forms.IntegerField(
        label="Produse pe pagină",
        required=False,
        min_value=1,
        max_value=100,
        initial=5,
        widget=forms.TextInput(attrs={'placeholder': 'Număr de produse pe pagină', 'type': 'number'}),
        error_messages={
            'min_value': 'Trebuie să afișați cel puțin 1 produs!',
            'max_value': 'Nu puteți afișa mai mult de 100 produse pe pagină!'
        }
    )


    # Validare nume
    def clean_nume(self):
        nume = self.cleaned_data.get('nume')
        if nume:  # daca utilizatorul a introdus ceva
            if len(nume.strip()) < 3:
                raise forms.ValidationError("Numele produsului trebuie să aibă minim 3 caractere!")
        return nume

    # Validare pret_max vs pret_min
    def clean(self):
        cleaned_data = super().clean()
        pret_min = cleaned_data.get('pret_min')
        pret_max = cleaned_data.get('pret_max')

        if pret_min is not None and pret_max is not None:
            if pret_max < pret_min:
                raise forms.ValidationError("Prețul maxim nu poate fi mai mic decât prețul minim!")


from django import forms
from .models import CategoriePachet, Pachet

class FiltruPacheteForm(forms.Form):
    nume_pachet = forms.CharField(required=False, label="Nume pachet")
    categorie = forms.ModelChoiceField(
        queryset=CategoriePachet.objects.all(),
        required=False,
        label="Categorie"
    )
    items_per_page = forms.IntegerField(
        label="Produse pe pagină",
        required=False,
        min_value=1,
        max_value=100,
        initial=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Număr de produse pe pagină'}),
        error_messages={
            'min_value': 'Trebuie să afișați cel puțin 1 produs!',
            'max_value': 'Nu puteți afișa mai mult de 100 produse pe pagină!'
        }
    )
    pret_min = forms.DecimalField(required=False, min_value=0, label="Preț minim")
    pret_max = forms.DecimalField(required=False, min_value=0, label="Preț maxim")

    def clean(self):
        cleaned = super().clean()
        categorie = cleaned.get("categorie")
        preset = self.initial.get("categorie")

        # Validare suplimentară: comparăm id-urile, nu obiectele direct
        if preset and categorie:
            if hasattr(categorie, 'id_categorie') and hasattr(preset, 'id_categorie'):
                if categorie.id_categorie != preset.id_categorie:
                    raise forms.ValidationError(
                        "Categoria nu poate fi modificată în pagina unei categorii."
                    )
            else:
                # fallback pentru cazuri rare
                if str(categorie) != str(preset):
                    raise forms.ValidationError(
                        "Categoria nu poate fi modificată în pagina unei categorii."
                    )
        elif preset and not categorie:
            # Dacă preset există dar nu s-a trimis categorie, forțăm eroare
            raise forms.ValidationError(
                "Categoria nu poate fi modificată în pagina unei categorii."
            )

        return cleaned


from django import forms
from django.core.exceptions import ValidationError
import datetime


TIPURI_MESAJ = [
    ('', 'Neselectat'),
    ('reclamatie', 'Reclamație'),
    ('intrebare', 'Întrebare'),
    ('review', 'Review'),
    ('cerere', 'Cerere'),
    ('programare', 'Programare')
]

#  Validatori personalizati 
from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime

TIPURI_MESAJ = [
    ('', 'Neselectat'),
    ('reclamatie', 'Reclamație'),
    ('intrebare', 'Întrebare'),
    ('review', 'Review'),
    ('cerere', 'Cerere'),
    ('programare', 'Programare'),
]

def validate_major(data_nasterii):
    if (date.today() - data_nasterii).days < 18 * 365:
        raise ValidationError("Trebuie să fiți major pentru a trimite mesaj.")

def validate_cnp(cnp, data_nasterii):
    if not cnp.isdigit():
        raise ValidationError("CNP-ul trebuie să conțină doar cifre.")
    if not cnp.startswith(('1','2', '5','6')):
        raise ValidationError("CNP-ul trebuie să înceapă cu 1 sau 2.")
    # verificam daca urmatoarele 6 cifre formeaza o data valida
    try:
        zi = int(cnp[5:7])
        luna = int(cnp[3:5])
        an = int(cnp[1:3])
        secol = 1900 if cnp[0] in '12' else 2000
        an_complet = secol + an
        from datetime import date
        if an != data_nasterii.year % 100:
            raise ValidationError("Anul din CNP nu corespunde cu data nașterii.")
        if luna != data_nasterii.month:
            raise ValidationError("Luna din CNP nu corespunde cu data nașterii.")
        if zi != data_nasterii.day:
            raise ValidationError("Ziua din CNP nu corespunde cu data nașterii.")
        azi = date.today()
        if an_complet > azi.year:
            raise ValidationError("Anul din CNP nu poate fi în viitor.")
        if not (1 <= luna <= 12):
            raise ValidationError("Luna din CNP trebuie să fie între 1 și 12.")
        if not (1 <= zi <= 31):
            raise ValidationError("Ziua din CNP trebuie să fie între 1 și 31.")
        if luna == 2 and zi > 28:
            raise ValidationError("Ziua din CNP nu poate fi mai mare de 28 pentru luna februarie.")
        # validare suplimentara pentru zilele din lunile cu 30 zile
        if luna in [4, 6, 9, 11] and zi > 30:
            raise ValidationError("Ziua din CNP nu poate fi mai mare de 30 pentru luna selectată.")
        from datetime import datetime
        datetime(year=an_complet, month=luna, day=zi)
    except ValueError:
        raise ValidationError("CNP-ul conține o dată invalidă.")

def validate_no_links(text):
    if "http://" in text or "https://" in text:
        raise ValidationError("Textul nu poate conține link-uri.")

def validate_message_words(text):
    words = re.findall(r"\b[0-9A-Za-zĂÂÎȘȚăâîșț]+\b", text)

    if not 5 <= len(words) <= 100:
        raise ValidationError("Mesajul trebuie să conțină între 5 și 100 de cuvinte.")

    for w in words:
        if len(w) > 15:
            raise ValidationError(
                f"Cuvântul '{w}' din mesaj este prea lung (max 15 caractere)."
            )
        

def clean_mesaj(self):
    mesaj = self.cleaned_data.get("mesaj", "")

    mesaj = re.sub(r'\s+', ' ', mesaj.strip())

    mesaj = re.sub(r'(?<=[\.\?\!]\s)([a-zăâîșț])', lambda m: m.group(1).upper(), mesaj)

    validate_message_words(mesaj)
    validate_text_django(mesaj)

    return mesaj

def validare_text(text, permite_gol=False):
    if permite_gol and text == "":
        return True
    if not text:
        return False
    if not text[0].isupper():
        return False
    if not re.fullmatch(r"[A-Za-z\- \.\?\!,]+", text):
        return False
    return True

def validate_text_django(value, permite_gol=False):
    if not validare_text(value, permite_gol=permite_gol):
        if permite_gol and value == "":
            return  # valid, prenume gol permis
        raise ValidationError(
            "Textul trebuie să înceapă cu literă mare și să conțină doar litere, spații sau cratime."
        )
    


def validate_capitalized(value):

    if not value:  # daca e gol, nu validam aici (in cazul prenumelui)
        return

    # sparge dupa spatiu sau cratima
    parts = re.split(r"([\s-])", value)
    # parcurgem doar cuvintele de dupa separator
    for i in range(1, len(parts), 2):
        sep = parts[i]
        next_word = parts[i+1] if i+1 < len(parts) else ''
        if next_word and next_word[0].isalpha() and not next_word[0].isupper():
            raise ValidationError(
                "Fiecare cuvânt după spațiu sau cratimă trebuie să înceapă cu literă mare!"
            )
def validate_email_not_temporary(email):
    domeniu = email.split('@')[-1]
    if domeniu in ['guerillamail.com', 'yopmail.com']:
        raise ValidationError("Nu se acceptă emailuri temporare.")
    
def clean_tip_mesaj(self):
    tip = self.cleaned_data.get('tip_mesaj')
    if not tip or tip == '' or tip == 'neselectat':
        raise ValidationError('Trebuie să selectați un tip de mesaj!')
    return tip

class ContactForm(forms.Form):
    nume = forms.CharField(
        max_length=10,
        required=True,
        label="Nume",
        validators=[ validate_capitalized, validate_text_django]
    )
    prenume = forms.CharField(
        max_length=10,
        required=False,
        label="Prenume",
        validators=[validate_capitalized, lambda v :validate_text_django( v, permite_gol=True)]
    )
    cnp = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        label="CNP",
        validators=[validate_cnp]
    )
    data_nasterii = forms.DateField(
        required=True,
        label="Data nașterii",
        validators=[validate_major],
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        validators=[validate_email_not_temporary]
    )
    confirmare_email = forms.EmailField(
        required=True,
        label="Confirmare Email"
    )
    tip_mesaj = forms.ChoiceField(
        choices=TIPURI_MESAJ,
        required=True,
        label="Tip mesaj",
        error_messages={
            'required': 'Trebuie să selectați un tip de mesaj!'
        }
    )
    subiect = forms.CharField(
        max_length=100,
        required=True,
        label="Subiect",
        validators=[validate_no_links]
    )
    minim_zile_asteptare = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=30,
        label="Minim zile de așteptare",
        help_text="Pentru review-uri/cereri minim 4 zile, pentru cereri/întrebări minim 2 zile."
    )
    mesaj = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Mesaj (semnătură inclusă)",
        validators=[validate_message_words, validate_no_links,validate_text_django]
    )

    def clean_tip_mesaj(self):
        tip = self.cleaned_data.get('tip_mesaj')
        if not tip or tip == '' or tip == 'neselectat':
            raise ValidationError('Trebuie să selectați un tip de mesaj!')
        return tip
    
    def clean(self):
        cleaned = super().clean()
        if not cleaned:
            return cleaned  # iesim daca sunt deja erori pe campuri

        cnp = cleaned.get("cnp")
        data_nasterii = cleaned.get("data_nasterii")

        if cnp and data_nasterii:
            if cnp.startswith(('1','2')):
                yy = int(cnp[1:3])
                mm = int(cnp[3:5])
            dd = int(cnp[5:7])
            secol = 1900 if cnp[0]=='1' else 2000
            an = secol + yy
            try:
                data_cnp = date(an, mm, dd)
                if data_cnp != data_nasterii:
                    self.add_error("cnp", "CNP-ul nu corespunde cu data nașterii!")
            except ValueError:
                self.add_error("cnp", "CNP-ul conține o dată invalidă!")
        cleaned = super().clean()
        email = cleaned.get("email")
        confirm = cleaned.get("confirmare_email")
        tip = cleaned.get("tip_mesaj")
        nume = cleaned.get("nume")

        if email and confirm and email != confirm:
            self.add_error("confirmare_email", "Emailurile nu coincid!")

        tip = cleaned.get("tip_mesaj")
        if not tip or tip == '' or tip == 'neselectat':
            self.add_error("tip_mesaj", "Trebuie să selectați un tip de mesaj!")
        
       
        # verificam minim zile in functie de tip
        min_zile = cleaned.get("minim_zile_asteptare")
        if tip is None is None:
            return cleaned
        if tip in ['review', 'cerere'] and min_zile < 4:
            self.add_error("minim_zile_asteptare", "Pentru review-uri/cereri minim 4 zile!")
        if tip in ['intrebare', 'reclamatie'] and min_zile < 2:
            self.add_error("minim_zile_asteptare", "Pentru întrebări/reclamații minim 2 zile!")
       

        mesaj = cleaned.get("mesaj")
        nume = cleaned.get("nume", "")
        prenume = cleaned.get("prenume", "")

        if mesaj:
            semnatura = f"{prenume} {nume}".strip()  # daca prenume e gol, merge ok
            if not mesaj.rstrip().lower().endswith(semnatura.lower()):
                self.add_error(
                    "mesaj",
                f"Mesajul trebuie să se încheie cu semnătura ({semnatura})!"
            )




        
        return cleaned
    

from django import forms
from .models import Produs

# forms.py
from django import forms
from .models import Serviciu, Telefon

class ServiciuForm(forms.ModelForm):
    class Meta:
        model = Serviciu
        fields = ['nume', 'pret', 'descriere_serviciu', 'tip', 'status', 'taxa_activare', 'imagine']
        labels = {
            'nume': 'Numele serviciului',
            'pret': 'Prețul serviciului',
        }
        help_texts = {
            'nume': 'Introduceți numele serviciului',
        }



def validate_imei_format(value):
    imei_regex = r'^\d{15}$' 
    
    if not re.match(imei_regex, value):
            raise ValidationError(
            'Codul IMEI trebuie să fie format din exact 15 cifre numerice!',
            code='imei_format_invalid'
        )


def validate_majuscula(value):
    if not value:
        return
    if not value[0].isupper():
        raise ValidationError(
            'Primul caracter trebuie să fie literă mare!',
            code='first_char_not_upper'
        )
    
def validate_caractere_speciale(value):
    if re.search(r'[^\w\săîâșțĂÎÂȘȚ\.\,\!\?\-]', value):
        raise ValidationError(
            'Textul conține caractere speciale nepermise!',
            code='special_characters_not_allowed'
        )


class TelefonForm(forms.ModelForm):

    nume = forms.CharField(
        max_length=100,
        required=True,
        label="Nume telefon",
        validators=[validate_majuscula],
        error_messages={
            'required': 'Acest câmp este obligatoriu!' ,
            'max_length': 'Numele telefonului nu poate depăși 100 de caractere!',
            'validators': 'Numele trebuie să înceapă cu literă mare!'
        }
    )

    descriere_telefon = forms.CharField(
        widget=forms.Textarea,
        label="Descriere telefon",
        required=True,
        validators=[validate_caractere_speciale, validate_majuscula],
        error_messages={
            'required': 'Acest câmp este obligatoriu!',
            'validators': 'Descrierea trebuie să înceapă cu literă mare și să nu conțină caractere speciale nepermise!'
        }
    )
        

    cost_cumparare=forms.DecimalField(
        label="Cost de cumpărare",
        required=True,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        error_messages={
            'min_value': 'Costul de cumpărare nu poate fi negativ!'
,
'required': 'Acest câmp este obligatoriu!'
        }
    )

    marja_profit=forms.IntegerField(
        label="Marja de profit (%)",
        required=True,
        min_value=0,
        max_value=100,
        help_text="Introduceți marja de profit ca procent (0-100%)",
        error_messages={
            'min_value': 'Marja de profit nu poate fi negativă!',
            'max_value': 'Marja de profit nu poate depăși 100%!',
            'required': 'Acest câmp este obligatoriu!'
        }
    )

    cod_imei = forms.CharField(
        max_length=15,
        min_length=15,
        required=True,
        label="Cod IMEI",
        help_text="Introduceți codul IMEI format din 15 cifre.",
        validators=[
            validate_imei_format
        ],
        error_messages={
            'required': 'Acest câmp este obligatoriu!',
            'min_length': 'Codul IMEI trebuie să conțină exact 15 cifre.',
            'max_length': 'Codul IMEI trebuie să conțină exact 15 cifre'
        }
    )
    class Meta:
        model = Telefon
        fields = ['nume', 'descriere_telefon', 'brand', 'model', 'cod_imei', 'imagine']
        labels = {
            'nume': 'Numele telefonului',
            'descriere_telefon': 'Descrierea telefonului',
            'brand': 'Marca telefonului',
            'model': 'Modelul telefonului',
            'cod_imei': 'Codul IMEI al telefonului',


        }
        help_texts = {
            'nume': 'Introduceți numele telefonului',
        }

    def clean_cost_cumparare(self):
            cost= self.cleaned_data.get('cost_cumparare')
            if cost is not None and cost < 0:
                raise forms.ValidationError("Costul de cumpărare nu poate fi negativ!")
            return cost

    def clean_marja_profit(self):
            marja= self.cleaned_data.get('marja_profit')
            if marja is not None and marja%5 !=0:
                raise forms.ValidationError("Marja de profit trebuie să fie multiplu de 5!")
            return marja



    def clean(self):
            cleaned_data = super().clean()




            brand = cleaned_data.get('brand')
            model = cleaned_data.get('model')
            nume = cleaned_data.get('nume')

            if nume:
            # vedem daca exista deja un produs cu acelasi nume
                qs = Telefon.objects.filter(nume__exact=nume)
            # Excludem obiectul curent in cazul editarii
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)

                if qs.exists():
                # atasam eroarea
                    self.add_error('nume', 
                    forms.ValidationError("Un produs cu acest Nume de telefon este deja înregistrat.")
                )   
        
        # 3. Validare la nivel de formular (Marca + Modelul trebuie sa fie in Nume)
        # Ne asiguram ca toate campurile exista si nu sunt None
            if brand and model and nume:
            # Construim sirul de referinta si le punem lower() pentru comparatie case-insensitive
                nume_complet_asteptat = f"{brand} {model}".lower()
            
            if nume_complet_asteptat not in nume.lower():
                # Mesaj de eroare personalizat
                # Folosim add_error pentru a atasa eroarea campului 'nume'
                self.add_error('nume', 
                    forms.ValidationError(
                        f"Numele comercial trebuie să conțină atât marca, cât și modelul. Așteptat: '{brand} {model}'."
                    )
                )
            cost_cumparare = cleaned_data.get('cost_cumparare')
            marja_profit = cleaned_data.get('marja_profit')

            if cost_cumparare is not None and marja_profit is not None:
                pret_calculat = Decimal(cost_cumparare) * (Decimal(1) + Decimal(marja_profit) / 100)
                cleaned_data['pret_calculat'] = pret_calculat
#  cleaned_data['stoc'] = 10 if pret_calculat > 500 else 0

                cleaned_data['cg_status'] = 'disponibil' if cleaned_data.get('stoc', 0) > 0 else 'indisponibil'

            return cleaned_data



class CreareUtilizatorForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=UtilizatorPersonalizat

        fields=UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
            'data_nasterii',
            'adresa',
            'telefon',
            'judet',
            'cnp',
            'nr_card_implicit',
        )



        def clean(self):
        #  Obtine datele curatate de la formularul parinte
            cleaned_data = super().clean()
        
        #  Extrage datele relevante
            data_nasterii = cleaned_data.get('data_nasterii')
            telefon = cleaned_data.get('telefon')
            cnp = cleaned_data.get('cnp')
            nr_card = cleaned_data.get('nr_card_implicit')
        
            errors = {}

        # varsta minima
            if data_nasterii:
                today = date.today()
                age = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
                if age < 18:
                    errors['data_nasterii'] = ValidationError(
                    'Trebuie să ai minim 18 ani pentru a te înregistra.'
                )

        # nr tel
            if telefon:
                if not telefon.isdigit():
                    errors['telefon'] = ValidationError('Numărul de telefon trebuie să conțină doar cifre.')
                elif len(telefon) < 10 or len(telefon) > 15:
                    errors['telefon'] = ValidationError('Numărul de telefon trebuie să aibă între 10 și 15 cifre.')
        # NOTA: Daca campul e obligatoriu, adaugi o validare de 'required' aici.

        # cnp
            if cnp:
                if not cnp.isdigit() or len(cnp) != 13:
                    errors['cnp'] = ValidationError('CNP-ul trebuie să aibă exact 13 cifre.')
            
            # unicitate cnp
                    if UtilizatorPersonalizat.objects.filter(cnp=cnp).exclude(pk=self.instance.pk).exists():
                        errors['cnp'] = ValidationError('Un utilizator cu acest CNP există deja.')

        # nr card
            if nr_card:
            # curat spatii
                nr_card_curat = nr_card.replace(' ', '')
            
                if not nr_card_curat.isdigit() or len(nr_card_curat) != 16:
                    errors['nr_card_implicit'] = ValidationError('Numărul de card trebuie să fie format din 16 cifre.')

        # obligatoriu judet
            if not cleaned_data.get('judet'):
                errors['judet'] = ValidationError('Câmpul Județ este obligatoriu.')
        
        
        # trimit erori
            if errors:
                raise ValidationError(errors)

        
            return cleaned_data



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nume utilizator", max_length=150)
    password = forms.CharField(label="Parolă", widget=forms.PasswordInput)
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat timp de o zi'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data
    

class LoginFormBlocat(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if getattr(user, "blocat", False):
            raise ValidationError(
                "Contul tău a fost blocat.",
                code="blocked",
            )

from django import forms
from .models import Promotie, CategoriePachet

class CrearePromotieForm(forms.ModelForm):
    categorii = forms.ModelMultipleChoiceField(
        queryset=CategoriePachet.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Categorii pentru promoție",
        help_text="Selectați una sau mai multe categorii pentru promoție."
    )
    class Meta:
        model = Promotie
        fields = ['nume', 'subiect_email', 'mesaj_email', 'discount', 'data_sfarsit', 'categorii']
        labels = {
            'nume': 'Nume promoție',
            'subiect_email': 'Subiect email',
            'mesaj_email': 'Mesaj email',
            'discount': 'Discount (%)',
            'data_sfarsit': 'Data expirare',
        }
        help_texts = {
            'discount': 'Procent discount (ex: 15 pentru 15%)',
            'data_sfarsit': 'Data la care expiră promoția',
        }
