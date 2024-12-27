import sqlite3
from datetime import datetime
from flet import *

def get_db_connection():
    conn = sqlite3.connect('storage/data/allocasseauto.db', timeout=10)
    return conn

#######################
# Table creation
#######################

# def drop_motors_table():
#     """
#     Drops the Motors table if it exists.
#     """
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute("DROP TABLE IF EXISTS Motors")
#         conn.commit()
#         print("Motors table dropped successfully.")

# drop_motors_table()

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Motors Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Motors (
        id VARCHAR(100) PRIMARY KEY,  
        marque VARCHAR(100) NOT NULL, 
        modele VARCHAR(100) NOT NULL, 
        annee INT NOT NULL , 
        kilometrage INT NOT NULL, 
        prix DECIMAL(10, 2) NOT NULL, 
        date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        description TEXT,
        statut TEXT, 
        date_achat DATE,
        fournisseur VARCHAR(200), 
        BL_facture VARCHAR(200) 
    )

    ''')

    # Create Clients Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_complet VARCHAR(230) NOT NULL,
        adresse VARCHAR(230),
        numero INT,
        mf VARCHAR(230) 
    )
    ''')
    
    # Create Billing Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Billing (
            ref VARCHAR(240) PRIMARY KEY,
            total_price FLOAT NOT NULL,
            client_id INTEGER NOT NULL,
            mode_paiement VARCHAR(230),
            description VARCHAR(250) DEFAULT 'Garantie limité de 30 jours pour les moteurs ESSENCE et 15 jours pour les moteurs DIESEL contre tout défaut de consommation de l’huile et de l’eau à partir de la date de vente du moteur. Tout défaut doit être notifié au vendeur dans les 30 Jours qui suivent la date de vente du moteur. En dehors de cette date, la garantie n’est plus valide.',
            transporteur VARCHAR(240),
            matricule VARCHAR(240),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES Clients(id)
        )
        ''')
    
    # create billing-motor table
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS Billing_Motors (
            billing_ref VARCHAR(240),
            motor_id VARCHAR(100),
            quantity INT NOT NULL,
            PRIMARY KEY (billing_ref, motor_id),
            FOREIGN KEY (billing_ref) REFERENCES Billing(ref),
            FOREIGN KEY (motor_id) REFERENCES Motors(id)
        )
        ''')

    conn.commit()
    conn.close()
    


# def migrate_database():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Alter the Billing_Motors table to add the quantity column
#     cursor.execute('''
#         ALTER TABLE Billing_Motors
#         ADD COLUMN quantity INT NOT NULL DEFAULT 1
#     ''')

#     conn.commit()
#     conn.close()

#######################
# billing CRUD operations
#######################

def insert_billing(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Billing (ref, total_price, client_id, mode_paiement, description, transporteur, matricule) VALUES (?, ?, ?, ?, ?, ?, ?)", 
        data
    )    
    conn.commit()
    conn.close()

def update_billing(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Billing SET total_price = ?, client_id = ?, mode_paiement = ?, description = ?, transporteur = ?, matricule = ?, date = ?  WHERE ref = ?", 
        data
    )
    conn.commit()
    conn.close()

def delete_billing_without_BM(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Billing WHERE ref = ?", (billing_ref,))
    conn.commit()
    conn.close()

def delete_billing(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete related entries in Billing_Motors table
        cursor.execute("DELETE FROM Billing_Motors WHERE billing_ref = ?", (billing_ref,))

        # Delete the billing entry in the Billing table
        cursor.execute("DELETE FROM Billing WHERE ref = ?", (billing_ref,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def fetch_billing():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Billing")
    billings = cursor.fetchall()
    conn.close()
    return billings

def search_billings(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Billing WHERE ref LIKE ? OR total_price LIKE ? OR client_id LIKE ? OR mode_paiement LIKE ? OR description LIKE ? OR transporteur LIKE ? OR matricule LIKE ? OR date LIKE ?", ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    billings = cursor.fetchall()
    conn.close()
    return billings


def get_all_billings(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.ref, b.total_price, b.client_id, b.mode_paiement, 
                    b.description, b.transporteur, b.matricule, b.date,
                    GROUP_CONCAT(m.motor_id, ', ') AS motors
                FROM Billing b
                LEFT JOIN Billing_Motors m ON b.ref = m.billing_ref
                GROUP BY b.ref
            """)
            results = cursor.fetchall()
        return results
    
    
def update_total_price(app, motor=None):
        total_price = 0.0
        motors_column = app.add_billing_form.controls[4]

        for control in motors_column.controls:
            checkbox = control.controls[0]
            quantity_field = control.controls[1]
            if isinstance(checkbox, Checkbox) and checkbox.value:
                motor_id = checkbox.label
                quantity = int(quantity_field.value) if quantity_field.value else 0
                price = get_motor_price(motor_id)
                total_price += price * quantity

        app.add_billing_form.controls[1].value = f"{total_price:.2f}"
        app.page.update()



def search_billings_motors_list(query):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.ref, b.total_price, b.client_id, b.mode_paiement, 
                   b.description, b.transporteur, b.matricule, b.date,
                   GROUP_CONCAT(m.motor_id, ', ') AS motors
            FROM Billing b
            LEFT JOIN Billing_Motors m ON b.ref = m.billing_ref
            WHERE b.ref LIKE ? OR b.total_price LIKE ? OR b.client_id LIKE ? OR b.mode_paiement LIKE ? OR b.description LIKE ? OR b.transporteur LIKE ? OR b.matricule LIKE ? OR b.date LIKE ? OR m.motor_id LIKE ?
            GROUP BY b.ref
        """, ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
    return results



def total_price_calcul(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get motor IDs and quantities from Billing_Motors table
    cursor.execute('''
        SELECT motor_id, quantity
        FROM Billing_Motors
        WHERE billing_ref = ?
    ''', (billing_ref,))

    motors = cursor.fetchall()

    total_price = 0.0

    for motor in motors:
        motor_id, quantity = motor

        # Query to get the price of the motor from Motors table
        cursor.execute('''
            SELECT prix
            FROM Motors
            WHERE id = ?
        ''', (motor_id,))

        price = cursor.fetchone()[0]
        total_price += price * quantity

    conn.close()
    return total_price


#######################
# billing generator operations
#######################

def get_billing_data(billing_ref):
    """
    Fetch billing data from the database.

    :param billing_ref: Billing reference number.
    :return: Dictionary containing billing data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.ref, b.total_price, b.client_id, b.mode_paiement, b.description, b.transporteur, b.matricule, b.date, c.nom_complet, c.mf, c.adresse
        FROM Billing b
        JOIN Clients c ON b.client_id = c.id
        WHERE b.ref = ?
    ''', (billing_ref,))
    billing_data = cursor.fetchone()
    conn.close()

    # Convert the date string to a datetime object
    date_str = billing_data[7]
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')  # Adjust the format string as per your date format in the database

    return {
        'ref': billing_data[0],
        'total_price': billing_data[1],
        'client_id': billing_data[2],
        'mode_paiement': billing_data[3],
        'description': billing_data[4],
        'transporteur': billing_data[5],
        'matricule': billing_data[6],
        'date': date_obj,  # Use the datetime object
        'client_name': billing_data[8],
        'client_mf': billing_data[9],
        'client_address': billing_data[10]
    }
    
    
def get_motors_data(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bm.motor_id, bm.quantity, m.marque, m.modele, m.description, m.prix
        FROM Billing_Motors bm
        JOIN Motors m ON bm.motor_id = m.id
        WHERE bm.billing_ref = ?
    ''', (billing_ref,))
    motors_data = cursor.fetchall()
    conn.close()
    return [{'motor_id': motor[0], 'quantity': motor[1], 'marque': motor[2], 'modele': motor[3], 'description': motor[4], 'prix': motor[5]} for motor in motors_data]


def get_motor_price(motor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT prix FROM Motors WHERE id = ?', (motor_id,))
    price = cursor.fetchone()
    conn.close()
    return price[0] if price else 0.00


#######################
# billing motor CRUD operations
#######################

def insert_Billing_Motors(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Billing_Motors (billing_ref, motor_id) VALUES (?, ?)", 
        data
    )
    conn.commit()
    conn.close()

def update_Billing_Motors(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Billing_Motors SET motor_id = ? WHERE billing_ref = ?", 
        data
    )
    conn.commit()
    conn.close()

def delete_Billing_Motors(Billing_Motors_billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Billing_Motors WHERE billing_ref = ?", (Billing_Motors_billing_ref,))
    conn.commit()
    conn.close()

def fetch_Billing_Motors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Billing_Motors")
    Billing_Motors = cursor.fetchall()
    conn.close()
    return Billing_Motors

def search_Billing_Motors(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Billing_Motors WHERE billing_ref LIKE ? OR motor_id LIKE ? ", ('%' + query + '%', '%' + query + '%'))
    Billing_Motors = cursor.fetchall()
    conn.close()
    return Billing_Motors


def get_selected_motors_by_billing_ref(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT motor_id, quantity
        FROM Billing_Motors
        WHERE billing_ref = ?
    ''', (billing_ref,))

    selected_motors = cursor.fetchall()
    conn.close()
    return selected_motors


def get_related_motors(billing_ref):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT motor_id, quantity
        FROM Billing_Motors
        WHERE billing_ref = ?
    ''', (billing_ref,))

    related_motors = cursor.fetchall()
    conn.close()
    return related_motors
    
#######################
# Client CRUD operations
#######################

def insert_client(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Clients (nom_complet, adresse, numero, mf) VALUES (?, ?, ?, ?)", 
        data
    )
    conn.commit()
    conn.close()

def update_client(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Clients SET nom_complet = ?, adresse = ?, numero = ?, mf = ? WHERE id = ?", 
        data
    )
    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

def fetch_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    clients = cursor.fetchall()
    conn.close()
    return clients

def search_clients(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients WHERE nom_complet LIKE ? OR adresse LIKE ? OR numero LIKE ? OR mf LIKE ?", ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    clients = cursor.fetchall()
    conn.close()
    return clients


def get_all_clients():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Clients")
        return [row[0] for row in cursor.fetchall()]


def get_client_by_id(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nom_complet, adresse, numero, mf FROM Clients WHERE id = ?", (client_id,))
    client = cursor.fetchone()
    conn.close()
    return client


def get_client_id(client_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Clients WHERE id = ?", (client_id,)
        )
        return cursor.fetchone()

#######################
# Motor CRUD operations
#######################

def insert_motor(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Motors (id, marque, modele, annee, kilometrage, prix, description, statut, date_achat, fournisseur, BL_facture) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
        data
    )
    conn.commit()
    conn.close()

def update_motor(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Motors SET marque = ?, modele = ?, annee = ?, kilometrage = ?, prix = ?, description = ?, statut = ?, date_achat = ?, fournisseur = ?, BL_facture = ? WHERE id = ?", 
        data
    )
    conn.commit()
    conn.close()

def delete_motor(motor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Motors WHERE id = ?", (motor_id,))
    conn.commit()
    conn.close()

def get_motors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Motors")
    motors = cursor.fetchall()
    conn.close()
    return motors

def fetch_motors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, marque, modele, annee, kilometrage, prix, description, statut, date_achat, fournisseur, BL_facture FROM Motors")
    motors = cursor.fetchall()
    conn.close()
    return motors

def get_motor_by_id(motor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, marque, modele, annee, kilometrage, prix, description, statut, date_achat, fournisseur, BL_facture FROM Motors WHERE id = ?", (motor_id,))
    motor = cursor.fetchone()
    conn.close()
    return motor


def fetch_motor_by_id(motor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Motors WHERE id = ?", (motor_id,))
    motor = cursor.fetchone()
    conn.close()
    return motor

def search_motors(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, marque, modele, annee, kilometrage, prix, description, statut, date_achat, fournisseur, BL_facture FROM Motors WHERE
        id LIKE ? OR
        marque LIKE ? OR
        modele LIKE ? OR
        annee LIKE ? OR
        kilometrage LIKE ? OR
        prix LIKE ? OR
        description LIKE ? OR
        statut LIKE ? OR
        date_achat LIKE ? OR
        fournisseur LIKE ? OR
        BL_facture LIKE ?
    """, (f"%{query}%",) * 11)
    motors = cursor.fetchall()
    conn.close()
    return motors

def get_all_motors():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, marque FROM Motors WHERE statut = 'Disponible'")
        return [{"id": row[0], "marque": row[1]} for row in cursor.fetchall()]

# Ensure the table is created when db.py is imported
create_table()

# migrate_database()