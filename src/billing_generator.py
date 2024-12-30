from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
from db import get_billing_data, get_motors_data
from datetime import datetime

def generate_billing_pdf(billing_ref):
    # Fetch billing and motors data from the database
    billing_data = get_billing_data(billing_ref)
    motors_data = get_motors_data(billing_ref)

    # Determine the default download directory
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    output_path = os.path.join(download_dir, f"billing_{billing_ref}.pdf")

    # Create a PDF canvas
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Add logos
    add_logos(c, width, height)

    draw_header(c, billing_data, width, height)

    # Add itemized billing table
    add_billing_items_table(c, motors_data, width, height)

    # Add payment and vehicle information
    add_payment_info(c, billing_data, height)

    # Add terms and conditions
    terms_y_position = add_terms_and_conditions(c, width, height)
    
    # Add signature
    add_signature(c, width, terms_y_position)

    # Save the PDF
    c.save()


def add_logos(c, width, height):
    # Paths to logo images
    mallouka_logo_path = os.path.join('src', 'assets', 'logo', 'mallouka_motors_logo.png')
    allo_casse_logo_path = os.path.join('src', 'assets', 'logo', 'allo_casse_auto_logo.jpg')

    # Load logo images
    mallouka_logo = ImageReader(mallouka_logo_path)
    allo_casse_logo = ImageReader(allo_casse_logo_path)

    # Define logo dimensions
    logo_width = 80
    logo_height = 80

    # Positions for logos
    left_logo_x = 40
    right_logo_x = width - logo_width - 40
    logo_y = height - logo_height - 20  # Adjust top margin

    # Draw logos
    c.drawImage(mallouka_logo, left_logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
    c.drawImage(allo_casse_logo, right_logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

    # Define title
    title = "Société Mallouka Motors"
    c.setFont('Helvetica-Bold', 22)

    # Calculate title position to center it between the logos
    title_width = c.stringWidth(title, 'Helvetica-Bold', 22)
    title_x = (left_logo_x + logo_width + right_logo_x) / 2 - title_width / 2
    title_y = logo_y + (logo_height / 2) - 7  # Center the title vertically with the logos

    # Draw the title
    c.drawString(title_x, title_y, title)


def add_company_info(c, y):
    # Set the initial font size
    c.setFont('Helvetica', 10)

    # Extract company details with labels and values
    company_details = [
        ("Adresse:", "Rue Ibn El Jazzar Route Hôpital, MONGI SLIM La Marsa"),
        ("Mobile:", "96 360 060 ; 44 511 011"),
        ("E-mail:", "malloukamotors21@gmail.com"),
        ("R.N.E:", "1798692D"),
        ("M.F:", "1798692DNM000")
    ]

    x = 40  # Left-side position
    for label, value in company_details:
        # Draw the label in bold
        c.setFont('Helvetica-Bold', 10)
        c.drawString(x, y, label)

        # Draw the value in normal font, slightly offset to the right
        c.setFont('Helvetica', 10)
        label_width = c.stringWidth(label, 'Helvetica-Bold', 10)
        c.drawString(x + label_width + 5, y, value)

        # Move to the next line
        y -= 12  # Line spacing


def add_billing_info(c, billing_data, width, y):
    c.setFont('Helvetica', 10)

    # Convert datetime to string format
    billing_date = billing_data['date'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(billing_data['date'], datetime) else billing_data['date']

    client_details = [
        f"Client: {billing_data['client_name']}",
        f"MF: {billing_data['client_mf']}",
        f"Adresse: {billing_data['client_address']}",
        f"Date: {billing_date}"  # Use formatted date string
    ]

    x = width - 220  # Right-side position
    for line in client_details:
        c.drawString(x, y, line)
        y -= 12  # Line spacing


def draw_header(c, billing_data, width, height):
    # Set starting `y` for the first line of text
    y = height - 140  # Adjust this value as needed for alignment

    # Draw company info on the left
    add_company_info(c, y)

    # Draw billing info on the right
    add_billing_info(c, billing_data, width, y)
    
    # Set font for the FACTURE number
    c.setFont('Helvetica-Bold', 15)
    
    # Calculate the position to center the FACTURE number
    facture_text = f"FACTURE N°: {billing_data['ref']}"
    text_width = c.stringWidth(facture_text, 'Helvetica-Bold', 15)
    x_center = (width - text_width) / 2
    
    # Draw the FACTURE number centrally below the billing info
    c.drawString(x_center, height - 225, facture_text)



def add_billing_items_table(c, motors_data, width, height):
    # Prepare the table data
    data = [["Réf", "Libellé", "Qté", "PT HT"]]
    total_ht = 0       

    # Add motor details to the table
    for motor in motors_data:
        libelle = f"Moteur usagé {motor['description']} {motor['marque']} {motor['modele']}"
        data.append([motor['motor_id'], libelle, motor['quantity'], f"{motor['quantity'] * motor['prix']:.2f}"])
        total_ht += motor['quantity'] * motor['prix']

    # Add an empty line before totals
    data.append(["", "", "", ""])  # Empty row

    # Calculate totals and taxes
    droit_de_timbre = 1
    tva = total_ht * 0.19
    net_a_payer = total_ht + droit_de_timbre + tva

    # Add totals and taxes to the table
    data.extend([
        ["", "Total HT", "", f"{total_ht:.2f}"],
        ["", "TVA 19%", "", f"{tva:.2f}"],
        ["", "Droit de Timbre", "", f"{droit_de_timbre:.2f}"],
        ["", "Net à payer", "", f"{net_a_payer:.2f}"]
    ])

    # Create the table
    table = Table(data, colWidths=[50, 250, 50, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey])  # Excludes last row
    ]))

    # Center the table horizontally
    table_width, table_height = table.wrap(width, height)
    x_center = (width - table_width) / 2

    # Draw the table below the FACTURE number
    table.drawOn(c, x_center, height - 320 - table_height)


def add_payment_info(c, billing_data, height):
    y = height - 500  # Starting y position
    
    # Draw "Mode de paiement:" in bold
    c.setFont('Helvetica-Bold', 10)
    c.drawString(40, y, "Mode de paiement:")
    
    # Draw the payment mode in normal font
    c.setFont('Helvetica', 10)
    c.drawString(150, y, billing_data['mode_paiement'])
    
    # Move to the next line for "Matricule:"
    y -= 20
    
    # Draw "Matricule:" in bold
    c.setFont('Helvetica-Bold', 10)
    c.drawString(40, y, "Matricule:")
    
    # Draw the matricule in normal font
    c.setFont('Helvetica', 10)
    c.drawString(100, y, billing_data['matricule'])


def add_terms_and_conditions(c, width, height):
    c.setFont('Helvetica', 8)

    # Add "NB:" as a title
    nb_y = height - 560
    c.drawString(40, nb_y, "NB:")

    # Define terms and wrap them to fit within the page width
    terms = (
        "Garantie limité de 30 jours pour les moteurs ESSENCE et 15 jours pour les moteurs DIESEL contre tout défaut de consommation de l’huile et de l’eau à partir de la date de vente du moteur. Tout défaut doit être notifié au vendeur dans les 30 Jours qui suivent la date de vente du moteur. En dehors de cette date, la garantie n’est plus valide."
    )

    # Set the maximum width for text wrapping
    max_width = width - 80  # Leave 40 px margin on both sides
    x = 40  # Starting x position (aligned to left margin)
    y = nb_y - 20 # Starting y position below "NB:"

    # Split the text into lines that fit within max_width
    wrapped_lines = []
    words = terms.split()
    current_line = ""
    for word in words:
        # Check if adding the word exceeds max_width
        if c.stringWidth(current_line + word, "Helvetica", 8) > max_width:
            wrapped_lines.append(current_line.strip())  # Add the current line to wrapped lines
            current_line = word + " "  # Start a new line
        else:
            current_line += word + " "  # Add the word to the current line

    # Add the last line
    if current_line:
        wrapped_lines.append(current_line.strip())

    # Draw each wrapped line, maintaining a fixed line height
    for line in wrapped_lines:
        c.drawString(x, y, line)
        y -= 12  # Move down by 12 px for the next line

    return y # Return the final y position after drawing terms

def add_signature(c, width, terms_y_position):
    signature_path = os.path.join('src', 'assets', 'signature.png')
    if os.path.exists(signature_path):
        signature = ImageReader(signature_path)
        signature_width = 150  
        signature_height = 75  
        x = width - signature_width - 40  # Right align with margin
        y = terms_y_position - signature_height - 10 # Position below terms with some margin
        c.drawImage(signature, x, y, width=signature_width, height=signature_height, mask='auto')
    else:
        print(f"Signature image not found at {signature_path}")
