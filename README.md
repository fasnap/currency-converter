# Currency Conversion 


This project is a simple currency conversion built using Python. It leverages the Open Exchange Rates API to fetch real-time and historical exchange rates, allowing users to convert amounts between different currencies. The application also stores conversion history in a SQLite database for future reference.

## Features
- **Real-time Currency Conversion:** Convert amounts between various currencies using the latest exchange rates.
- **Historical Exchange Rates:** Fetch historical exchange rates for the last 5 days.
- **Caching:** Store exchange rates locally to reduce API calls and enhance performance.
- **Conversion History:** Record and display a history of all currency conversions performed by the user.
- **User-Friendly Interface:** Simple command-line interface for user input.

## Requirements
- Python 3.x
- SQLite3
- Requests library (for making API calls)
- JSON (for caching exchange rates)

## Installation
1. **Clone the Repository:**

    ```bash
    git clone https://github.com/fasnap/currency-converter.git
    ```

2. **Install Required Libraries:**
   Ensure you have the required libraries installed. You can install the necessary libraries using pip:
   ```bash
   pip install requests
   ```

## Set Up API Key
1. Sign up at https://openexchangerates.org/ to obtain your API key.
2. Once you have your API key, open the code file and locate the following line:
   ```python
   API_KEY = "226ca57a998345e5ba16cdbb96293a07"


## Usage
1. **Run the Application:**

    ```bash
    python currency_converter.py
    ```
2. **Input Parameters:**
- When prompted, enter the amount you wish to convert.
- Specify the currency you are converting from (e.g., USD, EUR).
- Requests library (for making API calls)
- Specify the currency you are converting to (e.g., JPY, GBP).
3. **View Conversion History:**
After a successful conversion, you will have the option to view your conversion history. Simply type "yes" when prompted.

## References
- Open Exchange Rates API documentation: [Open Exchange Rates](https://openexchangerates.org/)