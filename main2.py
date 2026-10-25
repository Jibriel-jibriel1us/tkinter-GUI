
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ============================================================
# MUDON COMMUNITY DELIVERY SUPER APP
# Final Criterion C prototype
# Built with Python's standard tkinter library
#
# Final design combination:
# - Design Idea 4: dashboard, green/cream palette, clear navigation
# - Design Idea 3: accessible service browsing and ordering
# - Improvements: search, filters, promotions, cart, clearer
#   checkout, support, order-status demonstration
#
# Prototype limitations:
# - No real GPS, online payment, database or push notifications
# - Order tracking and notifications are demonstrations
# ============================================================

# ----------------------- COLOUR PALETTE -----------------------

DARK_GREEN = "#123D2B"
FOREST_GREEN = "#1F6948"
BRIGHT_GREEN = "#4CB782"
PALE_GREEN = "#EAF4ED"
CREAM = "#F7F6F0"
WHITE = "#FFFFFF"
TEXT = "#17201A"
MUTED = "#6B7280"
BORDER = "#E1E7E1"
LIGHT_GREY = "#F1F3F1"
ORANGE = "#F3A64A"
RED = "#C74747"

FONT = "Arial"


class MudonApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mudon | Community Delivery")
        self.geometry("1240x820")
        self.minsize(760, 620)
        self.configure(bg=CREAM)

        # Product data is stored locally for this prototype.
        self.cart = {}
        self.current_page = "home"
        self.active_category = "All"
        self.search_text = tk.StringVar()
        self.cart_count_label = None
        self.content = None
        self.sidebar = None

        self.services = [
            ("🍽", "Food Delivery", "Restaurants and meals", "food"),
            ("🛒", "Groceries", "Daily essentials", "groceries"),
            ("🧺", "Laundry", "Laundry and dry cleaning", "laundry"),
            ("✚", "Healthcare", "Pharmacy and wellbeing", "healthcare"),
            ("🧹", "Cleaning", "Home cleaning services", "cleaning"),
        ]

        # Demonstration data. Prices are illustrative, not live offers.
        self.restaurants = [
            {
                "name": "Green Bowl Kitchen",
                "category": "Healthy",
                "description": "Fresh bowls and wholesome meals",
                "time": "20–30 min",
                "rating": "4.8",
                "emoji": "🥗",
                "items": [
                    ("Avocado Power Bowl", 32.00, 38.00),
                    ("Grilled Chicken Bowl", 36.00, 42.00),
                    ("Fresh Mango Smoothie", 18.00, 22.00),
                ],
            },
            {
                "name": "The Neighbourhood Café",
                "category": "Cafe",
                "description": "Coffee, sandwiches and treats",
                "time": "15–25 min",
                "rating": "4.7",
                "emoji": "☕",
                "items": [
                    ("Iced Latte", 19.00, 22.00),
                    ("Halloumi Sandwich", 27.00, 31.00),
                    ("Chocolate Cookie", 9.00, 12.00),
                ],
            },
            {
                "name": "Little Italy",
                "category": "Italian",
                "description": "Comforting Italian favourites",
                "time": "25–35 min",
                "rating": "4.6",
                "emoji": "🍝",
                "items": [
                    ("Tomato Basil Pasta", 34.00, 39.00),
                    ("Margherita Pizza", 39.00, 45.00),
                    ("Garlic Bread", 14.00, 17.00),
                ],
            },
            {
                "name": "Sakura Table",
                "category": "Asian",
                "description": "Fresh Asian-inspired dishes",
                "time": "25–35 min",
                "rating": "4.8",
                "emoji": "🍱",
                "items": [
                    ("Vegetable Sushi Set", 29.00, 34.00),
                    ("Teriyaki Rice Bowl", 35.00, 41.00),
                    ("Edamame", 12.00, 15.00),
                ],
            },
        ]

        self._build_shell()
        self.show_home()

    # ----------------------- GENERAL HELPERS -----------------------

    def money(self, amount):
        return f"AED {amount:.2f}"

    def clear_content(self):
        if self.content:
            self.content.destroy()

        self.content = tk.Frame(self.main_area, bg=CREAM)
        self.content.grid(row=0, column=0, sticky="nsew")
        self.main_area.rowconfigure(0, weight=1)
        self.main_area.columnconfigure(0, weight=1)

    def make_label(
        self, parent, text, size=10, color=TEXT,
        bold=False, bg=None, **kwargs
    ):
        return tk.Label(
            parent,
            text=text,
            font=(FONT, size, "bold" if bold else "normal"),
            fg=color,
            bg=bg or parent.cget("bg"),
            **kwargs
        )

    def make_button(
        self, parent, text, command, primary=False,
        width=None, **kwargs
    ):
        bg = FOREST_GREEN if primary else WHITE
        fg = WHITE if primary else DARK_GREEN
        active_bg = DARK_GREEN if primary else PALE_GREEN

        return tk.Button(
            parent,
            text=text,
            command=command,
            font=(FONT, 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=WHITE if primary else DARK_GREEN,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=9,
            width=width,
            **kwargs
        )

    def make_card(self, parent, padding=16):
        return tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=padding,
            pady=padding
        )

    def section_heading(self, parent, title, subtitle=None):
        self.make_label(
            parent, title, 18, DARK_GREEN, True
        ).pack(anchor="w")

        if subtitle:
            self.make_label(
                parent, subtitle, 10, MUTED
            ).pack(anchor="w", pady=(4, 0))

    # ----------------------- APP SHELL -----------------------

    def _build_shell(self):
        self.header = tk.Frame(self, bg=WHITE, height=76)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        header_inner = tk.Frame(self.header, bg=WHITE)
        header_inner.pack(fill="both", expand=True, padx=22, pady=12)

        brand = tk.Frame(header_inner, bg=WHITE)
        brand.pack(side="left")

        logo = tk.Label(
            brand,
            text="⌖",
            font=(FONT, 23, "bold"),
            fg=WHITE,
            bg=FOREST_GREEN,
            width=2,
            height=1
        )
        logo.pack(side="left", padx=(0, 10))

        brand_text = tk.Frame(brand, bg=WHITE)
        brand_text.pack(side="left")

        self.make_label(
            brand_text, "MUDON", 17, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            brand_text, "COMMUNITY DELIVERY", 8, MUTED, True
        ).pack(anchor="w")

        right_header = tk.Frame(header_inner, bg=WHITE)
        right_header.pack(side="right")

        self.make_button(
            right_header, "♧  Help Centre",
            self.show_help
        ).pack(side="left", padx=4)

        self.make_button(
            right_header, "♧  Alerts",
            self.show_notifications
        ).pack(side="left", padx=4)

        self.cart_header_button = self.make_button(
            right_header, "🛍  Cart (0)",
            self.show_cart, primary=True
        )
        self.cart_header_button.pack(side="left", padx=(4, 0))

        self.body = tk.Frame(self, bg=CREAM)
        self.body.pack(fill="both", expand=True)

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        self.sidebar = tk.Frame(self.body, bg=DARK_GREEN, width=190)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.make_label(
            self.sidebar, "YOUR COMMUNITY", 9, "#B8D9C5",
            True, bg=DARK_GREEN
        ).pack(anchor="w", padx=18, pady=(24, 14))

        self.nav_buttons = {}

        nav_items = [
            ("⌂", "Home", self.show_home),
            ("🍽", "Food Delivery", self.show_food),
            ("🛒", "Groceries", lambda: self.show_service("Groceries")),
            ("🧺", "Laundry", lambda: self.show_service("Laundry")),
            ("✚", "Healthcare", lambda: self.show_service("Healthcare")),
            ("🧹", "Cleaning", lambda: self.show_service("Cleaning")),
            ("↗", "Track Order", self.show_tracking),
            ("?", "Help Centre", self.show_help),
        ]

        for icon, label, command in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f"{icon}   {label}",
                command=command,
                anchor="w",
                font=(FONT, 10, "bold" if label == "Home" else "normal"),
                bg=DARK_GREEN,
                fg=WHITE,
                activebackground=FOREST_GREEN,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=18,
                pady=12
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[label] = btn

        spacer = tk.Frame(self.sidebar, bg=DARK_GREEN)
        spacer.pack(fill="both", expand=True)

        location_box = tk.Frame(self.sidebar, bg="#1B5039", padx=12, pady=12)
        location_box.pack(fill="x", padx=12, pady=18)

        self.make_label(
            location_box, "DELIVERING TO", 8, "#B8D9C5",
            True, bg="#1B5039"
        ).pack(anchor="w")

        self.make_label(
            location_box, "⌖  Mudon, Dubai", 10, WHITE,
            True, bg="#1B5039"
        ).pack(anchor="w", pady=(6, 0))

        self.main_area = tk.Frame(self.body, bg=CREAM)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Keep navigation usable at narrower window widths.
        self.bind("<Configure>", self._responsive_sidebar)

    def _responsive_sidebar(self, event):
        if event.widget is not self:
            return

        width = self.winfo_width()

        if width < 900 and self.sidebar.winfo_manager():
            self.sidebar.grid_remove()
        elif width >= 900 and not self.sidebar.winfo_manager():
            self.sidebar.grid()
            self.sidebar.grid(row=0, column=0, sticky="ns")

    def set_active_nav(self, active):
        for label, button in self.nav_buttons.items():
            if label == active:
                button.configure(bg=FOREST_GREEN)
            else:
                button.configure(bg=DARK_GREEN)

    def update_cart_count(self):
        count = sum(item["qty"] for item in self.cart.values())
        self.cart_header_button.configure(text=f"🛍  Cart ({count})")

    # ----------------------- HOMEPAGE -----------------------

    def show_home(self):
        self.current_page = "home"
        self.set_active_nav("Home")
        self.clear_content()

        page = self.content
        self._page_padding(page)

        # Search is visible on the homepage and filters service names.
        search_card = tk.Frame(page, bg=CREAM)
        search_card.pack(fill="x", pady=(0, 16))

        search_top = tk.Frame(search_card, bg=CREAM)
        search_top.pack(fill="x")

        intro = tk.Frame(search_top, bg=CREAM)
        intro.pack(side="left", fill="x", expand=True)

        self.make_label(
            intro, "Good day, Mudon 👋", 22, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            intro, "Everyday essentials, delivered to your neighbourhood.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 0))

        self.make_label(
            search_top, "⌖  Mudon, Dubai", 10, FOREST_GREEN, True
        ).pack(side="right", padx=(8, 0), pady=8)

        search_row = tk.Frame(page, bg=WHITE, padx=10, pady=6,
                              highlightbackground=BORDER,
                              highlightthickness=1)
        search_row.pack(fill="x", pady=(0, 18))

        self.make_label(
            search_row, "⌕", 18, FOREST_GREEN, True, bg=WHITE
        ).pack(side="left", padx=(5, 8))

        entry = tk.Entry(
            search_row,
            textvariable=self.search_text,
            font=(FONT, 11),
            bg=WHITE,
            fg=TEXT,
            relief="flat",
            insertbackground=TEXT
        )
        entry.pack(side="left", fill="x", expand=True, ipady=8)
        entry.insert(0, "")
        entry.bind("<KeyRelease>", lambda event: self.filter_home_services())

        self.make_button(
            search_row, "Search", self.filter_home_services,
            primary=True
        ).pack(side="right", padx=4)

        # Promotion banner: original price, offer price and discount.
        promo = tk.Frame(page, bg=DARK_GREEN, padx=22, pady=18)
        promo.pack(fill="x", pady=(0, 20))

        promo_left = tk.Frame(promo, bg=DARK_GREEN)
        promo_left.pack(side="left", fill="x", expand=True)

        self.make_label(
            promo_left, "YOUR NEIGHBOURHOOD, DELIVERED.", 9,
            "#B8D9C5", True, bg=DARK_GREEN
        ).pack(anchor="w")

        self.make_label(
            promo_left, "Small errands. More time for you.", 19,
            WHITE, True, bg=DARK_GREEN
        ).pack(anchor="w", pady=(6, 5))

        self.make_label(
            promo_left, "Explore local services in one simple place.",
            10, "#E0EDE4", bg=DARK_GREEN
        ).pack(anchor="w")

        promo_right = tk.Frame(promo, bg="#1B5039", padx=14, pady=12)
        promo_right.pack(side="right", padx=(12, 0))

        self.make_label(
            promo_right, "COMMUNITY OFFER", 8, "#B8D9C5",
            True, bg="#1B5039"
        ).pack()

        self.make_label(
            promo_right, "Up to 20% off*", 15, WHITE,
            True, bg="#1B5039"
        ).pack(pady=4)

        self.make_label(
            promo_right, "*Illustrative offer", 8, "#E0EDE4",
            bg="#1B5039"
        ).pack()

        # Service cards
        service_header = tk.Frame(page, bg=CREAM)
        service_header.pack(fill="x", pady=(0, 10))

        self.make_label(
            service_header, "What do you need today?", 16,
            DARK_GREEN, True
        ).pack(side="left")

        self.make_label(
            service_header, "All services in one place", 9, MUTED
        ).pack(side="right", pady=5)

        self.service_grid = tk.Frame(page, bg=CREAM)
        self.service_grid.pack(fill="x", pady=(0, 20))

        self._draw_service_cards(self.service_grid, self.services)

        # Order tracking card
        tracking_card = self.make_card(page, padding=16)
        tracking_card.pack(fill="x", pady=(0, 18))

        tracking_left = tk.Frame(tracking_card, bg=WHITE)
        tracking_left.pack(side="left", fill="x", expand=True)

        self.make_label(
            tracking_left, "↗  Your orders, at a glance", 13,
            DARK_GREEN, True, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            tracking_left,
            "Check the progress of a demonstration order and see its delivery stages.",
            9, MUTED, bg=WHITE, wraplength=560, justify="left"
        ).pack(anchor="w", pady=(5, 0))

        self.make_button(
            tracking_card, "Track an order",
            self.show_tracking, primary=True
        ).pack(side="right", padx=(12, 0))

        # Recently featured restaurants
        self.section_heading(
            page, "Popular around Mudon",
            "Browse local-style food options in the prototype."
        )

        self._draw_restaurant_cards(page, self.restaurants[:3], columns=3)

        self.make_label(
            page,
            "Prototype notice: listings and prices are sample data, not live merchant offers.",
            8, MUTED
        ).pack(anchor="w", pady=(16, 4))

    def _page_padding(self, page):
        page.pack_propagate(False)
        # The content frame expands with the available window.
        page.configure(padx=22, pady=20)

    def _draw_service_cards(self, parent, services):
        for child in parent.winfo_children():
            child.destroy()

        width = max(self.winfo_width(), 760)
        if width < 900:
            columns = 2
        elif width < 1120:
            columns = 3
        else:
            columns = 5

        for col in range(columns):
            parent.grid_columnconfigure(col, weight=1, uniform="service")

        for index, (icon, name, description, key) in enumerate(services):
            row = index // columns
            col = index % columns

            card = tk.Frame(
                parent, bg=WHITE,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=12, pady=14
            )
            card.grid(row=row, column=col, sticky="nsew",
                      padx=4, pady=4)

            self.make_label(
                card, icon, 24, FOREST_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                card, name, 10, DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w", pady=(8, 3))

            self.make_label(
                card, description, 8, MUTED, bg=WHITE,
                wraplength=135, justify="left"
            ).pack(anchor="w")

            command = self.show_food if key == "food" else (
                lambda n=name: self.show_service(n)
            )

            self.make_button(
                card, "Explore →", command
            ).pack(anchor="w", pady=(10, 0))

    def filter_home_services(self):
        query = self.search_text.get().strip().lower()

        matches = [
            service for service in self.services
            if query in service[1].lower()
            or query in service[2].lower()
        ]

        self._draw_service_cards(self.service_grid, matches)

        if not matches:
            self.make_label(
                self.service_grid,
                "No matching services. Try food, laundry, groceries, cleaning or healthcare.",
                10, MUTED
            ).grid(row=0, column=0, sticky="w", padx=8, pady=12)

    # ----------------------- FOOD DELIVERY PAGE -----------------------

    def show_food(self):
        self.current_page = "food"
        self.active_category = "All"
        self.set_active_nav("Food Delivery")
        self.clear_content()
        page = self.content
        self._page_padding(page)

        top = tk.Frame(page, bg=CREAM)
        top.pack(fill="x", pady=(0, 14))

        self.make_label(
            top, "Food Delivery", 23, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            top, "Discover meals from restaurants around your community.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 0))

        # Search and cart shortcut
        search_row = tk.Frame(
            page, bg=WHITE, padx=10, pady=6,
            highlightbackground=BORDER, highlightthickness=1
        )
        search_row.pack(fill="x", pady=(0, 14))

        self.make_label(
            search_row, "⌕", 18, FOREST_GREEN, True, bg=WHITE
        ).pack(side="left", padx=(4, 8))

        food_search = tk.Entry(
            search_row, font=(FONT, 11),
            bg=WHITE, fg=TEXT, relief="flat",
            insertbackground=TEXT
        )
        food_search.pack(side="left", fill="x", expand=True, ipady=8)
        food_search.bind(
            "<KeyRelease>",
            lambda event: self.render_food_results(
                food_search.get().strip().lower()
            )
        )

        self.make_button(
            search_row, "View cart",
            self.show_cart, primary=True
        ).pack(side="right", padx=4)

        # Category filters
        filter_frame = tk.Frame(page, bg=CREAM)
        filter_frame.pack(fill="x", pady=(0, 16))

        self.make_label(
            filter_frame, "Browse by category", 10,
            DARK_GREEN, True
        ).pack(anchor="w", pady=(0, 8))

        categories = ["All", "Healthy", "Cafe", "Italian", "Asian"]
        self.category_buttons = {}

        buttons_row = tk.Frame(filter_frame, bg=CREAM)
        buttons_row.pack(anchor="w", fill="x")

        for category in categories:
            button = tk.Button(
                buttons_row,
                text=category,
                command=lambda c=category: self.set_category(c),
                font=(FONT, 9, "bold"),
                bg=FOREST_GREEN if category == "All" else WHITE,
                fg=WHITE if category == "All" else DARK_GREEN,
                activebackground=PALE_GREEN,
                activeforeground=DARK_GREEN,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=8
            )
            button.pack(side="left", padx=(0, 7), pady=2)
            self.category_buttons[category] = button

        self.food_results = tk.Frame(page, bg=CREAM)
        self.food_results.pack(fill="both", expand=True)

        self.render_food_results("")

    def set_category(self, category):
        self.active_category = category

        for name, button in self.category_buttons.items():
            if name == category:
                button.configure(bg=FOREST_GREEN, fg=WHITE)
            else:
                button.configure(bg=WHITE, fg=DARK_GREEN)

        # Keep the selected category and search filters together.
        self.render_food_results("")

    def render_food_results(self, query):
        for child in self.food_results.winfo_children():
            child.destroy()

        filtered = [
            restaurant for restaurant in self.restaurants
            if (self.active_category == "All"
                or restaurant["category"] == self.active_category)
            and (
                query in restaurant["name"].lower()
                or query in restaurant["description"].lower()
                or query in restaurant["category"].lower()
            )
        ]

        if not filtered:
            self.make_label(
                self.food_results,
                "No restaurants match those filters. Try another search or category.",
                10, MUTED
            ).pack(anchor="w", pady=18)
            return

        self.section_heading(
            self.food_results,
            f"{len(filtered)} restaurant(s)",
            "Sample listings • AED prices • Add items to your cart"
        )

        self._draw_restaurant_cards(
            self.food_results, filtered, columns=2
        )

    def _draw_restaurant_cards(self, parent, restaurants, columns=2):
        grid = tk.Frame(parent, bg=CREAM)
        grid.pack(fill="x", pady=(12, 0))

        width = max(self.winfo_width(), 760)
        if width < 900:
            columns = 1
        elif width < 1100:
            columns = min(columns, 2)

        for col in range(columns):
            grid.grid_columnconfigure(col, weight=1, uniform="restaurants")

        for index, restaurant in enumerate(restaurants):
            row = index // columns
            col = index % columns

            card = self.make_card(grid, padding=14)
            card.grid(
                row=row, column=col, sticky="nsew",
                padx=5, pady=5
            )

            top = tk.Frame(card, bg=WHITE)
            top.pack(fill="x")

            self.make_label(
                top, restaurant["emoji"], 28, FOREST_GREEN,
                True, bg=WHITE
            ).pack(side="left", padx=(0, 10))

            name_area = tk.Frame(top, bg=WHITE)
            name_area.pack(side="left", fill="x", expand=True)

            self.make_label(
                name_area, restaurant["name"], 12,
                DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                name_area, restaurant["category"], 9,
                FOREST_GREEN, True, bg=WHITE
            ).pack(anchor="w", pady=(3, 0))

            self.make_label(
                card, restaurant["description"], 9, MUTED,
                bg=WHITE, wraplength=330, justify="left"
            ).pack(anchor="w", pady=(10, 7))

            meta = tk.Frame(card, bg=WHITE)
            meta.pack(fill="x")

            self.make_label(
                meta,
                f"★ {restaurant['rating']}   •   {restaurant['time']}",
                9, MUTED, bg=WHITE
            ).pack(side="left")

            self.make_button(
                meta, "View menu →",
                lambda r=restaurant: self.show_menu(r),
                primary=True
            ).pack(side="right")

    # ----------------------- RESTAURANT MENU -----------------------

    def show_menu(self, restaurant):
        self.current_page = "menu"
        self.set_active_nav("Food Delivery")
        self.clear_content()
        page = self.content
        self._page_padding(page)

        self.make_button(
            page, "← Back to food delivery", self.show_food
        ).pack(anchor="w", pady=(0, 12))

        heading = tk.Frame(page, bg=CREAM)
        heading.pack(fill="x", pady=(0, 16))

        self.make_label(
            heading, f"{restaurant['emoji']}  {restaurant['name']}",
            22, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            heading,
            f"{restaurant['category']}  •  ★ {restaurant['rating']}  •  {restaurant['time']}",
            10, MUTED
        ).pack(anchor="w", pady=(5, 0))

        self.make_label(
            page, "Menu", 16, DARK_GREEN, True
        ).pack(anchor="w", pady=(0, 10))

        for item_name, price, original_price in restaurant["items"]:
            card = self.make_card(page, padding=12)
            card.pack(fill="x", pady=5)

            details = tk.Frame(card, bg=WHITE)
            details.pack(side="left", fill="x", expand=True)

            self.make_label(
                details, item_name, 11, DARK_GREEN, True,
                bg=WHITE
            ).pack(anchor="w")

            discount = round(
                (original_price - price) / original_price * 100
            )

            self.make_label(
                details,
                f"{self.money(price)}    Original: {self.money(original_price)}    {discount}% off",
                9, FOREST_GREEN, bg=WHITE
            ).pack(anchor="w", pady=(5, 0))

            self.make_button(
                card, "+ Add",
                lambda n=item_name, p=price, o=original_price:
                    self.add_to_cart(n, p, o),
                primary=True
            ).pack(side="right", padx=(10, 0))

        bottom = tk.Frame(page, bg=CREAM)
        bottom.pack(fill="x", pady=(16, 0))

        self.make_button(
            bottom, "View cart and checkout",
            self.show_cart, primary=True
        ).pack(side="right")

    # ----------------------- CART AND CHECKOUT -----------------------

    def add_to_cart(self, name, price, original_price):
        if name in self.cart:
            self.cart[name]["qty"] += 1
        else:
            self.cart[name] = {
                "price": price,
                "original": original_price,
                "qty": 1
            }

        self.update_cart_count()
        messagebox.showinfo(
            "Added to cart",
            f"{name} has been added to your cart."
        )

    def cart_subtotal(self):
        return sum(
            item["price"] * item["qty"]
            for item in self.cart.values()
        )

    def cart_original_total(self):
        return sum(
            item["original"] * item["qty"]
            for item in self.cart.values()
        )

    def change_quantity(self, name, amount):
        if name not in self.cart:
            return

        self.cart[name]["qty"] += amount

        if self.cart[name]["qty"] <= 0:
            del self.cart[name]

        self.update_cart_count()
        self.show_cart()

    def show_cart(self):
        self.current_page = "cart"
        self.set_active_nav("Food Delivery")
        self.clear_content()
        page = self.content
        self._page_padding(page)

        self.make_label(
            page, "Your shopping cart", 23, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            page, "Review your items before continuing to checkout.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 16))

        if not self.cart:
            empty = self.make_card(page, padding=24)
            empty.pack(fill="x", pady=10)

            self.make_label(
                empty, "🛍", 32, FOREST_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                empty, "Your cart is empty", 15,
                DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w", pady=(8, 5))

            self.make_label(
                empty, "Explore the menu and add items to get started.",
                10, MUTED, bg=WHITE
            ).pack(anchor="w")

            self.make_button(
                page, "Browse food delivery",
                self.show_food, primary=True
            ).pack(anchor="w", pady=12)
            return

        items_panel = tk.Frame(page, bg=CREAM)
        items_panel.pack(fill="both", expand=True)

        for name, item in self.cart.items():
            row = self.make_card(items_panel, padding=12)
            row.pack(fill="x", pady=4)

            info = tk.Frame(row, bg=WHITE)
            info.pack(side="left", fill="x", expand=True)

            self.make_label(
                info, name, 11, DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                info,
                f"{self.money(item['price'])} each  •  "
                f"Original: {self.money(item['original'])}",
                9, MUTED, bg=WHITE
            ).pack(anchor="w", pady=(4, 0))

            qty = tk.Frame(row, bg=WHITE)
            qty.pack(side="right")

            self.make_button(
                qty, "−",
                lambda n=name: self.change_quantity(n, -1)
            ).pack(side="left", padx=2)

            self.make_label(
                qty, str(item["qty"]), 11, DARK_GREEN,
                True, bg=WHITE, width=3
            ).pack(side="left", padx=3)

            self.make_button(
                qty, "+",
                lambda n=name: self.change_quantity(n, 1)
            ).pack(side="left", padx=2)

        summary = self.make_card(page, padding=16)
        summary.pack(fill="x", pady=(14, 0))

        subtotal = self.cart_subtotal()
        original = self.cart_original_total()
        savings = original - subtotal

        self.make_label(
            summary, "Order summary", 14, DARK_GREEN,
            True, bg=WHITE
        ).pack(anchor="w", pady=(0, 10))

        self._summary_line(summary, "Original total", self.money(original))
        self._summary_line(summary, "Discount savings", f"- {self.money(savings)}")
        self._summary_line(summary, "Delivery fee", "Not included in demo")
        self._summary_line(summary, "Subtotal", self.money(subtotal), bold=True)

        self.make_label(
            summary,
            "Discounts are calculated from the sample menu prices. No payment is taken.",
            8, MUTED, bg=WHITE, wraplength=600, justify="left"
        ).pack(anchor="w", pady=(8, 10))

        # Prominent button, following the checkout improvement.
        self.make_button(
            summary, "Continue to checkout",
            self.show_checkout, primary=True
        ).pack(anchor="e", pady=(4, 0))

        self.make_button(
            page, "← Continue browsing",
            self.show_food
        ).pack(anchor="w", pady=(12, 0))

    def _summary_line(self, parent, label, value, bold=False):
        line = tk.Frame(parent, bg=WHITE)
        line.pack(fill="x", pady=3)

        self.make_label(
            line, label, 10, DARK_GREEN if bold else MUTED,
            bold, bg=WHITE
        ).pack(side="left")

        self.make_label(
            line, value, 10, DARK_GREEN,
            bold, bg=WHITE
        ).pack(side="right")

    def show_checkout(self):
        if not self.cart:
            messagebox.showwarning(
                "Empty cart", "Please add an item before checkout."
            )
            return

        self.current_page = "checkout"
        self.clear_content()
        page = self.content
        self._page_padding(page)

        self.make_button(
            page, "← Back to cart", self.show_cart
        ).pack(anchor="w", pady=(0, 12))

        self.make_label(
            page, "Checkout", 23, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            page,
            "Enter your details to test the demonstration checkout.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 16))

        form = self.make_card(page, padding=20)
        form.pack(fill="x")

        self.make_label(
            form, "Delivery details", 14, DARK_GREEN,
            True, bg=WHITE
        ).pack(anchor="w", pady=(0, 12))

        self.name_entry = self._form_field(form, "Full name")
        self.address_entry = self._form_field(form, "Delivery address")
        self.phone_entry = self._form_field(form, "Phone number")

        self.make_label(
            form, f"Items subtotal: {self.money(self.cart_subtotal())}",
            12, FOREST_GREEN, True, bg=WHITE
        ).pack(anchor="w", pady=(16, 8))

        self.make_label(
            form,
            "Demo only: this form does not send your details or process a payment.",
            9, MUTED, bg=WHITE, wraplength=650, justify="left"
        ).pack(anchor="w", pady=(0, 14))

        self.make_button(
            form, "Place demo order",
            self.place_demo_order, primary=True
        ).pack(anchor="e")

    def _form_field(self, parent, label_text):
        wrapper = tk.Frame(parent, bg=WHITE)
        wrapper.pack(fill="x", pady=6)

        self.make_label(
            wrapper, label_text, 10, DARK_GREEN,
            True, bg=WHITE
        ).pack(anchor="w", pady=(0, 5))

        entry = tk.Entry(
            wrapper, font=(FONT, 11),
            bg=WHITE, fg=TEXT,
            relief="solid", bd=1,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=FOREST_GREEN
        )
        entry.pack(fill="x", ipady=8)
        return entry

    def place_demo_order(self):
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not name or not address or not phone:
            messagebox.showwarning(
                "Missing information",
                "Please complete your name, delivery address and phone number."
            )
            return

        # Deliberately do not store personal details persistently.
        total = self.cart_subtotal()
        self.cart.clear()
        self.update_cart_count()

        self.clear_content()
        page = self.content
        self._page_padding(page)

        success = self.make_card(page, padding=26)
        success.pack(fill="x", pady=20)

        self.make_label(
            success, "✓", 36, FOREST_GREEN, True, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            success, "Demo order placed!", 21, DARK_GREEN,
            True, bg=WHITE
        ).pack(anchor="w", pady=(8, 5))

        self.make_label(
            success,
            f"Thank you, {name}. Your sample order total was {self.money(total)}.",
            10, MUTED, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            success,
            "This confirms the interface flow only. No restaurant, courier or payment provider was contacted.",
            9, MUTED, bg=WHITE, wraplength=650, justify="left"
        ).pack(anchor="w", pady=(8, 14))

        self.make_button(
            success, "View order tracking demo",
            self.show_tracking, primary=True
        ).pack(anchor="w")

        self.make_button(
            page, "Return to homepage",
            self.show_home
        ).pack(anchor="w")

    # ----------------------- ORDER TRACKING -----------------------

    def show_tracking(self):
        self.current_page = "tracking"
        self.set_active_nav("Track Order")
        self.clear_content()
        page = self.content
        self._page_padding(page)

        self.make_label(
            page, "Order tracking", 23, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            page,
            "A demonstration of how delivery progress could be displayed.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 16))

        status = self.make_card(page, padding=20)
        status.pack(fill="x", pady=(0, 14))

        self.make_label(
            status, "ORDER #MD-2048", 9, MUTED,
            True, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            status, "Your order is on its way", 18,
            DARK_GREEN, True, bg=WHITE
        ).pack(anchor="w", pady=(6, 4))

        self.make_label(
            status, "Estimated arrival: 20–30 minutes (sample estimate)",
            10, FOREST_GREEN, True, bg=WHITE
        ).pack(anchor="w")

        stages = [
            ("✓", "Order confirmed", "Your order has been received (demo)."),
            ("✓", "Being prepared", "The restaurant is preparing your order (demo)."),
            ("●", "On the way", "The courier stage is shown for demonstration."),
            ("○", "Delivered", "This stage has not been completed in the demo."),
        ]

        for icon, title, description in stages:
            stage = tk.Frame(status, bg=WHITE)
            stage.pack(fill="x", pady=9)

            self.make_label(
                stage, icon, 16,
                FOREST_GREEN if icon in ("✓", "●") else MUTED,
                True, bg=WHITE, width=3
            ).pack(side="left", anchor="n")

            detail = tk.Frame(stage, bg=WHITE)
            detail.pack(side="left", fill="x", expand=True)

            self.make_label(
                detail, title, 11, DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                detail, description, 9, MUTED, bg=WHITE
            ).pack(anchor="w", pady=(3, 0))

        driver = self.make_card(page, padding=16)
        driver.pack(fill="x", pady=(0, 14))

        self.make_label(
            driver, "Courier support (demo)", 13,
            DARK_GREEN, True, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            driver,
            "A real version could display the driver's profile, live location, rating and secure call/chat options.",
            9, MUTED, bg=WHITE, wraplength=650, justify="left"
        ).pack(anchor="w", pady=(5, 10))

        actions = tk.Frame(driver, bg=WHITE)
        actions.pack(anchor="w")

        self.make_button(
            actions, "Call courier (demo)",
            lambda: messagebox.showinfo(
                "Demo feature",
                "Calling is not connected in this prototype."
            )
        ).pack(side="left", padx=(0, 8))

        self.make_button(
            actions, "Chat (demo)",
            lambda: messagebox.showinfo(
                "Demo feature",
                "Live chat is not connected in this prototype."
            )
        ).pack(side="left")

        self.make_label(
            page,
            "Important: this page does not use live GPS or real courier data.",
            9, MUTED
        ).pack(anchor="w", pady=(0, 12))

        self.make_button(
            page, "Return to homepage",
            self.show_home, primary=True
        ).pack(anchor="w")

    # ----------------------- OTHER SERVICES -----------------------

    def show_service(self, service_name):
        self.current_page = "service"
        self.set_active_nav(service_name)
        self.clear_content()
        page = self.content
        self._page_padding(page)

        service = next(
            (item for item in self.services if item[1] == service_name),
            None
        )

        icon = service[0] if service else "⌂"

        self.make_button(
            page, "← Back to homepage", self.show_home
        ).pack(anchor="w", pady=(0, 12))

        self.make_label(
            page, f"{icon}  {service_name}", 23,
            DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            page,
            f"Browse the {service_name.lower()} section of the Mudon community app.",
            10, MUTED
        ).pack(anchor="w", pady=(5, 16))

        card = self.make_card(page, padding=22)
        card.pack(fill="x")

        self.make_label(
            card, "One place for your everyday needs", 15,
            DARK_GREEN, True, bg=WHITE
        ).pack(anchor="w")

        self.make_label(
            card,
            "This service page is a navigation prototype. Connecting real service providers, live availability, booking, payments and account data would require additional development.",
            10, MUTED, bg=WHITE, wraplength=650,
            justify="left"
        ).pack(anchor="w", pady=(8, 14))

        if service_name == "Food Delivery":
            self.make_button(
                card, "Browse restaurants",
                self.show_food, primary=True
            ).pack(anchor="w")
        else:
            self.make_button(
                card, "Return to all services",
                self.show_home, primary=True
            ).pack(anchor="w")

    # ----------------------- HELP AND NOTIFICATIONS -----------------------

    def show_help(self):
        window = tk.Toplevel(self)
        window.title("Mudon Help Centre")
        window.configure(bg=CREAM)
        window.geometry("540x500")
        window.minsize(420, 400)
        window.transient(self)

        outer = tk.Frame(window, bg=CREAM, padx=22, pady=20)
        outer.pack(fill="both", expand=True)

        self.make_label(
            outer, "Help Centre", 22, DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            outer,
            "Quick answers for common questions.",
            10, MUTED
        ).pack(anchor="w", pady=(4, 16))

        faqs = [
            (
                "How do I find a service?",
                "Use the homepage search bar or select a service card."
            ),
            (
                "How do I add food to my cart?",
                "Open Food Delivery, choose a restaurant, then select + Add."
            ),
            (
                "How do I change item quantities?",
                "Open your cart and use the plus or minus buttons."
            ),
            (
                "Is tracking live?",
                "No. Tracking in this school prototype is simulated; real GPS requires an external tracking service."
            ),
            (
                "Can I pay online?",
                "No real payment is processed. Secure payment integration would be needed in a deployed app."
            ),
            (
                "How do I contact support?",
                "This Help Centre is a prototype. A live version would need a connected support service."
            ),
        ]

        for question, answer in faqs:
            item = self.make_card(outer, padding=11)
            item.pack(fill="x", pady=4)

            self.make_label(
                item, question, 10, DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                item, answer, 9, MUTED, bg=WHITE,
                wraplength=450, justify="left"
            ).pack(anchor="w", pady=(5, 0))

        self.make_button(
            outer, "Close", window.destroy, primary=True
        ).pack(anchor="e", pady=(12, 0))

    def show_notifications(self):
        window = tk.Toplevel(self)
        window.title("Alerts | Mudon")
        window.configure(bg=CREAM)
        window.geometry("440x320")
        window.transient(self)

        outer = tk.Frame(window, bg=CREAM, padx=22, pady=20)
        outer.pack(fill="both", expand=True)

        self.make_label(
            outer, "Alerts and updates", 20,
            DARK_GREEN, True
        ).pack(anchor="w")

        self.make_label(
            outer,
            "Example notifications for the interface design.",
            10, MUTED
        ).pack(anchor="w", pady=(4, 14))

        notices = [
            ("🌿 Community offer", "Sample promotions may be displayed here."),
            ("🛍 Cart reminder", "Your cart count updates as you add or remove items."),
            ("↗ Delivery update", "A live version could notify users of order progress."),
        ]

        for title, description in notices:
            card = self.make_card(outer, padding=12)
            card.pack(fill="x", pady=4)

            self.make_label(
                card, title, 10, DARK_GREEN, True, bg=WHITE
            ).pack(anchor="w")

            self.make_label(
                card, description, 9, MUTED, bg=WHITE,
                wraplength=350, justify="left"
            ).pack(anchor="w", pady=(4, 0))

        self.make_label(
            outer,
            "These are local examples, not real push notifications.",
            8, MUTED
        ).pack(anchor="w", pady=(10, 0))

    # ----------------------- START APPLICATION -----------------------

if __name__ == "__main__":
    app = MudonApp()
    app.mainloop()
