# Custom Index Tracker

A Python-based project to create, analyze, and visualize a custom equal-weighted index. This application dynamically tracks the performance of the index, identifies composition changes, and provides an interactive dashboard for visualization.

---

## **Table of Contents**
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Reason for Technology Choices](#reason-for-technology-choices)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## **Introduction**
This project provides a streamlined way to create and track a custom equal-weighted stock index. Users can analyze the index's performance, track changes in its composition, and visualize data through an interactive dashboard.

---

## **Features**
1. **Dynamic Index Construction**:
   - Fetches market data and constructs an equal-weighted index for top 100 stocks.
   - Tracks daily changes in the index composition.

2. **Interactive Dashboard**:
   - Displays index performance over the past month using a line chart.
   - Shows index composition for a selected day.
   - Highlights changes in index composition dynamically.

3. **Data Export**:
   - Exports index performance and composition to Excel and PDF files.
   - Automatically organizes exported files into an `output` folder.

4. **Configurable**:
   - Uses `.env` files for database and environment configuration.

---

## **Technologies Used**

| **Technology** | **Purpose**                          |
|-----------------|--------------------------------------|
| Python          | Core programming language           |
| SQLite3         | Lightweight, in-memory SQL database |
| Dash            | Interactive dashboard and UI        |
| Plotly          | Data visualization library          |
| pandas          | Data analysis and manipulation      |
| yfinance        | Stock market data retrieval         |
| FPDF            | PDF file generation                |
| openpyxl        | Excel file export                  |

---

## **Reason for Technology Choices**

1. **Python**:
   - Its rich ecosystem and libraries make it an ideal choice for financial data processing and visualization.
   - Simplicity and readability ensure rapid development.

2. **SQLite3**:
   - Lightweight SQL database that supports in-memory and file-based operations.
   - Easy to set up and ideal for small to medium datasets.

3. **Dash and Plotly**:
   - Enables the creation of highly interactive dashboards with minimal effort.
   - Plotly provides beautiful and customizable visualizations.

4. **pandas**:
   - Efficiently handles and processes tabular data.
   - Supports seamless integration with data sources like CSV and databases.

5. **yfinance**:
   - Reliable and straightforward library for fetching stock market data.

6. **FPDF and openpyxl**:
   - Provide comprehensive tools to export analysis results into professional reports.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/custom-index-tracker.git
cd custom-index-tracker
```

### **2. Create and Activate a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up the Environment**
Create a `.env` file in the root directory with the following content:
```
DB_PATH=custom_index.db
```

### **5. Run the Application**
```bash
python main.py
```

---

## **Usage**

1. **Run the Dashboard**:
   - Access the dashboard at `http://127.0.0.1:8050` after running the script.
   
2. **Interact with the Dashboard**:
   - Select a date to view the index composition dynamically.
   - View index performance, composition changes, and summary metrics.

3. **Export Data**:
   - Check the `output` folder for Excel and PDF reports.

---

## **Folder Structure**
```
custom-index-tracker/
├── src
│   ├── dashboard.py
│   ├── data_exported.py
│   ├── index_constructor.py
│   ├── market_data_fetcher.py
│   ├── data_exporter.py        # Handles data export to Excel and PDF
├── settings/
│   ├── .env
│   ├── config.py
├── database/
│   ├── database_manager.py # Manages SQLite database 
│   ├── query_manager.py    # Handles database queries
├── main.py                 # Main entry point for the project
├── requirements.txt        # Python dependencies
├── output/                 # Folder for exported 
│   ├── index_performance.xlsx
│   ├── index_performance.pdf
└── README.md               # Project documentation
```

---

## **Future Enhancements**
1. **Real-Time Updates**:
   - Integrate live data feeds for near real-time index tracking.
2. **Advanced Analytics**:
   - Add metrics like sector-wise breakdown and volatility analysis.
3. **User Authentication**:
   - Enable multiple users to create and track custom indices.
4. **Cloud Integration**:
   - Support cloud databases like PostgreSQL for scalability.

---

## **Contributing**
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Create a pull request.

---

## **License**
This project is licensed under the MIT License. See `LICENSE` for details.

---