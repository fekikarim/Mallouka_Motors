from flet import *
from Themer import ThemerMaster
from app_bar import AppBarMaster
from db import *
from collections import Counter
from datetime import datetime

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
        
        self.motor_chart = self.create_motor_chart()
        self.client_chart = self.create_client_chart()
        self.billing_chart = self.create_billing_chart()

        self.dashboard_frame = self.make_frame()

        self.controls = [
            self.dashboard_frame,
            self.upperbar,
        ]
        
    
    def get_dashboard_metrics(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(total_price) FROM Billing")
        total_revenue = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM Clients")
        total_clients = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity) FROM Billing_Motors")
        total_motors_sold = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM Motors WHERE statut = 'Disponible'")
        available_motors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Motors")
        total_motors = cursor.fetchone()[0]

        conn.close()
        return {
            "total_revenue": total_revenue,
            "total_clients": total_clients,
            "total_motors_sold": total_motors_sold,
            "available_motors": available_motors,
            "total_motors": total_motors
        }

    def create_motor_chart(self):
        motors = get_motors()
        status_counts = Counter(motor[8] for motor in motors)

        # Styling and dimensions
        normal_radius = 70
        hover_radius = 100
        normal_title_style = TextStyle(size=16, weight=FontWeight.BOLD)
        hover_title_style = TextStyle(
            size=18,
            weight=FontWeight.BOLD,
            shadow=BoxShadow(blur_radius=2, color=colors.BLACK54),
        )

        # Event handler for chart interactions
        def on_chart_event(e: PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            # Update the UI
            chart.update()

        # Create sections for the chart
        sections = []
        statuses = ["Disponible", "Reserve", "Vendu"]
        for status in statuses:
            count = status_counts.get(status, 0)
            total_motors = len(motors)
            percentage = (count / total_motors) * 100 if total_motors > 0 else 0
            sections.append(
                PieChartSection(
                    value=percentage,
                    title=f"{percentage:.1f}%",
                    color={
                        "Disponible": Colors.PRIMARY_CONTAINER,
                        "Reserve": Colors.PURPLE,
                        "Vendu": Colors.TERTIARY_CONTAINER,
                    }.get(status, Colors.OUTLINE),
                    radius=normal_radius,
                    title_style=normal_title_style,
                )
            )

        # Create the chart
        chart = PieChart(
            sections=sections,
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event,  # Attach the event handler
            expand=True,
        )

        return chart


    def create_client_chart(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nom_complet, COUNT(b.client_id)
            FROM Clients c
            LEFT JOIN Billing b ON c.id = b.client_id
            GROUP BY c.nom_complet
        """)
        client_billing_counts = cursor.fetchall()
        conn.close()

        bar_groups = []
        for i, (client_name, billing_count) in enumerate(client_billing_counts):
            bar_groups.append(
                BarChartGroup(
                    x=i,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=billing_count,
                            width=15,
                            tooltip=f"{client_name}: {billing_count}",
                            border_radius=3,
                        ),
                    ],
                )
            )

        chart = BarChart(
            bar_groups=bar_groups,
            border=border.all(1, self.themer.outline),
            left_axis=ChartAxis(labels_size=40,title=Text("Number of Billings"), title_size=40,),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(
                        value=i,
                        label=Container(
                            Text(client_name),
                            padding=10,
                        ),
                    )
                    for i, (client_name, _) in enumerate(client_billing_counts)
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ChartGridLines(
                color=Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=Colors.with_opacity(0.5, Colors.GREY_300),
            interactive=True,
            expand=True,
        )
        
        return chart

    def create_billing_chart(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date FROM Billing")
        billing_dates = cursor.fetchall()
        conn.close()

        daily_billings = Counter(datetime.fromisoformat(date[0]).strftime('%Y-%m-%d') for date in billing_dates)
        sorted_dates = sorted(daily_billings.keys())

        data_points = [
            LineChartDataPoint(i, daily_billings[date])
            for i, date in enumerate(sorted_dates)
        ]

        chart = LineChart(
            data_series=[
                LineChartData(
                    data_points=data_points,
                    stroke_width=3,
                    stroke_cap_round=True,
                ),
            ],
            border=border.all(1, self.themer.outline),
            left_axis=ChartAxis(labels_size=40,title=Text("Number of Billings"), title_size=40,),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(
                        value=i,
                        label=Container(
                            Text(date.split('-')[2], size=10),  # Display only the day
                            padding=padding.only(top=8),
                        ),
                    )
                    for i, date in enumerate(sorted_dates)
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ChartGridLines(
                color=Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=Colors.with_opacity(0.5, Colors.GREY_300),
            interactive=True,
            expand=True,
        )
        
        return chart

    def make_frame(self):
        metrics = self.get_dashboard_metrics()
        self.dashboard_frame = SafeArea(
            content=Column(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                Text("Dashboard Overview", size=24, text_align='center', weight='bold'),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        margin=margin.only(top=20, bottom=20),
                        alignment=alignment.center,
                    ),
                    ResponsiveRow(
                        controls=[
                            Image(
                                src=f"./mallouka_motors_logo.png",
                                width=150,
                                height=150,
                                fit=ImageFit.CONTAIN
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing={"xs": 10},
                    ),
                    Divider(height=4),
                    ResponsiveRow(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Container(content=Text(f"Total Revenue: ${metrics['total_revenue']:.2f}"), col={"sm": 6, "md": 4, "lg": 2}, alignment=alignment.center),
                            Container(content=Text(f"Total Clients: {metrics['total_clients']}"), col={"sm": 6, "md": 4, "lg": 2}, alignment=alignment.center),
                            Container(content=Text(f"Total Motors Sold: {metrics['total_motors_sold']}"), col={"sm": 6, "md": 4, "lg": 2}, alignment=alignment.center),
                            Container(content=Text(f"Available Motors: {metrics['available_motors']}"), col={"sm": 6, "md": 4, "lg": 2}, alignment=alignment.center),
                            Container(content=Text(f"Total Motors: {metrics['total_motors']}"), col={"sm": 6, "md": 4, "lg": 2}, alignment=alignment.center),
                        ],
                    ),
                    Divider(height=4),
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=Column(
                                    controls=[
                                        self.motor_chart,  # The chart goes here                                        
                                    ],
                                    alignment=MainAxisAlignment.CENTER,  # Center both chart and button
                                    spacing=10,  # Space between chart and button
                                ),
                                alignment=alignment.center,
                                col={"sm": 12, "md": 6},
                            ),
                            
                            ElevatedButton(
                                "View Details",
                                style=ButtonStyle(shape=RoundedRectangleBorder(radius=180)),
                                on_click=lambda _: self.page.go("/motors"),
                                expand=True,  # Expands the button width                                
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing={"xs": 10},
                    ),
                    Divider(height=50),
                    ResponsiveRow(
                        controls=[
                            
                            Container(
                                content=Column(
                                    controls=[
                                        self.client_chart,                                     
                                    ],
                                    alignment=MainAxisAlignment.CENTER,  # Center both chart and button
                                    spacing=10,  # Space between chart and button
                                ),
                                alignment=alignment.center,
                                col={"sm": 12, "md": 6},
                            ),
                            
                            ElevatedButton(
                                "View Details",
                                style=ButtonStyle(shape=RoundedRectangleBorder(radius=180)),
                                on_click=lambda _: self.page.go("/clients"),
                                expand=True,
                            ),

                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing={"xs": 10},
                    ),
                    Divider(height=50),
                    ResponsiveRow(
                        controls=[
                            
                            Container(
                                content=Column(
                                    controls=[
                                        self.billing_chart,                                   
                                    ],
                                    alignment=MainAxisAlignment.CENTER,  # Center both chart and button
                                    spacing=10,  # Space between chart and button
                                ),
                                alignment=alignment.center,
                                col={"sm": 12, "md": 6},
                            ),
                            
                            ElevatedButton(
                                "View Details",
                                style=ButtonStyle(shape=RoundedRectangleBorder(radius=180)),
                                on_click=lambda _: self.page.go("/billing"),
                                expand=True,
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
