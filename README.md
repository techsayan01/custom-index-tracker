
# Custom Equal-Weighted Stock Index Tracker

Construct and track an equal-weighted custom index comprising top 100 US stocks based on their market cap - Altemetrik


To create a virtual environment, go to your project’s directory and run the following command. This will create a new virtual environment in a local folder named .venv:

```bash
python3 -m venv .venv
```

Activate a virtual environment

```bash
source .venv/bin/activate
```

To confirm the virtual environment is activated, check the location of your Python interpreter:

```bash
which python
```

To deactivate a virtual environment

```bash
deactivate
```

```
See more here: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
```
---

## Overview

This project involves constructing and tracking an equal-weighted custom index of the top 100 US stocks based on their market capitalization. The index is updated daily, with a focus on visualizing its performance and tracking changes in composition over time. Additionally, the project includes functionality to export the index performance and composition data to Excel and PDF formats and provides an interactive dashboard for visualization.

---

## Features

1. **Index Construction**:  
   - Identifies the top 100 US stocks by market capitalization daily.
   - Constructs an equal-weighted index.
   - Automatically rebalances the index when composition changes occur.

2. **Data Persistence**:  
   - Stores stock price and market cap data in a SQLite database.

3. **Visualization**:  
   - Line chart of the index's performance over the past month.
   - Bar chart showing daily composition changes.
   - Highlight days with significant changes in index composition.

4. **Data Export**:  
   - Export performance and composition data to Excel.
   - Export visualizations to PDF.

5. **Interactive Dashboard**:  
   - View index performance and composition changes dynamically.

---

## Project Architecture

The project follows the **SOLID principles** to ensure modularity, scalability, and maintainability.

### Key Components

1. **Data Fetcher (`data_fetcher.py`)**  
   Handles fetching stock data using the `yfinance` API and performing data preprocessing.

2. **Database Manager (`database_manager.py`)**  
   Manages data persistence using SQLite, including schema creation, data insertion, and querying.

3. **Index Calculator (`index_calculator.py`)**  
   Constructs the equal-weighted index, rebalances the composition daily, and calculates performance.

4. **Dashboard (`dashboard.py`)**  
   Creates visualizations for performance and composition changes using `matplotlib`.

5. **Data Exporter (`data_exporter.py`)**  
   Provides functionality to export data and charts to Excel and PDF formats.

---

## Dependencies

Install the following Python packages to run the project:

- **`pandas`**: Data manipulation and analysis.  
- **`yfinance`**: Fetching stock market data.  
- **`matplotlib`**: Data visualization.  
- **`openpyxl`**: Exporting data to Excel files.  
- **`reportlab`** and **`matplotlib.backends.backend_pdf`**: Exporting visualizations to PDF.  
- **`sqlite3`**: Lightweight SQL database for data persistence.  

Install all dependencies with the following command:

```bash
pip install pandas yfinance matplotlib openpyxl reportlab
```
or
```bash
pip install -r requirements.txt
```

---

## Data Source

We use the `yfinance` library to fetch stock market data. It provides:
- Stock prices (daily open, high, low, close).
- Market capitalization (calculated as `close price * shares outstanding`).

---

## File Structure

```plaintext
├── data_fetcher.py         # Fetches and preprocesses stock data
├── database_manager.py     # Handles database operations
├── index_calculator.py        # Constructs and rebalances the index
├── dashboard.py            # Visualization of index performance and composition changes
├── data_exporter.py        # Exports data to Excel and PDF
├── main.py                 # Main script to run the project
├── requirements.txt        # List of dependencies
└── README.md               # Project documentation
└── .env               		# Setting the environment variable
```

---

The database for this project has a simple, normalized structure. It consists of three key tables to manage stock data, market capitalization, and the index's performance. Here's the structure:

---

### **1. `stock_prices` Table**
Stores daily closing prices for all stocks.

| **Column Name** | **Data Type** | **Description**                                |
|------------------|---------------|------------------------------------------------|
| `Date`           | DATE          | The trading date.                             |
| `Ticker`         | TEXT          | The stock's ticker symbol (e.g., AAPL).       |
| `Close`          | FLOAT         | The closing price of the stock on that date.  |

**Primary Key**: `(Date, Ticker)`

---

### **2. `market_caps` Table**
Holds the market capitalization for stocks.

| **Column Name** | **Data Type** | **Description**                             |
|------------------|---------------|---------------------------------------------|
| `Ticker`         | TEXT          | The stock's ticker symbol.                 |
| `MarketCap`      | FLOAT         | The stock's market capitalization (USD).   |

**Primary Key**: `Ticker`

---

### **3. `index_performance` Table**
Tracks the daily performance of the custom index.

| **Column Name** | **Data Type** | **Description**                                    |
|------------------|---------------|---------------------------------------------------|
| `Date`           | DATE          | The trading date.                                 |
| `IndexValue`     | FLOAT         | The equal-weighted index value on that date.      |

**Primary Key**: `Date`

---

### **Relationships Between Tables**
1. **`market_caps` ↔ `stock_prices`**:  
   The `Ticker` column in both tables links market capitalization data with stock prices.

2. **Index Composition and Performance**:  
   The `index_performance` table is computed based on `stock_prices` and the top 100 stocks from `market_caps`.

---

### **Schema Diagram**
```
stock_prices
----------------
| Date         |
| Ticker       | ----+
| Close        |     |
----------------      |
                     |
market_caps          |
----------------      |
| Ticker       | <---+
| MarketCap    |
----------------

index_performance
----------------
| Date         |
| IndexValue   |
----------------
```

---

### **Key Points**
- The database uses SQLite for simplicity, but the structure is compatible with other SQL engines (e.g., PostgreSQL, MySQL).
- All tables are normalized to avoid redundancy and improve query efficiency.
- Data access and transformations rely on SQL queries for clarity and maintainability.

## Implementation Steps

### 1. Data Fetching and Preprocessing
- **File**: `data_fetcher.py`  
- Use `yfinance` to fetch daily stock price data (open, high, low, close) and shares outstanding.
- Calculate the market capitalization for each stock (`close price * shares outstanding`).

### 2. Data Storage
- **File**: `database_manager.py`  
- Use SQLite for data persistence.
- Define the database schema with two tables:
  - `stock_prices`: Stores stock prices and market cap data.
  - `index_performance`: Tracks daily index performance and composition.

### 3. Index Construction
- **File**: `index_calculator.py`  
- Identify the top 100 stocks by market cap for each day.
- Rebalance the index if the top 100 stocks change.
- Calculate the equal-weighted index value.

### 4. Visualization
- **File**: `dashboard.py`  
- Visualize:
  - Index performance over time (line chart).
  - Daily changes in index composition (bar chart).

### 5. Data Export
- **File**: `data_exporter.py`  
- Export:
  - Performance and composition data to Excel.
  - Charts and tables to PDF.

---

## How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-repository/custom-index-tracker.git
cd custom-index-tracker
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create the Database with sqlite3


```bash
sqlite3 stocks.db
```

### Step 3a: List the tables

```sql
.tables
```

### Step 3b: Check the schema

```sql
.schema stocks
```

### Step 3c i -- DANGER - To flush the database for creating new entry
```bash
    sqlite3 stocks.db
```
### Step 3c ii -- DANGER - To flush the tables
```sql
    DELETE FROM your_table_name;
    
```

### Step 3c iii -- DANGER - To flush the db
```sql
    .database;
```
Extract the location
```bash
rm -rf "<database path>"
```

### Step 3d: Exit the sqlite3

```sql
.exit
```

### Step 4: Run the Script

```bash
python main.py
```

### Step 4: Explore Outputs

- View the interactive dashboard with visualizations.
- Check exported Excel and PDF files in the `root-project` directory.

---


## Scalability and Maintenance

### Scalability
- **Data Sources**: Extend support for multiple APIs like Alpha Vantage or IEX Cloud.
- **Real-time Updates**: Incorporate live data streaming for real-time visualization.
- **Advanced Analytics**: Add performance metrics (e.g., daily returns, cumulative returns).

### Maintenance
- **Automated Updates**: Use schedulers (e.g., `cron`, `APScheduler`) to fetch data daily.
- **Modular Design**: Each component is independent, making updates easier.

---

## Challenges and Solutions

1. **Handling Missing Data**: Impute or exclude missing data during preprocessing.  
2. **Dynamic Scaling for Large Data**: Use a cloud database for higher scalability.  
3. **Visualization Overlaps**: Adjust layouts dynamically to avoid label overlap.

---

## Author

Created by **[Sayan Biswas]** as part of a stock index tracking project - Altemetrix. Contributions and feedback are welcome!

---