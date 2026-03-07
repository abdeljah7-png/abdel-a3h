from django.contrib import admin, messages
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import Facture, LigneFacture
from django.db.models import Max


# ===============================
# INLINE LIGNES FACTURE
# ===============================
class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1
    

# ===============================
# ADMIN FACTURE
# ===============================
@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):

    inlines = [LigneFactureInline]

    list_display = (
        "numero",
        "client",
        "date",
        "total_ttc",
        "statut_colore",
        "bouton_valider",
        "bouton_pdf",
        "bouton_xml",
        "bouton_email",
    )

    fields = (
        "numero",
        "client",
        "mf_client",
        "adresse_client",
        "telephone_client",
        "email_client",
        "statut",
    )

    readonly_fields = (
        "numero",
        "mf_client",
        "adresse_client",
        "telephone_client",
        "email_client",
    )

    # ===============================
    # TOTAL DYNAMIQUE
    # ===============================
    def total_ttc(self, obj):
        totaux = obj.calculer_totaux()
        if totaux and totaux["total_ttc"] is not None:
            return f"{totaux['total_ttc']:.3f} TND"
        return "0.000 TND"

    total_ttc.short_description = "Total TTC"

    # ===============================
    # STATUT COULEUR
    # ===============================
    def statut_colore(self, obj):
        couleurs = {
            "brouillon": "gray",
            "validee": "green",
            "payee": "blue",
        }
        return format_html(
            '<b style="color:{}">{}</b>',
            couleurs.get(obj.statut, "black"),
            obj.get_statut_display()
        )

    statut_colore.short_description = "Statut"

    # ===============================
    # BOUTONS
    # ===============================
    def bouton_valider(self, obj):
        if obj.statut == "validee":
            return "✔ Validée"

        url = reverse("admin:valider_facture", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" '
            'style="background:#28a745;color:white;padding:4px 8px;border-radius:4px;">'
            'Valider</a>', url
        )

    bouton_valider.short_description = "Valider"

    def bouton_pdf(self, obj):
        url = reverse("facture_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background:#007bff;color:white;padding:4px 8px;border-radius:4px;">'
            'PDF</a>', url
        )

    bouton_pdf.short_description = "PDF"

    def bouton_xml(self, obj):
        url = reverse("facture_xml", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background:#6f42c1;color:white;padding:4px 8px;border-radius:4px;">'
            'XML</a>', url
        )

    bouton_xml.short_description = "XML"

    def bouton_email(self, obj):
        url = reverse("envoyer_facture", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" '
            'style="background:#fd7e14;color:white;padding:4px 8px;border-radius:4px;">'
            'Email</a>', url
        )

    bouton_email.short_description = "Email"

    # ===============================
    # URL VALIDATION
    # ===============================
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "valider/<int:facture_id>/",
                self.admin_site.admin_view(self.valider_view),
                name="valider_facture",
            ),
        ]
        return custom + urls

    def valider_view(self, request, facture_id):
        facture = Facture.objects.get(id=facture_id)
        facture.valider()
        self.message_user(request, "Facture validée ✔", messages.SUCCESS)
        return redirect("/admin/ventes/facture/")

    class Media:
        js = ("admin/js/client_auto.js",)


# ===============================
# ADMIN LIGNE FACTURE
# ===============================
@admin.register(LigneFacture)
class LigneFactureAdmin(admin.ModelAdmin):
    list_display = ("facture", "produit", "taux_rem", "quantite", "prix_ht", "taux_tva")