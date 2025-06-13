import flet as ft

STORAGE_KEY = "app_theme"

class ThemerMaster:
    def __init__(self, page: ft.Page, main_app):
        self.page = page
        self.main_app = main_app

        # Enhanced Light Theme
        self.light_theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#2563EB",  # Modern blue
                on_primary="#FFFFFF",
                primary_container="#DBEAFE",
                on_primary_container="#1E3A8A",
                secondary="#7C3AED",  # Purple accent
                on_secondary="#FFFFFF",
                secondary_container="#EDE9FE",
                on_secondary_container="#5B21B6",
                tertiary="#059669",  # Green accent
                on_tertiary="#FFFFFF",
                tertiary_container="#D1FAE5",
                on_tertiary_container="#064E3B",
                error="#DC2626",
                on_error="#FFFFFF",
                error_container="#FEE2E2",
                on_error_container="#991B1B",
                background="#FFFFFF",
                on_background="#111827",
                surface="#F9FAFB",
                on_surface="#111827",
                surface_variant="#F3F4F6",
                on_surface_variant="#6B7280",
                outline="#D1D5DB",
                outline_variant="#E5E7EB",
                shadow="#000000",
                scrim="#000000",
                inverse_surface="#1F2937",
                on_inverse_surface="#F9FAFB",
                inverse_primary="#93C5FD",
            ),
        )

        # Enhanced Dark Theme
        self.dark_theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#3B82F6",  # Bright blue for dark mode
                on_primary="#1E3A8A",
                primary_container="#1E40AF",
                on_primary_container="#DBEAFE",
                secondary="#8B5CF6",  # Purple accent
                on_secondary="#3C1A78",
                secondary_container="#6D28D9",
                on_secondary_container="#EDE9FE",
                tertiary="#10B981",  # Green accent
                on_tertiary="#064E3B",
                tertiary_container="#047857",
                on_tertiary_container="#D1FAE5",
                error="#EF4444",
                on_error="#7F1D1D",
                error_container="#B91C1C",
                on_error_container="#FEE2E2",
                background="#0F172A",
                on_background="#F1F5F9",
                surface="#1E293B",
                on_surface="#F1F5F9",
                surface_variant="#334155",
                on_surface_variant="#CBD5E1",
                outline="#475569",
                outline_variant="#64748B",
                shadow="#000000",
                scrim="#000000",
                inverse_surface="#F1F5F9",
                on_inverse_surface="#0F172A",
                inverse_primary="#1E40AF",
            ),
        )

        # Custom styling properties
        self.card_elevation = 2
        self.border_radius = 12
        self.button_radius = 8
        self.input_radius = 8

        # Typography scale
        self.text_styles = {
            "display_large": ft.TextStyle(size=57, weight=ft.FontWeight.W_400),
            "display_medium": ft.TextStyle(size=45, weight=ft.FontWeight.W_400),
            "display_small": ft.TextStyle(size=36, weight=ft.FontWeight.W_400),
            "headline_large": ft.TextStyle(size=32, weight=ft.FontWeight.W_400),
            "headline_medium": ft.TextStyle(size=28, weight=ft.FontWeight.W_400),
            "headline_small": ft.TextStyle(size=24, weight=ft.FontWeight.W_400),
            "title_large": ft.TextStyle(size=22, weight=ft.FontWeight.W_500),
            "title_medium": ft.TextStyle(size=16, weight=ft.FontWeight.W_500),
            "title_small": ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
            "body_large": ft.TextStyle(size=16, weight=ft.FontWeight.W_400),
            "body_medium": ft.TextStyle(size=14, weight=ft.FontWeight.W_400),
            "body_small": ft.TextStyle(size=12, weight=ft.FontWeight.W_400),
            "label_large": ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
            "label_medium": ft.TextStyle(size=12, weight=ft.FontWeight.W_500),
            "label_small": ft.TextStyle(size=11, weight=ft.FontWeight.W_500),
        }

        self.theme_switch = ft.Switch(
            label="Mode Sombre",
            label_position=ft.LabelPosition.LEFT,
            value=False,  # Initial value, will be updated by load_theme
            on_change=self.toggle_theme,
            active_color="#3B82F6",
            inactive_thumb_color="#CBD5E1",
            inactive_track_color="#E2E8F0",
        )

        self.current_theme = self.load_theme()
        self.apply_theme()
    def apply_theme(self):
        """Apply the current theme to the page."""
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme = self.dark_theme
        else:
            self.page.theme = self.light_theme
        self.page.update()

    def load_theme(self):
        """Loads the last selected theme from client storage."""
        saved_theme = self.page.client_storage.get(STORAGE_KEY)
        if saved_theme == "dark":
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_switch.value = True
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_switch.value = False
        self.apply_theme()

    def toggle_theme(self, e):
        """Toggles the theme and saves the selection to client storage."""
        self.page.theme_mode = (
            ft.ThemeMode.DARK if not self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.LIGHT
        )
        self.page.client_storage.set(STORAGE_KEY, "dark" if self.page.theme_mode == ft.ThemeMode.DARK else "light")
        self.apply_theme()

    def get_card_style(self, elevated=True):
        """Get consistent card styling."""
        if elevated:
            return {
                "bgcolor": ft.colors.SURFACE,
                "border_radius": self.border_radius,
                "padding": 20,
                "shadow": ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=self.card_elevation * 4,
                    color=ft.colors.with_opacity(0.1, ft.colors.SHADOW),
                    offset=ft.Offset(0, self.card_elevation),
                ),
                "border": ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            }
        else:
            return {
                "bgcolor": ft.colors.SURFACE_VARIANT,
                "border_radius": self.border_radius,
                "padding": 20,
                "border": ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            }

    def get_button_style(self, variant="primary"):
        """Get consistent button styling."""
        if variant == "primary":
            return ft.ButtonStyle(
                bgcolor=ft.colors.PRIMARY,
                color=ft.colors.ON_PRIMARY,
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=self.button_radius),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
            )
        elif variant == "secondary":
            return ft.ButtonStyle(
                bgcolor=ft.colors.SECONDARY,
                color=ft.colors.ON_SECONDARY,
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=self.button_radius),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
            )
        elif variant == "outline":
            return ft.ButtonStyle(
                bgcolor=ft.colors.TRANSPARENT,
                color=ft.colors.PRIMARY,
                side=ft.BorderSide(2, ft.colors.PRIMARY),
                shape=ft.RoundedRectangleBorder(radius=self.button_radius),
                padding=ft.padding.symmetric(horizontal=24, vertical=12),
            )
        elif variant == "text":
            return ft.ButtonStyle(
                bgcolor=ft.colors.TRANSPARENT,
                color=ft.colors.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=self.button_radius),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
            )

    def get_input_style(self):
        """Get consistent input field styling."""
        return {
            "border_radius": self.input_radius,
            "border_color": ft.colors.OUTLINE,
            "focused_border_color": ft.colors.PRIMARY,
            "filled": True,
            "fill_color": ft.colors.SURFACE_VARIANT,
        }

    def get_text_style(self, style_name):
        """Get text style by name."""
        return self.text_styles.get(style_name, self.text_styles["body_medium"])

    def create_section_title(self, text, size="headline_small"):
        """Create a consistent section title."""
        return ft.Text(
            text,
            style=self.get_text_style(size),
            weight=ft.FontWeight.W_600,
            color=ft.colors.ON_SURFACE,
        )

    def create_card_container(self, content, elevated=True, padding=20):
        """Create a styled card container."""
        style = self.get_card_style(elevated)
        return ft.Container(
            content=content,
            bgcolor=style["bgcolor"],
            border_radius=style["border_radius"],
            padding=padding,
            shadow=style.get("shadow"),
            border=style.get("border"),
        )

    def create_metric_card(self, title, value, icon=None, color=None, key=None):
        """Create an enhanced metric display card with modern professional design."""
        # Create gradient background
        gradient_color = color or ft.colors.PRIMARY

        # Enhanced gradient colors for modern look (used in future enhancements)

        # Icon with enhanced styling and gradient background - reduced size
        icon_widget = ft.Container(
            content=ft.Icon(
                icon or ft.icons.ANALYTICS,
                size=24,  # Reduced from 32
                color=ft.colors.WHITE,
            ),
            width=48,  # Reduced from 64
            height=48,  # Reduced from 64
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[gradient_color, ft.colors.with_opacity(0.8, gradient_color)],
            ),
            border_radius=16,  # Reduced from 20
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,  # Reduced from 12
                color=ft.colors.with_opacity(0.3, gradient_color),  # Reduced opacity
                offset=ft.Offset(0, 4),  # Reduced from 6
            ),
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_OUT),
        ) if icon else None

        # Value text with reduced font size for better balance
        value_text = ft.Text(
            str(value),
            style=self.get_text_style("headline_medium"),  # Reduced from headline_large
            weight=ft.FontWeight.W_700,  # Reduced from W_800
            color=ft.colors.ON_SURFACE,
            animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

        # Title with reduced font size
        title_text = ft.Text(
            title,
            style=self.get_text_style("body_small"),  # Reduced from body_medium
            color=ft.colors.ON_SURFACE_VARIANT,
            weight=ft.FontWeight.W_500,  # Reduced from W_600
        )

        # Enhanced trend indicator with animation
        trend_indicator = ft.Container(
            content=ft.Icon(
                ft.icons.TRENDING_UP,
                size=18,
                color=ft.colors.GREEN_600,
            ),
            animate=ft.animation.Animation(200, ft.AnimationCurve.BOUNCE_OUT),
            visible=False,  # Will be enabled in future updates
        )

        # Content layout with optimized spacing for better balance
        content = ft.Column([
            ft.Row([
                icon_widget,
                ft.Column([
                    ft.Row([
                        title_text,
                        trend_indicator,
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=2),  # Reduced spacing
                    value_text,
                ], spacing=2, expand=True),  # Reduced spacing
            ], alignment=ft.MainAxisAlignment.START, spacing=16),  # Reduced spacing
        ], spacing=0)

        # Enhanced card container with reduced padding for better visual balance
        card = ft.Container(
            content=content,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[ft.colors.SURFACE, ft.colors.with_opacity(0.95, ft.colors.SURFACE)],
            ),
            border_radius=16,  # Reduced from 20
            padding=18,  # Reduced from 24
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,  # Reduced from 16
                color=ft.colors.with_opacity(0.1, ft.colors.SHADOW),  # Reduced opacity
                offset=ft.Offset(0, 6),  # Reduced from 8
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.12, gradient_color)),  # Reduced border width
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_hover=self._create_card_hover_handler(gradient_color),
        )

        # Store reference to value text for updates
        if key:
            return {
                'card': card,
                'value_text': value_text,
                'title_text': title_text,
                'icon_widget': icon_widget,
                'trend_indicator': trend_indicator
            }

        return card

    def _create_card_hover_handler(self, gradient_color):
        """Create hover effect handler for metric cards with reduced effects."""
        def on_hover(e):
            if e.data == "true":  # Mouse enter
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=16,  # Reduced from 24
                    color=ft.colors.with_opacity(0.15, ft.colors.SHADOW),  # Reduced opacity
                    offset=ft.Offset(0, 8),  # Reduced from 12
                )
                e.control.border = ft.border.all(1.5, ft.colors.with_opacity(0.25, gradient_color))  # Reduced border
            else:  # Mouse leave
                e.control.shadow = ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=12,  # Reduced from 16
                    color=ft.colors.with_opacity(0.1, ft.colors.SHADOW),  # Reduced opacity
                    offset=ft.Offset(0, 6),  # Reduced from 8
                )
                e.control.border = ft.border.all(1, ft.colors.with_opacity(0.12, gradient_color))  # Reduced border
            e.control.update()
        return on_hover

    def create_enhanced_modal_dialog(self, title, content, actions, width=None, height=None):
        """
        Create an enhanced modal dialog with modern styling and animations.

        Args:
            title (str): Dialog title
            content: Dialog content (usually a form)
            actions (list): List of action buttons
            width (int): Optional dialog width
            height (int): Optional dialog height

        Returns:
            AlertDialog: Enhanced modal dialog
        """
        # Enhanced title with icon and styling
        title_widget = ft.Row([
            ft.Icon(
                ft.icons.EDIT,
                size=24,
                color=ft.colors.PRIMARY,
            ),
            ft.Text(
                title,
                style=self.get_text_style("headline_small"),
                weight=ft.FontWeight.W_600,
                color=ft.colors.ON_SURFACE,
            ),
        ], spacing=12)

        # Enhanced content container with proper styling
        content_container = ft.Container(
            content=content,
            padding=ft.padding.all(20),
            border_radius=self.border_radius,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        # Enhanced action buttons with proper styling
        enhanced_actions = []
        for action in actions:
            if hasattr(action, 'text'):
                if action.text.lower() in ['annuler', 'cancel']:
                    # Cancel button styling
                    enhanced_action = ft.ElevatedButton(
                        text=action.text,
                        style=self.get_button_style("outline"),
                        on_click=action.on_click,
                        icon=ft.icons.CANCEL,
                    )
                else:
                    # Primary action button styling
                    enhanced_action = ft.ElevatedButton(
                        text=action.text,
                        style=self.get_button_style("primary"),
                        on_click=action.on_click,
                        icon=ft.icons.CHECK,
                    )
                enhanced_actions.append(enhanced_action)
            else:
                enhanced_actions.append(action)

        # Create enhanced dialog
        dialog = ft.AlertDialog(
            modal=True,
            title=title_widget,
            content=content_container,
            actions=enhanced_actions,
            actions_alignment=ft.MainAxisAlignment.END,
            actions_padding=ft.padding.all(20),
            content_padding=ft.padding.all(0),
            title_padding=ft.padding.all(20),
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor=ft.colors.SURFACE,
            shadow_color=ft.colors.with_opacity(0.3, ft.colors.SHADOW),
            elevation=8,
            scrollable=True,
            open=True,
        )

        # Set custom dimensions if provided
        if width or height:
            dialog.content = ft.Container(
                content=content_container,
                width=width,
                height=height,
            )

        return dialog

    def create_enhanced_form_field(self, label, value="", field_type="text", options=None,
                                 required=False, read_only=False, multiline=False,
                                 prefix_icon=None, validation_pattern=None):
        """
        Create an enhanced form field with modern styling and validation.

        Args:
            label (str): Field label
            value (str): Initial value
            field_type (str): Field type ('text', 'number', 'dropdown', 'date')
            options (list): Options for dropdown fields
            required (bool): Whether field is required
            read_only (bool): Whether field is read-only
            multiline (bool): Whether text field is multiline
            prefix_icon: Icon for the field
            validation_pattern (str): Regex pattern for validation

        Returns:
            Control: Enhanced form field
        """
        input_style = self.get_input_style()

        # Base field configuration
        field_config = {
            "label": label,
            "value": str(value) if value is not None else "",
            "read_only": read_only,
            "border_radius": input_style["border_radius"],
            "border_color": input_style["border_color"],
            "focused_border_color": input_style["focused_border_color"],
            "filled": input_style["filled"],
            "fill_color": input_style["fill_color"],
            "label_style": self.get_text_style("body_medium"),
            "text_style": self.get_text_style("body_large"),
        }

        # Add icon if provided
        if prefix_icon:
            field_config["prefix_icon"] = prefix_icon

        # Add validation if required
        if required:
            field_config["helper_text"] = "* Champ obligatoire"
            field_config["helper_style"] = ft.TextStyle(
                color=ft.colors.ERROR,
                size=12,
            )

        # Create field based on type
        if field_type == "dropdown":
            # Filter out parameters not supported by Dropdown
            dropdown_config = {k: v for k, v in field_config.items()
                             if k not in ['multiline', 'input_filter', 'read_only', 'keyboard_type']}

            # Enhanced dropdown styling
            dropdown_config.update({
                "content_padding": ft.padding.symmetric(horizontal=16, vertical=12),
                "alignment": ft.alignment.center_left,
                "text_size": 14,
                "icon_size": 20,
                "dense": False,
                "max_menu_height": 300,  # Limit dropdown height
                "enable_feedback": True,  # Enable visual feedback
            })

            field = ft.Dropdown(
                **dropdown_config,
                options=[ft.dropdown.Option(key=opt[0], text=opt[1]) if isinstance(opt, tuple)
                        else ft.dropdown.Option(key=opt, text=opt) for opt in (options or [])],
                disabled=read_only,  # Use disabled instead of read_only for dropdowns
            )
        elif field_type == "number":
            field_config["input_filter"] = ft.InputFilter(
                allow=True,
                regex_string=r"^[0-9]*\.?[0-9]*$",
                replacement_string=""
            )
            field_config["keyboard_type"] = ft.KeyboardType.NUMBER
            field = ft.TextField(**field_config)
        elif field_type == "date":
            field_config["hint_text"] = "YYYY-MM-DD"
            field_config["input_filter"] = ft.InputFilter(
                allow=True,
                regex_string=r"^[0-9\-]*$",
                replacement_string=""
            )
            field = ft.TextField(**field_config)
        else:  # text field
            if multiline:
                field_config["multiline"] = True
                field_config["min_lines"] = 3
                field_config["max_lines"] = 5
            field = ft.TextField(**field_config)

        # Wrap in container for consistent spacing
        return ft.Container(
            content=field,
            margin=ft.margin.only(bottom=16),
            animate_opacity=300,
            animate_scale=300,
        )

    def create_loading_overlay(self, message="Chargement en cours..."):
        """
        Create a loading overlay for modal operations.

        Args:
            message (str): Loading message

        Returns:
            Container: Loading overlay
        """
        return ft.Container(
            content=ft.Column([
                ft.ProgressRing(
                    width=40,
                    height=40,
                    stroke_width=4,
                    color=ft.colors.PRIMARY,
                ),
                ft.Container(height=16),
                ft.Text(
                    message,
                    style=self.get_text_style("body_medium"),
                    color=ft.colors.ON_SURFACE,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0),
            padding=ft.padding.all(40),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.9, ft.colors.SURFACE),
            border_radius=self.border_radius,
        )

