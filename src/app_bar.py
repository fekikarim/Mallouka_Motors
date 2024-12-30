from flet import *
from Themer import ThemerMaster

class AppBarMaster():
    def __init__(self, page : Page, parent_class, themer : ThemerMaster, title: str, icon: Icons):
        
        super().__init__()
        
        self.page = page
        self.parent_class = parent_class
        self.themer = themer

        self.expand = True
        
        self.app_bar_frame = self.make_frame(title, icon)
        
        self.controls = [
            self.app_bar_frame,
        ]
        
    def make_frame(self, title: str, icon: Icons):
        self.upperbar = AppBar(
            leading=Icon(icon),
            title=Text(title, text_align='center'),
            actions=[
                PopupMenuButton(
                    items=[                
                        PopupMenuItem(
                            content=Row([Icon(Icons.DASHBOARD), Text("Dashboard", color="white")]),
                            on_click=lambda _: self.page.go("/")
                        ),
                        PopupMenuItem(),
                        PopupMenuItem(
                            content=Row([Icon(Icons.CAR_REPAIR), Text("Motors", color="white")]),
                            on_click=lambda _: self.page.go("/motors")
                        ),
                        PopupMenuItem(
                            content=Row([Icon(Icons.PERSON), Text("Clients", color="white")]),
                            on_click=lambda _: self.page.go("/clients")
                        ),
                        PopupMenuItem(
                            content=Row([Icon(Icons.PAYMENT), Text("Billing", color="white")]),
                            on_click=lambda _: self.page.go("/billing")
                        ),
                        PopupMenuItem(),
                        PopupMenuItem(
                            content=Row([Icon(Icons.SETTINGS), Text("Settings", color="white")]),
                            on_click=lambda _: self.page.go("/settings")
                        ),
                    ],
                    bgcolor="#605A56",
                ),
            ],
            center_title=True,
            color="white",
            bgcolor="#2D96DA",
        )
        
        return self.upperbar
        
    def update(self):
        self.page.update()