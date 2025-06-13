import os
from datetime import datetime

# Check for reportlab dependency
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib import colors
    from reportlab.platypus import Table, TableStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not installed. PDF generation will not work.")

from db import get_billing_data, get_motors_data

def generate_billing_pdf(billing_ref):
    """
    Generate a professional PDF invoice for the given billing reference.

    Args:
        billing_ref (str): The billing reference number

    Returns:
        str: Path to generated PDF file or error message
    """

    if not REPORTLAB_AVAILABLE:
        error_msg = "PDF generation requires reportlab library. Please install it with: pip install reportlab"
        print(error_msg)
        return error_msg

    try:
        # Validate billing reference
        if not billing_ref:
            raise ValueError("Billing reference cannot be empty")

        # Fetch billing and motors data from the database
        billing_data = get_billing_data(billing_ref)
        if not billing_data:
            raise ValueError(f"No billing data found for reference: {billing_ref}")

        motors_data = get_motors_data(billing_ref)
        if not motors_data:
            raise ValueError(f"No motors data found for billing reference: {billing_ref}")

        # Determine output directory with fallback options
        output_path = get_output_path(billing_ref)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Create a PDF canvas
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Add logos (with error handling for missing files)
        add_logos(c, width, height)

        # Draw header with billing information
        draw_header(c, billing_data, width, height)

        # Add itemized billing table
        add_billing_items_table(c, motors_data, width, height)

        # Add payment and vehicle information
        add_payment_info(c, billing_data, height)

        # Add terms and conditions
        terms_y_position = add_terms_and_conditions(c, width, height)

        # Add signature (with error handling for missing files)
        add_signature(c, width, terms_y_position)

        # Save the PDF
        c.save()

        print(f"PDF generated successfully: {output_path}")
        return output_path

    except Exception as e:
        error_msg = f"Error generating PDF for billing {billing_ref}: {str(e)}"
        print(error_msg)
        return error_msg

def get_output_path(billing_ref):
    """
    Determine the best output path for the PDF file.

    Args:
        billing_ref (str): The billing reference number

    Returns:
        str: Full path for the output PDF file
    """
    # Try multiple directory options in order of preference
    possible_dirs = [
        os.getenv("FLET_APP_STORAGE_DATA"),  # Flet storage directory
        os.path.join(os.path.expanduser('~'), 'Downloads'),  # User Downloads
        os.path.join(os.path.expanduser('~'), 'Documents'),  # User Documents
        os.getcwd(),  # Current working directory
        os.path.join(os.getcwd(), 'output'),  # Output subdirectory
    ]

    for directory in possible_dirs:
        if directory and os.path.exists(directory):
            try:
                # Test if we can write to this directory
                test_file = os.path.join(directory, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                return os.path.join(directory, f"facture_{billing_ref}.pdf")
            except (OSError, PermissionError):
                continue

    # Fallback to current directory
    return os.path.join(os.getcwd(), f"facture_{billing_ref}.pdf")


def add_logos(c, width, height):
    """
    Add company logos and title to the PDF with error handling for missing files.

    Args:
        c: ReportLab canvas object
        width: Page width
        height: Page height
    """
    # Try multiple possible logo paths
    possible_logo_paths = [
        os.path.join(os.getenv("FLET_APP_STORAGE_DATA", ""), 'mallouka_motors_logo.png'),
        os.path.join('src', 'assets', 'logo', 'mallouka_motors_logo.png'),
        os.path.join('assets', 'logo', 'mallouka_motors_logo.png'),
        os.path.join(os.getcwd(), 'mallouka_motors_logo.png'),
        os.path.join(os.getcwd(), 'src', 'assets', 'logo', 'mallouka_motors_logo.png'),
    ]

    # Define logo dimensions
    logo_width = 80
    logo_height = 80

    # Positions for logos
    left_logo_x = 40
    logo_y = height - logo_height - 20  # Adjust top margin

    # Try to load and draw the logo
    logo_loaded = False
    for logo_path in possible_logo_paths:
        if logo_path and os.path.exists(logo_path):
            try:
                mallouka_logo = ImageReader(logo_path)
                c.drawImage(mallouka_logo, left_logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
                logo_loaded = True
                print(f"Logo loaded successfully from: {logo_path}")
                break
            except Exception as e:
                print(f"Failed to load logo from {logo_path}: {e}")
                continue

    if not logo_loaded:
        print("Warning: Could not load company logo. PDF will be generated without logo.")
        # Draw a placeholder rectangle
        c.setStrokeColor(colors.grey)
        c.setFillColor(colors.lightgrey)
        c.rect(left_logo_x, logo_y, logo_width, logo_height, fill=1, stroke=1)

        # Add "LOGO" text in the placeholder
        c.setFillColor(colors.black)
        c.setFont('Helvetica', 12)
        text_x = left_logo_x + logo_width/2 - c.stringWidth("LOGO", 'Helvetica', 12)/2
        text_y = logo_y + logo_height/2 - 6
        c.drawString(text_x, text_y, "LOGO")

    # Define and draw title
    title = "Société Mallouka Motors"
    c.setFont('Helvetica-Bold', 22)
    c.setFillColor(colors.black)

    # Calculate title position to center it
    title_width = c.stringWidth(title, 'Helvetica-Bold', 22)
    title_x = (width - title_width) / 2
    title_y = logo_y + (logo_height / 2) - 7  # Center the title vertically with the logo

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
    """
    Add company signature to the PDF with error handling for missing files.

    Args:
        c: ReportLab canvas object
        width: Page width
        terms_y_position: Y position after terms and conditions
    """
    # Try multiple possible signature paths
    possible_signature_paths = [
        os.path.join(os.getenv("FLET_APP_STORAGE_DATA", ""), 'signature.png'),
        os.path.join('src', 'assets', 'signature.png'),
        os.path.join('assets', 'signature.png'),
        os.path.join(os.getcwd(), 'signature.png'),
        os.path.join(os.getcwd(), 'src', 'assets', 'signature.png'),
    ]

    signature_width = 150
    signature_height = 75
    x = width - signature_width - 40  # Right align with margin
    y = terms_y_position - signature_height - 10  # Position below terms with some margin

    # Try to load and draw the signature
    signature_loaded = False
    for signature_path in possible_signature_paths:
        if signature_path and os.path.exists(signature_path):
            try:
                signature = ImageReader(signature_path)
                c.drawImage(signature, x, y, width=signature_width, height=signature_height, mask='auto')
                signature_loaded = True
                print(f"Signature loaded successfully from: {signature_path}")
                break
            except Exception as e:
                print(f"Failed to load signature from {signature_path}: {e}")
                continue

    if not signature_loaded:
        print("Warning: Could not load signature. Adding text signature instead.")
        # Add a text-based signature as fallback
        c.setFont('Helvetica-Bold', 12)
        c.setFillColor(colors.black)

        # Draw signature box
        c.setStrokeColor(colors.grey)
        c.rect(x, y, signature_width, signature_height, fill=0, stroke=1)

        # Add signature text
        signature_text = "Signature & Cachet"
        text_x = x + signature_width/2 - c.stringWidth(signature_text, 'Helvetica-Bold', 12)/2
        text_y = y + signature_height/2 - 6
        c.drawString(text_x, text_y, signature_text)

        # Add company name
        c.setFont('Helvetica', 10)
        company_text = "Mallouka Motors"
        text_x = x + signature_width/2 - c.stringWidth(company_text, 'Helvetica', 10)/2
        text_y = y + 15
        c.drawString(text_x, text_y, company_text)
