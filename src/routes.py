from flet import *

class Routes:
    def __init__(self, page: Page, main_app):
        self.page = page
        self.main_app = main_app
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.create_app_views()

    def route_change(self, route):
        self.page.views.clear()

        if self.page.route == "/":
            self.page.views.append(self.main_view)
        elif self.page.route == "/motors":
            self.page.views.append(self.motors_view)
        elif self.page.route == "/clients":
            self.page.views.append(self.clients_view)
        elif self.page.route.startswith("/billing/"):
            parts = self.page.route.split("/")
            if len(parts) == 3 and parts[1] == "billing":
                try:
                    billing_ref = parts[2]
                    self.page.views.append(self.main_app.billing.billing_detail_view(billing_ref))
                except Exception as e:
                    print(f"Error navigating to billing detail: {e}")
                    self.page.go("/billing")
        elif self.page.route == "/billing":
            self.page.views.append(self.billings_view)
        elif self.page.route == "/settings":
            self.page.views.append(self.settings_view)

        self.page.update()
        
        
    def view_pop(self, view):
        try:
            self.page.views.pop()
            top_view = self.page.views[-1]
            self.page.go(top_view.route)
        except:
            pass

    def make_view(self, route: str, controls: list[Control], app_bar: Control | Container = Container(), bgcolor: str | None = None):
        return View(
            route=route,
            controls=controls,
            appbar=app_bar,
            bgcolor=bgcolor,
            scroll="auto",
        )

    def create_app_views(self):
        
        p = Container(
                content=Column(
                    controls=[
                        self.main_app.themer.theme_switch,
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                margin=margin.only(top=20, bottom=20),
                alignment=alignment.center,
            )
        
        self.main_view = self.make_view(
            '/',
            [
                self.main_app.dashboard.dashboard_frame,
            ],
            app_bar=self.main_app.dashboard.upperbar,
        )

        self.motors_view = self.make_view(
            '/motors',
            [
                self.main_app.motors.motors_frame,
            ],
            app_bar=self.main_app.motors.upperbar,
        )

        self.clients_view = self.make_view(
            '/clients',
            [
                self.main_app.clients.clients_frame,
            ],
            app_bar=self.main_app.clients.upperbar,
        )

        self.billings_view = self.make_view(
            '/billing',
            [
                self.main_app.billing.billing_frame,
            ],
            app_bar=self.main_app.billing.upperbar,
        )

        self.settings_view = self.make_view(
            '/settings',
            [
                self.main_app.settings.settings_frame,
                p
            ],
            app_bar=self.main_app.settings.upperbar,
        )
