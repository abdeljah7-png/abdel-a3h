from django.core.mail import EmailMessage
from django.http import HttpResponse
from io import BytesIO
from .pdf import generer_facture_pdf

def envoyer_facture_email(facture, request):
    buffer = BytesIO()
    generer_facture_pdf(buffer, facture.id)

    email = EmailMessage(
        subject=f"Facture {facture.numero}",
        body="Veuillez trouver votre facture en pièce jointe.",
        to=[facture.client.email],
    )

    email.attach(f"facture_{facture.numero}.pdf", buffer.getvalue(), "application/pdf")
    email.send()