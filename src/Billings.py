from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster    
from db import *

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
        self.mode_paiement = TextField(label="Mode Paiment", col={"md": 4})
        self.description = TextField(label="Description", multiline=True, col={"md": 4})
        self.transporteur = TextField(label="transporteur", col={"md": 6})
        self.matricule = TextField(label="matricule", col={"md": 6})
        
        self.client_dropdown = Dropdown(label="Client", col={"md": 4}, options=[])
        self.selected_motors = []  # List of tuples (motor_id, quantity)
        self.motors_tags_row = Row(alignment=MainAxisAlignment.CENTER, wrap=True, scroll="auto")
        
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
        
        
    def _load_clients_for_dropdown(self):
        clients = get_all_clients_with_names()
        self.client_dropdown.options.clear()
        for client_id, client_name in clients:
            self.client_dropdown.options.append(dropdown.Option(key=client_id, text=client_name))
        self.page.update()


    def _calculate_total_price(self):
        total = 0.0
        for motor_id, quantity in self.selected_motors:
            price = get_motor_price(motor_id)
            total += price * quantity
        self.prix_totale.value = f"{total:.2f}"
        self.page.update()
        
        
    def _update_motor_tags(self):
        self.motors_tags_row.controls.clear()
        for motor_id, quantity in self.selected_motors:
            self.motors_tags_row.controls.append(BillingMotorTag(self, motor_id, quantity))
        self.page.update()

    def remove_selected_motor(self, motor_id):
        self.selected_motors = [(mid, qty) for mid, qty in self.selected_motors if mid != motor_id]
        self._update_motor_tags()
        self._calculate_total_price()
        self.page.update()
        
        
    def _open_select_motors_dialog(self, e):
        available_motors = get_all_motors()
        motor_options = [dropdown.Option(key=motor['id'], text=f"{motor['id']} - {motor['marque']}") for motor in available_motors]
        self.selected_motor_id = Dropdown(label="Motor", options=motor_options, col=6)
        self.selected_motor_quantity = TextField(label="Quantity", value="1", col=6, keyboard_type=KeyboardType.NUMBER)

        def close_dialog(e):
            self.page.close_dialog()

        def add_motor(e):
            motor_id = self.selected_motor_id.value
            quantity = int(self.selected_motor_quantity.value) if self.selected_motor_quantity.value else 1
            if motor_id and quantity > 0:
                found = False
                for i, (mid, qty) in enumerate(self.selected_motors):
                    if mid == motor_id:
                        self.selected_motors[i] = (mid, qty + quantity)
                        found = True
                        break
                if not found:
                    self.selected_motors.append((motor_id, quantity))
                self._update_motor_tags()
                self._calculate_total_price()
                self.page.close_dialog()
            else:
                self.page.show_snack_bar(SnackBar(Text("Please select a motor and a valid quantity.")))

        self.page.dialog = AlertDialog(
            modal=True,
            title=Text("Select Motors"),
            content=Column([
                self.selected_motor_id,
                self.selected_motor_quantity,
            ]),
            actions=[
                TextButton("Cancel", on_click=close_dialog),
                ElevatedButton("Add Motor", on_click=add_motor),
            ],
            open=True,
        )
        self.page.update()
        
    def open_edit_quantity_dialog(self, motor_id, current_quantity):
        quantity_editor = TextField(label="Quantity", value=str(current_quantity), keyboard_type=KeyboardType.NUMBER)

        def close_edit_dialog(e):
            self.page.close_dialog()

        def save_quantity(e):
            new_quantity = int(quantity_editor.value) if quantity_editor.value else 0
            if new_quantity > 0:
                for i, (mid, qty) in enumerate(self.selected_motors):
                    if mid == motor_id:
                        self.selected_motors[i] = (mid, new_quantity)
                        break
                self._update_motor_tags()
                self._calculate_total_price()
                self.page.close_dialog()
            else:
                self.page.show_snack_bar(SnackBar(Text("Quantity must be greater than 0.")))

        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(f"Edit Quantity for {motor_id}"),
            content=Column([
                Text(f"Motor ID: {motor_id}"),
                quantity_editor,
            ]),
            actions=[
                TextButton("Cancel", on_click=close_edit_dialog),
                ElevatedButton("Save", on_click=save_quantity),
            ],
            open=True,
        )
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
                            ElevatedButton(
                                "Select Motors",
                                icon=Icons.ADD_SHOPPING_CART,
                                style=ButtonStyle(bgcolor='green', color='white', padding=15),
                                col={"md": 4},
                                on_click=self._open_select_motors_dialog
                            ),
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
    
    def billing_detail_view(self, billing_ref):
        billing_data = get_billing_data(billing_ref)
        if billing_data:
            self.billing_ref.value = billing_data['ref']
            self.billing_ref.disabled = True
            self.prix_totale.value = str(billing_data['total_price'])
            self.client_dropdown.value = billing_data['client_id']
            self.mode_paiement.value = billing_data['mode_paiement']
            self.description.value = billing_data['description']
            self.transporteur.value = billing_data['transporteur']
            self.matricule.value = billing_data['matricule']
            self.selected_motors = get_selected_motors_by_billing_ref(billing_ref)
            self._update_motor_tags()

            return View(
                route=f"/billing/{billing_ref}",
                controls=[
                    Text(f"Billing Details - Ref: {billing_ref}", style="headlineMedium"),
                    self.billing_ref,
                    self.prix_totale,
                    self.client_dropdown,
                    self.mode_paiement,
                    self.description,
                    self.transporteur,
                    self.matricule,
                    self.motors_tags_row,
                    ElevatedButton("Back to Billings", on_click=lambda _: self.page.go("/billing")),
                ],
            )
        else:
            return View(
                route=f"/billing/{billing_ref}",
                controls=[
                    Text("Billing not found.", style="headlineMedium"),
                    ElevatedButton("Back to Billings", on_click=lambda _: self.page.go("/billing")),
                ],
            )
            
    
    
    def _update_motor_tags(self):
        self.motors_tags_row.controls.clear()
        for motor_id, quantity in self.selected_motors:
            self.motors_tags_row.controls.append(BillingMotorTag(self, motor_id, quantity))
        self.page.update()

    def remove_selected_motor(self, motor_id):
        self.selected_motors = [(mid, qty) for mid, qty in self.selected_motors if mid != motor_id]
        self._update_motor_tags()
        self._calculate_total_price()
        self.page.update()
    
    def add_billing(self, e):
        if not self.billing_ref.value:
            self.page.show_snack_bar(SnackBar(Text("Please enter a billing reference.")))
            return
        if not self.client_dropdown.value:
            self.page.show_snack_bar(SnackBar(Text("Please select a client.")))
            return
        if not self.selected_motors:
            self.page.show_snack_bar(SnackBar(Text("Please select at least one motor.")))
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
            for motor_id, quantity in self.selected_motors:
                insert_Billing_Motors((billing_data["billing_ref"], motor_id, quantity))
            self.page.show_snack_bar(SnackBar(Text("Billing Added Successfully")))
            self.clear_form()
            self.load_billings()
            self.page.update()
        except Exception as ex:
            self.page.show_snack_bar(SnackBar(Text(f"Error adding billing: {ex}")))
        
    
    
    
    def on_search_change(self, e):
        query = e.control.value
        self.load_billings(query)
        
    def update_form(self, form_fields):
        return SafeArea(
                content=Column(
                    controls=[
                        self.billing_add_title,
                        ResponsiveRow(
                            [
                                TextField(label="ID - Reference", value=form_fields[0], col={"md": 4}),
                                TextField(label="Prix Totale", value=form_fields[1], col={"md": 4}),
                                # the elevated button below needs to open an alert dialog to select motors from the motors list and quantity so it's basically a form that have an input dropdown that have motor_id options (where statut="Disponible") and an input text field for the quantity ; the client will choose a motor and it's quantity and then after clicking on add motor the dialog will close and the selected motor will be added in a one row that will have the motor_id tag with his quantity for example : "ABCD, 2" and then the client can add more motors by clicking on the button again ; also he can remove a motor by clicking on the "x" icon that will be on the right of each motor tag ; also he can edit the quantity by clicking on the motor tag and then a dialog will open with the motor_id and the quantity input text field so he can edit the quantity and then click on save to save the changes or cancel to cancel the changes
                                # ElevatedButton(
                                #     "Select Motors",
                                #     icon=Icons.ADD_SHOPPING_CART,
                                #     style=ButtonStyle(
                                #         bgcolor='green',
                                #         color='white',
                                #         padding=15,
                                #     ),
                                #     col={"md": 4},
                                #     on_click=lambda e: ...
                                # ),
                                
                                # this dropdown below will have the clients list ; the options will be the clients names and the client will choose one of them ; by adding a billing the client id of the client which the user select will be added to the billing row
                                # Dropdown(
                                #     label="Client",
                                #     options=[
                                #         dropdown.Option("Rami"),
                                #         dropdown.Option("Ahmed"),
                                #         dropdown.Option("Sami"),
                                #     ],
                                #     col={"md": 4}
                                # ),
                                
                                TextField(label="Mode Paiment", value=form_fields[4], col={"md": 4}),
                                TextField(label="Description", value=form_fields[5], multiline=True, col={"md": 4}),
                                TextField(label="transporteur", value=form_fields[6], col={"md": 6}),
                                TextField(label="matricule", value=form_fields[7], col={"md": 6}),
                                
                                ElevatedButton(
                                    text="Update",
                                    icon=Icons.ADD,
                                    style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                    on_click=self.add_billing,
                                    col={"md": 2},
                                    expand=True,
                                ),
                                ElevatedButton(
                                    text="Cancel",
                                    icon=Icons.ADD,
                                    style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                    on_click=self.page.go("/billings"),
                                    col={"md": 2},
                                    expand=True,
                                ),
                                
                            ],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                expand=True,
            )
        
    def update_billing_subpage(self, billing_id):
        self.edit_billing_id = billing_id
        billing = get_billing_by_id(billing_id)
        if billing:
            client_form_col = self.update_form(billing)
            self.page.update()
            
            self.page.dialog = AlertDialog(
                modal=True,
                title=Text("Update Billing", size=24, weight='bold'),
                content=client_form_col,
                actions=[
                    TextButton(text="Cancel", on_click=lambda _: self.page.close_dialog()),
                    TextButton(text="Update", on_click=lambda _: self.update_client_data(client_form_col)),
                ],
                actions_alignment=MainAxisAlignment.END,
                open=True,
                scrollable=True,
            )
            self.page.update()
            
            
    def update_client_data(self, form_fields):
        if self.edit_billing_ref:
            billing_data = {
                "billing_ref": form_fields.controls[0].value,
                "prix_totale": form_fields.controls[1].value,
                #### motors - billing relation ; the client will select motors from the motors list and add them to the billing also he have the quantity of each motor
                #### client - billing relation ; the user will select a client from the clients dropdown list and add it to the billing
                "mode_paiement": form_fields.controls[4].value,
                "description": form_fields.controls[5].value,
                "transporteur": form_fields.controls[6].value,
                "matricule": form_fields.controls[7].value,
            }
            
            update_billing_data = (
                billing_data["billing_ref"],
                billing_data["prix_totale"],
                #### motors - billing relation ; the client will select motors from the motors list and add them to the billing also he have the quantity of each motor
                #### client - billing relation ; the user will select a client from the clients dropdown list and add it to the billing
                billing_data["mode_paiement"],
                billing_data["description"],
                billing_data["transporteur"],
                billing_data["matricule"],
                self.edit_billing_ref
            )                        
            
            update_billing(update_billing_data)
            self.page.show_snack_bar(SnackBar(Text(f"{billing_data["billing_ref"]} Updated Successfully")))
            self.page.go("/billings")
            self.load_billings()
            self.page.update()
            self.edit_billing_ref = None
            
            
    def confirm_delete(self, e):
        billing_ref = e
        delete_billing(billing_ref)
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
                                    IconButton(icon=icons.EDIT, on_click=lambda e, billing_ref=billing[0]: self.page.go(f"/billing/{billing_ref}"), data=billing[0]),
                                    IconButton(icon=icons.DELETE, on_click=self.delete_billing_handler, data=billing[0]),
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
        self.motors_tags = None
        self.client_id.value = ""
        self.mode_paiement.value = ""
        self.description.value = ""
        self.transporteur.value = ""
        self.matricule.value = ""
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
        
        
        

class BillingMotorTag():
    def __init__(self, parent, motor_id, quantity):
        super().__init__()
        self.parent = parent
        self.motor_id = motor_id
        self.quantity = quantity

    def build(self):
        return Chip(
            label=Text(f"{self.motor_id}, {self.quantity}"),
            on_delete=self.delete_tag,
            on_click=self.edit_quantity,
            delete_icon_color=colors.RED_500,
        )

    def delete_tag(self, e):
        self.parent.remove_selected_motor(self.motor_id)

    def edit_quantity(self, e):
        self.parent.open_edit_quantity_dialog(self.motor_id, self.quantity)