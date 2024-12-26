from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster    

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
        
        self.billing_frame = self.make_frame()
        
        self.controls = [
            self.billing_frame,
            self.upperbar,
        ]

    def make_frame(self):
        
        self.billing_frame = SafeArea(
            content=Column(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                Text("Add Billing", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    ),
                    ResponsiveRow(
                        [
                            TextField(label="ID - Reference", col={"md": 4}),
                            TextField(label="Prix Totale", col={"md": 4}),
                            ElevatedButton(
                                "Select Motors",
                                icon=Icons.ADD_SHOPPING_CART,
                                style=ButtonStyle(
                                    bgcolor='green',
                                    color='white',
                                    padding=15,
                                ),
                                col={"md": 4},
                                on_click=lambda e: ...
                            ),
                            Dropdown(
                                label="Client",
                                options=[
                                    dropdown.Option("Rami"),
                                    dropdown.Option("Ahmed"),
                                    dropdown.Option("Sami"),
                                ],
                                col={"md": 4}
                            ),
                            TextField(label="Mode Paiment", col={"md": 4}),
                            TextField(label="Description", multiline=True, col={"md": 4}),
                            TextField(label="transporteur", col={"md": 6}),
                            TextField(label="matricule", col={"md": 6}),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    ResponsiveRow(
                        controls=[
                            ElevatedButton(
                                "Add Billing",
                                icon=Icons.ADD,
                                style=ButtonStyle(bgcolor='green', color='white', padding=15, shape=ContinuousRectangleBorder(360)),
                                col={"md": 2},
                                expand=True,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    Container(
                        content=Column(
                            controls=[
                                Text("Billing List", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Row(
                                    controls=[
                                        DataTable(
                                            columns=[
                                                DataColumn(Text("Action")),
                                                DataColumn(Text("Reference")),
                                                DataColumn(Text("Total Price")),
                                                DataColumn(Text("Client")),
                                                DataColumn(Text("Mode Paiement")),
                                                DataColumn(Text("Description")),
                                                DataColumn(Text("Transporteur")),
                                                DataColumn(Text("Matricule")),
                                                DataColumn(Text("Date")),
                                                DataColumn(Text("Motors"))
                                            ],
                                            rows=[
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("+ - x")),
                                                        DataCell(Text("AA")),
                                                        DataCell(Text("150")),
                                                        DataCell(Text("med")),
                                                        DataCell(Text("cheque")),
                                                        DataCell(Text("xxxxxxxxxx")),
                                                        DataCell(Text("rochdi")),
                                                        DataCell(Text("160TN6262")),
                                                        DataCell(Text("2024-02-11")),
                                                        DataCell(Text("citroen, peugeot"))
                                                    ]
                                                )
                                            ],
                                            border=border.all(1, "black"),
                                            horizontal_lines=border.BorderSide(1, "black"),
                                            vertical_lines=border.BorderSide(1, "black"),
                                        ),
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

    def update(self) -> None:
        if self.is_mounted():
            super().update()
            
            
    def is_mounted(self) -> bool:
        if self.page is None:
            return False
        for view in self.page.views:
            for control in view.controls:
                if self == control.content:
                    # print("is mounted")
                    return True    
        # print("is not mounted")
        return False
