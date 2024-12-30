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

        self.page_name = "Allo Casse Auto - Billings"
        self.icon = Icons.PAYMENT
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame

        self.billing_add_title = Container(
                        content=Column(
                            controls=[
                                Text("Add Billing", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    )

        self.billing_ref = TextField(label="ID - Reference", col={"md": 4})
        self.prix_totale = TextField(label="Prix Totale", col={"md": 4}, read_only=True)
        self.mode_paiement = TextField(label="Mode Paiment", col={"md": 6})
        self.description = TextField(label="Description", multiline=True, col={"md": 6})
        self.transporteur = TextField(label="transporteur", col={"md": 6})
        self.matricule = TextField(label="matricule", col={"md": 6})

        self.client_dropdown = Dropdown(label="Client", col={"md": 4}, options=[])
        self.motor_rows = []
        self.motors_column = Column()
        self.add_motor_button = IconButton(
            icon=Icons.ADD,
            style=ButtonStyle(shape=CircleBorder()),
            on_click=self.add_new_motor_row,
            col={"xs": 3, "sm": 4, "md": 3, "lg": 2},
        )

        self.billing_list_title = Container(
                        content=Column(
                            controls=[
                                Text("Billing List", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    )

        self.search_bar = ResponsiveRow(
                                        controls=[
                                            TextField(
                                                label="Search Billings",
                                                on_change=self.on_search_change,
                                                col={"md": 6},
                                                ),
                                            ],
                                        alignment=MainAxisAlignment.CENTER,
                                        spacing=10,
                                        expand=True,
                                        )

        self.billings_data_table = DataTable(
                                            columns=[
                                                DataColumn(Text("Action")),
                                                DataColumn(Text("Reference")),
                                                DataColumn(Text("Prix Totale")),
                                                DataColumn(Text("Client")),
                                                DataColumn(Text("Mode Paiement")),
                                                DataColumn(Text("Description")),
                                                DataColumn(Text("Transporteur")),
                                                DataColumn(Text("Matricule")),
                                                DataColumn(Text("Date")),
                                                DataColumn(Text("Related Motors"))
                                            ],
                                            rows=[],
                                            border=border.all(1, "black"),
                                            horizontal_lines=border.BorderSide(1, "black"),
                                            vertical_lines=border.BorderSide(1, "black"),
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
        motor_id_dropdown = Dropdown(label="Motor ID", options=motor_options, col={"xs": 3, "sm": 4, "md": 3, "lg": 2}, on_change=self._calculate_total_price_dynamic)
        quantity_field = TextField(label="Quantity", value="1", col={"xs": 3, "sm": 4, "md": 3, "lg": 2}, keyboard_type=KeyboardType.NUMBER, on_change=self._calculate_total_price_dynamic)
        delete_button = IconButton(icon=icons.DELETE, style=ButtonStyle(shape=CircleBorder()), on_click=self.delete_motor_row, col={"xs": 3, "sm": 4, "md": 3, "lg": 2}, data=len(self.motor_rows))

        motor_row = ResponsiveRow(
            controls=[
            motor_id_dropdown,
            quantity_field,
            delete_button,
            self.add_motor_button,
            ], 
            alignment=MainAxisAlignment.CENTER
            
        )

        self.motor_rows.append(motor_row)
        self.motors_column.controls.append(motor_row)
        self.page.update()

    def delete_motor_row(self, e):
        index_to_delete = e.control.data
        if 0 <= index_to_delete < len(self.motor_rows):
            del self.motor_rows[index_to_delete]
            self.motors_column.controls.clear()
            for i, row in enumerate(self.motor_rows):
                row.controls[-1].data = i  # Update the delete button's data
                self.motors_column.controls.append(row)
            self._calculate_total_price_dynamic()
            self.page.update()

    def _calculate_total_price_dynamic(self, e=None):
        total = 0.0
        for row in self.motor_rows:
            motor_id_dropdown = row.controls[0]
            quantity_field = row.controls[1]
            if motor_id_dropdown.value and quantity_field.value:
                price = get_motor_price(motor_id_dropdown.value)
                quantity = int(quantity_field.value)
                total += price * quantity
        self.prix_totale.value = f"{total:.2f}"
        self.page.update()

    def make_frame(self):

        self.billing_frame = SafeArea(
            content=Column(
                controls=[
                    self.billing_add_title,
                    ResponsiveRow(
                        [
                            self.billing_ref,
                            self.prix_totale,
                            self.client_dropdown,
                            self.mode_paiement,
                            self.description,
                            self.transporteur,
                            self.matricule,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    ResponsiveRow(
                        controls=[
                            self.motors_column,                            
                            ], 
                        alignment=MainAxisAlignment.CENTER
                    ),

                    ResponsiveRow(
                        controls=[
                            ElevatedButton(
                                text="Add Billing",
                                icon=Icons.ADD,
                                style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                on_click=self.add_billing,
                                col={"md": 2},
                                expand=True,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    self.billing_list_title,
                    self.search_bar,
                    Container(
                        content=Column(
                            controls=[
                                Row(
                                    controls=[
                                        self.billings_data_table,
                                    ],
                                    scroll="auto",
                                    alignment=MainAxisAlignment.CENTER,
                                )
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        padding=padding.all(20),
                        alignment=alignment.center,
                        expand=True,
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )

        return self.billing_frame

    def add_billing(self, e):
        if not self.billing_ref.value:
            self.page.show_snack_bar(SnackBar(Text("Please enter a billing reference.")))
            return
        if not self.client_dropdown.value:
            self.page.show_snack_bar(SnackBar(Text("Please select a client.")))
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
            for row in self.motor_rows:
                motor_id_dropdown = row.controls[0]
                quantity_field = row.controls[1]
                if motor_id_dropdown.value and quantity_field.value:
                    insert_Billing_Motors((billing_data["billing_ref"], motor_id_dropdown.value, int(quantity_field.value)))
            self.page.show_snack_bar(SnackBar(Text("Billing Added Successfully")))
            self.clear_form()
            self.load_billings()
            self.page.update()
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(f"Error adding billing: {ex}")))

    def on_search_change(self, e):
        query = e.control.value
        self.load_billings(query)


    def form_dialog_column(self, billing_data, billing_motors_data):
        available_motors = get_all_motors()

        form_controls = [
            TextField(value=billing_data[0], label="ID - Reference", read_only=True, width=300),
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
        self.edit_billing_ref = billing_ref
        billing_data = get_billing_by_ref(billing_ref)
        billing_motors_data = get_related_motors(billing_ref)

        if billing_data:
            update_form = self.form_dialog_column(billing_data, billing_motors_data)
            self.page.dialog = AlertDialog(
                modal=True,
                title=Text("Update Billing", size=24, weight='bold'),
                content=update_form,
                actions=[
                    TextButton("Cancel", on_click=lambda _: self.page.close_dialog()),
                    TextButton("Update", on_click=lambda _: self.update_billing_data()),
                ],
                actions_alignment=MainAxisAlignment.END,
                open=True,
                scrollable=True,
            )
            self.page.update()

    def update_billing_data(self):
        if self.edit_billing_ref:
            dialog = self.page.dialog
            form_controls = dialog.content.controls

            updated_billing_data = {
                "billing_ref": form_controls[0].value,
                "total_price": float(form_controls[1].value),
                "client_id": int(form_controls[2].value),
                "mode_paiement": form_controls[3].value,
                "description": form_controls[4].value,
                "transporteur": form_controls[5].value,
                "matricule": form_controls[6].value,
            }

            update_billing_header_data = (
                updated_billing_data["total_price"],
                updated_billing_data["client_id"],
                updated_billing_data["mode_paiement"],
                updated_billing_data["description"],
                updated_billing_data["transporteur"],
                updated_billing_data["matricule"],
                self.edit_billing_ref,
            )
            update_billing(update_billing_header_data)

            # Update related motors
            delete_Billing_Motors_by_billing_ref(self.edit_billing_ref)

            motor_id = str(dialog.content.controls[8].controls[1].controls[0].value)
            quantity = int(dialog.content.controls[8].controls[1].controls[1].value)
            if motor_id and quantity > 0:
                insert_Billing_Motors((self.edit_billing_ref, motor_id, quantity))

            self.page.show_snack_bar(SnackBar(Text(f"Billing with Ref {self.edit_billing_ref} updated!")))
            self.page.close_dialog()
            self.load_billings()
            self.page.update()
            self.edit_billing_ref = None
            
    def confirm_delete(self, e):
        billing_ref = e
        delete_billing(billing_ref)
        delete_Billing_Motors(billing_ref)
        self.page.show_snack_bar(SnackBar(Text(f"Billing with Ref {billing_ref} deleted!")))
        self.load_billings()
        self.page.close_dialog()
        self.page.update()

    def delete_billing_handler(self, e):
        billing_ref = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(value=f"Are you sure you want to delete billing Ref {billing_ref}?"),
            content=Text("This action cannot be undone."),
            actions=[
                TextButton(text="Cancel", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Delete", on_click=lambda _: self.confirm_delete(billing_ref)),
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True,
            scrollable=True,
        )
        self.page.update()
        
        
    def generate_billing_pdf_button_click(self, e, billing_ref):
        output_path = f"billing_{billing_ref}.pdf"
        generate_billing_pdf(billing_ref)
        self.page.snack_bar = SnackBar(Text(f"Billing PDF generated: {output_path}"))
        self.page.snack_bar.open = True
        self.page.update()

    def load_billings(self, query=""):

        if query:
            billings = search_billings_motors_list(query)
        else:
            billings = get_all_billings_with_motors()

        self.billings_data_table.rows.clear()

        for billing in billings:

            # Fetch related motors and their quantities for the current billing
            related_motors = get_related_motors(billing[0])  # Assuming billing[0] is the billing reference
            motors_info = ", ".join([f"{motor[0]} (Qty: {motor[1]})" for motor in related_motors])

            self.billings_data_table.rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Row(
                                [
                                    IconButton(icon=Icons.PICTURE_AS_PDF, on_click=lambda e, billing_ref=billing[0]: self.generate_billing_pdf_button_click(e, billing_ref)),
                                    IconButton(icon=Icons.EDIT, on_click=lambda e, billing_ref=billing[0]: self.open_update_dialog(billing_ref), data=billing[0]),
                                    IconButton(icon=Icons.DELETE, on_click=self.delete_billing_handler, data=billing[0]),
                                ],
                                alignment=MainAxisAlignment.CENTER
                            )
                        ),
                        DataCell(Text(billing[0])), # reference
                        DataCell(Text(billing[1])), # prix totale
                        DataCell(Text(str(billing[2]))), # client
                        DataCell(Text(str(billing[3]))), # mode paiement
                        DataCell(Text(str(billing[4]))), # description
                        DataCell(Text(str(billing[5]))), # transporteur
                        DataCell(Text(billing[6])), # matricule
                        DataCell(Text(billing[7])), # date
                        DataCell(Text(motors_info)), # related motors with quantities

                    ],
                )
            )

        self.page.update()

    def clear_form(self):
        self.billing_ref.value = ""
        self.prix_totale.value = ""
        self.client_dropdown.value = None
        self.mode_paiement.value = ""
        self.description.value = ""
        self.transporteur.value = ""
        self.matricule.value = ""
        self.motor_rows.clear()
        self.motors_column.controls.clear()
        self.add_new_motor_row() # Add at least one empty row
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