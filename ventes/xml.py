import xml.etree.ElementTree as ET
from django.shortcuts import get_object_or_404
from .models import Facture

def generer_xml_facture(facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    root = ET.Element("Facture")
    ET.SubElement(root, "Numero").text = facture.numero
    ET.SubElement(root, "Date").text = str(facture.date)
    ET.SubElement(root, "Client").text = facture.client.nom
    ET.SubElement(root, "TotalHT").text = str(facture.total_ht)
    ET.SubElement(root, "TVA").text = str(facture.total_tva)
    ET.SubElement(root, "TotalTTC").text = str(facture.total_ttc)

    lignes = ET.SubElement(root, "Lignes")

    for l in facture.lignes.all():
        ligne = ET.SubElement(lignes, "Ligne")
        ET.SubElement(ligne, "Produit").text = l.produit.designation
        ET.SubElement(ligne, "Quantite").text = str(l.quantite)
        ET.SubElement(ligne, "PrixHT").text = str(l.prix_ht)

    return ET.tostring(root, encoding="utf-8", method="xml")