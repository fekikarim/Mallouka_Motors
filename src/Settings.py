from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster
from datetime import datetime

class Settings:
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):
        
        super().__init__()
        
        
        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True
        
        self.page_name = "Mallouka Motors - Paramètres"
        self.icon = Icons.SETTINGS
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame
        
        self.switcher = Container(
                content=Column(
                    controls=[
                        self.parent_class.themer.theme_switch,
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                margin=margin.only(top=20, bottom=20),
                alignment=alignment.center,
            )
        
        self.page.bottom_appbar = BottomAppBar(
            shape=NotchShape.CIRCULAR,
            content=Container(
                content=Text(
                    "Développé par ",
                    spans=[
                        TextSpan(
                            "Karim Feki",
                            url="https://www.linkedin.com/in/karimfeki/",
                            style=TextStyle(
                                decoration=TextDecoration.UNDERLINE,
                                color=colors.BLUE_ACCENT_700,
                            ),
                        ),
                        TextSpan(" ©"),
                    ],
                ),
                expand=True,
                alignment=alignment.center,
            ),
            expand=True,
        )
        
        self.settings_frame = self.make_frame()
        
        self.controls = [
            self.settings_frame,
            self.upperbar,
        ]
        
    def open_about_dialog(self, e):
        dlg = AlertDialog(
            content=Container(
                content=Column(
                    [
                        # Header
                        Row(
                            [
                                Text(
                                    "Mallouka Motors",
                                    style=self.themer.get_text_style("headline_small"),
                                    color=colors.ON_SURFACE,
                                    weight=FontWeight.W_600,
                                ),
                                IconButton(
                                    icon=Icons.CLOSE,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        bgcolor=colors.with_opacity(0.1, colors.ON_SURFACE),
                                    ),
                                    icon_color=colors.ON_SURFACE_VARIANT,
                                    on_click=lambda _: self.page.close_dialog(),
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),

                        Container(height=16),

                        # Company Logo
                        Container(
                            content=Image(
                                src="./logo/mallouka_motors_logo.png",
                                width=80,
                                height=80,
                                fit=ImageFit.CONTAIN,
                            ),
                            alignment=alignment.center,
                            margin=margin.only(bottom=16),
                        ),

                        # Description
                        Text(
                            "Mallouka Motors est une boutique de pièces détachées automobiles de premier plan, spécialisée dans l'approvisionnement et la fourniture de moteurs de voitures d'occasion haut de gamme en provenance directe d'Europe.",
                            style=self.themer.get_text_style("body_medium"),
                            color=colors.ON_SURFACE,
                            text_align=TextAlign.JUSTIFY,
                        ),

                        Container(height=16),

                        Text(
                            "Notre engagement inébranlable est d'aider nos clients à transformer leurs véhicules, les faisant passer d'un état de faiblesse à une puissance et des performances incomparables.",
                            style=self.themer.get_text_style("body_medium"),
                            color=colors.ON_SURFACE_VARIANT,
                            text_align=TextAlign.JUSTIFY,
                        ),

                        Container(height=24),

                        # Social Links
                        Text(
                            "Nous contacter",
                            style=self.themer.get_text_style("title_small"),
                            color=colors.ON_SURFACE,
                            weight=FontWeight.W_600,
                        ),

                        Container(height=12),

                        Row(
                            [
                                IconButton(
                                    icon=Icons.MAIL,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        bgcolor=colors.with_opacity(0.1, colors.PRIMARY),
                                        padding=padding.all(12),
                                    ),
                                    icon_color=colors.PRIMARY,
                                    tooltip="Email",
                                    on_click=lambda _: self.page.launch_url("mailto:malloukamotors21@gmail.com"),
                                ),
                                IconButton(
                                    content=Image(
                                        src="./icons/instagram.svg",
                                        color=colors.PRIMARY,
                                        width=24,
                                        height=24,
                                    ),
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        bgcolor=colors.with_opacity(0.1, colors.PRIMARY),
                                        padding=padding.all(12),
                                    ),
                                    tooltip="Instagram",
                                    on_click=lambda _: self.page.launch_url("https://www.instagram.com/allo.casse.auto.tn/"),
                                ),
                                IconButton(
                                    icon=Icons.TIKTOK,
                                    style=ButtonStyle(
                                        shape=CircleBorder(),
                                        bgcolor=colors.with_opacity(0.1, colors.PRIMARY),
                                        padding=padding.all(12),
                                    ),
                                    icon_color=colors.PRIMARY,
                                    tooltip="TikTok",
                                    on_click=lambda _: self.page.launch_url("https://www.tiktok.com/@allo.casse.auto.tn"),
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            spacing=16,
                        ),
                    ],
                    spacing=0,
                ),
                width=400,
                padding=20,
            ),
            bgcolor=colors.SURFACE,
            shape=RoundedRectangleBorder(radius=16),
            adaptive=True,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def make_frame(self):
        self.settings_frame = SafeArea(
            content=Column(
                controls=[
                    # Settings Header
                    Container(
                        content=self.themer.create_section_title("Paramètres", "display_small"),
                        margin=margin.only(bottom=40),
                        alignment=alignment.center,
                    ),

                    # Theme Settings Card
                    self.themer.create_card_container(
                        content=Column([
                            Row([
                                Icon(
                                    icons.PALETTE,
                                    size=24,
                                    color=colors.PRIMARY,
                                ),
                                Text(
                                    "Apparence",
                                    style=self.themer.get_text_style("title_medium"),
                                    color=colors.ON_SURFACE,
                                ),
                            ], spacing=12),
                            Container(height=16),
                            Row([
                                Column([
                                    Text(
                                        "Mode Sombre",
                                        style=self.themer.get_text_style("body_large"),
                                        color=colors.ON_SURFACE,
                                    ),
                                    Text(
                                        "Basculer entre le mode clair et sombre",
                                        style=self.themer.get_text_style("body_small"),
                                        color=colors.ON_SURFACE_VARIANT,
                                    ),
                                ], expand=True, spacing=4),
                                self.parent_class.themer.theme_switch,
                            ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=0),
                        elevated=True,
                        padding=24,
                    ),

                    Container(height=20),

                    # About Section Card
                    self.themer.create_card_container(
                        content=Column([
                            Row([
                                Icon(
                                    icons.INFO,
                                    size=24,
                                    color=colors.PRIMARY,
                                ),
                                Text(
                                    "À propos",
                                    style=self.themer.get_text_style("title_medium"),
                                    color=colors.ON_SURFACE,
                                ),
                            ], spacing=12),
                            Container(height=16),
                            ElevatedButton(
                                content=Row(
                                    [
                                        Icon(icons.INFO_OUTLINE, size=20),
                                        Text("Voir les informations"),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=8,
                                ),
                                style=self.themer.get_button_style("outline"),
                                on_click=self.open_about_dialog,
                            ),
                        ], spacing=0),
                        elevated=True,
                        padding=24,
                    ),

                    Container(height=40),

                    # Footer
                    Container(
                        content=Text(
                            "Développé par ",
                            spans=[
                                TextSpan(
                                    "Karim Feki",
                                    url="https://www.linkedin.com/in/karimfeki/",
                                    style=TextStyle(
                                        decoration=TextDecoration.UNDERLINE,
                                        color=colors.PRIMARY,
                                        weight=FontWeight.W_500,
                                    ),
                                ),
                                TextSpan(f" © {datetime.now().year}"),
                            ],
                            style=self.themer.get_text_style("body_medium"),
                            color=colors.ON_SURFACE_VARIANT,
                            text_align=TextAlign.CENTER,
                        ),
                        alignment=alignment.center,
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            expand=True,
        )
        return self.settings_frame


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
