import requests
from datetime import datetime, timedelta

# Constant for API
API_URL = "https://openexchangerates.org/api/"
API_KEY = "226ca57a998345e5ba16cdbb96293a07"

# Function to fetch live exchange rates
def get_exchange_rates():
    url = f"{API_URL}latest.json?app_id={API_KEY}"
    response=requests.get(url)
    return response.json()['rates']

# Function to convert currency based on exchange rates 
def convert_currency(amount,from_currency,to_currency):
    rates=get_exchange_rates()
    if from_currency!='USD':
        amount_in_usd = amount/rates[from_currency]
        exchange_rate=1/rates[from_currency]
    else:
        amount_in_usd=amount
        exchange_rate=rates[to_currency]
    converted_amount=amount_in_usd * rates[to_currency]
    return converted_amount, exchange_rate

# Function to fetch historical exchange rates for the past 5 days
def get_historical_rates(from_currency, to_currency):
    historical_rates = {}
    for past_days in range(1, 6):
        date=(datetime.now() - timedelta(days=past_days)).strftime('%Y-%m-%d')
        url=f"{API_URL}historical/{date}.json?app_id={API_KEY}"
        response=requests.get(url)
        rates=response.json().get('rates', {})
        if from_currency=='USD':
            historical_rates[date]=rates[to_currency]
        else:
            rate_to_usd=rates.get(from_currency, None)
            rates_to_target=rates.get(to_currency, None)
            if rate_to_usd and rates_to_target:
                historical_rates[date]=rates_to_target/rate_to_usd
    return historical_rates
    
# Main program to handle user input and display results
def main():
    amount = float(input("Enter the amount : "))
    from_currency = input("Enter the currency to covert from : ")
    to_currency = input("Enter the currency to covert to : ")
    
    # Convert currency
    converted_amount, exchange_rate = convert_currency(amount, from_currency, to_currency)
    
    # Print the conversion result
    print(f"{amount} {from_currency} = {converted_amount} {to_currency}")
    print(f"Exchange Rate = 1 {from_currency} = {exchange_rate} {to_currency}")

    # Fetch and display historical echange rates
    print("Historical Exchange Rates (Last 5 Days)")
    historical_rates=get_historical_rates(from_currency, to_currency)
    for date, rate in historical_rates.items():
        print(f"{date} : 1 {from_currency} = {rate} {to_currency}")

if __name__=="__main__":
    main()