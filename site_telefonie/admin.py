from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produs, Serviciu, Telefon, Pachet, CategoriePachet, Promotie

#admin.site.register(Produs)
admin.site.register(Serviciu)
admin.site.register(Telefon)
#admin.site.register(Pachet)
admin.site.register(CategoriePachet)
admin.site.register(Promotie)

class CategoriePachetAdmin(admin.ModelAdmin):
    list_display = ('nume_categorie', 'icon')

class PachetAdmin(admin.ModelAdmin):
    list_per_page=5
    list_display = ('id_pachet', 'nume_pachet', 'descriere_pachet', 'tip', 'cod_promo', 'data_crearii')  # afiseaza campurile in lista de obiecte
    list_filter = ('cod_promo', 'tip')  # adauga filtre laterale
    search_fields = ('nume_pachet', 'tip')  # permite cautarea dupa anumite campuri
    empty_value_display = 'nul' # se va afisa cuvantul 'nul' pentru campurile fara valori
    ordering = ['nume_pachet'] # crescator pentru titlu; dar autorii aceleiasi carti in ordine descrescatoare
    list_per_page = 10 # numarul de inregistrari afisate pe pagina
    fieldsets = (
        ('Informatii principale', {   # sectiune vizibila mereu
            'fields': ('nume_pachet', 'tip', 'apartine', 'contine')
        }),
        ('Optional / Avansat', {      # sectiune colapsabila
            'classes': ('collapse',),  # face sectiunea colapsabila
            'fields': ('descriere_pachet', 'cod_promo', 'promotie'),
        }),
    )
    filter_horizontal = ('contine',)  # sau filter_vertical = ('contine',)


class ProdusAdmin(admin.ModelAdmin):
    list_per_page=5
admin.site.register(Produs, ProdusAdmin)
admin.site.register(Pachet, PachetAdmin)


# Titlul din bara de sus
admin.site.site_header = "Panou administrare"

# Titlul din tab-ul browserului
admin.site.site_title = "Administrare "

# Titlul paginii principale a admin
admin.site.index_title = "Bine ai venit în panoul de administrare"



from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UtilizatorPersonalizat

@admin.register(UtilizatorPersonalizat)
class UtilizatorPersonalizatAdmin(UserAdmin):
    model = UtilizatorPersonalizat

    list_display = ("username", "email", "email_confirmat", "is_staff", "is_active")
    search_fields = ("username", "email", "telefon", "cnp")
    ordering = ("username",)

    # AICI apar campurile suplimentare dupa ce am salvat userul (pagina de editare)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Informații personale"), {"fields": ("first_name", "last_name", "email")}),
        (_("Date adiționale"), {"fields": (
            "data_nasterii",
            "adresa",
            "telefon",
            "judet",
            "nr_card_implicit",
            "cnp",
            "cod",
            "email_confirmat",
        )}),
        (_("Permisiuni"), {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "blocat",
            "groups",
            "user_permissions",
        )}),
        (_("Date importante"), {"fields": ("last_login", "date_joined")}),
    )

    # AICI (pagina de creare) punem DOAR username + parole,
    # ca sa NU apara campurile suplimentare inainte de Save.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2"),
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        # superuser -> nimic special
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)

        # moderator -> doar anumite campuri editabile
        is_moderator = request.user.groups.filter(name="Moderatori").exists()
        if is_moderator:
            allowed = {"first_name", "last_name", "email", "blocat"}

            # colectam toate campurile din fieldsets
            all_fields = set()
            for _, opts in self.fieldsets:
                all_fields.update(opts.get("fields", ()))

            # readonly = tot minus allowed
            return tuple(sorted(all_fields - allowed))

        return super().get_readonly_fields(request, obj)