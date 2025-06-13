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

        self.page_name = "Mallouka Motors"
        self.icon = Icons.DASHBOARD
        self.ub = AppBarMaster(self.page, self.parent_class, self.themer, self.page_name, self.icon)
        self.upperbar = self.ub.app_bar_frame

        # Initialize metric cards as instance variables for real-time updates
        self.metric_cards = {}
        self.current_metrics = {}

        self.motor_chart = self.create_motor_chart()
        self.client_chart = self.create_client_chart()
        self.billing_chart = self.create_billing_chart()

        self.dashboard_frame = self.make_frame()

        self.controls = [
            self.dashboard_frame,
            self.upperbar,
        ]

        # Load initial data
        self.load_dashboard_data()
        
    
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

    def load_dashboard_data(self):
        """Load and refresh all dashboard data with error handling"""
        try:
            new_metrics = self.get_dashboard_metrics()
            self.current_metrics = new_metrics
            self.refresh_dashboard_stats()
        except Exception as e:
            print(f"Error loading dashboard data: {e}")
            if hasattr(self, 'page') and self.page:
                self.page.show_snack_bar(SnackBar(Text("Erreur lors du chargement des statistiques")))

    def refresh_dashboard_stats(self):
        """Refresh only the statistics without recreating the entire dashboard"""
        if not hasattr(self, 'metric_cards') or not self.metric_cards:
            return

        try:
            metrics = self.current_metrics

            # Update each metric card with new values and animations
            metric_configs = [
                ("total_revenue", f"{metrics['total_revenue']:.2f} DT", icons.ATTACH_MONEY, colors.GREEN_500),
                ("total_clients", str(metrics['total_clients']), icons.PEOPLE, colors.BLUE_500),
                ("total_motors_sold", str(metrics['total_motors_sold']), icons.TRENDING_UP, colors.PURPLE_500),
                ("available_motors", str(metrics['available_motors']), icons.INVENTORY, colors.ORANGE_500),
                ("total_motors", str(metrics['total_motors']), icons.CAR_REPAIR, colors.TEAL_500),
            ]

            for key, value, _, _ in metric_configs:
                if key in self.metric_cards:
                    # Update the value text in the metric card with animation
                    value_text = self.metric_cards[key]['value_text']
                    if value_text and value_text.value != value:
                        # Add subtle animation for value changes
                        value_text.opacity = 0.7
                        value_text.value = value
                        value_text.opacity = 1.0

            # Update charts if needed
            self._refresh_charts()

            # Update the page to reflect changes
            if hasattr(self, 'page') and self.page:
                self.page.update()

        except Exception as e:
            print(f"Error refreshing dashboard stats: {e}")

    def _refresh_charts(self):
        """Refresh charts data for real-time updates"""
        try:
            # Update motor chart
            if hasattr(self, 'motor_chart'):
                self.motor_chart = self.create_motor_chart()

            # Update client chart
            if hasattr(self, 'client_chart'):
                self.client_chart = self.create_client_chart()

            # Update billing chart
            if hasattr(self, 'billing_chart'):
                self.billing_chart = self.create_billing_chart()

        except Exception as e:
            print(f"Error refreshing charts: {e}")

    def refresh_dashboard_async(self):
        """Asynchronous dashboard refresh for better performance"""
        import threading

        def refresh_worker():
            try:
                self.load_dashboard_data()
            except Exception as e:
                print(f"Error in async dashboard refresh: {e}")

        # Run refresh in background thread to avoid UI blocking
        thread = threading.Thread(target=refresh_worker, daemon=True)
        thread.start()

    def create_enhanced_metric_cards(self, metrics):
        """Create enhanced metric cards with modern design and store references for updates"""
        metric_configs = [
            ("total_revenue", "Revenu Total", f"{metrics['total_revenue']:.2f} DT", icons.ATTACH_MONEY, colors.GREEN_500),
            ("total_clients", "Total Clients", str(metrics['total_clients']), icons.PEOPLE, colors.BLUE_500),
            ("total_motors_sold", "Moteurs Vendus", str(metrics['total_motors_sold']), icons.TRENDING_UP, colors.PURPLE_500),
            ("available_motors", "Moteurs Disponibles", str(metrics['available_motors']), icons.INVENTORY, colors.ORANGE_500),
            ("total_motors", "Total Moteurs", str(metrics['total_motors']), icons.CAR_REPAIR, colors.TEAL_500),
        ]

        controls = []
        self.metric_cards = {}  # Reset metric cards storage

        for key, title, value, icon, color in metric_configs:
            # Create enhanced metric card with reference storage
            card_data = self.themer.create_metric_card(title, value, icon, color, key=key)

            # Store references for real-time updates
            self.metric_cards[key] = card_data

            # Enhanced responsive container with perfect centering
            card_container = Container(
                content=Container(
                    content=card_data['card'],
                    alignment=alignment.center,
                ),
                col={
                    "xs": 12,    # Full width on extra small screens
                    "sm": 6,     # Half width on small screens
                    "md": 4,     # One-third width on medium screens
                    "lg": 2.4,   # Five cards per row on large screens
                    "xl": 2.4    # Five cards per row on extra large screens
                },
                alignment=alignment.center,
                animate=animation.Animation(400, AnimationCurve.EASE_OUT),
                animate_scale=animation.Animation(300, AnimationCurve.EASE_OUT),
            )

            controls.append(card_container)

        return controls

    def update_metric_card_value(self, key, new_value):
        """Update a specific metric card value with animation"""
        if key in self.metric_cards:
            try:
                value_text = self.metric_cards[key]['value_text']
                if value_text and value_text.value != str(new_value):
                    # Animate value change
                    value_text.opacity = 0.5
                    value_text.update()

                    # Update value
                    value_text.value = str(new_value)
                    value_text.opacity = 1.0
                    value_text.update()

                    # Add subtle scale animation to the card
                    card = self.metric_cards[key]['card']
                    if hasattr(card, 'scale'):
                        card.scale = 1.02
                        card.update()
                        # Reset scale after animation
                        import time
                        time.sleep(0.1)
                        card.scale = 1.0
                        card.update()

            except Exception as e:
                print(f"Error updating metric card {key}: {e}")

    def create_motor_chart(self):
        motors = get_motors()
        status_counts = Counter(motor[8] for motor in motors)

        # Enhanced styling and dimensions with better responsiveness
        normal_radius = 70
        hover_radius = 95
        normal_title_style = TextStyle(
            size=13,
            weight=FontWeight.W_600,
            color=colors.ON_SURFACE,
        )
        hover_title_style = TextStyle(
            size=15,
            weight=FontWeight.W_700,
            color=colors.ON_SURFACE,
            shadow=BoxShadow(blur_radius=4, color=colors.with_opacity(0.3, colors.SHADOW)),
        )

        # Enhanced event handler for chart interactions with tooltip support
        def on_chart_event(e: PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            chart.update()

        # Create sections with modern colors and enhanced tooltips
        sections = []
        statuses = ["Disponible", "Reserve", "Vendu"]
        colors_map = {
            "Disponible": colors.GREEN_400,
            "Reserve": colors.ORANGE_400,
            "Vendu": colors.BLUE_400,
        }

        for status in statuses:
            count = status_counts.get(status, 0)
            total_motors = len(motors)
            percentage = (count / total_motors) * 100 if total_motors > 0 else 0
            sections.append(
                PieChartSection(
                    value=percentage,
                    title=f"{status}\n{count} moteurs\n{percentage:.1f}%",
                    color=colors_map.get(status, colors.GREY_400),
                    radius=normal_radius,
                    title_style=normal_title_style,
                )
            )

        # Create the enhanced chart with better sizing
        chart = PieChart(
            sections=sections,
            sections_space=3,
            center_space_radius=40,
            on_chart_event=on_chart_event,
            expand=True,
        )

        # Dynamic container with responsive sizing
        card_style = self.themer.get_card_style(elevated=True)
        return Container(
            content=chart,
            bgcolor=card_style.get("bgcolor"),
            border_radius=card_style.get("border_radius"),
            border=card_style.get("border"),
            shadow=card_style.get("shadow"),
            height=400,  # Increased height for better tooltip visibility
            width=400,   # Fixed width for consistent pie chart appearance
            padding=padding.all(20),  # Added padding to prevent tooltip cutoff
            clip_behavior=ClipBehavior.NONE,  # Allow tooltips to extend beyond container
        )


    def create_client_chart(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nom_complet, COUNT(b.client_id)
            FROM Clients c
            LEFT JOIN Billing b ON c.id = b.client_id
            GROUP BY c.nom_complet
            LIMIT 10
        """)
        client_billing_counts = cursor.fetchall()
        conn.close()

        # Calculate dynamic height based on number of clients
        num_clients = len(client_billing_counts)
        base_height = 350
        dynamic_height = max(base_height, base_height + (num_clients * 5))

        bar_groups = []
        for i, (client_name, billing_count) in enumerate(client_billing_counts):
            bar_groups.append(
                BarChartGroup(
                    x=i,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=billing_count,
                            width=25,  # Slightly wider bars for better visibility
                            tooltip=f"{client_name}: {billing_count} factures",
                            border_radius=8,
                            color=colors.PRIMARY,
                            gradient=LinearGradient(
                                begin=alignment.bottom_center,
                                end=alignment.top_center,
                                colors=[colors.PRIMARY, colors.PRIMARY_CONTAINER],
                            ),
                        ),
                    ],
                )
            )

        chart = BarChart(
            bar_groups=bar_groups,
            border=border.all(1, colors.OUTLINE_VARIANT),
            left_axis=ChartAxis(
                labels_size=50,  # Increased for better readability
                title=Text(
                    "Nombre de Factures",
                    style=self.themer.get_text_style("label_medium"),
                    color=colors.ON_SURFACE_VARIANT,
                ),
                title_size=50,
            ),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(
                        value=i,
                        label=Container(
                            Text(
                                client_name[:12] + "..." if len(client_name) > 12 else client_name,
                                style=self.themer.get_text_style("label_small"),
                                color=colors.ON_SURFACE_VARIANT,
                                text_align=TextAlign.CENTER,
                            ),
                            padding=padding.all(10),  # Increased padding
                        ),
                    )
                    for i, (client_name, _) in enumerate(client_billing_counts)
                ],
                labels_size=60,  # Increased for better label visibility
            ),
            horizontal_grid_lines=ChartGridLines(
                color=colors.OUTLINE_VARIANT,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=colors.with_opacity(0.95, colors.SURFACE),
            interactive=True,
            expand=True,
            max_y=None,  # Allow dynamic Y-axis scaling
        )

        card_style = self.themer.get_card_style(elevated=True)
        return Container(
            content=chart,
            bgcolor=card_style.get("bgcolor"),
            border_radius=card_style.get("border_radius"),
            border=card_style.get("border"),
            shadow=card_style.get("shadow"),
            height=dynamic_height,  # Dynamic height based on content
            padding=padding.all(25),  # Increased padding to prevent tooltip cutoff
            clip_behavior=ClipBehavior.NONE,  # Allow tooltips to extend beyond container
        )


    def create_billing_chart(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date FROM Billing ORDER BY date DESC LIMIT 30")
        billing_dates = cursor.fetchall()
        conn.close()

        daily_billings = Counter(datetime.fromisoformat(date[0]).strftime('%Y-%m-%d') for date in billing_dates)
        sorted_dates = sorted(daily_billings.keys())[-15:]  # Show last 15 days

        # Enhanced data points - tooltips handled by chart level
        data_points = [
            LineChartDataPoint(i, daily_billings[date])
            for i, date in enumerate(sorted_dates)
        ]

        # Calculate dynamic height based on data range
        max_value = max(daily_billings.values()) if daily_billings else 1
        base_height = 350
        dynamic_height = max(base_height, base_height + (max_value * 10))

        chart = LineChart(
            data_series=[
                LineChartData(
                    data_points=data_points,
                    stroke_width=5,  # Slightly thicker line for better visibility
                    stroke_cap_round=True,
                    color=colors.SECONDARY,
                    gradient=LinearGradient(
                        begin=alignment.top_center,
                        end=alignment.bottom_center,
                        colors=[
                            colors.with_opacity(0.4, colors.SECONDARY),
                            colors.with_opacity(0.1, colors.SECONDARY),
                        ],
                    ),
                    curved=True,
                    point=True,  # Show data points
                ),
            ],
            border=border.all(1, colors.OUTLINE_VARIANT),
            left_axis=ChartAxis(
                labels_size=50,  # Increased for better readability
                title=Text(
                    "Nombre de Factures",
                    style=self.themer.get_text_style("label_medium"),
                    color=colors.ON_SURFACE_VARIANT,
                ),
                title_size=50,
            ),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(
                        value=i,
                        label=Container(
                            Text(
                                date.split('-')[2],  # Show day only
                                style=self.themer.get_text_style("label_small"),
                                color=colors.ON_SURFACE_VARIANT,
                                text_align=TextAlign.CENTER,
                            ),
                            padding=padding.all(10),  # Increased padding
                        ),
                    )
                    for i, date in enumerate(sorted_dates)
                ],
                labels_size=50,  # Increased for better label visibility
            ),
            horizontal_grid_lines=ChartGridLines(
                color=colors.OUTLINE_VARIANT,
                width=1,
                dash_pattern=[3, 3]
            ),
            vertical_grid_lines=ChartGridLines(
                color=colors.OUTLINE_VARIANT,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=colors.with_opacity(0.95, colors.SURFACE),
            interactive=True,
            expand=True,
            max_y=None,  # Allow dynamic Y-axis scaling
        )

        card_style = self.themer.get_card_style(elevated=True)
        return Container(
            content=chart,
            bgcolor=card_style.get("bgcolor"),
            border_radius=card_style.get("border_radius"),
            border=card_style.get("border"),
            shadow=card_style.get("shadow"),
            height=dynamic_height,  # Dynamic height based on data
            padding=padding.all(25),  # Increased padding to prevent tooltip cutoff
            clip_behavior=ClipBehavior.NONE,  # Allow tooltips to extend beyond container
        )


    def make_frame(self):
        metrics = self.get_dashboard_metrics()
        self.dashboard_frame = SafeArea(
            content=Column(
                controls=[
                    # Header Section
                    Container(
                        content=Column(
                            controls=[
                                self.themer.create_section_title(
                                    "Aperçu du Tableau de Bord",
                                    "display_small"
                                ),
                                Text(
                                    "Bienvenue dans votre espace de gestion",
                                    style=self.themer.get_text_style("body_large"),
                                    color=colors.ON_SURFACE_VARIANT,
                                    text_align=TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        margin=margin.only(top=20, bottom=30),
                        alignment=alignment.center,
                    ),

                    # Logo Section
                    Container(
                        content=Image(
                            src=f"./logo/mallouka_motors_logo.png",
                            width=120,
                            height=120,
                            fit=ImageFit.CONTAIN
                        ),
                        alignment=alignment.center,
                        margin=margin.only(bottom=30),
                    ),

                    # Enhanced Metrics Section with Perfect Responsive Centering
                    Container(
                        content=Container(
                            content=Column([
                                # Section Header with Perfect Centering
                                Container(
                                    content=Row([
                                        Icon(icons.ANALYTICS, size=24, color=colors.PRIMARY),
                                        Text(
                                            "Statistiques Générales",
                                            style=self.themer.get_text_style("headline_small"),
                                            weight=FontWeight.W_600,
                                            color=colors.ON_SURFACE,
                                        ),
                                    ],
                                    spacing=10,
                                    alignment=MainAxisAlignment.CENTER,
                                    tight=True,
                                    ),
                                    margin=margin.only(bottom=20),
                                    alignment=alignment.center,
                                ),

                                # Perfectly Centered Responsive Metrics Cards Container
                                Container(
                                    content=ResponsiveRow(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=self.create_enhanced_metric_cards(metrics),
                                        run_spacing=16,
                                        spacing=16,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    alignment=alignment.center,
                                    padding=padding.symmetric(horizontal=16),
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            alignment=alignment.center,
                            width=min(1400, self.page.window_width * 0.98) if hasattr(self.page, 'window_width') else 1400,
                            padding=padding.symmetric(horizontal=20),
                        ),
                        margin=margin.only(bottom=32),
                        alignment=alignment.center,
                    ),
                    Container(height=40),

                    # Decorative Image
                    Container(
                        content=Image(
                            src=f"diy_mefteh.gif",
                            width=150,
                            height=150,
                            fit=ImageFit.CONTAIN
                        ),
                        alignment=alignment.center,
                        margin=margin.only(bottom=30),
                    ),

                    # Motor Status Chart Section
                    self.themer.create_section_title("Répartition des Statuts des Moteurs"),
                    Container(height=20),

                    # Legend
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=Row([
                                    Container(
                                        width=16,
                                        height=16,
                                        bgcolor=colors.GREEN_400,
                                        border_radius=8,
                                    ),
                                    Text(
                                        "Disponible",
                                        style=self.themer.get_text_style("label_medium"),
                                        color=colors.ON_SURFACE,
                                    ),
                                ], spacing=8),
                                col={"xs": 4, "sm": 4, "md": 3, "lg": 2},
                            ),
                            Container(
                                content=Row([
                                    Container(
                                        width=16,
                                        height=16,
                                        bgcolor=colors.ORANGE_400,
                                        border_radius=8,
                                    ),
                                    Text(
                                        "Réservé",
                                        style=self.themer.get_text_style("label_medium"),
                                        color=colors.ON_SURFACE,
                                    ),
                                ], spacing=8),
                                col={"xs": 4, "sm": 4, "md": 3, "lg": 2},
                            ),
                            Container(
                                content=Row([
                                    Container(
                                        width=16,
                                        height=16,
                                        bgcolor=colors.BLUE_400,
                                        border_radius=8,
                                    ),
                                    Text(
                                        "Vendu",
                                        style=self.themer.get_text_style("label_medium"),
                                        color=colors.ON_SURFACE,
                                    ),
                                ], spacing=8),
                                col={"xs": 4, "sm": 4, "md": 3, "lg": 2},
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        spacing=16,
                    ),
                    Container(height=20),

                    # Enhanced Chart Container with better responsive sizing
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=self.motor_chart,
                                col={"xs": 12, "sm": 12, "md": 10, "lg": 8, "xl": 6},
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing=20,
                    ),
                    Container(height=20),

                    # Action Button
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=ElevatedButton(
                                    "Voir les détails",
                                    style=self.themer.get_button_style("primary"),
                                    icon=icons.ARROW_FORWARD,
                                    on_click=lambda _: self.page.go("/motors"),
                                ),
                                col={"xs": 6, "sm": 4, "md": 3, "lg": 2},
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Container(height=60),

                    # Decorative Image
                    Container(
                        content=Image(
                            src=f"busy_fixing.gif",
                            width=150,
                            height=300,
                            fit=ImageFit.CONTAIN
                        ),
                        alignment=alignment.center,
                        margin=margin.only(bottom=30),
                    ),

                    # Client Billing Chart Section
                    self.themer.create_section_title("Facturations par Client"),
                    Container(height=20),

                    # Enhanced Client Chart Container with better responsive sizing
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=self.client_chart,
                                col={"xs": 12, "sm": 12, "md": 12, "lg": 10, "xl": 8},
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing=20,
                    ),
                    Container(height=20),

                    ResponsiveRow(
                        controls=[
                            Container(
                                content=ElevatedButton(
                                    "Voir les détails",
                                    style=self.themer.get_button_style("primary"),
                                    icon=icons.ARROW_FORWARD,
                                    on_click=lambda _: self.page.go("/clients"),
                                ),
                                col={"xs": 6, "sm": 4, "md": 3, "lg": 2},
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Container(height=60),

                    # Decorative Image
                    Container(
                        content=Image(
                            src=f"repairing.gif",
                            width=150,
                            height=150,
                            fit=ImageFit.CONTAIN
                        ),
                        alignment=alignment.center,
                        margin=margin.only(bottom=30),
                    ),

                    # Billing Evolution Chart Section
                    self.themer.create_section_title("Évolution des Facturations"),
                    Container(height=20),

                    # Enhanced Billing Chart Container with better responsive sizing
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=self.billing_chart,
                                col={"xs": 12, "sm": 12, "md": 12, "lg": 10, "xl": 8},
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        run_spacing=20,
                    ),
                    Container(height=20),

                    ResponsiveRow(
                        controls=[
                            Container(
                                content=ElevatedButton(
                                    "Voir les détails",
                                    style=self.themer.get_button_style("primary"),
                                    icon=icons.ARROW_FORWARD,
                                    on_click=lambda _: self.page.go("/billing"),
                                ),
                                col={"xs": 6, "sm": 4, "md": 3, "lg": 2},
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),

                    Container(height=60),

                    # Footer Image
                    Container(
                        content=Image(
                            src=f"./fella.gif",
                            width=150,
                            height=150,
                            fit=ImageFit.CONTAIN
                        ),
                        alignment=alignment.center,
                        margin=margin.only(bottom=30),
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
