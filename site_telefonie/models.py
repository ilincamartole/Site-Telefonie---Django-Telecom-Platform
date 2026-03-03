from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser,Group, Permission
from datetime import date
from django.conf import settings


class Produs(models.Model):
    """Model părinte pentru toate produsele (servicii și telefoane)"""
    id_produs = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=200)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    


    class Meta:
        verbose_name_plural = "Produse"
        permissions = [
            ("vizualizeaza_oferta", "Poate vizualiza oferta speciala (banner 50%)"),]

    def __str__(self):
        return self.nume


class Serviciu(Produs):
    """Model pentru servicii (telefonie, internet, cablu, etc.)"""
    id_serviciu = models.AutoField(primary_key=True)
    descriere_serviciu = models.TextField()
    imagine = models.ImageField(upload_to='servicii/', null=True, blank=True)
    # Camp cu choices
    tip = models.CharField(max_length=50, choices=[
        ('telefonie', 'Telefonie mobila'),
        ('internet', 'Internet fibră optică'),
        ('cablu', 'TV Cablu'),
    ])
    # Camp cu choices și valoare default
    status = models.CharField(max_length=20, choices=[
        ('activ', 'Activ'),
        ('inactiv', 'Inactiv'),
    ], default='activ')
    # Camp cu valoare default
    taxa_activare = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Servicii"

    def __str__(self):
        return f"{self.nume} - {self.tip}"


class Telefon(Produs):
    """Model pentru telefoane"""
    id_telefon = models.AutoField(primary_key=True)
    descriere_telefon = models.TextField()
    imagine = models.ImageField(upload_to='telefoane/', null=True, blank=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    # Camp cu valoare default
    stoc = models.IntegerField(default=0)
    # Camp cu choices și valoare default
    cg_status = models.CharField(max_length=20, choices=[
        ('disponibil', 'Disponibil'),
        ('indisponibil', 'Indisponibil'),
        ('comanda', 'La comandă'),
    ], default='disponibil')
    # Camp unic (altul decât id)
    cod_imei = models.CharField(max_length=15, unique=True, 
                                 help_text="Cod IMEI unic pentru telefon")

    class Meta:
        verbose_name_plural = "Telefoane"

    def __str__(self):
        return f"{self.brand} {self.model}"


class CategoriePachet(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    # Camp unic
    nume_categorie = models.CharField(max_length=100, unique=True)
    descriere_categorie = models.TextField(null=True, blank=True)
    durata_minima = models.IntegerField(help_text="Durata minimă în luni")
    icon = models.CharField(max_length=50, blank=True, help_text="fa-solid fa-wifi")

    class Meta:
        verbose_name_plural = "Categorii Pachete"

    def __str__(self):
        return self.nume_categorie
    



class Promotie(models.Model):
    id_promotie = models.AutoField(primary_key=True)
    
    # nume promotie
    nume = models.CharField(max_length=100, default="Promotie Generica") 
    
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Procent discount (ex: 15.00 pentru 15%)"
    )
    
    data_inceput = models.DateField(default=timezone.now) # Echivalent data_creare
    data_sfarsit = models.DateField(null=True, blank=True) # Echivalent data_expirare
    
    # descriere
    descriere_promotie = models.TextField(
        null=True, blank=True,
        help_text="Descriere internă a promoției"
    )


    # mailuri
    subiect_email = models.CharField(max_length=255, null=True, blank=True, help_text="Subiectul care apare în mail")
    mesaj_email = models.TextField(null=True, blank=True, help_text="Mesajul trimis clienților")


    categorii = models.ManyToManyField(
        CategoriePachet,
        related_name='promotii',
        help_text='Categorii pentru care se aplică promoția'
    )

    class Meta:
        verbose_name_plural = "Promoții"

    def __str__(self):
        return f"{self.nume} ({self.discount}%)"

class Pachet(models.Model):
    """Model pentru pachete de servicii și produse"""
    id_pachet = models.AutoField(primary_key=True)
    
    nume_pachet = models.CharField(max_length=200)
    descriere_pachet = models.TextField(null=True, blank=True)
    data_crearii = models.DateTimeField(auto_now_add=True)
    tip = models.CharField(max_length=50)
    cod_promo = models.CharField(max_length=50, null=True, blank=True, 
                                 help_text="Cod promoțional opțional")
    
    # Relatii
    contine = models.ManyToManyField(
        Produs, 
        related_name='pachete',
        help_text="Produse incluse în pachet (servicii și telefoane)"
    )

   
    apartine = models.ForeignKey(
        CategoriePachet,
        on_delete=models.CASCADE,
        related_name='pachete'
    )
    
    promotie = models.ForeignKey(
        Promotie,
        on_delete=models.SET_NULL,  #daca promotia e stearsa, pachetul ramane
        null=True,
        blank=True,
        related_name='pachete',
        help_text="Promoție aplicată pachetului (opțional)"
    )

    class Meta:
        verbose_name_plural = "Pachete"

    def __str__(self):
        return self.nume_pachet



# Validator pentru varsta minima - MINIM 18 ANI
def validate_min_age(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Utilizatorul trebuie să aibă minim 18 ani.')



JUDETE_CHOICES = [
    ('AB', 'Alba'),
    ('AR', 'Arad'),
    ('AG', 'Argeș'),
    ('BC', 'Bacău'),
    ('BH', 'Bihor'),
    ('BN', 'Bistrița-Năsăud'),
    ('BT', 'Botoșani'),
    ('BV', 'Brașov'),
    ('BR', 'Brăila'),
    ('B', 'București'), # Capitala, inclusa frecvent in liste
    ('BZ', 'Buzău'),
    ('CS', 'Caraș-Severin'),
    ('CL', 'Călărași'),
    ('CJ', 'Cluj'),
    ('CT', 'Constanța'),
    ('CV', 'Covasna'),
    ('DB', 'Dâmbovița'),
    ('DJ', 'Dolj'),
    ('GL', 'Galați'),
    ('GR', 'Giurgiu'),
    ('GJ', 'Gorj'),
    ('HR', 'Harghita'),
    ('HD', 'Hunedoara'),
    ('IL', 'Ialomița'),
    ('IS', 'Iași'),
    ('IF', 'Ilfov'),
    ('MM', 'Maramureș'),
    ('MH', 'Mehedinți'),
    ('MS', 'Mureș'),
    ('NT', 'Neamț'),
    ('OT', 'Olt'),
    ('PH', 'Prahova'),
    ('SM', 'Satu Mare'),
    ('SJ', 'Sălaj'),
    ('SB', 'Sibiu'),
    ('SV', 'Suceava'),
    ('TR', 'Teleorman'),
    ('TM', 'Timiș'),
    ('TL', 'Tulcea'),
    ('VS', 'Vaslui'),
    ('VL', 'Vâlcea'),
    ('VN', 'Vrancea'),
]



class UtilizatorPersonalizat(AbstractUser):
    # Campurile suplimentare solicitate (5 obligatorii + CNP extra)
    blocat = models.BooleanField(default=False, verbose_name="Blocat")
    # 1. Data Nasterii (Validare 1: Varsta)
    data_nasterii = models.DateField(
        validators=[validate_min_age],
        null=True, blank=True,
    )

    # 2. Adresa
    adresa = models.CharField(
        max_length=255,
        verbose_name="Adresă"
    )
    
    # 3. Numar de telefon (Validare 2: 10 cifre)
    telefon = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Numărul de telefon trebuie să conțină 10 cifre.')],
        verbose_name="Număr de Telefon"
    )

    # 4. Judet
    judet = models.CharField(
        max_length=50,
        choices=JUDETE_CHOICES,
        verbose_name="Județ"
    )
    
    # 5. Numar implicit de card (Validare 3: 16 cifre)
    nr_card_implicit = models.CharField(
        max_length=16,
        blank=True,
        null=True, # Permitem sa fie lasat gol
        validators=[RegexValidator(r'^\d{16}$', 'Numarul de card trebuie sa contina 16 cifre.')],
        verbose_name="Numar Card Implicit (16 cifre)"
    )

    # 6. CNP (Camp suplimentar)
    cnp = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Cod Numeric Personal"
    )

    cod=models.CharField(max_length=100, blank=True, null=True)
    email_confirmat=models.BooleanField(default=False)
    

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('Grupuri la care aparține utilizatorul.'),
        related_name="custom_user_groups", # Nume unic
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Permisiuni specifice pentru acest utilizator.'),
        related_name="custom_user_permissions", # Nume unic
        related_query_name="custom_user_permission",
    )

    class Meta:
        verbose_name = "Utilizator Personalizat"
        verbose_name_plural = "Utilizatori Personalizați"

    def __str__(self):
        return self.username
    



class Vizualizare(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pachet = models.ForeignKey(Pachet, on_delete=models.CASCADE) 
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data'] # ordonam cronologic