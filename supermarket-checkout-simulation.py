from __future__ import annotations
from time import sleep
from difflib import get_close_matches
from typing import List, Tuple, Dict

CURRENCY = "€"
SLEEP_SHORT = 0.3
SLEEP_MED = 0.5

# Initial stock (product -> {price, quantity})
stock: Dict[str, Dict[str, float | int]] = {
    "rice": {"price": 5.50, "quantity": 10},
    "beans": {"price": 7.20, "quantity": 8},
    "pasta": {"price": 3.80, "quantity": 15},
    "oil": {"price": 6.00, "quantity": 5},
}

# Shopping cart: list of tuples (product, quantity, unit_price)
cart: List[Tuple[str, int, float]] = []


def fmt_money(value: float) -> str:
    """Format a float value as currency with two decimals."""
    return f"{CURRENCY} {value:.2f}"


def safe_input(prompt: str) -> str:
    """
    Wrapper for input() to handle user interruptions (Ctrl+C / Ctrl+D).
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        raise


def read_positive_int(prompt: str, minimum: int = 1, maximum: int | None = None) -> int:
    """
    Reads a positive integer from the user, ensuring it is >= minimum and <= maximum (if provided).
    Retries until a valid input is given.
    """
    while True:
        try:
            value_str = safe_input(prompt).strip()
            value = int(value_str)
            if value < minimum:
                print(f"Attention: please enter an integer >= {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Attention: the maximum allowed is {maximum}.")
                continue
            return value
        except ValueError:
            print("Invalid input: please enter an integer.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise


def show_stock() -> None:
    """Displays the available stock (product, price, and quantity)."""
    print("\n=== AVAILABLE STOCK ===")
    if not stock:
        print("No products available.")
        return

    for product in sorted(stock.keys()):
        data = stock[product]
        print(f"{product.capitalize()} - Price: {fmt_money(float(data['price']))} | "
              f"Quantity: {int(data['quantity'])}")


def choose_product_name() -> str | None:
    """
    Ask for a product name; if not found, show up to 3 suggestions and let the user pick one.
    Returns the chosen product key (lowercase) or None if the user cancels/opts out.
    """
    while True:
        try:
            product = safe_input("Enter the product name (or 0 to cancel): ").strip().lower()
            if product in ("0", ""):
                return None

            if product in stock:
                return product

            matches = get_close_matches(product, stock.keys(), n=3, cutoff=0.6)
            if matches:
                print("\nProduct not found. Did you mean:")
                for i, m in enumerate(matches, 1):
                    print(f"{i}) {m.capitalize()}")
                print("0) None of these (type again)")
                choice = read_positive_int("Choose an option: ", minimum=0, maximum=len(matches))
                if choice == 0:
                    continue
                return matches[choice - 1]
            else:
                print("Product not found and no suggestions. Use 'Show stock' to see available products.")
        except KeyboardInterrupt:
            print("\nAction cancelled by user.")
            return None


def add_product() -> None:
    """
    Adds a product to the shopping cart with interactive disambiguation:
    - Lets the user choose among close matches if the product isn't found
    - Ensures quantity is positive and available
    - Updates cart and stock
    """
    try:
        product = choose_product_name()
        if not product:
            print("No product selected.")
            return

        available = int(stock[product]["quantity"])
        if available <= 0:
            print(f"No stock available for '{product}'.")
            return

        quantity = read_positive_int(
            f"Enter the desired quantity (available: {available}): ",
            minimum=1
        )

        if quantity > available:
            print(f"Not enough stock. Only {available} left.")
            return

        unit_price = float(stock[product]["price"])
        cart.append((product, quantity, unit_price))
        stock[product]["quantity"] = available - quantity

        print(f"{quantity}x {product} added to cart!")
    except KeyboardInterrupt:
        print("\nAction cancelled by user.")


def show_total() -> None:
    """Calculates and displays the total value of the cart."""
    print("\n=== SHOPPING CART ===")
    if not cart:
        print("Your cart is empty.")
        return

    total = 0.0
    for product, qty, price in cart:
        subtotal = qty * price
        total += subtotal
        print(f"{product.capitalize()} x{qty} - {fmt_money(subtotal)}")

    print(f"\nTotal purchase value: {fmt_money(total)}")


def menu() -> None:
    """Main interactive menu loop."""
    while True:
        print("\n=== MENU ===")
        print("1) Show stock")
        print("2) Add product to cart")
        print("3) Checkout (show total)")
        print("4) Show final stock")
        print("0) Exit")

        try:
            option = safe_input("Choose an option: ").strip()
            sleep(SLEEP_SHORT)

            if option == "1":
                show_stock()
            elif option == "2":
                add_product()
            elif option == "3":
                show_total()
            elif option == "4":
                show_stock()
            elif option == "0":
                sleep(SLEEP_MED)
                print("Exiting system...")
                break
            else:
                print("Invalid option! Try again.")

        except KeyboardInterrupt:
            print("\nInterruption detected. To exit, choose option 0.")
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")
            print("The system will continue running.")


def main() -> None:
    """Program entry point."""
    try:
        menu()
    except Exception as e:
        print(f"Critical unhandled error: {type(e).__name__}: {e}")
        print("Exiting the program safely.")


if __name__ == "__main__":
    main()
