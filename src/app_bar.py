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

    def create_menu_item(self, icon, text, route):
        """Create a styled menu item."""
        return PopupMenuItem(
            content=Row([
                Icon(
                    icon,
                    size=20,
                    color=colors.ON_SURFACE,
                ),
                Text(
                    text,
                    color=colors.ON_SURFACE,
                    weight=FontWeight.W_500,
                    size=14,
                )
            ], spacing=12),
            on_click=lambda _: self.page.go(route),
            padding=padding.symmetric(horizontal=16, vertical=12),
        )

    def make_frame(self, title: str, icon: Icons):
        self.upperbar = AppBar(
            leading=Container(
                content=Icon(
                    icon,
                    size=24,
                    color=colors.ON_PRIMARY,
                ),
                padding=padding.all(8),
            ),
            title=Text(
                title,
                text_align='center',
                style=self.themer.get_text_style("title_large"),
                color=colors.ON_PRIMARY,
                weight=FontWeight.W_600,
            ),
            actions=[
                PopupMenuButton(
                    icon=icons.MENU,
                    icon_color=colors.ON_PRIMARY,
                    icon_size=24,
                    items=[
                        self.create_menu_item(Icons.DASHBOARD, "Tableau de bord", "/"),
                        PopupMenuItem(height=1),  # Divider
                        self.create_menu_item(Icons.CAR_REPAIR, "Moteurs", "/motors"),
                        self.create_menu_item(Icons.PERSON, "Clients", "/clients"),
                        self.create_menu_item(Icons.PAYMENT, "Facturation", "/billing"),
                        PopupMenuItem(height=1),  # Divider
                        self.create_menu_item(Icons.SETTINGS, "Paramètres", "/settings"),
                    ],
                    bgcolor=colors.SURFACE,
                    elevation=8,
                    shape=RoundedRectangleBorder(radius=12),
                    padding=padding.symmetric(vertical=8),
                ),
                Container(width=8),  # Spacing
            ],
            center_title=True,
            bgcolor=colors.PRIMARY,
            elevation=4,
            shadow_color=colors.with_opacity(0.3, colors.SHADOW),
        )

        return self.upperbar
        
    def update(self):
        self.page.update()