from django.contrib import admin
from .models import Produit

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "designation",
        "prix_ht",
        "taux_tva",
        "stock",
    )
    search_fields = (
        "reference",
        "designation",
    )
    list_filter = ("taux_tva",)
    ordering = ("designation",)