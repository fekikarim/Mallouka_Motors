from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster

class Settings:
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):
        
        super().__init__()
        
        
        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True
        
        self.page_name = "Allo Casse Auto - Settings"
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
                    "Developed by ",
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
            content=Column(
                [
                    Row(
                        [
                            Text("Mallouka Motors", size=20, weight=FontWeight.BOLD),
                            IconButton(
                                icon=Icons.CLOSE,
                                style=ButtonStyle(shape=CircleBorder()),
                                on_click=lambda _: self.page.close_dialog(),
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    Divider(), 
                    Text(
                        "Mallouka Motors is a premier Auto Parts Store, specializing in sourcing and providing top-tier used car motors directly from Europe. Our unwavering commitment is to empower our clients to transform their vehicles, taking them from a state of weakness to unparalleled strength and performance. We meticulously select each motor, ensuring exceptional quality and reliability. At Mallouka Motors, we don't just sell parts; we deliver the potential for your car to become the best version of itself.",
                        text_align=TextAlign.JUSTIFY,
                    ),
                    Row(
                        [
                            IconButton(
                                icon=Icons.MAIL,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    padding=padding.all(10),
                                ),
                                on_click=lambda _: self.page.launch_url("mailto:malloukamotors21@gmail.com"),
                            ),
                            IconButton(
                                content=Image(
                                    src="./icons/instagram.svg",
                                    color=Colors.PRIMARY,
                                ),
                                style=ButtonStyle(
                                    color=Colors.PRIMARY,
                                    shape=CircleBorder(),
                                    padding=padding.all(10),
                                ),
                                on_click=lambda _: self.page.launch_url("https://www.instagram.com/allo.casse.auto.tn/"),
                            ),
                            IconButton(
                                icon=Icons.TIKTOK,
                                style=ButtonStyle(
                                    shape=CircleBorder(),
                                    padding=padding.all(10),
                                ),
                                on_click=lambda _: self.page.launch_url("https://www.tiktok.com/@allo.casse.auto.tn"),
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                tight=True,
            ),
            adaptive=True,
            on_dismiss=lambda e: print("Dialog dismissed!"),
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def make_frame(self):
        self.settings_frame = Container(
            content=Column(
                controls=[
                    Container(
                        content=Text("Settings", size=24, text_align='center', weight='bold'),
                        margin=margin.only(top=20, bottom=10),
                        alignment=alignment.center,
                    ),
                    self.switcher,
                    ElevatedButton(
                        content=Row(
                            [
                                Icon(icons.INFO_OUTLINE),
                                Text("About Us"),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            tight=True,
                        ),
                        on_click=self.open_about_dialog,
                    ),
                    Divider(height=50),
                    self.page.bottom_appbar,
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                expand=True,
            ),
            padding=padding.all(20),
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
