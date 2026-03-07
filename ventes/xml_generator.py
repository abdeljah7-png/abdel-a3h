from django.http import HttpResponse
import xml.etree.ElementTree as ET
from datetime import datetime


def generer_facture_xml(facture):

    totaux = facture.calculer_totaux()

    # ======================
    # ROOT
    # ======================
    root = ET.Element("Invoice")
    root.set("xmlns", "urn:tunisie:facture:electronique:1.0")
    root.set("generated", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    # ======================
    # IDENTIFICATION
    # ======================
    ET.SubElement(root, "InvoiceNumber").text = str(facture.numero)
    ET.SubElement(root, "IssueDate").text = facture.date.strftime("%Y-%m-%d")
    ET.SubElement(root, "Currency").text = "TND"

    # ======================
    # SUPPLIER (SOCIETE)
    # ======================
    supplier = ET.SubElement(root, "Supplier")

    ET.SubElement(supplier, "Name").text = "MA SOCIETE SARL"
    ET.SubElement(supplier, "TaxNumber").text = "1234567/A/B/C/000"
    ET.SubElement(supplier, "Country").text = "TN"

    # ======================
    # CUSTOMER
    # ======================
    customer = ET.SubElement(root, "Customer")

    ET.SubElement(customer, "Name").text = facture.client.nom
    ET.SubElement(customer, "TaxNumber").text = facture.mf_client or ""
    ET.SubElement(customer, "Address").text = facture.adresse_client or ""
    ET.SubElement(customer, "Phone").text = facture.telephone_client or ""
    ET.SubElement(customer, "Email").text = facture.email_client or ""

    # ======================
    # INVOICE LINES
    # ======================
    lines = ET.SubElement(root, "InvoiceLines")

    for ligne in facture.lignes.all():

        line = ET.SubElement(lines, "Line")

        montant_ht = ligne.quantite * ligne.prix_ht
        montant_tva = montant_ht * ligne.taux_tva / 100
        montant_ttc = montant_ht + montant_tva

        ET.SubElement(line, "ProductName").text = str(ligne.produit)
        ET.SubElement(line, "Quantity").text = str(ligne.quantite)
        ET.SubElement(line, "UnitPriceHT").text = f"{ligne.prix_ht:.3f}"
        ET.SubElement(line, "VATRate").text = f"{ligne.taux_tva}"
        ET.SubElement(line, "AmountHT").text = f"{montant_ht:.3f}"
        ET.SubElement(line, "AmountVAT").text = f"{montant_tva:.3f}"
        ET.SubElement(line, "AmountTTC").text = f"{montant_ttc:.3f}"

    # ======================
    # TOTALS
    # ======================
    totals = ET.SubElement(root, "Totals")

    ET.SubElement(totals, "TotalHT").text = f"{totaux['total_ht']:.3f}"
    ET.SubElement(totals, "TotalVAT").text = f"{totaux['total_tva']:.3f}"
    ET.SubElement(totals, "TotalTTC").text = f"{totaux['total_ttc']:.3f}"

    # ======================
    # LEGAL NOTE
    # ======================
    ET.SubElement(root, "LegalNotice").text = (
        "TVA appliquée conformément à la législation tunisienne en vigueur."
    )

    # ======================
    # GENERATION
    # ======================
    tree = ET.ElementTree(root)

    response = HttpResponse(content_type="application/xml")
    response["Content-Disposition"] = f'attachment; filename="facture_{facture.numero}.xml"'

    tree.write(response, encoding="utf-8", xml_declaration=True)

    return response