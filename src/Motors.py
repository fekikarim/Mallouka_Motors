from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster
from db import *

class Motors(UserControl):
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):
        super().__init__()
        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True

        self.page_name = "Mallouka Motors - Moteurs"
        self.icon = Icons.CAR_REPAIR
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame

        # Enhanced form fields with consistent styling
        input_style = self.themer.get_input_style()

        self.id_ref = TextField(
            label="ID - Reference",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.TAG,
        )
        self.marque = TextField(
            label="Marque",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.BRANDING_WATERMARK,
        )
        self.modele = TextField(
            label="Modèle",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.MODEL_TRAINING,
        )
        self.annee = TextField(
            label="Année",
            col={"md": 4},
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
            **input_style,
            prefix_icon=icons.CALENDAR_TODAY,
        )
        self.kilometrage = TextField(
            label="Kilométrage",
            col={"md": 4},
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
            **input_style,
            prefix_icon=icons.SPEED,
            suffix_text="km",
        )
        self.prix = TextField(
            label="Prix",
            col={"md": 4},
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
            **input_style,
            prefix_icon=icons.ATTACH_MONEY,
            suffix_text="DT",
        )
        self.description = TextField(
            label="Description",
            col={"md": 8},
            multiline=True,
            min_lines=3,
            max_lines=5,
            **input_style,
            prefix_icon=icons.DESCRIPTION,
        )
        self.status = Dropdown(
            label="Statut",
            options=[
                dropdown.Option("Disponible", text="🟢 Disponible"),
                dropdown.Option("Vendu", text="🔵 Vendu"),
                dropdown.Option("Reserve", text="🟠 Réservé"),
            ],
            col={"md": 4},
            **input_style,
            prefix_icon=icons.INFO,
        )
        self.date_achats = TextField(
            label="Date d'Achat",
            hint_text="YYYY-MM-DD",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.EVENT,
        )
        self.fournisseur = TextField(
            label="Fournisseur",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.BUSINESS,
        )
        self.bl_facture = TextField(
            label="BL - Facture",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.RECEIPT,
        )

        self.motors_data_table = DataTable(
            columns=[
                DataColumn(
                    Text(
                        "Actions",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "ID - Référence",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Marque",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Modèle",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Année",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Kilométrage",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Prix (DT)",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Description",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Statut",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Date d'Achat",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Fournisseur",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "BL - Facture",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
            ],
            rows=[],
            border=border.all(1, colors.OUTLINE_VARIANT),
            horizontal_lines=border.BorderSide(1, colors.OUTLINE_VARIANT),
            vertical_lines=border.BorderSide(1, colors.OUTLINE_VARIANT),
            heading_row_color=colors.SURFACE_VARIANT,
            data_row_color={
                MaterialState.HOVERED: colors.with_opacity(0.08, colors.ON_SURFACE),
                MaterialState.SELECTED: colors.with_opacity(0.12, colors.PRIMARY),
            },
            expand=True,
        )
        
        
        self.motors_list_title = self.themer.create_section_title("Liste des Moteurs")

        search_input_style = self.themer.get_input_style()
        self.search_bar = ResponsiveRow(
            controls=[
                TextField(
                    label="Rechercher des moteurs",
                    on_change=self.on_search_change,
                    col={"md": 8, "lg": 6},
                    **search_input_style,
                    prefix_icon=icons.SEARCH,
                    hint_text="Rechercher par ID, marque, modèle...",
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

        self.edit_motor_id = None  # To store the ID of the motor being edited

        self.title_container = Container(
            content=self.themer.create_section_title("Ajouter un Moteur"),
            margin=margin.only(bottom=20),
            alignment=alignment.center,
        )

        self.motors_frame = self.make_frame()

        self.controls = [
            self.motors_frame,
            self.upperbar,
        ]
        self.load_motors()

    def make_frame(self):
        self.motors_frame = SafeArea(
            content=Column(
                controls=[
                    # Add Motor Form Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.title_container,
                                Container(height=24),
                                ResponsiveRow(
                                    [
                                        self.id_ref,
                                        self.marque,
                                        self.modele,
                                        self.annee,
                                        self.kilometrage,
                                        self.prix,
                                        self.description,
                                        self.status,
                                        self.date_achats,
                                        self.fournisseur,
                                        self.bl_facture,
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    run_spacing=20,
                                ),
                                Container(height=24),
                                ResponsiveRow(
                                    [
                                        Container(
                                            content=ElevatedButton(
                                                text="Ajouter le Moteur",
                                                icon=Icons.ADD,
                                                style=self.themer.get_button_style("primary"),
                                                on_click=self.add_motor,
                                            ),
                                            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                                        ),
                                        Container(
                                            content=ElevatedButton(
                                                text="Vider",
                                                icon=Icons.CLEAR,
                                                style=self.themer.get_button_style("outline"),
                                                on_click=self.clear_form,
                                            ),
                                            col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                                        ),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                            ], spacing=0),
                            elevated=True,
                            padding=40,
                        ),
                        width=1200,  # Standardized form width
                        alignment=alignment.center,
                    ),

                    Container(height=40),

                    # Motors List Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.motors_list_title,
                                Container(height=24),
                                self.search_bar,
                                Container(height=24),
                                Container(
                                    content=Row(
                                        controls=[
                                            self.motors_data_table,
                                        ],
                                        scroll="auto",
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    expand=True,
                                ),
                            ], spacing=0),
                            elevated=True,
                            padding=30,
                        ),
                        width=1200,  # Standardized table width
                        alignment=alignment.center,
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            expand=True,
        )
        return self.motors_frame

    def clear_form(self, e=None):
        """Clear all form fields and set focus to first field"""
        self.id_ref.value = ""
        self.marque.value = ""
        self.modele.value = ""
        self.annee.value = ""
        self.kilometrage.value = ""
        self.prix.value = ""
        self.description.value = ""
        self.status.value = None
        self.date_achats.value = ""
        self.fournisseur.value = ""
        self.bl_facture.value = ""

        # Set focus to the first input field for better UX (only if control is mounted)
        try:
            if self.is_mounted():
                self.id_ref.focus()
        except:
            pass  # Ignore focus errors if control is not ready

        if self.is_mounted():
            self.page.show_snack_bar(SnackBar(Text("Formulaire vidé")))
        self.page.update()

    def add_motor(self, e):
        motor_data = {
            "id": self.id_ref.value,
            "marque": self.marque.value,
            "modele": self.modele.value,
            "annee": int(self.annee.value) if self.annee.value else None,
            "kilometrage": int(self.kilometrage.value) if self.kilometrage.value else None,
            "prix": float(self.prix.value) if self.prix.value else None,
            "description": self.description.value,
            "statut": self.status.value,
            "date_achat": self.date_achats.value,
            "fournisseur": self.fournisseur.value,
            "bl_facture": self.bl_facture.value,
        }
        
        # Add new motor
        insert_motor_data = (
            motor_data['id'],
            motor_data['marque'],
            motor_data['modele'],
            motor_data['annee'],
            motor_data['kilometrage'],
            motor_data['prix'],
            motor_data['description'],
            motor_data['statut'],
            motor_data['date_achat'],
            motor_data['fournisseur'],
            motor_data['bl_facture'],
        )
        insert_motor(insert_motor_data)
        self.page.show_snack_bar(SnackBar(Text("Nouveau moteur ajouté avec succès !")))

        self.clear_form()
        self.load_motors()

        # Refresh billing page motor dropdowns if it exists
        if hasattr(self.parent_class, 'billing') and self.parent_class.billing:
            self.parent_class.billing.refresh_data()

        # Refresh dashboard statistics instantly with async update
        if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
            self.parent_class.dashboard.refresh_dashboard_async()

        self.page.update()
        

    def on_search_change(self, e):
        query = e.control.value
        self.load_motors(query)
    
    def create_enhanced_motor_form(self, form_fields):
        """
        Create an enhanced motor form with modern styling and validation.

        Args:
            form_fields: Current motor data

        Returns:
            Column: Enhanced form with validation
        """
        # Create form fields with enhanced styling
        form_controls = [
            self.themer.create_enhanced_form_field(
                label="ID - Référence",
                value=form_fields[0],
                field_type="text",
                read_only=True,
                prefix_icon=icons.TAG,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Marque",
                value=form_fields[1],
                field_type="text",
                prefix_icon=icons.BRANDING_WATERMARK,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Modèle",
                value=form_fields[2],
                field_type="text",
                prefix_icon=icons.CAR_REPAIR,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Année",
                value=form_fields[3],
                field_type="number",
                prefix_icon=icons.CALENDAR_TODAY,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Kilométrage",
                value=form_fields[4],
                field_type="number",
                prefix_icon=icons.SPEED,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Prix (DT)",
                value=form_fields[5],
                field_type="number",
                prefix_icon=icons.ATTACH_MONEY,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Description",
                value=form_fields[6],
                field_type="text",
                multiline=True,
                prefix_icon=icons.DESCRIPTION,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Statut",
                value=form_fields[7],
                field_type="dropdown",
                options=[
                    ("Disponible", "🟢 Disponible"),
                    ("Vendu", "🔵 Vendu"),
                    ("Reserve", "🟠 Réservé")
                ],
                prefix_icon=icons.INFO,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Date d'Achat",
                value=form_fields[8],
                field_type="date",
                prefix_icon=icons.EVENT,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Fournisseur",
                value=form_fields[9],
                field_type="text",
                prefix_icon=icons.BUSINESS,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="BL - Facture",
                value=form_fields[10],
                field_type="text",
                prefix_icon=icons.RECEIPT,
                required=False
            ),
        ]

        return Column(
            controls=form_controls,
            spacing=0,
            scroll=ScrollMode.AUTO,
            expand=True,
        )

    def open_update_dialog(self, motor_id):
        """
        Open enhanced update dialog for motor with modern styling and validation.

        Args:
            motor_id: ID of the motor to update
        """
        try:
            self.edit_motor_id = motor_id
            motor = get_motor_by_id(motor_id)

            if not motor:
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.ERROR, color=colors.WHITE),
                        Text("Moteur non trouvé", color=colors.WHITE),
                    ]),
                    bgcolor=colors.RED_500
                ))
                return

            # Create enhanced form
            motor_form = self.create_enhanced_motor_form(motor)

            # Create enhanced dialog with modern styling
            actions = [
                TextButton(text="Annuler", on_click=lambda _: self._close_dialog_with_animation()),
                TextButton(text="Mettre à jour", on_click=lambda _: self._handle_motor_update(motor_form)),
            ]

            self.page.dialog = self.themer.create_enhanced_modal_dialog(
                title="Mettre à jour le Moteur",
                content=motor_form,
                actions=actions,
                width=600,
                height=700
            )

            self.page.update()

        except Exception as e:
            print(f"Error opening motor update dialog: {e}")
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    Icon(icons.ERROR, color=colors.WHITE),
                    Text(f"Erreur: {str(e)}", color=colors.WHITE),
                ]),
                bgcolor=colors.RED_500
            ))

    def _close_dialog_with_animation(self):
        """Close dialog with smooth animation."""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.edit_motor_id = None

    def _handle_motor_update(self, form_container):
        """
        Handle motor update with enhanced validation and feedback.

        Args:
            form_container: Container with form fields
        """
        try:
            # Show loading indicator
            self._show_loading_overlay("Mise à jour en cours...")

            # Extract form data with validation
            form_data = self._extract_motor_form_data(form_container)

            if not self._validate_motor_data(form_data):
                self._hide_loading_overlay()
                return

            # Update motor in database
            self._update_motor_in_database(form_data)

            # Hide loading and show success
            self._hide_loading_overlay()
            self._show_success_message(f"Moteur {self.edit_motor_id} mis à jour avec succès!")

            # Close dialog and refresh data
            self._close_dialog_with_animation()
            self._refresh_all_data()

        except Exception as e:
            self._hide_loading_overlay()
            self._show_error_message(f"Erreur lors de la mise à jour: {str(e)}")
            print(f"Error updating motor: {e}")

    def _show_loading_overlay(self, message):
        """Show loading overlay in dialog."""
        if self.page.dialog:
            loading_overlay = self.themer.create_loading_overlay(message)
            self.page.dialog.content = loading_overlay
            self.page.update()

    def _hide_loading_overlay(self):
        """Hide loading overlay and restore form."""
        if self.page.dialog and self.edit_motor_id:
            motor = get_motor_by_id(self.edit_motor_id)
            if motor:
                motor_form = self.create_enhanced_motor_form(motor)
                self.page.dialog.content = Container(
                    content=motor_form,
                    padding=padding.all(20),
                    border_radius=self.themer.border_radius,
                    bgcolor=colors.SURFACE_VARIANT,
                    border=border.all(1, colors.OUTLINE_VARIANT),
                )
                self.page.update()

    def _extract_motor_form_data(self, form_container):
        """
        Extract and validate form data from the enhanced form.

        Args:
            form_container: Container with form fields

        Returns:
            dict: Extracted form data
        """
        try:
            # Navigate through the container structure to get form fields
            form_controls = form_container.controls

            # Extract values from enhanced form fields
            motor_data = {
                "id": self._get_field_value(form_controls[0]),  # ID (read-only)
                "marque": self._get_field_value(form_controls[1]),
                "modele": self._get_field_value(form_controls[2]),
                "annee": self._get_field_value(form_controls[3]),
                "kilometrage": self._get_field_value(form_controls[4]),
                "prix": self._get_field_value(form_controls[5]),
                "description": self._get_field_value(form_controls[6]),
                "statut": self._get_field_value(form_controls[7]),
                "date_achat": self._get_field_value(form_controls[8]),
                "fournisseur": self._get_field_value(form_controls[9]),
                "bl_facture": self._get_field_value(form_controls[10]),
            }

            return motor_data

        except Exception as e:
            print(f"Error extracting form data: {e}")
            raise ValueError("Erreur lors de l'extraction des données du formulaire")

    def _get_field_value(self, field_container):
        """Extract value from enhanced form field container."""
        try:
            # Navigate through container to get the actual field
            field = field_container.content
            return field.value if hasattr(field, 'value') else ""
        except:
            return ""

    def _validate_motor_data(self, motor_data):
        """
        Validate motor form data with user feedback.

        Args:
            motor_data (dict): Motor data to validate

        Returns:
            bool: True if valid, False otherwise
        """
        errors = []

        # Required field validation
        if not motor_data.get("marque", "").strip():
            errors.append("La marque est obligatoire")

        if not motor_data.get("modele", "").strip():
            errors.append("Le modèle est obligatoire")

        if not motor_data.get("prix", "").strip():
            errors.append("Le prix est obligatoire")

        if not motor_data.get("statut", "").strip():
            errors.append("Le statut est obligatoire")

        # Numeric validation
        try:
            if motor_data.get("annee", "").strip():
                annee = int(motor_data["annee"])
                if annee < 1900 or annee > 2030:
                    errors.append("L'année doit être entre 1900 et 2030")
        except ValueError:
            errors.append("L'année doit être un nombre valide")

        try:
            if motor_data.get("kilometrage", "").strip():
                km = int(motor_data["kilometrage"])
                if km < 0:
                    errors.append("Le kilométrage ne peut pas être négatif")
        except ValueError:
            errors.append("Le kilométrage doit être un nombre valide")

        try:
            if motor_data.get("prix", "").strip():
                prix = float(motor_data["prix"])
                if prix <= 0:
                    errors.append("Le prix doit être supérieur à 0")
        except ValueError:
            errors.append("Le prix doit être un nombre valide")

        # Date validation
        if motor_data.get("date_achat", "").strip():
            date_str = motor_data["date_achat"]
            if not self._validate_date_format(date_str):
                errors.append("La date d'achat doit être au format YYYY-MM-DD")

        # Show errors if any
        if errors:
            error_message = "Erreurs de validation:\n" + "\n".join(f"• {error}" for error in errors)
            self._show_error_message(error_message)
            return False

        return True

    def _validate_date_format(self, date_str):
        """Validate date format YYYY-MM-DD."""
        try:
            from datetime import datetime
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def _update_motor_in_database(self, motor_data):
        """
        Update motor in database with proper error handling.

        Args:
            motor_data (dict): Validated motor data
        """
        try:
            # Convert data types
            annee = int(motor_data["annee"]) if motor_data.get("annee", "").strip() else None
            kilometrage = int(motor_data["kilometrage"]) if motor_data.get("kilometrage", "").strip() else None
            prix = float(motor_data["prix"]) if motor_data.get("prix", "").strip() else None

            update_data = (
                motor_data["marque"],
                motor_data["modele"],
                annee,
                kilometrage,
                prix,
                motor_data["description"],
                motor_data["statut"],
                motor_data["date_achat"],
                motor_data["fournisseur"],
                motor_data["bl_facture"],
                self.edit_motor_id,
            )

            update_motor(update_data)

        except Exception as e:
            print(f"Database update error: {e}")
            raise ValueError("Erreur lors de la mise à jour en base de données")

    def _refresh_all_data(self):
        """Refresh all related data after motor update."""
        try:
            # Refresh motors table
            self.load_motors()

            # Refresh billing page motor dropdowns if it exists
            if hasattr(self.parent_class, 'billing') and self.parent_class.billing:
                self.parent_class.billing.refresh_data()

            # Refresh dashboard statistics instantly with async update
            if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
                self.parent_class.dashboard.refresh_dashboard_async()

        except Exception as e:
            print(f"Error refreshing data: {e}")

    def _show_success_message(self, message):
        """Show success message with enhanced styling."""
        self.page.show_snack_bar(SnackBar(
            content=Row([
                Icon(icons.CHECK_CIRCLE, color=colors.WHITE),
                Text(message, color=colors.WHITE, expand=True),
            ]),
            bgcolor=colors.GREEN_500,
            duration=3000
        ))

    def _show_error_message(self, message):
        """Show error message with enhanced styling."""
        self.page.show_snack_bar(SnackBar(
            content=Row([
                Icon(icons.ERROR, color=colors.WHITE),
                Text(message, color=colors.WHITE, expand=True),
            ]),
            bgcolor=colors.RED_500,
            duration=5000
        ))
    
    
    def confirm_delete(self, e):
        motor_id = e
        delete_motor(motor_id)
        self.page.show_snack_bar(SnackBar(Text(f"Moteur avec l'ID {motor_id} supprimé !")))
        self.load_motors()

        # Refresh dashboard statistics instantly with async update
        if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
            self.parent_class.dashboard.refresh_dashboard_async()

        self.page.close_dialog()
        self.page.update()

    def delete_motor_handler(self, e):
        motor_id = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(value=f"Êtes-vous sûr de vouloir supprimer le moteur avec l'ID {motor_id} ?"),
            content=Text("Cette action ne peut pas être annulée."),
            actions=[
                TextButton(text="Annuler", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Supprimer", on_click=lambda _: self.confirm_delete(motor_id)),
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True,
            scrollable=True,
        )
        self.page.update()

    def load_motors(self, query=""):

        if query:
            motors = search_motors(query)
        else:
            motors = fetch_motors()

        self.motors_data_table.rows.clear()

        for motor in motors:
            # Format price with currency
            formatted_price = f"{float(motor[5]):.2f} DT" if motor[5] else "0.00 DT"

            # Format status with color coding
            status_color = colors.GREEN if motor[7] == "Disponible" else colors.BLUE if motor[7] == "Vendu" else colors.ORANGE
            status_display = Container(
                content=Text(
                    motor[7],
                    style=self.themer.get_text_style("body_medium"),
                    weight=FontWeight.W_600,
                    color=status_color,
                ),
                padding=padding.symmetric(horizontal=8, vertical=4),
            )

            # Format date
            formatted_date = motor[8][:10] if motor[8] else ""

            # Truncate description
            description = motor[6][:30] + "..." if len(str(motor[6])) > 30 else str(motor[6])

            self.motors_data_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Row(
                                [
                                    IconButton(
                                        icon=icons.EDIT,
                                        icon_color=colors.PRIMARY,
                                        tooltip="Modifier",
                                        on_click=lambda e, motor_id=motor[0]: self.open_update_dialog(motor_id),
                                        data=motor[0]
                                    ),
                                    IconButton(
                                        icon=icons.DELETE,
                                        icon_color=colors.ERROR,
                                        tooltip="Supprimer",
                                        on_click=self.delete_motor_handler,
                                        data=motor[0]
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=4,
                            )
                        ),
                        DataCell(Text(
                            motor[0],
                            style=self.themer.get_text_style("body_medium"),
                            weight=FontWeight.W_600,
                        )),  # ID
                        DataCell(Text(
                            motor[1],
                            style=self.themer.get_text_style("body_medium"),
                            weight=FontWeight.W_500,
                        )),  # Marque
                        DataCell(Text(
                            str(motor[2]),
                            style=self.themer.get_text_style("body_medium"),
                        )),  # Modèle
                        DataCell(Text(
                            str(motor[3]),
                            style=self.themer.get_text_style("body_medium"),
                        )),  # Année
                        DataCell(Text(
                            f"{motor[4]:,} km" if motor[4] else "N/A",
                            style=self.themer.get_text_style("body_medium"),
                        )),  # Kilométrage
                        DataCell(Text(
                            formatted_price,
                            style=self.themer.get_text_style("body_medium"),
                            weight=FontWeight.W_600,
                            color=colors.PRIMARY,
                        )),  # Prix
                        DataCell(Text(
                            description,
                            style=self.themer.get_text_style("body_small"),
                            overflow=TextOverflow.ELLIPSIS,
                        )),  # Description
                        DataCell(status_display),  # Statut
                        DataCell(Text(
                            formatted_date,
                            style=self.themer.get_text_style("body_small"),
                            color=colors.ON_SURFACE_VARIANT,
                        )),  # Date
                        DataCell(Text(
                            motor[9],
                            style=self.themer.get_text_style("body_medium"),
                        )),  # Fournisseur
                        DataCell(Text(
                            motor[10],
                            style=self.themer.get_text_style("body_medium"),
                        )),  # BL - Facture
                    ],
                )
            )

        self.page.update()



    def update(self) -> None:
        if self.is_mounted:
            super().update()

    def is_mounted(self) -> bool:
        if self.page is None:
            return False
        for view in self.page.views:
            for control in view.controls:
                if self == control.content:
                    return True
        return False

    def did_mount(self):
        self.is_mounted = True

    def will_unmount(self):
        self.is_mounted = False