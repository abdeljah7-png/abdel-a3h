# Create your views here.
from django.http import HttpResponse
from .xml import generer_xml_facture
from django.shortcuts import render
from django.http import HttpResponse
from .pdf import generer_facture_pdf
from django.shortcuts import get_object_or_404, redirect
from .email import envoyer_facture_email
from .models import Facture
from django.shortcuts import redirect
from django.contrib import messages
from .models import Facture
from django.http import JsonResponse
from .models import Produit
from .xml_generator import generer_facture_xml


def facture_xml(request, facture_id):
    from .models import Facture
    facture = Facture.objects.get(id=facture_id)
    return generer_facture_xml(facture)

def facture_pdf(request, facture_id):
    facture = Facture.objects.get(id=facture_id)
    return generer_facture_pdf(facture)



def facture_xml(request, facture_id):
    xml_data = generer_xml_facture(facture_id)
    response = HttpResponse(xml_data, content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename="facture.xml"'
    return response


def envoyer_facture(request, facture_id):
    facture = Facture.objects.get(id=facture_id)

    # ici tu peux ajouter envoi email réel plus tard
    messages.success(request, f"Facture {facture.numero} envoyée (simulation).")

    return redirect("/admin/ventes/facture/")

def produit_info(request, produit_id):
    produit = Produit.objects.get(id=produit_id)

    return JsonResponse({
        "prix_ht": float(produit.prix_ht),
        "taux_tva": float(produit.taux_tva),
    })