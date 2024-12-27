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
        
        self.page_name = "Allo Casse Auto - Clients"
        self.icon = Icons.PERSON
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame
        
        self.client_add_title = Container(
                        content=Column(
                            controls=[
                                Text("Add Clients", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    )
        self.client_name = TextField(label="Nom Complet", col={"md": 4})
        self.client_address = TextField(label="Adresse", col={"md": 4})
        self.client_number = TextField(label="Numero", col={"md": 4}, input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""), prefix_text="+216")
        self.client_mf = TextField(label="MF", col={"md": 10})
        
        self.client_list_title = Container(
                        content=Column(
                            controls=[
                                Text("Clients List", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    )
        
        
        self.search_bar = ResponsiveRow( 
                                        controls=[
                                            TextField(
                                                label="Search Clients", 
                                                on_change=self.on_search_change,
                                                col={"md": 6},
                                                ),
                                            ], 
                                        alignment=MainAxisAlignment.CENTER, 
                                        spacing=10, 
                                        expand=True,                                         
                                        )
        
        
        self.clients_data_table = DataTable(
                                    columns=[
                                        DataColumn(Text("Actions")),
                                        DataColumn(Text("ID")),
                                        DataColumn(Text("Nom Complet")),
                                        DataColumn(Text("Adresse")),
                                        DataColumn(Text("Numero")),
                                        DataColumn(Text("MF")),
                                    ],
                                    rows=[],
                                    border=border.all(1, "black"),
                                    horizontal_lines=border.BorderSide(1, "black"),
                                    vertical_lines=border.BorderSide(1, "black"),
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
                    self.client_add_title,
                    ResponsiveRow(
                        [
                            self.client_name,
                            self.client_address,
                            self.client_number,
                            self.client_mf,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    ResponsiveRow(
                        controls=[
                            ElevatedButton(
                                text="Add Client",
                                icon=Icons.ADD,
                                style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                on_click=self.add_client,
                                col={"md": 2},
                                expand=True,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    self.client_list_title,
                    self.search_bar,
                    Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            self.clients_data_table,
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
        
        return self.clients_frame
    
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
        self.page.show_snack_bar(SnackBar(Text("Client Added Successfully")))
        
        self.clear_form()
        self.load_clients()
        self.page.update()
        
    def on_search_change(self, e):
        query = e.control.value
        self.load_clients(query)
        
    def form_dialog_column(self, form_fields):
        return Column(
            controls=[
                TextField(label="Nom Complet", value=form_fields[0]),
                TextField(label="Adresse", value=form_fields[1]),
                TextField(label="Numero", value=form_fields[2], input_filter=InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""), prefix_text="+216"),
                TextField(label="MF", value=form_fields[3]),                
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )
        
    def open_update_dialog(self, client_id):
        self.edit_client_id = client_id
        client = get_client_by_id(client_id)
        if client:
            client_form_col = self.form_dialog_column(client)
            self.page.update()
            
            self.page.dialog = AlertDialog(
                modal=True,
                title=Text("Update Client", size=24, weight='bold'),
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
        if self.edit_client_id:
            client_data = {
                "client_name": form_fields.controls[0].value,
                "client_address": form_fields.controls[1].value,
                "client_number": form_fields.controls[2].value,
                "client_mf": form_fields.controls[3].value,
            }
            
            update_client_data = (
                client_data["client_name"],
                client_data["client_address"],
                client_data["client_number"],
                client_data["client_mf"],
                self.edit_client_id,
            )
            
            update_client(update_client_data)
            self.page.show_snack_bar(SnackBar(Text(f"{client_data['client_name']} Updated Successfully")))
            self.page.close_dialog()
            self.load_clients()
            self.page.update()
            self.edit_client_id = None
            
    
    def confirm_delete(self, e):
        client_id = e
        delete_client(client_id)
        self.page.show_snack_bar(SnackBar(Text("Client Deleted Successfully")))
        self.load_clients()
        self.page.close_dialog()
        self.page.update()
        
    def delete_client_handler(self, e):
        client_id = e.control.data
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text("Delete Client", size=24, weight='bold'),
            content=Text("Are you sure you want to delete this client?"),
            actions=[
                TextButton(text="Cancel", on_click=lambda _: self.page.close_dialog()),
                TextButton(text="Delete", on_click=lambda _: self.confirm_delete(client_id)),
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
        
        table_rows = [
            DataRow(
                cells=[
                    DataCell(
                        Row(
                            [
                                IconButton(icon=Icons.EDIT, on_click=lambda e, client_id=client[0]: self.open_update_dialog(client_id), data=client[0]),
                                IconButton(icon=icons.DELETE, on_click=self.delete_client_handler, data=client[0]),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                        )
                    ),
                    DataCell(Text(client[0])),
                    DataCell(Text(client[1])),
                    DataCell(Text(client[2])),
                    DataCell(Text(client[3])),
                    DataCell(Text(client[4])),                    
                ],                
            ) for client in clients
        ]
        
        self.clients_data_table.rows.extend(table_rows)
        self.page.update()
        
        
    def clear_form(self):
        self.client_name.value = ""
        self.client_address.value = ""
        self.client_number.value = ""
        self.client_mf.value = ""
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