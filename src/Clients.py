from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster
from db import *

class Clients:
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):
        
        super().__init__()        
        
        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True
        
        self.page_name = "Mallouka Motors - Clients"
        self.icon = Icons.PERSON
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame
        
        # Enhanced form fields with consistent styling
        input_style = self.themer.get_input_style()

        self.client_add_title = self.themer.create_section_title("Ajouter un Client")

        self.client_name = TextField(
            label="Nom Complet",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.PERSON,
        )
        self.client_address = TextField(
            label="Adresse",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.LOCATION_ON,
        )
        self.client_number = TextField(
            label="Numéro de Téléphone",
            col={"md": 6},
            input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
            prefix_text="+216",
            **input_style,
            prefix_icon=icons.PHONE,
        )
        self.client_mf = TextField(
            label="Matricule Fiscal (MF)",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.BUSINESS_CENTER,
        )

        self.client_list_title = self.themer.create_section_title("Liste des Clients")

        search_input_style = self.themer.get_input_style()
        self.search_bar = ResponsiveRow(
            controls=[
                TextField(
                    label="Rechercher des clients",
                    on_change=self.on_search_change,
                    col={"md": 8, "lg": 6},
                    **search_input_style,
                    prefix_icon=icons.SEARCH,
                    hint_text="Rechercher par nom, adresse, numéro...",
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )
        
        
        self.clients_data_table = DataTable(
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
                        "ID",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Nom Complet",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Adresse",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Numéro de Téléphone",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Matricule Fiscal",
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
        
        self.edit_client_id = None
        
        self.clients_frame = self.make_frame()
        
        self.controls = [
            self.clients_frame,
            self.upperbar,
        ]
        
        self.load_clients()

    def make_frame(self):
        self.clients_frame = SafeArea(
            content=Column(
                controls=[
                    # Add Client Form Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.client_add_title,
                                Container(height=24),
                                ResponsiveRow(
                                    [
                                        self.client_name,
                                        self.client_address,
                                        self.client_number,
                                        self.client_mf,
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    run_spacing=20,
                                ),
                                Container(height=24),
                                ResponsiveRow(
                                    controls=[
                                        Container(
                                            content=ElevatedButton(
                                                text="Ajouter le Client",
                                                icon=Icons.ADD,
                                                style=self.themer.get_button_style("primary"),
                                                on_click=self.add_client,
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

                    # Clients List Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.client_list_title,
                                Container(height=24),
                                self.search_bar,
                                Container(height=24),
                                Container(
                                    content=Row(
                                        controls=[
                                            self.clients_data_table,
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

        return self.clients_frame

    def clear_form(self, e=None):
        """Clear all form fields and set focus to first field"""
        self.client_name.value = ""
        self.client_address.value = ""
        self.client_number.value = ""
        self.client_mf.value = ""

        # Set focus to the first input field for better UX (only if control is mounted)
        try:
            if self.is_mounted():
                self.client_name.focus()
        except:
            pass  # Ignore focus errors if control is not ready

        if self.is_mounted():
            self.page.show_snack_bar(SnackBar(Text("Formulaire vidé")))
        self.page.update()

    def add_client(self, e):
        client_data = {
            "client_name": self.client_name.value,
            "client_address": self.client_address.value,
            "client_number": self.client_number.value,
            "client_mf": self.client_mf.value,
        }
        
        # add new client
        insert_client_data = (
            client_data["client_name"],
            client_data["client_address"],
            client_data["client_number"],
            client_data["client_mf"],
        )
        
        insert_client(insert_client_data)
        self.page.show_snack_bar(SnackBar(Text("Client ajouté avec succès !")))

        self.clear_form()
        self.load_clients()

        # Refresh billing page client dropdown if it exists
        if hasattr(self.parent_class, 'billing') and self.parent_class.billing:
            self.parent_class.billing._load_clients_for_dropdown()

        # Refresh dashboard statistics instantly with async update
        if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
            self.parent_class.dashboard.refresh_dashboard_async()

        self.page.update()
        
    def on_search_change(self, e):
        query = e.control.value
        self.load_clients(query)
        
    def create_enhanced_client_form(self, form_fields):
        """
        Create an enhanced client form with modern styling and validation.

        Args:
            form_fields: Current client data

        Returns:
            Column: Enhanced form with validation
        """
        # Create form fields with enhanced styling
        form_controls = [
            self.themer.create_enhanced_form_field(
                label="Nom Complet",
                value=form_fields[0],
                field_type="text",
                prefix_icon=icons.PERSON,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Adresse",
                value=form_fields[1],
                field_type="text",
                prefix_icon=icons.LOCATION_ON,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Numéro de Téléphone",
                value=form_fields[2],
                field_type="number",
                prefix_icon=icons.PHONE,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Matricule Fiscal (MF)",
                value=form_fields[3],
                field_type="text",
                prefix_icon=icons.BADGE,
                required=False
            ),
        ]

        return Column(
            controls=form_controls,
            spacing=0,
            scroll=ScrollMode.AUTO,
            expand=True,
        )
        
    def open_update_dialog(self, client_id):
        """
        Open enhanced update dialog for client with modern styling and validation.

        Args:
            client_id: ID of the client to update
        """
        try:
            self.edit_client_id = client_id
            client = get_client_by_id(client_id)

            if not client:
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.ERROR, color=colors.WHITE),
                        Text("Client non trouvé", color=colors.WHITE),
                    ]),
                    bgcolor=colors.RED_500
                ))
                return

            # Create enhanced form
            client_form = self.create_enhanced_client_form(client)

            # Create enhanced dialog with modern styling
            actions = [
                TextButton(text="Annuler", on_click=lambda _: self._close_dialog_with_animation()),
                TextButton(text="Mettre à jour", on_click=lambda _: self._handle_client_update(client_form)),
            ]

            self.page.dialog = self.themer.create_enhanced_modal_dialog(
                title="Mettre à jour le Client",
                content=client_form,
                actions=actions,
                width=500,
                height=600
            )

            self.page.update()

        except Exception as e:
            print(f"Error opening client update dialog: {e}")
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
        self.edit_client_id = None

    def _handle_client_update(self, form_container):
        """
        Handle client update with enhanced validation and feedback.

        Args:
            form_container: Container with form fields
        """
        try:
            # Show loading indicator
            self._show_loading_overlay("Mise à jour en cours...")

            # Extract form data with validation
            form_data = self._extract_client_form_data(form_container)

            if not self._validate_client_data(form_data):
                self._hide_loading_overlay()
                return

            # Update client in database
            self._update_client_in_database(form_data)

            # Hide loading and show success
            self._hide_loading_overlay()
            self._show_success_message(f"Client {form_data['client_name']} mis à jour avec succès!")

            # Close dialog and refresh data
            self._close_dialog_with_animation()
            self._refresh_all_data()

        except Exception as e:
            self._hide_loading_overlay()
            self._show_error_message(f"Erreur lors de la mise à jour: {str(e)}")
            print(f"Error updating client: {e}")

    def _show_loading_overlay(self, message):
        """Show loading overlay in dialog."""
        if self.page.dialog:
            loading_overlay = self.themer.create_loading_overlay(message)
            self.page.dialog.content = loading_overlay
            self.page.update()

    def _hide_loading_overlay(self):
        """Hide loading overlay and restore form."""
        if self.page.dialog and self.edit_client_id:
            client = get_client_by_id(self.edit_client_id)
            if client:
                client_form = self.create_enhanced_client_form(client)
                self.page.dialog.content = Container(
                    content=client_form,
                    padding=padding.all(20),
                    border_radius=self.themer.border_radius,
                    bgcolor=colors.SURFACE_VARIANT,
                    border=border.all(1, colors.OUTLINE_VARIANT),
                )
                self.page.update()
            
    def _extract_client_form_data(self, form_container):
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
            client_data = {
                "client_name": self._get_field_value(form_controls[0]),
                "client_address": self._get_field_value(form_controls[1]),
                "client_number": self._get_field_value(form_controls[2]),
                "client_mf": self._get_field_value(form_controls[3]),
            }

            return client_data

        except Exception as e:
            print(f"Error extracting client form data: {e}")
            raise ValueError("Erreur lors de l'extraction des données du formulaire")

    def _get_field_value(self, field_container):
        """Extract value from enhanced form field container."""
        try:
            # Navigate through container to get the actual field
            field = field_container.content
            return field.value if hasattr(field, 'value') else ""
        except:
            return ""

    def _validate_client_data(self, client_data):
        """
        Validate client form data with user feedback.

        Args:
            client_data (dict): Client data to validate

        Returns:
            bool: True if valid, False otherwise
        """
        errors = []

        # Required field validation
        if not client_data.get("client_name", "").strip():
            errors.append("Le nom complet est obligatoire")

        # Phone number validation
        phone = client_data.get("client_number", "").strip()
        if phone and not phone.isdigit():
            errors.append("Le numéro de téléphone doit contenir uniquement des chiffres")

        if phone and len(phone) < 8:
            errors.append("Le numéro de téléphone doit contenir au moins 8 chiffres")

        # Email validation (basic)
        email = client_data.get("client_email", "").strip()
        if email and "@" not in email:
            errors.append("L'adresse email n'est pas valide")

        # Show errors if any
        if errors:
            error_message = "Erreurs de validation:\n" + "\n".join(f"• {error}" for error in errors)
            self._show_error_message(error_message)
            return False

        return True

    def _update_client_in_database(self, client_data):
        """
        Update client in database with proper error handling.

        Args:
            client_data (dict): Validated client data
        """
        try:
            update_client_data = (
                client_data["client_name"],
                client_data["client_address"],
                client_data["client_number"],
                client_data["client_mf"],
                self.edit_client_id,
            )

            update_client(update_client_data)

        except Exception as e:
            print(f"Database update error: {e}")
            raise ValueError("Erreur lors de la mise à jour en base de données")

    def _refresh_all_data(self):
        """Refresh all related data after client update."""
        try:
            # Refresh clients table
            self.load_clients()

            # Refresh billing page client dropdowns if it exists
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
        client_id = e
        delete_client(client_id)
        self.page.show_snack_bar(SnackBar(Text("Client supprimé avec succès")))
        self.load_clients()

        # Refresh dashboard statistics instantly with async update
        if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
            self.parent_class.dashboard.refresh_dashboard_async()

        self.page.close_dialog()
        self.page.update()
        
    def delete_client_handler(self, e):
        client_id = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text("Supprimer le Client", size=24, weight='bold'),
            content=Text("Êtes-vous sûr de vouloir supprimer ce client ?"),
            actions=[
                TextButton(text="Annuler", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Supprimer", on_click=lambda _: self.confirm_delete(client_id)),
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True,
            scrollable=True,
        )
        self.page.update()
        
    
    def load_clients(self, query=""):
        
        if query:
            clients = search_clients(query)
        else:
            clients = fetch_clients()
            
        self.clients_data_table.rows.clear()
        
        for client in clients:
            # Create enhanced client name display
            client_name_display = Container(
                content=Row([
                    Icon(icons.PERSON, size=16, color=colors.PRIMARY),
                    Text(
                        client[1],
                        style=self.themer.get_text_style("body_medium"),
                        weight=FontWeight.W_500,
                        color=colors.ON_SURFACE,
                        overflow=TextOverflow.ELLIPSIS,
                    ),
                ], spacing=8, tight=True),
                padding=padding.symmetric(horizontal=8, vertical=4),
            )

            # Format phone number
            phone_display = Text(
                client[3] if client[3] else "N/A",
                style=self.themer.get_text_style("body_medium"),
                color=colors.ON_SURFACE_VARIANT,
            )

            # Truncate address if too long
            address = client[2][:40] + "..." if len(str(client[2])) > 40 else str(client[2])

            self.clients_data_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Row(
                                [
                                    IconButton(
                                        icon=Icons.EDIT,
                                        icon_color=colors.PRIMARY,
                                        tooltip="Modifier",
                                        on_click=lambda e, client_id=client[0]: self.open_update_dialog(client_id),
                                        data=client[0]
                                    ),
                                    IconButton(
                                        icon=icons.DELETE,
                                        icon_color=colors.ERROR,
                                        tooltip="Supprimer",
                                        on_click=self.delete_client_handler,
                                        data=client[0]
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=4,
                            )
                        ),
                        DataCell(Text(
                            str(client[0]),
                            style=self.themer.get_text_style("body_medium"),
                            weight=FontWeight.W_600,
                        )),  # ID
                        DataCell(client_name_display),  # Nom Complet with icon
                        DataCell(Text(
                            address,
                            style=self.themer.get_text_style("body_medium"),
                            overflow=TextOverflow.ELLIPSIS,
                        )),  # Adresse
                        DataCell(phone_display),  # Numéro
                        DataCell(Text(
                            client[4] if client[4] else "N/A",
                            style=self.themer.get_text_style("body_medium"),
                            color=colors.ON_SURFACE_VARIANT,
                        )),  # MF
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