from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster

class Motors:
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
        
    

    def make_frame(self):
        self.motors_frame = SafeArea(
            content=Column(
                controls=[
                    self.title_container,
                    ResponsiveRow(
                        [
                            TextField(label="ID - Reference", col={"md": 4}),
                            TextField(label="Marque", col={"md": 4}),
                            TextField(label="Modele", col={"md": 4}),
                            TextField(label="Année", col={"md": 4}),
                            TextField(label="Kilometrage", col={"md": 4}),
                            TextField(label="Prix", col={"md": 4}),
                            TextField(label="Description", col={"md": 4}),
                            Dropdown(
                                label="Status",
                                options=[
                                    dropdown.Option("Disponible"),
                                    dropdown.Option("Vendu"),
                                    dropdown.Option("Reserve"),
                                ],
                                col={"md": 4}
                            ),
                            TextField(label="Description", multiline=True, col={"md": 4}),
                            TextField(label="Date Achats", col={"md": 4}),
                            TextField(label="Fournisseur", col={"md": 4}),
                            TextField(label="BL - Facture", col={"md": 4}),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),

                    ResponsiveRow(
                        [
                            ElevatedButton(
                                "Add Motor",
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
                                Text("Motors List", size=24, text_align='center', weight='bold'),
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
                                                    DataColumn(Text("ID")),
                                                    DataColumn(Text("Name")),
                                                    DataColumn(Text("Model")),
                                                    DataColumn(Text("Year")),
                                                    DataColumn(Text("Color")),
                                                    DataColumn(Text("Price")),
                                                    DataColumn(Text("Status"))
                                                ],
                                                rows=[
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("+ - x")),
                                                            DataCell(Text("1")),
                                                            DataCell(Text("Toyota")),
                                                            DataCell(Text("Corolla")),
                                                            DataCell(Text("2010")),
                                                            DataCell(Text("Black")),
                                                            DataCell(Text("2000")),
                                                            DataCell(Text("Available")),
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
        
        return self.motors_frame

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
