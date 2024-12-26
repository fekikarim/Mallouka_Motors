from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster

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
        
        self.clients_frame = self.make_frame()
        
        self.controls = [
            self.clients_frame,
            self.upperbar,
        ]

    def make_frame(self):
        
        self.clients_frame = SafeArea(
            content=Column(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                Text("Add Clients", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    ),
                    ResponsiveRow(
                        [
                            TextField(label="Nom Complet", col={"md": 4}),
                            TextField(label="Adresse", col={"md": 4}),
                            TextField(label="Numero", col={"md": 4}),
                            TextField(label="MF", col={"md": 10}),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    
                    ResponsiveRow(
                        controls=[
                            ElevatedButton(
                                "Add Client",
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
                                Text("Clients List", size=24, text_align='center', weight='bold'),
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
                                                    DataColumn(Text("Actions")),
                                                    DataColumn(Text("ID")),
                                                    DataColumn(Text("Nom Complet")),
                                                    DataColumn(Text("Adresse")),
                                                    DataColumn(Text("Numero")),
                                                    DataColumn(Text("MF")),
                                                ],
                                                rows=[
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("1")),
                                                            DataCell(Text("Toyota")),
                                                            DataCell(Text("Corolla")),
                                                            DataCell(Text("2010")),
                                                            DataCell(Text("Black")),
                                                            DataCell(Text("2000")),
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
        
        return self.clients_frame

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
