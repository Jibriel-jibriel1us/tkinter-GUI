import tkinter as tk
from tkinter import messagebox
import random


# ============================================================
# MUDON DELIVERY APP
# Final Day 7 Redesign
# ============================================================

# -------------------- COLOURS --------------------

GREEN = "#1F7A45"
DARK_GREEN = "#14532D"
LIGHT_GREEN = "#EAF6ED"
PALE_GREEN = "#F6FAF7"

WHITE = "#FFFFFF"
BLACK = "#17201A"
GREY = "#6B7280"
LIGHT_GREY = "#E5E7EB"

ORANGE = "#F59E0B"
PALE_ORANGE = "#FFF4D6"

RED = "#DC2626"
PALE_RED = "#FEECEC"

# -------------------- MAIN WINDOW --------------------

root = tk.Tk()
root.title("Mudon Delivery")
root.geometry("1440x900")
root.resizable(True, True)
root.configure(bg=PALE_GREEN)

# -------------------- APP DATA --------------------

cart = []
order_placed = False
order_number = None
order_total = 0


# ============================================================
# PRODUCT DATA
# name, original price, icon, discount percentage
# ============================================================

service_items = {

    "Food Delivery": [
        ("Pizza", 35, "🍕", 20),
        ("Burger", 28, "🍔", 15),
        ("Chicken Wrap", 24, "🌯", 10),
        ("Pasta", 32, "🍝", 0),
    ],

    "Groceries": [
        ("Milk", 8, "🥛", 0),
        ("Bread", 6, "🍞", 10),
        ("Eggs", 12, "🥚", 0),
        ("Fruit Box", 25, "🍎", 20),
    ],

    "Laundry": [
        ("Shirt Cleaning", 10, "👕", 0),
        ("Trousers Cleaning", 15, "👖", 10),
        ("Suit Cleaning", 35, "🧥", 15),
        ("Bed Sheet Cleaning", 25, "🛏️", 0),
    ],

    "Healthcare": [
        ("First Aid Kit", 30, "🩹", 10),
        ("Vitamin C", 20, "🍊", 0),
        ("Thermometer", 25, "🌡️", 15),
        ("Personal Care", 18, "🧴", 0),
    ],

    "Cleaning": [
        ("Standard Cleaning", 60, "🧹", 10),
        ("Deep Cleaning", 120, "✨", 15),
        ("Kitchen Cleaning", 80, "🍽️", 0),
        ("Bathroom Cleaning", 70, "🚿", 10),
    ],

    "More Services": [
        ("Local Service", 0, "⋯", 0),
    ]
}


service_icons = {
    "Food Delivery": "🍔",
    "Groceries": "🛒",
    "Laundry": "🧺",
    "Healthcare": "🌿",
    "Cleaning": "🧹",
    "More Services": "•••"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def sale_price(price, discount):
    return round(price * (1 - discount / 100), 2)


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def make_button(parent, text, command, primary=True, width=None):
    if primary:
        bg = GREEN
        fg = WHITE
        active_bg = DARK_GREEN
    else:
        bg = WHITE
        fg = GREEN
        active_bg = LIGHT_GREEN

    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11, "bold"),
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=15,
        pady=9
    )

    if width:
        button.config(width=width)

    return button


def header(title, back_command=None):
    """
    Creates the top navigation bar.
    """

    top = tk.Frame(root, bg=WHITE, height=70)
    top.pack(fill="x")
    top.pack_propagate(False)

    if back_command:
        back_button = tk.Button(
            top,
            text="←",
            command=back_command,
            font=("Arial", 20, "bold"),
            bg=WHITE,
            fg=GREEN,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        back_button.pack(side="left", padx=20)

    brand = tk.Label(
        top,
        text="▣ MUDON",
        font=("Arial", 20, "bold"),
        bg=WHITE,
        fg=GREEN
    )
    brand.pack(side="left", padx=10)

    title_label = tk.Label(
        top,
        text=title,
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=BLACK
    )
    title_label.pack(side="left", padx=25)

    cart_button = tk.Button(
        top,
        text=f"🛒  Cart ({len(cart)})",
        command=open_cart,
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=GREEN,
        relief="flat",
        cursor="hand2"
    )
    cart_button.pack(side="right", padx=20)


def add_to_cart(name, price, discount):
    discounted = sale_price(price, discount)

    cart.append({
        "name": name,
        "original_price": price,
        "price": discounted,
        "discount": discount
    })

    messagebox.showinfo(
        "Added to Cart",
        f"{name} has been added to your cart."
    )


def calculate_total():
    return round(sum(item["price"] for item in cart), 2)


# ============================================================
# HOME PAGE
# ============================================================

def open_home():
    clear_screen()

    # ---------------- TOP NAVIGATION ----------------

    top = tk.Frame(root, bg=WHITE, height=70)
    top.pack(fill="x")
    top.pack_propagate(False)

    logo = tk.Label(
        top,
        text="▣ MUDON",
        font=("Arial", 22, "bold"),
        bg=WHITE,
        fg=GREEN
    )
    logo.pack(side="left", padx=30)

    help_button = tk.Button(
        top,
        text="?",
        command=open_faq,
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=GREEN,
        relief="flat",
        cursor="hand2"
    )
    help_button.pack(side="right", padx=10)

    cart_button = tk.Button(
        top,
        text=f"🛒 {len(cart)}",
        command=open_cart,
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=GREEN,
        relief="flat",
        cursor="hand2"
    )
    cart_button.pack(side="right", padx=10)

    # ---------------- MAIN CONTENT ----------------

    content = tk.Frame(root, bg=PALE_GREEN)
    content.pack(fill="both", expand=True)

    # Welcome section

    welcome = tk.Frame(content, bg=PALE_GREEN)
    welcome.pack(fill="x", padx=45, pady=(25, 10))

    tk.Label(
        welcome,
        text="Hi there! 👋",
        font=("Arial", 13),
        bg=PALE_GREEN,
        fg=GREY
    ).pack(anchor="w")

    tk.Label(
        welcome,
        text="What would you like\nto do today?",
        font=("Arial", 27, "bold"),
        bg=PALE_GREEN,
        fg=BLACK,
        justify="left"
    ).pack(anchor="w", pady=(3, 12))

    # ---------------- SEARCH ----------------

    search_frame = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    search_frame.pack(fill="x", padx=45, pady=5)

    tk.Label(
        search_frame,
        text="🔍",
        font=("Arial", 15),
        bg=WHITE
    ).pack(side="left", padx=(15, 5))

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 12),
        bd=0,
        bg=WHITE,
        fg=BLACK
    )
    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        pady=14
    )

    def search_home():
        search_text = search_entry.get().lower().strip()

        if not search_text:
            return

        for service in service_items:

            if search_text in service.lower():
                open_service(service)
                return

            for item in service_items[service]:
                if search_text in item[0].lower():
                    open_service(service)
                    return

        messagebox.showinfo(
            "Search",
            "No matching service or product was found."
        )

    search_entry.bind("<Return>", lambda event: search_home())

    search_button = tk.Button(
        search_frame,
        text="Search",
        command=search_home,
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE,
        relief="flat",
        cursor="hand2",
        padx=15,
        pady=7
    )
    search_button.pack(side="right", padx=6, pady=6)

    # ---------------- PROMOTION ----------------

    promotion = tk.Frame(
        content,
        bg=GREEN,
        height=125
    )
    promotion.pack(fill="x", padx=45, pady=18)
    promotion.pack_propagate(False)

    promo_left = tk.Frame(promotion, bg=GREEN)
    promo_left.pack(side="left", padx=25, pady=18)

    tk.Label(
        promo_left,
        text="20% OFF",
        font=("Arial", 26, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        promo_left,
        text="On selected orders",
        font=("Arial", 11),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w")

    tk.Label(
        promo_left,
        text="Use code: MUDON20",
        font=("Arial", 10, "bold"),
        bg=GREEN,
        fg=WHITE
    ).pack(anchor="w", pady=(3, 0))

    make_button(
        promotion,
        "Order Now →",
        lambda: open_service("Food Delivery"),
        primary=False
    ).pack(side="right", padx=30, pady=35)

    # ---------------- CATEGORIES ----------------

    category_title = tk.Frame(content, bg=PALE_GREEN)
    category_title.pack(fill="x", padx=45)

    tk.Label(
        category_title,
        text="Popular Categories",
        font=("Arial", 16, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack(side="left")

    tk.Label(
        category_title,
        text="See all",
        font=("Arial", 10, "bold"),
        bg=PALE_GREEN,
        fg=GREEN
    ).pack(side="right")

    categories = tk.Frame(content, bg=PALE_GREEN)
    categories.pack(fill="x", padx=40, pady=10)

    for service in service_items:

        card = tk.Frame(
            categories,
            bg=WHITE,
            width=145,
            height=100,
            highlightbackground=LIGHT_GREY,
            highlightthickness=1,
            cursor="hand2"
        )
        card.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )
        card.pack_propagate(False)

        tk.Label(
            card,
            text=service_icons[service],
            font=("Arial", 25),
            bg=WHITE
        ).pack(pady=(10, 3))

        tk.Label(
            card,
            text=service,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack()

        card.bind(
            "<Button-1>",
            lambda event, s=service: open_service(s)
        )

    # ---------------- LOWER SECTION ----------------

    lower = tk.Frame(content, bg=PALE_GREEN)
    lower.pack(fill="x", padx=45, pady=18)

    # Free delivery card

    free_card = tk.Frame(
        lower,
        bg=LIGHT_GREEN,
        height=100
    )
    free_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10)
    )
    free_card.pack_propagate(False)

    tk.Label(
        free_card,
        text="🚴  Free Delivery",
        font=("Arial", 15, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack(anchor="w", padx=20, pady=(18, 2))

    tk.Label(
        free_card,
        text="On orders over AED 20",
        font=("Arial", 10),
        bg=LIGHT_GREEN,
        fg=GREY
    ).pack(anchor="w", padx=20)

    # Tracking card

    tracking_card = tk.Frame(
        lower,
        bg=WHITE,
        height=100,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    tracking_card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(10, 0)
    )
    tracking_card.pack_propagate(False)

    tk.Label(
        tracking_card,
        text="📍 Track Your Order",
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(anchor="w", padx=20, pady=(18, 2))

    tk.Label(
        tracking_card,
        text="View your current delivery",
        font=("Arial", 10),
        bg=WHITE,
        fg=GREY
    ).pack(anchor="w", padx=20)

    make_button(
        tracking_card,
        "Track →",
        open_tracking,
        primary=False
    ).pack(side="right", padx=15, pady=25)

    # ---------------- BOTTOM NAVIGATION ----------------

    nav = tk.Frame(
        root,
        bg=WHITE,
        height=70,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    nav.pack(fill="x")
    nav.pack_propagate(False)

    nav_items = [
        ("⌂\nHome", open_home),
        ("🛒\nOrders", open_cart),
        ("📍\nTrack", open_tracking),
        ("?", open_faq)
    ]

    for text, command in nav_items:

        button = tk.Button(
            nav,
            text=text,
            command=command,
            font=("Arial", 9, "bold"),
            bg=WHITE,
            fg=GREEN,
            relief="flat",
            cursor="hand2"
        )

        button.pack(
            side="left",
            expand=True,
            fill="both"
        )


# ============================================================
# SERVICE PAGE
# ============================================================

def open_service(service_name):

    clear_screen()

    header(
        service_name,
        open_home
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(fill="both", expand=True)

    tk.Label(
        main,
        text=service_icons[service_name],
        font=("Arial", 40),
        bg=PALE_GREEN
    ).pack(pady=(25, 5))

    tk.Label(
        main,
        text=service_name,
        font=("Arial", 25, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack()

    tk.Label(
        main,
        text="Choose from the available options below",
        font=("Arial", 11),
        bg=PALE_GREEN,
        fg=GREY
    ).pack(pady=(3, 20))

    # Search products

    search_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    search_frame.pack(fill="x", padx=100)

    tk.Label(
        search_frame,
        text="🔍",
        bg=WHITE,
        font=("Arial", 14)
    ).pack(side="left", padx=10)

    search_entry = tk.Entry(
        search_frame,
        bd=0,
        font=("Arial", 11),
        bg=WHITE
    )
    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        pady=12
    )

    # Products container

    products_frame = tk.Frame(
        main,
        bg=PALE_GREEN
    )
    products_frame.pack(
        fill="both",
        expand=True,
        padx=70,
        pady=20
    )

    def display_products(items):

        for widget in products_frame.winfo_children():
            widget.destroy()

        if not items:
            tk.Label(
                products_frame,
                text="No products found.",
                font=("Arial", 14),
                bg=PALE_GREEN,
                fg=GREY
            ).pack(pady=40)
            return

        for name, price, icon, discount in items:

            card = tk.Frame(
                products_frame,
                bg=WHITE,
                highlightbackground=LIGHT_GREY,
                highlightthickness=1
            )
            card.pack(
                fill="x",
                pady=6
            )

            # Product icon

            tk.Label(
                card,
                text=icon,
                font=("Arial", 30),
                bg=WHITE
            ).pack(
                side="left",
                padx=20,
                pady=12
            )

            # Product information

            info = tk.Frame(
                card,
                bg=WHITE
            )
            info.pack(
                side="left",
                fill="x",
                expand=True,
                pady=10
            )

            tk.Label(
                info,
                text=name,
                font=("Arial", 13, "bold"),
                bg=WHITE,
                fg=BLACK
            ).pack(anchor="w")

            price_row = tk.Frame(
                info,
                bg=WHITE
            )
            price_row.pack(anchor="w", pady=(5, 0))

            if discount > 0:

                tk.Label(
                    price_row,
                    text=f"AED {price:.2f}",
                    font=("Arial", 10, "overstrike"),
                    bg=WHITE,
                    fg=GREY
                ).pack(side="left", padx=(0, 8))

                discounted = sale_price(
                    price,
                    discount
                )

                tk.Label(
                    price_row,
                    text=f"AED {discounted:.2f}",
                    font=("Arial", 13, "bold"),
                    bg=WHITE,
                    fg=GREEN
                ).pack(side="left", padx=(0, 8))

                tk.Label(
                    price_row,
                    text=f"{discount}% OFF",
                    font=("Arial", 9, "bold"),
                    bg=PALE_ORANGE,
                    fg=ORANGE,
                    padx=5
                ).pack(side="left")

            else:

                tk.Label(
                    price_row,
                    text=f"AED {price:.2f}",
                    font=("Arial", 13, "bold"),
                    bg=WHITE,
                    fg=GREEN
                ).pack(side="left")

            make_button(
                card,
                "ADD +",
                lambda n=name, p=price, d=discount:
                add_to_cart(n, p, d),
                primary=True
            ).pack(
                side="right",
                padx=20,
                pady=20
            )

    def search_products():

        text = search_entry.get().lower().strip()

        items = service_items[service_name]

        filtered = [
            item for item in items
            if text in item[0].lower()
        ]

        display_products(filtered)

    search_entry.bind(
        "<KeyRelease>",
        lambda event: search_products()
    )

    display_products(
        service_items[service_name]
    )


# ============================================================
# CART PAGE
# ============================================================

def open_cart():

    clear_screen()

    header(
        "Your Cart",
        open_home
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(
        fill="both",
        expand=True,
        padx=70,
        pady=30
    )

    tk.Label(
        main,
        text="Your Cart",
        font=("Arial", 27, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack(anchor="w")

    if not cart:

        empty = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=LIGHT_GREY,
            highlightthickness=1
        )
        empty.pack(
            fill="x",
            pady=30
        )

        tk.Label(
            empty,
            text="🛒",
            font=("Arial", 45),
            bg=WHITE
        ).pack(pady=(30, 10))

        tk.Label(
            empty,
            text="Your cart is empty",
            font=("Arial", 17, "bold"),
            bg=WHITE
        ).pack()

        tk.Label(
            empty,
            text="Add something from one of our services.",
            font=("Arial", 10),
            bg=WHITE,
            fg=GREY
        ).pack(pady=5)

        make_button(
            empty,
            "Continue Shopping",
            open_home
        ).pack(pady=25)

        return

    # Cart items

    items_frame = tk.Frame(
        main,
        bg=PALE_GREEN
    )
    items_frame.pack(
        fill="both",
        expand=True,
        pady=15
    )

    for item in cart:

        row = tk.Frame(
            items_frame,
            bg=WHITE,
            highlightbackground=LIGHT_GREY,
            highlightthickness=1
        )
        row.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            row,
            text=item["name"],
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        if item["discount"] > 0:

            tk.Label(
                row,
                text=f"AED {item['original_price']:.2f}",
                font=("Arial", 9, "overstrike"),
                bg=WHITE,
                fg=GREY
            ).pack(side="right", padx=5)

        tk.Label(
            row,
            text=f"AED {item['price']:.2f}",
            font=("Arial", 12, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            side="right",
            padx=20
        )

    # Total

    total = calculate_total()

    total_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    total_frame.pack(
        fill="x",
        pady=10
    )

    tk.Label(
        total_frame,
        text="Total",
        font=("Arial", 15, "bold"),
        bg=WHITE
    ).pack(
        side="left",
        padx=20,
        pady=18
    )

    tk.Label(
        total_frame,
        text=f"AED {total:.2f}",
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=GREEN
    ).pack(
        side="right",
        padx=20
    )

    make_button(
        main,
        "PROCEED TO CHECKOUT  →",
        lambda: open_checkout(),
        primary=True
    ).pack(
        fill="x",
        pady=10
    )


# ============================================================
# CHECKOUT PAGE
# ============================================================

def open_checkout():

    clear_screen()

    header(
        "Checkout",
        open_cart
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(
        fill="both",
        expand=True,
        padx=100,
        pady=30
    )

    tk.Label(
        main,
        text="Complete Your Order",
        font=("Arial", 27, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack(anchor="w")

    tk.Label(
        main,
        text="Enter your delivery details below.",
        font=("Arial", 11),
        bg=PALE_GREEN,
        fg=GREY
    ).pack(anchor="w", pady=(3, 20))

    form = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    form.pack(
        fill="x",
        pady=5
    )

    fields = {}

    field_names = [
        ("Full Name", "Enter your name"),
        ("Delivery Address", "Enter your address"),
        ("Phone Number", "Enter your phone number")
    ]

    for label_text, placeholder in field_names:

        tk.Label(
            form,
            text=label_text,
            font=("Arial", 10, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        entry = tk.Entry(
            form,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        entry.pack(
            fill="x",
            padx=25,
            ipady=7
        )

        fields[label_text] = entry

    # Order total

    total = calculate_total()

    tk.Label(
        form,
        text=f"Order Total: AED {total:.2f}",
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=GREEN
    ).pack(
        anchor="w",
        padx=25,
        pady=20
    )

    def place_order():

        global order_placed
        global order_number
        global order_total

        name = fields["Full Name"].get().strip()
        address = fields["Delivery Address"].get().strip()
        phone = fields["Phone Number"].get().strip()

        if not name or not address or not phone:

            messagebox.showwarning(
                "Missing Information",
                "Please complete all delivery details."
            )
            return

        order_placed = True
        order_number = random.randint(
            10000,
            99999
        )
        order_total = total

        cart.clear()

        open_confirmation(
            name,
            order_number,
            total
        )

    make_button(
        main,
        "PLACE ORDER  ✓",
        place_order,
        primary=True
    ).pack(
        fill="x",
        pady=20
    )


# ============================================================
# CONFIRMATION PAGE
# ============================================================

def open_confirmation(
    name,
    number,
    total
):

    clear_screen()

    header(
        "Order Confirmed",
        open_home
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        main,
        text="✓",
        font=("Arial", 65, "bold"),
        bg=LIGHT_GREEN,
        fg=GREEN
    ).pack(
        pady=(60, 10)
    )

    tk.Label(
        main,
        text="Order Confirmed!",
        font=("Arial", 30, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack()

    tk.Label(
        main,
        text=f"Thank you, {name}!",
        font=("Arial", 14),
        bg=PALE_GREEN,
        fg=GREY
    ).pack(pady=8)

    card = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    card.pack(
        padx=250,
        pady=20,
        fill="x"
    )

    tk.Label(
        card,
        text=f"Order #{number}",
        font=("Arial", 15, "bold"),
        bg=WHITE,
        fg=GREEN
    ).pack(pady=(20, 5))

    tk.Label(
        card,
        text=f"Total: AED {total:.2f}",
        font=("Arial", 12),
        bg=WHITE
    ).pack(pady=(0, 20))

    make_button(
        main,
        "TRACK MY ORDER  →",
        open_tracking,
        primary=True
    ).pack(
        padx=250,
        fill="x",
        pady=10
    )

    make_button(
        main,
        "BACK TO HOME",
        open_home,
        primary=False
    ).pack(
        padx=250,
        fill="x"
    )


# ============================================================
# TRACKING PAGE
# ============================================================

def open_tracking():

    clear_screen()

    header(
        "Track Order",
        open_home
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(
        fill="both",
        expand=True,
        padx=100,
        pady=30
    )

    tk.Label(
        main,
        text="Track Your Order",
        font=("Arial", 27, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack(anchor="w")

    if not order_placed:

        card = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=LIGHT_GREY,
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=30
        )

        tk.Label(
            card,
            text="📍",
            font=("Arial", 45),
            bg=WHITE
        ).pack(pady=(30, 10))

        tk.Label(
            card,
            text="No active order",
            font=("Arial", 18, "bold"),
            bg=WHITE
        ).pack()

        tk.Label(
            card,
            text="Place an order to start tracking your delivery.",
            font=("Arial", 10),
            bg=WHITE,
            fg=GREY
        ).pack(pady=(5, 20))

        make_button(
            card,
            "START SHOPPING",
            open_home
        ).pack(pady=(0, 30))

        return

    # Order number

    tk.Label(
        main,
        text=f"Order #{order_number}",
        font=("Arial", 12, "bold"),
        bg=PALE_GREEN,
        fg=GREEN
    ).pack(anchor="w", pady=(5, 20))

    # Status

    status = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    status.pack(
        fill="x",
        pady=5
    )

    tk.Label(
        status,
        text="🛵",
        font=("Arial", 35),
        bg=WHITE
    ).pack(
        side="left",
        padx=25,
        pady=20
    )

    status_info = tk.Frame(
        status,
        bg=WHITE
    )
    status_info.pack(
        side="left",
        pady=20
    )

    tk.Label(
        status_info,
        text="Order is being prepared",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=BLACK
    ).pack(anchor="w")

    tk.Label(
        status_info,
        text="Your delivery is on its way through Mudon.",
        font=("Arial", 10),
        bg=WHITE,
        fg=GREY
    ).pack(anchor="w", pady=3)

    # Progress

    progress = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=LIGHT_GREY,
        highlightthickness=1
    )
    progress.pack(
        fill="x",
        pady=15
    )

    steps = [
        ("✓", "Order placed"),
        ("✓", "Order confirmed"),
        ("●", "Being prepared"),
        ("○", "Out for delivery"),
        ("○", "Delivered")
    ]

    for icon, text in steps:

        row = tk.Frame(
            progress,
            bg=WHITE
        )
        row.pack(
            fill="x",
            padx=30,
            pady=7
        )

        tk.Label(
            row,
            text=icon,
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=GREEN if icon != "○" else GREY
        ).pack(side="left")

        tk.Label(
            row,
            text=text,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=BLACK if icon != "○" else GREY
        ).pack(
            side="left",
            padx=15
        )

    # Map placeholder

    map_frame = tk.Frame(
        main,
        bg=LIGHT_GREEN,
        height=150
    )
    map_frame.pack(
        fill="x",
        pady=5
    )
    map_frame.pack_propagate(False)

    tk.Label(
        map_frame,
        text="📍",
        font=("Arial", 35),
        bg=LIGHT_GREEN,
        fg=GREEN
    ).pack(pady=(20, 0))

    tk.Label(
        map_frame,
        text="Live delivery map",
        font=("Arial", 12, "bold"),
        bg=LIGHT_GREEN,
        fg=DARK_GREEN
    ).pack()

    tk.Label(
        map_frame,
        text="GPS tracking prototype",
        font=("Arial", 9),
        bg=LIGHT_GREEN,
        fg=GREY
    ).pack()


# ============================================================
# HELP / FAQ PAGE
# ============================================================

def open_faq():

    clear_screen()

    header(
        "Help & Support",
        open_home
    )

    main = tk.Frame(
        root,
        bg=PALE_GREEN
    )
    main.pack(
        fill="both",
        expand=True,
        padx=100,
        pady=30
    )

    tk.Label(
        main,
        text="Help & Support",
        font=("Arial", 27, "bold"),
        bg=PALE_GREEN,
        fg=BLACK
    ).pack(anchor="w")

    tk.Label(
        main,
        text="Find answers to common questions.",
        font=("Arial", 11),
        bg=PALE_GREEN,
        fg=GREY
    ).pack(anchor="w", pady=(3, 20))

    faqs = [
        (
            "How do I place an order?",
            "Choose a service, select a product, add it to your cart and proceed to checkout."
        ),
        (
            "How do I track my order?",
            "Open Track Order from the home page or from the order confirmation screen."
        ),
        (
            "Can I search for products?",
            "Yes. Use the search bar on the home page or inside each service."
        ),
        (
            "Are the discounts automatically calculated?",
            "Yes. The app automatically calculates the discounted price."
        ),
        (
            "Is the GPS map real?",
            "No. The current map is a prototype representation of the GPS tracking feature."
        )
    ]

    for question, answer in faqs:

        card = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=LIGHT_GREY,
            highlightthickness=1
        )
        card.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            card,
            text="?",
            font=("Arial", 13, "bold"),
            bg=GREEN,
            fg=WHITE,
            width=3
        ).pack(
            side="left",
            padx=15,
            pady=15
        )

        text_frame = tk.Frame(
            card,
            bg=WHITE
        )
        text_frame.pack(
            side="left",
            fill="x",
            expand=True,
            pady=12
        )

        tk.Label(
            text_frame,
            text=question,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=BLACK
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=answer,
            font=("Arial", 9),
            bg=WHITE,
            fg=GREY,
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=(3, 0))


# ============================================================
# START APP
# ============================================================

open_home()

root.mainloop()

