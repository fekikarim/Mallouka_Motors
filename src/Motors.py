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

        self.page_name = "Allo Casse Auto - Motors"
        self.icon = Icons.CAR_REPAIR
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame

        self.id_ref = TextField(label="ID - Reference", col={"md": 4})
        self.marque = TextField(label="Marque", col={"md": 4})
        self.modele = TextField(label="Modele", col={"md": 4})
        self.annee = TextField(label="Année", col={"md": 4}, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        self.kilometrage = TextField(label="Kilometrage", col={"md": 4}, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        self.prix = TextField(label="Prix", col={"md": 4}, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        self.description = TextField(label="Description", col={"md": 4}, multiline=True)
        self.status = Dropdown(
            label="Status",
            options=[
                dropdown.Option("Disponible"),
                dropdown.Option("Vendu"),
                dropdown.Option("Reserve"),
            ],
            col={"md": 4}
        )
        self.date_achats = TextField(label="Date Achats", hint_text="YYYY-MM-DD", col={"md": 4})
        self.fournisseur = TextField(label="Fournisseur", col={"md": 6})
        self.bl_facture = TextField(label="BL - Facture", col={"md": 6})

        self.motors_data_table = DataTable(
            columns=[
                DataColumn(Text("Actions")),
                DataColumn(Text("ID - Reference")), # id
                DataColumn(Text("Marque")), # marque 
                DataColumn(Text("Modele")), # modele
                DataColumn(Text("Annee")), # annee
                DataColumn(Text("Kilometrage")), # kilometrage
                DataColumn(Text("Prix")), # prix
                DataColumn(Text("Description")), # description
                DataColumn(Text("Status")), # statut
                DataColumn(Text("Date Achats")), # date_achat
                DataColumn(Text("Fournisseur")), # fournisseur
                DataColumn(Text("BL - Facture")), # bl_facture
            ],
            rows=[],
            border=border.all(1, "black"),
            horizontal_lines=border.BorderSide(1, "black"),
            vertical_lines=border.BorderSide(1, "black"),
            expand=True,
        )
        
        
        self.motors_list_title = Container(
                        content=Column(
                            controls=[
                                Text("Motors List", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    )
        
        self.search_bar = ResponsiveRow( 
                                        controls=[
                                            TextField(
                                                label="Search Motors", 
                                                on_change=self.on_search_change,
                                                col={"md": 6},
                                                ),
                                            ], 
                                        alignment=MainAxisAlignment.CENTER, 
                                        spacing=10, 
                                        expand=True,                                         
                                        )

        self.edit_motor_id = None  # To store the ID of the motor being edited

        self.title_container = Row(
            controls=[
                Text("Add Motors", size=24, text_align='center', weight='bold'),
            ],
            alignment=MainAxisAlignment.CENTER,
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
                    self.title_container,
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
                        spacing=10,
                    ),

                    ResponsiveRow(
                        [
                            ElevatedButton(
                                text="Add Motor",
                                icon=Icons.ADD,
                                style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                on_click=self.add_motor,
                                col={"md": 2},
                                expand=True,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    self.motors_list_title,
                    self.search_bar,
                    Container(
                        content=Column(
                            controls=[
                                Row(
                                    controls=[
                                        self.motors_data_table,
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
        return self.motors_frame

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
        self.page.show_snack_bar(SnackBar(Text("New motor added successfully!")))

        self.clear_form()
        self.load_motors()
        self.page.update()
        

    def on_search_change(self, e):
        query = e.control.value
        self.load_motors(query)
    
    def form_dialog_column(self, form_fields):
        return Column(
            controls=[
                TextField(value=form_fields[0], label="ID - Reference", read_only=True, width=300),
                TextField(value=form_fields[1], label="Marque", width=300),
                TextField(value=form_fields[2], label="Modele", width=300),
                TextField(value=form_fields[3], label="Année", width=300, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                TextField(value=form_fields[4], label="Kilometrage", width=300, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                TextField(value=form_fields[5], label="Prix", width=300, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                TextField(value=form_fields[6], label="Description", width=300, multiline=True),
                Dropdown(
                    value=form_fields[7],
                    label="Status",
                    options=[
                        dropdown.Option("Disponible"),
                        dropdown.Option("Vendu"),
                        dropdown.Option("Reserve"),
                    ],
                    width=300
                ),
                TextField(value=form_fields[8], label="Date Achats", hint_text="YYYY-MM-DD", width=300),
                TextField(value=form_fields[9], label="Fournisseur", width=300),
                TextField(value=form_fields[10], label="BL - Facture", width=300),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

    def open_update_dialog(self, motor_id):
        self.edit_motor_id = motor_id
        motor = get_motor_by_id(motor_id)
        if motor:
            motor_form_col = self.form_dialog_column(motor)
            self.page.update()

            self.page.dialog = AlertDialog(
                modal=True,
                title=Text("Update Motor", size=24, weight='bold'),
                content=motor_form_col,
                actions=[
                    TextButton(text="Cancel", on_click=lambda _: self.page.close_dialog()),
                    TextButton(text="Update", on_click=lambda _: self.update_motor_data(motor_form_col)),
                ],
                actions_alignment=MainAxisAlignment.END,
                open=True,
                scrollable=True,
            )
            self.page.update()

    def update_motor_data(self, form_fields):        
        if self.edit_motor_id:
            motor_data = {
                "id": form_fields.controls[0].value,
                "marque": form_fields.controls[1].value,
                "modele": form_fields.controls[2].value,
                "annee": int(form_fields.controls[3].value) if form_fields.controls[3].value else None,
                "kilometrage": int(form_fields.controls[4].value) if form_fields.controls[4].value else None,
                "prix": float(form_fields.controls[5].value) if form_fields.controls[5].value else None,
                "description": form_fields.controls[6].value,
                "statut": form_fields.controls[7].value,
                "date_achat": form_fields.controls[8].value,
                "fournisseur": form_fields.controls[9].value,
                "bl_facture": form_fields.controls[10].value,
            }

            update_data = (
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
                motor_data['id'],
            )
            update_motor(update_data)
            self.page.show_snack_bar(SnackBar(Text(f"Motor with ID {self.edit_motor_id} updated!")))
            self.page.close_dialog()
            self.clear_form()
            self.load_motors()
            self.page.update()
            self.edit_motor_id = None    
    
    
    def confirm_delete(self, e):
        motor_id = e
        delete_motor(motor_id)
        self.page.show_snack_bar(SnackBar(Text(f"Motor with ID {motor_id} deleted!")))
        self.load_motors()
        self.page.close_dialog()
        self.page.update()

    def delete_motor_handler(self, e):
        motor_id = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(value=f"Are you sure you want to delete motor ID {motor_id}?"),
            content=Text("This action cannot be undone."),
            actions=[
                TextButton(text="Cancel", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Delete", on_click=lambda _: self.confirm_delete(motor_id)),
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

        table_rows = [
            DataRow(
                cells=[
                    DataCell(
                        Row(
                            [
                                IconButton(icon=icons.EDIT, on_click=lambda e, motor_id=motor[0]: self.open_update_dialog(motor_id), data=motor[0]),
                                IconButton(icon=icons.DELETE, on_click=self.delete_motor_handler, data=motor[0]),
                            ],
                            alignment=MainAxisAlignment.CENTER
                        )
                    ),
                    DataCell(Text(motor[0])),
                    DataCell(Text(motor[1])),
                    DataCell(Text(str(motor[2]))),
                    DataCell(Text(str(motor[3]))),
                    DataCell(Text(str(motor[4]))),
                    DataCell(Text(str(motor[5]))),
                    DataCell(Text(motor[6])),
                    DataCell(Text(motor[7])),
                    DataCell(Text(motor[8])),
                    DataCell(Text(motor[9])),
                    DataCell(Text(motor[10])),
                    
                ],
            ) for motor in motors
        ]

        self.motors_data_table.rows.extend(table_rows)
        self.page.update()

    def clear_form(self):
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