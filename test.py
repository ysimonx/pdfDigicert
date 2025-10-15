from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, timestamps
import logging

# Configurer le logging pour voir les messages de pyHanko
logging.basicConfig(level=logging.INFO)

# --- Configuration ---
PDF_IN = 'document_a_horodater.pdf'
PDF_OUT = 'document_horodate.pdf'

# URL du serveur d'horodatage DigiCert (RFC 3161)
DIGICERT_TSA_URL = 'http://timestamp.digicert.com'

# 1. Configurer le service d'horodatage (TSA)
timestamper = timestamps.HTTPTimeStamper(DIGICERT_TSA_URL)

# 2. Créer le PDF timestamper
pdf_timestamper = signers.PdfTimeStamper(timestamper)

# 3. Traiter le document
with open(PDF_IN, 'rb') as inf:
    w = IncrementalPdfFileWriter(inf)

    # 4. Appliquer l'horodatage
    # pyHanko crée automatiquement un champ de signature invisible pour l'horodatage
    out = pdf_timestamper.timestamp_pdf(
        w,
        md_algorithm='sha256'
    )

    # 5. Enregistrer le PDF horodaté
    with open(PDF_OUT, 'wb') as outf:
        outf.write(out.read())

print(f"Le document a été horodaté avec succès par DigiCert : {PDF_OUT}")