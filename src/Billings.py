import os
from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster
from db import *
from billing_generator import generate_billing_pdf

class Billings:
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):

        super().__init__()

        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True

        self.page_name = "Mallouka Motors - Factures"
        self.icon = Icons.PAYMENT
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame

        # Enhanced form fields with consistent styling
        input_style = self.themer.get_input_style()

        self.billing_add_title = self.themer.create_section_title("Créer une Facture")

        self.billing_ref = TextField(
            label="Référence de Facture",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.RECEIPT_LONG,
            hint_text="Ex: FAC-2024-001",
        )
        self.prix_totale = TextField(
            label="Prix Total",
            col={"md": 4},
            read_only=True,
            **input_style,
            prefix_icon=icons.ATTACH_MONEY,
            suffix_text="DT",
            bgcolor=colors.SURFACE_VARIANT,
        )
        self.mode_paiement = TextField(
            label="Mode de Paiement",
            col={"md": 4},
            **input_style,
            prefix_icon=icons.PAYMENT,
            hint_text="Ex: Espèces, Chèque, Virement",
        )
        self.description = TextField(
            label="Description",
            multiline=True,
            col={"md": 12},
            min_lines=3,
            max_lines=5,
            **input_style,
            prefix_icon=icons.DESCRIPTION,
            hint_text="Description détaillée de la facture...",
        )
        self.transporteur = TextField(
            label="Transporteur",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.LOCAL_SHIPPING,
            hint_text="Nom du transporteur",
        )
        self.matricule = TextField(
            label="Matricule",
            col={"md": 6},
            **input_style,
            prefix_icon=icons.CONFIRMATION_NUMBER,
            hint_text="Matricule du véhicule",
        )

        self.client_dropdown = Dropdown(
            label="Client",
            col={"md": 4},
            options=[],
            **input_style,
            prefix_icon=icons.PERSON,
            hint_text="Sélectionner un client",
        )
        self.motor_rows = []
        self.motors_column = Column(spacing=12)
        self.add_motor_button = IconButton(
            icon=Icons.ADD,
            style=ButtonStyle(
                shape=CircleBorder(),
                bgcolor=colors.PRIMARY,
                color=colors.ON_PRIMARY,
                padding=12,
            ),
            tooltip="Ajouter un moteur",
            on_click=self.add_new_motor_row,
        )

        self.billing_list_title = self.themer.create_section_title("Liste des Factures")

        search_input_style = self.themer.get_input_style()
        self.search_bar = ResponsiveRow(
            controls=[
                TextField(
                    label="Rechercher des factures",
                    on_change=self.on_search_change,
                    col={"md": 8, "lg": 6},
                    **search_input_style,
                    prefix_icon=icons.SEARCH,
                    hint_text="Rechercher par référence, client, mode de paiement...",
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

        self.billings_data_table = DataTable(
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
                        "Référence",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Prix Total (DT)",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Client",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Mode Paiement",
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
                        "Transporteur",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Matricule",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Date",
                        style=self.themer.get_text_style("label_large"),
                        weight=FontWeight.W_700,
                        color=colors.PRIMARY,
                    )
                ),
                DataColumn(
                    Text(
                        "Moteurs Associés",
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

        self.edit_billing_ref = None

        self.billing_frame = self.make_frame()

        self.controls = [
            self.billing_frame,
            self.upperbar,
        ]

        self.load_billings()
        self._load_clients_for_dropdown()
        self.add_new_motor_row()

    def _load_clients_for_dropdown(self):
        clients = get_all_clients_with_names()
        self.client_dropdown.options.clear()
        for client_id, client_name in clients:
            self.client_dropdown.options.append(dropdown.Option(key=client_id, text=client_name))
        self.page.update()

    def add_new_motor_row(self, e=None):
        available_motors = get_all_motors()
        motor_options = [dropdown.Option(key=motor['id'], text=f"{motor['id']} - {motor['marque']}") for motor in available_motors]

        input_style = self.themer.get_input_style()

        motor_id_dropdown = Dropdown(
            label="Moteur",
            options=motor_options,
            col={"xs": 12, "sm": 6, "md": 4, "lg": 4},
            on_change=self._calculate_total_price_dynamic,
            **input_style,
            prefix_icon=icons.SETTINGS,
            hint_text="Sélectionner un moteur",
        )
        quantity_field = TextField(
            label="Quantité",
            value="1",
            col={"xs": 6, "sm": 3, "md": 2, "lg": 2},
            keyboard_type=KeyboardType.NUMBER,
            on_change=self._calculate_total_price_dynamic,
            **input_style,
            prefix_icon=icons.NUMBERS,
        )
        delete_button = IconButton(
            icon=icons.DELETE,
            style=ButtonStyle(
                shape=CircleBorder(),
                bgcolor=colors.with_opacity(0.1, colors.ERROR),
                color=colors.ERROR,
                padding=8,
            ),
            tooltip="Supprimer cette ligne",
            on_click=self.delete_motor_row,
            data=len(self.motor_rows)
        )

        # Create a card container for each motor row
        motor_row_content = ResponsiveRow(
            controls=[
                motor_id_dropdown,
                quantity_field,
                Container(
                    content=delete_button,
                    col={"xs": 6, "sm": 3, "md": 2, "lg": 1},
                    alignment=alignment.center,
                ),
            ],
            alignment=MainAxisAlignment.START,
            spacing=12,
        )

        card_style = self.themer.get_card_style(elevated=False)
        motor_row_card = Container(
            content=motor_row_content,
            bgcolor=card_style["bgcolor"],
            border_radius=card_style["border_radius"],
            border=card_style.get("border"),
            padding=16,
            margin=margin.only(bottom=8),
        )

        self.motor_rows.append(motor_row_card)
        self.motors_column.controls.clear()
        self.motors_column.controls.extend(self.motor_rows)

        # Add the "Add Motor" button at the end
        add_button_container = Container(
            content=Row([
                self.add_motor_button,
                Text(
                    "Ajouter un moteur",
                    style=self.themer.get_text_style("body_medium"),
                    color=colors.PRIMARY,
                ),
            ], spacing=8),
            alignment=alignment.center_left,
            margin=margin.only(top=8),
        )
        self.motors_column.controls.append(add_button_container)

        self.page.update()

    def delete_motor_row(self, e):
        index_to_delete = e.control.data
        if 0 <= index_to_delete < len(self.motor_rows):
            del self.motor_rows[index_to_delete]
            self.motors_column.controls.clear()

            # Re-add all motor rows with updated indices
            for i, row in enumerate(self.motor_rows):
                # Update the delete button's data index
                delete_btn = row.content.controls[2].content  # Navigate to the delete button
                delete_btn.data = i
                self.motors_column.controls.append(row)

            # Add the "Add Motor" button at the end
            add_button_container = Container(
                content=Row([
                    self.add_motor_button,
                    Text(
                        "Ajouter un moteur",
                        style=self.themer.get_text_style("body_medium"),
                        color=colors.PRIMARY,
                    ),
                ], spacing=8),
                alignment=alignment.center_left,
                margin=margin.only(top=8),
            )
            self.motors_column.controls.append(add_button_container)

            self._calculate_total_price_dynamic()
            self.page.update()

    def _calculate_total_price_dynamic(self, e=None):
        total = 0.0
        for row in self.motor_rows:
            # Navigate through the card structure to get the dropdown and text field
            row_controls = row.content.controls  # ResponsiveRow controls
            motor_id_dropdown = row_controls[0]  # First control is the dropdown
            quantity_field = row_controls[1]     # Second control is the quantity field

            if motor_id_dropdown.value and quantity_field.value:
                try:
                    price = get_motor_price(motor_id_dropdown.value)
                    quantity = int(quantity_field.value)
                    total += price * quantity
                except (ValueError, TypeError):
                    continue  # Skip invalid entries

        self.prix_totale.value = f"{total:.2f}"
        self.page.update()

    def make_frame(self):
        self.billing_frame = SafeArea(
            content=Column(
                controls=[
                    # Add Billing Form Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.billing_add_title,
                                Container(height=24),

                                # Basic Information
                                ResponsiveRow(
                                    [
                                        self.billing_ref,
                                        self.prix_totale,
                                        self.client_dropdown,
                                        self.mode_paiement,
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    run_spacing=20,
                                ),

                                Container(height=20),

                                # Description
                                ResponsiveRow(
                                    [self.description],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    run_spacing=20,
                                ),

                                Container(height=20),

                                # Transport Information
                                ResponsiveRow(
                                    [
                                        self.transporteur,
                                        self.matricule,
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=20,
                                    run_spacing=20,
                                ),

                                Container(height=24),

                                # Motors Section
                                Text(
                                    "Moteurs",
                                    style=self.themer.get_text_style("title_medium"),
                                    color=colors.ON_SURFACE,
                                    weight=FontWeight.W_600,
                                ),
                                Container(height=16),
                                self.motors_column,

                                Container(height=24),

                                # Action Buttons
                                ResponsiveRow(
                                    controls=[
                                        Container(
                                            content=ElevatedButton(
                                                text="Créer la Facture",
                                                icon=Icons.ADD,
                                                style=self.themer.get_button_style("primary"),
                                                on_click=self.add_billing,
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

                    # Billings List Section
                    Container(
                        content=self.themer.create_card_container(
                            content=Column([
                                self.billing_list_title,
                                Container(height=24),
                                self.search_bar,
                                Container(height=24),
                                Container(
                                    content=Row(
                                        controls=[
                                            self.billings_data_table,
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

        return self.billing_frame

    def add_billing(self, e):
        if not self.billing_ref.value:
            self.page.show_snack_bar(SnackBar(Text("Veuillez entrer une référence de facturation.")))
            return
        if not self.client_dropdown.value:
            self.page.show_snack_bar(SnackBar(Text("Veuillez sélectionner un client.")))
            return

        # Validate that at least one motor is selected
        has_motors = False
        for row in self.motor_rows:
            row_controls = row.content.controls
            motor_id_dropdown = row_controls[0]
            quantity_field = row_controls[1]
            if motor_id_dropdown.value and quantity_field.value:
                has_motors = True
                break

        if not has_motors:
            self.page.show_snack_bar(SnackBar(Text("Veuillez sélectionner au moins un moteur.")))
            return

        billing_data = {
            "billing_ref": self.billing_ref.value,
            "total_price": float(self.prix_totale.value) if self.prix_totale.value else 0.0,
            "client_id": int(self.client_dropdown.value),
            "mode_paiement": self.mode_paiement.value,
            "description": self.description.value,
            "transporteur": self.transporteur.value,
            "matricule": self.matricule.value,
        }

        insert_billing_header_data = (
            billing_data["billing_ref"],
            billing_data["total_price"],
            billing_data["client_id"],
            billing_data["mode_paiement"],
            billing_data["description"],
            billing_data["transporteur"],
            billing_data["matricule"],
        )

        try:
            insert_billing(insert_billing_header_data)

            # Insert motor data with updated structure
            for row in self.motor_rows:
                row_controls = row.content.controls
                motor_id_dropdown = row_controls[0]
                quantity_field = row_controls[1]
                if motor_id_dropdown.value and quantity_field.value:
                    insert_Billing_Motors((billing_data["billing_ref"], motor_id_dropdown.value, int(quantity_field.value)))

            self.page.show_snack_bar(SnackBar(Text("Facture créée avec succès !")))
            self.clear_form()
            self.load_billings()
            self.refresh_data()  # Refresh all data

            # Refresh dashboard statistics instantly with async update
            if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
                self.parent_class.dashboard.refresh_dashboard_async()

            self.page.update()
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(f"Erreur lors de la création de la facture : {ex}")))

    def on_search_change(self, e):
        query = e.control.value
        self.load_billings(query)


    def form_dialog_column(self, billing_data, billing_motors_data):
        available_motors = get_all_motors()

        form_controls = [
            TextField(value=billing_data[0], label="ID - Référence", read_only=True, width=300),
            TextField(value=billing_data[1], label="Prix Totale", read_only=True, width=300),
            Dropdown(
                label="Client",
                options=[dropdown.Option(key=client[0], text=client[1]) for client in get_all_clients_with_names()],
                value=str(billing_data[2]),
                width=300
            ),
            TextField(value=billing_data[3], label="Mode Paiment", width=300),
            TextField(value=billing_data[4], label="Description", multiline=True, width=300),
            TextField(value=billing_data[5], label="transporteur", width=300),
            TextField(value=billing_data[6], label="matricule", width=300),
        ]

        edit_motor_rows = []
        edit_motors_column = Column()
        
        def _calculate_update_total_price_dynamic(e=None):
            total = 0.0
            for row in edit_motor_rows:
                motor_id_dropdown = row.controls[0]
                quantity_field = row.controls[1]
                if motor_id_dropdown.value and quantity_field.value:
                    price = get_motor_price(motor_id_dropdown.value)
                    quantity = int(quantity_field.value)
                    total += price * quantity
            form_controls[1].value = f"{total:.2f}"
            self.page.update()

        def add_new_edit_motor_row(e=None, motor_id=None, quantity=0):
            motor_options = [dropdown.Option(key=motor['id'], text=f"{motor['id']} - {motor['marque']}") for motor in available_motors]
            motor_dropdown = Dropdown(label="Motor ID", options=motor_options, col={"md": 3}, value=motor_id, on_change=_calculate_update_total_price_dynamic)
            quantity_field = TextField(label="Quantity", value=str(quantity), col={"md": 3}, keyboard_type=KeyboardType.NUMBER, on_change=_calculate_update_total_price_dynamic)
            delete_button = IconButton(icon=icons.DELETE, on_click=delete_edit_motor_row, col={"md": 3}, data=len(edit_motor_rows))

            motor_row = ResponsiveRow(
                controls=[
                    motor_dropdown, 
                    quantity_field, 
                    delete_button,
                ], 
                alignment=MainAxisAlignment.SPACE_BETWEEN
            )
            edit_motor_rows.append(motor_row)
            edit_motors_column.controls.append(motor_row)
            self.page.update()

        def delete_edit_motor_row(e):
            index_to_delete = e.control.data
            if 0 <= index_to_delete < len(edit_motor_rows):
                del edit_motor_rows[index_to_delete]
                edit_motors_column.controls.clear()
                for i, row in enumerate(edit_motor_rows):
                    row.controls[-1].data = i
                    edit_motors_column.controls.append(row)
                self.page.update()

        # Populate existing motors
        for motor in billing_motors_data:
            print(motor)
            add_new_edit_motor_row(motor_id=motor[0], quantity=motor[1])

        add_motor_button = IconButton(icon=icons.ADD, on_click=add_new_edit_motor_row)
        edit_motors_column.controls.append(add_motor_button)

        form_controls.append(Text("Related Motors", weight="bold"))
        form_controls.append(edit_motors_column)

        return Column(controls=form_controls, width=400, scroll="adaptive")   
    
    def open_update_dialog(self, billing_ref):
        """
        Open completely redesigned update dialog for billing with full functionality.

        Args:
            billing_ref: Reference of the billing to update
        """
        try:
            self.edit_billing_ref = billing_ref
            billing_data = get_billing_by_ref(billing_ref)
            billing_motors_data = get_related_motors(billing_ref)

            if not billing_data:
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.ERROR, color=colors.WHITE),
                        Text("Facture non trouvée", color=colors.WHITE),
                    ]),
                    bgcolor=colors.RED_500
                ))
                return

            # Initialize motor rows tracking
            self.update_motor_rows = []
            self.update_total_price_field = None

            # Create the complete update form
            update_form = self._create_complete_billing_update_form(billing_data, billing_motors_data)

            # Create dialog actions
            actions = [
                TextButton(
                    text="Annuler",
                    on_click=lambda _: self._close_update_dialog(),
                    style=self.themer.get_button_style("secondary")
                ),
                TextButton(
                    text="Mettre à jour",
                    on_click=lambda _: self._save_billing_update(),
                    style=self.themer.get_button_style("primary")
                ),
            ]

            # Create and show dialog
            self.page.dialog = self.themer.create_enhanced_modal_dialog(
                title="Mettre à jour la Facture",
                content=update_form,
                actions=actions,
                width=800,
                height=900
            )

            self.page.dialog.open = True
            self.page.update()

            # Calculate initial total price
            self._update_total_price()

        except Exception as e:
            print(f"Error opening billing update dialog: {e}")
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    Icon(icons.ERROR, color=colors.WHITE),
                    Text(f"Erreur: {str(e)}", color=colors.WHITE),
                ]),
                bgcolor=colors.RED_500
            ))

    def _create_complete_billing_update_form(self, billing_data, billing_motors_data):
        """
        Create a complete, fully functional billing update form.

        Args:
            billing_data: Current billing data
            billing_motors_data: Related motors data

        Returns:
            Container: Complete update form
        """
        # Create form fields with direct references for easy access
        self.update_ref_field = self.themer.create_enhanced_form_field(
            label="Référence",
            value=billing_data[0],
            field_type="text",
            read_only=True,
            prefix_icon=icons.TAG,
            required=True
        )

        self.update_total_price_field = self.themer.create_enhanced_form_field(
            label="Prix Total (DT)",
            value=str(billing_data[1]),
            field_type="number",
            read_only=True,
            prefix_icon=icons.ATTACH_MONEY,
            required=True
        )

        self.update_client_field = self.themer.create_enhanced_form_field(
            label="Client",
            value=str(billing_data[2]),
            field_type="dropdown",
            options=[(str(client[0]), client[1]) for client in get_all_clients_with_names()],
            prefix_icon=icons.PERSON,
            required=True
        )

        self.update_payment_field = self.themer.create_enhanced_form_field(
            label="Mode de Paiement",
            value=billing_data[3],
            field_type="dropdown",
            options=[
                ("Espèce", "💵 Espèce"),
                ("Chèque", "📝 Chèque"),
                ("Virement", "🏦 Virement"),
                ("Carte", "💳 Carte")
            ],
            prefix_icon=icons.PAYMENT,
            required=True
        )

        self.update_description_field = self.themer.create_enhanced_form_field(
            label="Description",
            value=billing_data[4],
            field_type="text",
            multiline=True,
            prefix_icon=icons.DESCRIPTION,
            required=False
        )

        self.update_transporteur_field = self.themer.create_enhanced_form_field(
            label="Transporteur",
            value=billing_data[5],
            field_type="text",
            prefix_icon=icons.LOCAL_SHIPPING,
            required=False
        )

        self.update_matricule_field = self.themer.create_enhanced_form_field(
            label="Matricule",
            value=billing_data[6],
            field_type="text",
            prefix_icon=icons.CONFIRMATION_NUMBER,
            required=False
        )

        # Create motors section
        motors_section = self._create_motors_section(billing_motors_data)

        # Combine all form elements
        form_content = Column([
            self.update_ref_field,
            self.update_total_price_field,
            self.update_client_field,
            self.update_payment_field,
            self.update_description_field,
            self.update_transporteur_field,
            self.update_matricule_field,
            motors_section,
        ], spacing=16, scroll=ScrollMode.AUTO, expand=True)

        return Container(
            content=form_content,
            padding=padding.all(20),
            expand=True
        )

    def create_enhanced_billing_form(self, billing_data, billing_motors_data):
        """
        Create an enhanced billing form with modern styling and validation.

        Args:
            billing_data: Current billing data
            billing_motors_data: Related motors data

        Returns:
            Column: Enhanced form with validation
        """
        # Create basic form fields with enhanced styling
        form_controls = [
            self.themer.create_enhanced_form_field(
                label="Référence",
                value=billing_data[0],
                field_type="text",
                read_only=True,
                prefix_icon=icons.TAG,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Prix Total (DT)",
                value=billing_data[1],
                field_type="number",
                read_only=True,
                prefix_icon=icons.ATTACH_MONEY,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Client",
                value=str(billing_data[2]),
                field_type="dropdown",
                options=[(str(client[0]), client[1]) for client in get_all_clients_with_names()],
                prefix_icon=icons.PERSON,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Mode de Paiement",
                value=billing_data[3],
                field_type="dropdown",
                options=["Espèce", "Chèque", "Virement", "Carte"],
                prefix_icon=icons.PAYMENT,
                required=True
            ),
            self.themer.create_enhanced_form_field(
                label="Description",
                value=billing_data[4],
                field_type="text",
                multiline=True,
                prefix_icon=icons.DESCRIPTION,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Transporteur",
                value=billing_data[5],
                field_type="text",
                prefix_icon=icons.LOCAL_SHIPPING,
                required=False
            ),
            self.themer.create_enhanced_form_field(
                label="Matricule",
                value=billing_data[6],
                field_type="text",
                prefix_icon=icons.CONFIRMATION_NUMBER,
                required=False
            ),
        ]

        # Add motors section
        motors_section = self._create_enhanced_motors_section(billing_motors_data)
        form_controls.extend(motors_section)

        return Column(
            controls=form_controls,
            spacing=0,
            scroll=ScrollMode.AUTO,
            expand=True,
        )

    def _create_motors_section(self, billing_motors_data):
        """
        Create a completely functional motors section with real-time price calculation.

        Args:
            billing_motors_data: Current motors data

        Returns:
            Container: Motors section container
        """
        # Initialize motor rows tracking
        self.update_motor_rows = []

        # Motors section header
        motors_header = Container(
            content=Row([
                Icon(icons.CAR_REPAIR, color=colors.PRIMARY, size=24),
                Text(
                    "Moteurs Associés",
                    style=self.themer.get_text_style("headline_small"),
                    weight=FontWeight.W_600,
                    color=colors.ON_SURFACE,
                ),
            ], spacing=12),
            margin=margin.only(top=20, bottom=16),
        )

        # Motors container for dynamic content
        self.motors_container = Column(spacing=12)

        # Create motor rows for existing data
        for motor in billing_motors_data:
            motor_row = self._create_motor_row(motor[0], motor[1])
            self.motors_container.controls.append(motor_row)
            self.update_motor_rows.append(motor_row)

        # Ensure at least one motor row exists
        if not billing_motors_data:
            empty_row = self._create_motor_row()
            self.motors_container.controls.append(empty_row)
            self.update_motor_rows.append(empty_row)

        # Add motor button
        add_motor_button = Container(
            content=ElevatedButton(
                text="Ajouter un Moteur",
                icon=icons.ADD,
                style=self.themer.get_button_style("outline"),
                on_click=self._add_motor_row,
            ),
            margin=margin.only(top=16),
        )

        # Combine all motor section elements
        motors_section_content = Column([
            motors_header,
            self.motors_container,
            add_motor_button,
        ], spacing=0)

        return Container(
            content=motors_section_content,
            margin=margin.only(top=20),
            padding=padding.all(16),
            border=border.all(1, colors.OUTLINE_VARIANT),
            border_radius=self.themer.border_radius,
            bgcolor=colors.SURFACE_VARIANT,
        )

    def _create_motor_row(self, motor_id=None, quantity=0):
        """
        Create a single motor row with real-time price calculation.

        Args:
            motor_id: Motor ID to pre-select
            quantity: Quantity to pre-fill

        Returns:
            Container: Motor row container
        """
        # Get available motors
        available_motors = get_all_motors()
        motor_options = [(motor['id'], f"{motor['id']} - {motor['marque']}") for motor in available_motors]

        # Create motor dropdown
        motor_dropdown = self.themer.create_enhanced_form_field(
            label="Moteur",
            value=str(motor_id) if motor_id else "",
            field_type="dropdown",
            options=motor_options,
            prefix_icon=icons.CAR_REPAIR,
            required=True
        )

        # Create quantity field
        quantity_field = self.themer.create_enhanced_form_field(
            label="Quantité",
            value=str(quantity) if quantity > 0 else "1",
            field_type="number",
            prefix_icon=icons.NUMBERS,
            required=True
        )

        # Add change event handlers for real-time price calculation
        motor_dropdown.content.on_change = lambda _: self._update_total_price()
        quantity_field.content.on_change = lambda _: self._update_total_price()

        # Create delete button
        delete_button = IconButton(
            icon=icons.DELETE,
            icon_color=colors.ERROR,
            tooltip="Supprimer cette ligne",
            on_click=lambda _: self._remove_motor_row(motor_row),
        )

        # Create motor row container
        motor_row = Container(
            content=Row([
                Container(content=motor_dropdown, expand=2),
                Container(content=quantity_field, expand=1),
                Container(content=delete_button, width=50),
            ], spacing=12),
            margin=margin.only(bottom=12),
            padding=padding.all(16),
            border=border.all(1, colors.OUTLINE_VARIANT),
            border_radius=self.themer.border_radius,
            bgcolor=colors.SURFACE,
            animate_opacity=300,
            animate_scale=300,
        )

        # Store references for easy access
        motor_row.motor_dropdown = motor_dropdown.content
        motor_row.quantity_field = quantity_field.content
        motor_row.delete_button = delete_button

        return motor_row

    def _add_motor_row(self, _=None):
        """Add a new motor row to the form."""
        try:
            # Create new motor row
            new_row = self._create_motor_row()

            # Add to containers
            self.motors_container.controls.append(new_row)
            self.update_motor_rows.append(new_row)

            # Update UI and recalculate price
            self.page.update()
            self._update_total_price()

        except Exception as e:
            print(f"Error adding motor row: {e}")

    def _remove_motor_row(self, row_to_remove):
        """Remove a motor row from the form."""
        try:
            # Ensure at least one motor row remains
            if len(self.update_motor_rows) <= 1:
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.WARNING, color=colors.WHITE),
                        Text("Au moins un moteur doit être présent", color=colors.WHITE),
                    ]),
                    bgcolor=colors.ORANGE_500
                ))
                return

            # Remove from containers
            if row_to_remove in self.motors_container.controls:
                self.motors_container.controls.remove(row_to_remove)
            if row_to_remove in self.update_motor_rows:
                self.update_motor_rows.remove(row_to_remove)

            # Update UI and recalculate price
            self.page.update()
            self._update_total_price()

        except Exception as e:
            print(f"Error removing motor row: {e}")

    def _update_total_price(self):
        """Update the total price based on selected motors and quantities."""
        try:
            total = 0.0

            for motor_row in self.update_motor_rows:
                motor_id = motor_row.motor_dropdown.value
                quantity_str = motor_row.quantity_field.value

                if motor_id and quantity_str and str(quantity_str).isdigit():
                    quantity = int(quantity_str)
                    if quantity > 0:
                        price = get_motor_price(motor_id)
                        total += price * quantity

            # Update the total price field
            if hasattr(self, 'update_total_price_field'):
                self.update_total_price_field.content.value = f"{total:.2f}"
                self.page.update()

        except Exception as e:
            print(f"Error updating total price: {e}")

    def _close_update_dialog(self):
        """Close the update dialog."""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.edit_billing_ref = None

    def _save_billing_update(self):
        """Save the billing update with validation."""
        try:
            # Validate form data
            if not self._validate_update_form():
                return

            # Show loading
            self._show_loading_message("Mise à jour en cours...")

            # Extract and save data
            billing_data = self._extract_update_form_data()
            self._update_billing_database(billing_data)

            # Show success and close
            self._show_success_message(f"Facture {self.edit_billing_ref} mise à jour avec succès!")
            self._close_update_dialog()
            self._refresh_all_data()

        except Exception as e:
            print(f"Error saving billing update: {e}")
            self._show_error_message(f"Erreur lors de la mise à jour: {str(e)}")

    def _validate_update_form(self):
        """Validate the update form data."""
        errors = []

        # Validate client selection
        client_value = self.update_client_field.content.value
        if not client_value or client_value.strip() == "":
            errors.append("Le client est obligatoire")

        # Validate payment mode
        payment_value = self.update_payment_field.content.value
        if not payment_value or payment_value.strip() == "":
            errors.append("Le mode de paiement est obligatoire")

        # Validate motors
        valid_motors = 0
        for motor_row in self.update_motor_rows:
            motor_id = motor_row.motor_dropdown.value
            quantity_str = motor_row.quantity_field.value

            if motor_id and quantity_str and str(quantity_str).isdigit() and int(quantity_str) > 0:
                valid_motors += 1

        if valid_motors == 0:
            errors.append("Au moins un moteur avec une quantité valide est requis")

        # Show errors if any
        if errors:
            error_message = "Erreurs de validation:\n" + "\n".join(f"• {error}" for error in errors)
            self._show_error_message(error_message)
            return False

        return True

    def _extract_update_form_data(self):
        """Extract data from the update form."""
        # Extract basic billing data
        billing_data = {
            "billing_ref": self.edit_billing_ref,
            "total_price": self.update_total_price_field.content.value,
            "client_id": self.update_client_field.content.value,
            "mode_paiement": self.update_payment_field.content.value,
            "description": self.update_description_field.content.value,
            "transporteur": self.update_transporteur_field.content.value,
            "matricule": self.update_matricule_field.content.value,
        }

        # Extract motors data
        motors_data = []
        for motor_row in self.update_motor_rows:
            motor_id = motor_row.motor_dropdown.value
            quantity_str = motor_row.quantity_field.value

            if motor_id and quantity_str and str(quantity_str).isdigit() and int(quantity_str) > 0:
                motors_data.append((motor_id, int(quantity_str)))

        billing_data["motors"] = motors_data
        return billing_data

    def _update_billing_database(self, billing_data):
        """Update billing data in the database."""
        try:
            # Convert data types
            total_price = float(billing_data["total_price"]) if billing_data.get("total_price", "").strip() else 0.0
            client_id = int(billing_data["client_id"]) if billing_data.get("client_id", "").strip() else None

            # Update billing header
            update_billing_header_data = (
                total_price,
                client_id,
                billing_data["mode_paiement"],
                billing_data["description"],
                billing_data["transporteur"],
                billing_data["matricule"],
                self.edit_billing_ref,
            )
            update_billing(update_billing_header_data)

            # Update related motors
            delete_Billing_Motors_by_billing_ref(self.edit_billing_ref)

            # Insert new motors
            for motor_id, quantity in billing_data.get("motors", []):
                insert_Billing_Motors((self.edit_billing_ref, motor_id, quantity))

        except Exception as e:
            print(f"Database update error: {e}")
            raise ValueError("Erreur lors de la mise à jour en base de données")

    def _show_loading_message(self, message):
        """Show loading message."""
        self.page.show_snack_bar(SnackBar(
            content=Row([
                ProgressRing(width=16, height=16, stroke_width=2, color=colors.WHITE),
                Text(message, color=colors.WHITE),
            ]),
            bgcolor=colors.BLUE_500
        ))

    def _create_enhanced_motors_section(self, billing_motors_data):
        """
        Create enhanced motors section for billing form.

        Args:
            billing_motors_data: Current motors data

        Returns:
            list: List of motor-related form controls
        """
        motors_controls = []

        # Motors section header
        motors_header = Container(
            content=Row([
                Icon(icons.CAR_REPAIR, color=colors.PRIMARY),
                Text(
                    "Moteurs Associés",
                    style=self.themer.get_text_style("headline_small"),
                    weight=FontWeight.W_600,
                    color=colors.ON_SURFACE,
                ),
            ], spacing=12),
            margin=margin.only(top=20, bottom=10),
        )
        motors_controls.append(motors_header)

        # Store motor rows for dynamic updates
        self.edit_motor_rows = []

        # Create motor rows for existing data
        for motor in billing_motors_data:
            motor_row = self._create_enhanced_motor_row(motor[0], motor[1])
            motors_controls.append(motor_row)
            self.edit_motor_rows.append(motor_row)

        # If no existing motors, add one empty row
        if not billing_motors_data:
            empty_row = self._create_enhanced_motor_row()
            motors_controls.append(empty_row)
            self.edit_motor_rows.append(empty_row)

        # Store reference for initial price calculation
        self._should_calculate_initial_price = True

        # Add button for new motor rows
        def add_motor_row_handler(_):
            """Handle adding new motor row with proper form reference."""
            try:
                # Create new motor row
                new_row = self._create_enhanced_motor_row()

                # Add to edit_motor_rows list for tracking
                if not hasattr(self, 'edit_motor_rows'):
                    self.edit_motor_rows = []
                self.edit_motor_rows.append(new_row)

                # Insert before the add button (last control)
                motors_controls.insert(-1, new_row)

                # Update dialog content and recalculate price
                self.page.update()
                self._calculate_billing_total_price()

            except Exception as e:
                print(f"Error adding motor row: {e}")

        add_motor_button = Container(
            content=ElevatedButton(
                text="Ajouter un Moteur",
                icon=icons.ADD,
                style=self.themer.get_button_style("outline"),
                on_click=add_motor_row_handler,
            ),
            margin=margin.only(top=10),
        )
        motors_controls.append(add_motor_button)

        return motors_controls

    def _create_enhanced_motor_row(self, motor_id=None, quantity=0):
        """Create an enhanced motor row with modern styling and price calculation."""
        available_motors = get_all_motors()
        motor_options = [(motor['id'], f"{motor['id']} - {motor['marque']}") for motor in available_motors]

        # Create a unique identifier for this row
        row_id = f"motor_row_{len(self.edit_motor_rows) if hasattr(self, 'edit_motor_rows') else 0}"

        # Create motor dropdown with change handler
        motor_dropdown_container = Container()
        motor_dropdown = self.themer.create_enhanced_form_field(
            label="Moteur",
            value=str(motor_id) if motor_id else "",
            field_type="dropdown",
            options=motor_options,
            prefix_icon=icons.CAR_REPAIR,
            required=True
        )

        # Add change event handler to the actual dropdown field
        actual_dropdown = motor_dropdown.content
        actual_dropdown.on_change = lambda _: self._calculate_billing_total_price()
        motor_dropdown_container.content = motor_dropdown

        # Create quantity field with change handler
        quantity_field_container = Container()
        quantity_field = self.themer.create_enhanced_form_field(
            label="Quantité",
            value=str(quantity) if quantity > 0 else "1",
            field_type="number",
            prefix_icon=icons.NUMBERS,
            required=True
        )

        # Add change event handler to the actual text field
        actual_quantity_field = quantity_field.content
        actual_quantity_field.on_change = lambda _: self._calculate_billing_total_price()
        quantity_field_container.content = quantity_field

        delete_button = Container(
            content=IconButton(
                icon=icons.DELETE,
                icon_color=colors.ERROR,
                tooltip="Supprimer cette ligne",
                on_click=lambda _: self._remove_motor_row_from_form(row_id),
                data=row_id,
            ),
            margin=margin.only(top=20),
        )

        motor_row = Container(
            content=Row([
                Container(content=motor_dropdown_container, expand=2),
                Container(content=quantity_field_container, expand=1),
                delete_button,
            ], spacing=10),
            margin=margin.only(bottom=10),
            padding=padding.all(12),
            border=border.all(1, colors.OUTLINE_VARIANT),
            border_radius=self.themer.border_radius,
            bgcolor=colors.SURFACE_VARIANT,
            data=row_id,  # Store the row ID for identification
            animate_opacity=300,  # Add smooth animation
            animate_scale=300,
        )

        return motor_row

    def _calculate_billing_total_price(self):
        """Calculate total price based on selected motors and quantities in the billing update form."""
        try:
            if not hasattr(self, 'edit_motor_rows') or not self.page.dialog:
                return

            total = 0.0

            for motor_row in self.edit_motor_rows:
                try:
                    # Navigate through the enhanced container structure
                    row_content = motor_row.content  # Row
                    motor_container = row_content.controls[0].content  # First container (motor dropdown)
                    quantity_container = row_content.controls[1].content  # Second container (quantity field)

                    # Get the actual field values
                    motor_dropdown = motor_container.content.content  # Navigate through enhanced field structure
                    quantity_field = quantity_container.content.content

                    motor_id = motor_dropdown.value
                    quantity_str = quantity_field.value

                    if motor_id and quantity_str and str(quantity_str).isdigit():
                        quantity = int(quantity_str)
                        if quantity > 0:
                            price = get_motor_price(motor_id)
                            total += price * quantity

                except Exception as e:
                    print(f"Error calculating price for motor row: {e}")
                    continue

            # Update the total price field in the dialog
            if self.page.dialog and self.page.dialog.content:
                content = self.page.dialog.content
                if isinstance(content, Container) and hasattr(content, 'content'):
                    form = content.content
                    if hasattr(form, 'controls') and len(form.controls) > 1:
                        # The total price field should be the second control (index 1)
                        total_price_field = form.controls[1]
                        if hasattr(total_price_field, 'content') and hasattr(total_price_field.content, 'value'):
                            total_price_field.content.value = f"{total:.2f}"
                            self.page.update()

        except Exception as e:
            print(f"Error calculating billing total price: {e}")

    def _close_dialog_with_animation(self):
        """Close dialog with smooth animation."""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
        self.edit_billing_ref = None

    def _handle_billing_update(self, form_container):
        """
        Handle billing update with enhanced validation and feedback.

        Args:
            form_container: Container with form fields
        """
        try:
            # Show loading indicator
            self._show_loading_overlay("Mise à jour en cours...")

            # Extract form data with validation
            form_data = self._extract_billing_form_data(form_container)

            if not self._validate_billing_data(form_data):
                self._hide_loading_overlay()
                return

            # Update billing in database
            self._update_billing_in_database(form_data)

            # Hide loading and show success
            self._hide_loading_overlay()
            self._show_success_message(f"Facture {self.edit_billing_ref} mise à jour avec succès!")

            # Close dialog and refresh data
            self._close_dialog_with_animation()
            self._refresh_all_data()

        except Exception as e:
            self._hide_loading_overlay()
            self._show_error_message(f"Erreur lors de la mise à jour: {str(e)}")
            print(f"Error updating billing: {e}")

    def _show_loading_overlay(self, message):
        """Show loading overlay in dialog."""
        if self.page.dialog:
            loading_overlay = self.themer.create_loading_overlay(message)
            self.page.dialog.content = loading_overlay
            self.page.update()

    def _hide_loading_overlay(self):
        """Hide loading overlay and restore form."""
        if self.page.dialog and self.edit_billing_ref:
            billing_data = get_billing_by_ref(self.edit_billing_ref)
            billing_motors_data = get_related_motors(self.edit_billing_ref)
            if billing_data:
                billing_form = self.create_enhanced_billing_form(billing_data, billing_motors_data)
                self.page.dialog.content = Container(
                    content=billing_form,
                    padding=padding.all(20),
                    border_radius=self.themer.border_radius,
                    bgcolor=colors.SURFACE_VARIANT,
                    border=border.all(1, colors.OUTLINE_VARIANT),
                )
                self.page.update()
            
    def _extract_billing_form_data(self, form_container):
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
            billing_data = {
                "billing_ref": self._get_field_value(form_controls[0]),
                "total_price": self._get_field_value(form_controls[1]),
                "client_id": self._get_field_value(form_controls[2]),
                "mode_paiement": self._get_field_value(form_controls[3]),
                "description": self._get_field_value(form_controls[4]),
                "transporteur": self._get_field_value(form_controls[5]),
                "matricule": self._get_field_value(form_controls[6]),
            }

            # Extract motors data from enhanced motor rows
            motors_data = []
            if hasattr(self, 'edit_motor_rows'):
                for motor_row in self.edit_motor_rows:
                    try:
                        # Navigate through the enhanced container structure
                        row_content = motor_row.content  # Row
                        motor_container = row_content.controls[0].content  # First container (motor dropdown)
                        quantity_container = row_content.controls[1].content  # Second container (quantity field)

                        # Get the actual field values - navigate through enhanced field structure
                        motor_dropdown = motor_container.content.content  # Enhanced field -> Container -> Dropdown
                        quantity_field = quantity_container.content.content  # Enhanced field -> Container -> TextField

                        motor_id = motor_dropdown.value
                        quantity = quantity_field.value

                        if motor_id and quantity and str(quantity).isdigit() and int(quantity) > 0:
                            motors_data.append((motor_id, int(quantity)))
                            print(f"Extracted motor: {motor_id}, quantity: {quantity}")
                    except Exception as e:
                        print(f"Error extracting motor data from row: {e}")
                        continue

            print(f"Total motors extracted: {len(motors_data)}")

            billing_data["motors"] = motors_data

            return billing_data

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

    def _validate_billing_data(self, billing_data):
        """
        Validate billing form data with user feedback.

        Args:
            billing_data (dict): Billing data to validate

        Returns:
            bool: True if valid, False otherwise
        """
        errors = []

        # Required field validation
        if not billing_data.get("client_id", "").strip():
            errors.append("Le client est obligatoire")

        if not billing_data.get("mode_paiement", "").strip():
            errors.append("Le mode de paiement est obligatoire")

        # Motors validation
        if not billing_data.get("motors", []):
            errors.append("Au moins un moteur doit être ajouté à la facture")

        # Show errors if any
        if errors:
            error_message = "Erreurs de validation:\n" + "\n".join(f"• {error}" for error in errors)
            self._show_error_message(error_message)
            return False

        return True

    def _update_billing_in_database(self, billing_data):
        """
        Update billing in database with proper error handling.

        Args:
            billing_data (dict): Validated billing data
        """
        try:
            # Convert data types
            total_price = float(billing_data["total_price"]) if billing_data.get("total_price", "").strip() else 0.0
            client_id = int(billing_data["client_id"]) if billing_data.get("client_id", "").strip() else None

            # Update billing header
            update_billing_header_data = (
                total_price,
                client_id,
                billing_data["mode_paiement"],
                billing_data["description"],
                billing_data["transporteur"],
                billing_data["matricule"],
                self.edit_billing_ref,
            )
            update_billing(update_billing_header_data)

            # Update related motors
            delete_Billing_Motors_by_billing_ref(self.edit_billing_ref)

            # Insert new motors
            for motor_id, quantity in billing_data.get("motors", []):
                insert_Billing_Motors((self.edit_billing_ref, motor_id, quantity))

        except Exception as e:
            print(f"Database update error: {e}")
            raise ValueError("Erreur lors de la mise à jour en base de données")

    def _refresh_all_data(self):
        """Refresh all related data after billing update."""
        try:
            # Refresh billings table
            self.load_billings()

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

    def _add_new_motor_row_to_form(self, motors_controls):
        """Add a new motor row to the form."""
        try:
            if self.page.dialog and self.page.dialog.content:
                # Create new motor row
                new_row = self._create_enhanced_motor_row()

                # Add to edit_motor_rows list for tracking
                if not hasattr(self, 'edit_motor_rows'):
                    self.edit_motor_rows = []
                self.edit_motor_rows.append(new_row)

                # Insert before the add button (last control)
                motors_controls.insert(-1, new_row)

                # Update dialog content
                self.page.update()
        except Exception as e:
            print(f"Error adding motor row: {e}")

    def _remove_motor_row_from_form(self, row_id):
        """Remove a motor row from the form."""
        try:
            if self.page.dialog and self.page.dialog.content:
                # Find and remove the row from the dialog content
                content = self.page.dialog.content
                if isinstance(content, Container) and hasattr(content, 'content'):
                    form = content.content
                    if hasattr(form, 'controls'):
                        # Find the row to remove
                        for i, control in enumerate(form.controls):
                            if hasattr(control, 'data') and control.data == row_id:
                                form.controls.pop(i)
                                break

                        # Also remove from edit_motor_rows if it exists
                        if hasattr(self, 'edit_motor_rows'):
                            self.edit_motor_rows = [row for row in self.edit_motor_rows if getattr(row, 'data', None) != row_id]

                # Update dialog content and recalculate price
                self.page.update()
                self._calculate_billing_total_price()

        except Exception as e:
            print(f"Error removing motor row: {e}")

    def confirm_delete(self, e):
        """Handle billing deletion with enhanced feedback."""
        try:
            billing_ref = e

            # Show loading indicator
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    ProgressRing(width=16, height=16, stroke_width=2, color=colors.WHITE),
                    Text("Suppression en cours...", color=colors.WHITE),
                ]),
                bgcolor=colors.BLUE_500
            ))

            # Delete billing and related motors
            delete_billing(billing_ref)
            delete_Billing_Motors(billing_ref)

            # Show success message
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    Icon(icons.CHECK_CIRCLE, color=colors.WHITE),
                    Text(f"Facture {billing_ref} supprimée avec succès!", color=colors.WHITE),
                ]),
                bgcolor=colors.GREEN_500
            ))

            # Refresh data
            self.load_billings()

            # Refresh dashboard statistics instantly with async update
            if hasattr(self.parent_class, 'dashboard') and self.parent_class.dashboard:
                self.parent_class.dashboard.refresh_dashboard_async()

            # Close dialog
            self.page.close_dialog()
            self.page.update()

        except Exception as e:
            print(f"Error deleting billing: {e}")
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    Icon(icons.ERROR, color=colors.WHITE),
                    Text(f"Erreur lors de la suppression: {str(e)}", color=colors.WHITE),
                ]),
                bgcolor=colors.RED_500
            ))

    def delete_billing_handler(self, e):
        billing_ref = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(value=f"Êtes-vous sûr de vouloir supprimer la facture Réf {billing_ref}?"),
            content=Text("Cette action est irréversible."),
            actions=[
                TextButton(text="Annuler", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Delete", on_click=lambda _: self.confirm_delete(billing_ref)),
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True,
            scrollable=True,
        )
        self.page.update()
        
        
    def generate_billing_pdf_button_click(self, e, billing_ref):
        """
        Handle PDF generation button click with enhanced error handling and user feedback.

        Args:
            e: Event object
            billing_ref: Billing reference number
        """
        try:
            # Show loading message
            self.page.show_snack_bar(SnackBar(
                Text("Génération du PDF en cours..."),
                bgcolor=colors.BLUE_500
            ))

            # Generate the PDF
            output = generate_billing_pdf(billing_ref)

            # Check if output is an error message or file path
            if output and os.path.exists(output):
                # Success - PDF file was created
                file_name = os.path.basename(output)
                success_message = f"✅ PDF généré avec succès: {file_name}"

                # Show success message with action button
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.CHECK_CIRCLE, color=colors.WHITE),
                        Text(success_message, color=colors.WHITE),
                        IconButton(
                            icon=icons.FOLDER_OPEN,
                            icon_color=colors.WHITE,
                            tooltip="Ouvrir le dossier",
                            on_click=lambda _: self._open_file_location(output)
                        )
                    ]),
                    bgcolor=colors.GREEN_500,
                    duration=5000
                ))

                print(f"PDF generated successfully: {output}")

            else:
                # Error occurred during PDF generation
                error_message = str(output) if output else "Erreur inconnue lors de la génération du PDF"

                # Show error message
                self.page.show_snack_bar(SnackBar(
                    content=Row([
                        Icon(icons.ERROR, color=colors.WHITE),
                        Text(f"❌ Erreur: {error_message}", color=colors.WHITE, expand=True),
                    ]),
                    bgcolor=colors.RED_500,
                    duration=8000
                ))

                print(f"PDF generation failed: {error_message}")

        except Exception as ex:
            # Handle unexpected errors
            error_message = f"Erreur inattendue: {str(ex)}"
            self.page.show_snack_bar(SnackBar(
                content=Row([
                    Icon(icons.ERROR, color=colors.WHITE),
                    Text(f"❌ {error_message}", color=colors.WHITE, expand=True),
                ]),
                bgcolor=colors.RED_500,
                duration=8000
            ))
            print(f"Unexpected error in PDF generation: {ex}")

        self.page.update()

    def _open_file_location(self, file_path):
        """
        Open the file location in the system file explorer.

        Args:
            file_path: Path to the generated PDF file
        """
        try:
            import subprocess
            import platform

            # Get the directory containing the file
            directory = os.path.dirname(file_path)

            # Open file explorer based on the operating system
            system = platform.system()
            if system == "Windows":
                subprocess.run(["explorer", directory], check=True)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", directory], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", directory], check=True)
            else:
                print(f"Cannot open file explorer on {system}")

        except Exception as e:
            print(f"Failed to open file location: {e}")
            # Show fallback message with file path
            self.page.show_snack_bar(SnackBar(
                Text(f"Fichier sauvegardé dans: {file_path}"),
                bgcolor=colors.BLUE_500
            ))

    def load_billings(self, query=""):
        """Load billings with enhanced client name display and professional formatting."""

        if query:
            billings = search_billings_motors_list(query)
        else:
            billings = get_all_billings_with_motors()

        self.billings_data_table.rows.clear()

        for billing in billings:
            # Fetch client name by ID for professional display
            client_data = get_client_by_id(billing[2])  # billing[2] is client_id
            client_name = client_data[0] if client_data else f"Client ID: {billing[2]}"

            # Fetch related motors and their quantities for the current billing
            related_motors = get_related_motors(billing[0])  # billing[0] is the billing reference
            motors_info = ", ".join([f"{motor[0]} (Qty: {motor[1]})" for motor in related_motors])

            # Format price with currency
            formatted_price = f"{float(billing[1]):.2f} DT" if billing[1] else "0.00 DT"

            # Format date for better readability
            formatted_date = billing[7][:10] if billing[7] else ""  # Extract date part only

            # Create enhanced client display with professional styling
            client_display = Container(
                content=Row([
                    Icon(icons.PERSON, size=16, color=colors.PRIMARY),
                    Text(
                        client_name,
                        style=self.themer.get_text_style("body_medium"),
                        weight=FontWeight.W_500,
                        color=colors.ON_SURFACE,
                        overflow=TextOverflow.ELLIPSIS,
                    ),
                ], spacing=8, tight=True),
                padding=padding.symmetric(horizontal=8, vertical=4),
            )

            # Create enhanced price display
            price_display = Container(
                content=Text(
                    formatted_price,
                    style=self.themer.get_text_style("body_medium"),
                    weight=FontWeight.W_600,
                    color=colors.PRIMARY,
                ),
                padding=padding.symmetric(horizontal=8, vertical=4),
            )

            self.billings_data_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Row(
                                [
                                    IconButton(
                                        icon=Icons.PICTURE_AS_PDF,
                                        icon_color=colors.ERROR,
                                        tooltip="Générer PDF",
                                        on_click=lambda e, billing_ref=billing[0]: self.generate_billing_pdf_button_click(e, billing_ref)
                                    ),
                                    IconButton(
                                        icon=Icons.EDIT,
                                        icon_color=colors.PRIMARY,
                                        tooltip="Modifier",
                                        on_click=lambda e, billing_ref=billing[0]: self.open_update_dialog(billing_ref),
                                        data=billing[0]
                                    ),
                                    IconButton(
                                        icon=Icons.DELETE,
                                        icon_color=colors.ERROR,
                                        tooltip="Supprimer",
                                        on_click=self.delete_billing_handler,
                                        data=billing[0]
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                spacing=4,
                            )
                        ),
                        DataCell(Text(
                            billing[0],
                            style=self.themer.get_text_style("body_medium"),
                            weight=FontWeight.W_600,
                        )), # reference
                        DataCell(price_display), # prix totale with enhanced formatting
                        DataCell(client_display), # client with professional display
                        DataCell(Text(
                            str(billing[3]),
                            style=self.themer.get_text_style("body_medium"),
                        )), # mode paiement
                        DataCell(Text(
                            str(billing[4])[:50] + "..." if len(str(billing[4])) > 50 else str(billing[4]),
                            style=self.themer.get_text_style("body_small"),
                            overflow=TextOverflow.ELLIPSIS,
                        )), # description (truncated)
                        DataCell(Text(
                            str(billing[5]),
                            style=self.themer.get_text_style("body_medium"),
                        )), # transporteur
                        DataCell(Text(
                            billing[6],
                            style=self.themer.get_text_style("body_medium"),
                        )), # matricule
                        DataCell(Text(
                            formatted_date,
                            style=self.themer.get_text_style("body_small"),
                            color=colors.ON_SURFACE_VARIANT,
                        )), # date
                        DataCell(Text(
                            motors_info,
                            style=self.themer.get_text_style("body_small"),
                            overflow=TextOverflow.ELLIPSIS,
                        )), # related motors with quantities
                    ],
                )
            )

        self.page.update()

    def refresh_data(self):
        """Refresh all data including clients and motors for dropdowns"""
        self._load_clients_for_dropdown()
        # Refresh motor options in existing rows
        available_motors = get_all_motors()
        motor_options = [dropdown.Option(key=motor['id'], text=f"{motor['id']} - {motor['marque']}") for motor in available_motors]

        for row in self.motor_rows:
            row_controls = row.content.controls
            motor_dropdown = row_controls[0]
            motor_dropdown.options = motor_options

        self.page.update()

    def clear_form(self, e=None):
        """Clear all form fields and reset to initial state"""
        self.billing_ref.value = ""
        self.prix_totale.value = "0.00"
        self.client_dropdown.value = None
        self.mode_paiement.value = ""
        self.description.value = ""
        self.transporteur.value = ""
        self.matricule.value = ""

        # Clear motor rows and add one empty row
        self.motor_rows.clear()
        self.motors_column.controls.clear()
        self.add_new_motor_row()  # Add at least one empty row

        # Set focus to the first input field for better UX (only if control is mounted)
        try:
            if self.is_mounted():
                self.billing_ref.focus()
        except:
            pass  # Ignore focus errors if control is not ready

        if self.is_mounted():
            self.page.show_snack_bar(SnackBar(Text("Formulaire vidé")))
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