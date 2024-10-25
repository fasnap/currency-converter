import sqlite3
import requests
from datetime import datetime, timedelta
import os
import json

# Constant
API_URL = "https://openexchangerates.org/api/"
API_KEY = "226ca57a998345e5ba16cdbb96293a07"
CACHE_EXPIRY = timedelta(hours=1)
CACHE_FILE = "exchange_rate_cache.json"

# Create or connect to a SQLite database
conn = sqlite3.connect("currency_conversions.db")
cursor = conn.cursor()

# Create a table for storing conversion history if it doesn't exist
cursor.execute(
    """CREATE TABLE IF NOT EXISTS conversions(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            amount DECIMAL, 
            from_currency varchar, 
            to_currency varchar,
            converted_amount DECIMAL, 
            exchange_rate DECIMAL, 
            date DATE)"""
)
conn.commit()


def load_cache():
    """Load cached exchange rates from a JSON file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            cached_data = json.load(file)
            # Convert back the last_fetch time string to datetime
            cached_data["last_fetch"] = (
                datetime.fromisoformat(cached_data["last_fetch"])
                if cached_data["last_fetch"]
                else None
            )
            return cached_data
    return {"rates": None, "last_fetch": None}


def save_cache(cached_rates):
    """Save exchange rates and last fetch time to a JSON file."""
    if cached_rates["last_fetch"] is not None:
        cached_rates["last_fetch"] = cached_rates["last_fetch"].isoformat()
    with open(CACHE_FILE, "w") as file:
        json.dump(cached_rates, file)


def get_exchange_rates():
    """Fetch and return exchange rates, using cached data if available."""
    cached_rates = load_cache()
    current_time = datetime.now()

    # Check if cached rates are valid
    if cached_rates["rates"] is not None and cached_rates["last_fetch"] is not None:
        if (current_time - cached_rates["last_fetch"]) < CACHE_EXPIRY:
            return cached_rates["rates"]

    # Fetch fresh data from API
    try:
        url = f"{API_URL}latest.json?app_id={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()

        if "rates" in response_data:
            cached_rates["rates"] = response_data["rates"]
            cached_rates["last_fetch"] = current_time
            save_cache(cached_rates)
            print("New data cached")
        else:
            print("Error: Rates not found in response.")
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching exchange rates")
        return None

    return cached_rates["rates"]


def convert_currency(amount, from_currency, to_currency):
    """Convert currency using exchange rates."""
    rates = get_exchange_rates()
    if rates is None:
        print("Error: Unable to fetch exchange rates. Conversion cannot be completed.")
        return None, None

    # Handle currency conversion
    try:
        amount_in_usd = (
            amount / rates[from_currency] if from_currency != "USD" else amount
        )
        exchange_rate = (
            rates[to_currency] / rates[from_currency]
            if from_currency != "USD"
            else rates[to_currency]
        )
        converted_amount = amount_in_usd * rates[to_currency]
        return converted_amount, exchange_rate
    except KeyError as e:
        print("Error : Currency not found in rates")
        return None, None


def get_historical_rates(from_currency, to_currency):
    """Fetch historical exchange rates for the last 5 days."""
    historical_rates = {}
    for past_days in range(1, 6):
        date = (datetime.now() - timedelta(days=past_days)).strftime("%Y-%m-%d")
        url = f"{API_URL}historical/{date}.json?app_id={API_KEY}"
        response = requests.get(url)
        rates = response.json().get("rates", {})

        if from_currency == "USD":
            historical_rates[date] = rates[to_currency]
        else:
            rate_to_usd = rates.get(from_currency, None)
            rates_to_target = rates.get(to_currency, None)
            if rate_to_usd and rates_to_target:
                historical_rates[date] = rates_to_target / rate_to_usd
    return historical_rates


def save_conversion_to_db(
    amount, from_currency, to_currency, converted_amount, exchange_rate
):
    """Save conversion details to the database."""
    cursor.execute(
        """INSERT INTO conversions (amount,from_currency,to_currency, 
        converted_amount,exchange_rate,date)
        VALUES(?, ?, ?, ?, ?, ?)""",
        (
            amount,
            from_currency,
            to_currency,
            converted_amount,
            exchange_rate,
            datetime.now().date(),
        ),
    )
    conn.commit()


def show_conversion_history():
    """Display conversion history from the database."""
    cursor.execute("SELECT * FROM conversions")
    rows = cursor.fetchall()
    if not rows:
        print("No conversion history found.")
        return
    for row in rows:
        print(row)


def main():
    """Main function to handle currency conversion."""
    amount = float(input("Enter the amount : "))
    from_currency = input("Enter the currency to covert from : ").upper()
    to_currency = input("Enter the currency to covert to : ").upper()

    # Convert currency
    converted_amount, exchange_rate = convert_currency(
        amount, from_currency, to_currency
    )

    # Save to database
    if converted_amount is not None:
        save_conversion_to_db(
            amount, from_currency, to_currency, converted_amount, exchange_rate
        )

        # Print the conversion result
        print(f"{amount} {from_currency} = {converted_amount} {to_currency}")
        print(f"Exchange Rate = 1 {from_currency} = {exchange_rate} {to_currency}")

        # Fetch and display historical echange rates for the last 5 days
        print("Historical Exchange Rates (Last 5 Days)")
        historical_rates = get_historical_rates(from_currency, to_currency)
        for date, rate in historical_rates.items():
            print(f"{date} : 1 {from_currency} = {rate} {to_currency}")

    # Option to display full history of user conversions
    show_history = input(
        "Would you like to see your conversion history? (yes/no):"
    ).lower()
    if show_history == "yes":
        show_conversion_history()


if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
