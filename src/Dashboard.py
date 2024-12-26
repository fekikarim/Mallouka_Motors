from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster

class Dashboard:
    def __init__(self, page: Page, parent_class, themer: ThemerMaster):
        
        super().__init__()
        
        self.page = page
        self.parent_class = parent_class
        self.themer = themer
        self.expand = True
        
        self.page_name = "Allo Casse Auto"
        self.icon = Icons.DASHBOARD
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame
        
        self.dashboard_frame = self.make_frame()
        
        self.controls = [
            self.dashboard_frame,
            self.upperbar,
        ]
        
        
    def make_frame(self):
        self.dashboard_frame = SafeArea(
            content=Column(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                Text("Welcome!", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    ),
                    ResponsiveRow(
                        controls=[
                            Image(
                                src=f"../assets/allo_casse_auto_logo.jpg",
                                width=150,
                                height=150,
                                fit=ImageFit.CONTAIN
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing={"xs": 10},
                    ),
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
        
        return self.dashboard_frame


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
