# Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Domain](#domain)
- [Problem Statement](#problem-statement)
- [Approach](#approach)
- [Results & Features](#results--features)
- [Dataset](#dataset)
- [Learning Outcomes](#learning-outcomes)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Execution Workflow](#execution-workflow)
- [Database Schema](#database-schema)
- [Screenshots / Demo](#screenshots--demo)
- [Demo Video](#demo-video)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

This project aims to create an interactive and user-friendly data visualization dashboard for PhonePe Pulse data using Streamlit and Plotly. It involves a complete end-to-end data pipeline: extracting raw data from the PhonePe Pulse GitHub repository, transforming it into a clean and structured format, storing it in a MySQL database, and finally building a dynamic web application for insightful geo-visualizations and data exploration.

## Technologies Used

* **Python 3.x:** Core programming language.
* **Pandas:** For data manipulation and cleaning.
* **MySQL:** Relational database for data storage.
* **`mysql-connector-python`:** Python library for MySQL connectivity.
* **Streamlit:** For building the interactive web dashboard.
* **Plotly:** For creating rich, interactive, and geo-spatial visualizations.
* **Git / GitHub:** Version control and repository management.

## Domain

Fintech (Financial Technology)

## Problem Statement

The raw data available in the PhonePe Pulse GitHub repository is extensive and in a nested JSON structure, making it difficult to extract immediate insights. The challenge is to process this raw data, store it efficiently, and present it through an intuitive dashboard that allows users to easily explore various financial metrics and trends across different geographical regions and time periods.

## Approach

Our solution follows a systematic approach:

1.  **Data Extraction:**
    * Programmatically clone the official PhonePe Pulse GitHub repository (https://github.com/PhonePe/pulse) using Python's `subprocess` module or `GitPython`.
    * Identify and read the relevant JSON data files (e.g., `data/aggregated/transaction/country/india/state/`, `data/top/transaction/country/india/state/`).

2.  **Data Transformation:**
    * Use Pandas to load the JSON data into DataFrames.
    * Perform comprehensive data cleaning, including:
        * Handling nested JSON structures by flattening them.
        * Standardizing column names.
        * Converting data types (e.g., year, quarter, amount to numeric).
        * Handling potential missing values or inconsistencies.
    * Aggregate and structure the data into suitable formats for relational database storage (e.g., separate tables for aggregated transactions, top transactions, aggregated users, top users, etc.).

3.  **Database Insertion:**
    * Set up a MySQL database.
    * Define a robust database schema (refer to [Database Schema](#database-schema) section).
    * Utilize `mysql-connector-python` to connect to MySQL.
    * Create tables programmatically or via an SQL script.
    * Insert the cleaned and transformed data into the respective MySQL tables using `executemany` for efficiency.

4.  **Dashboard Creation (Streamlit & Plotly):**
    * Develop a `dashboard_app.py` using Streamlit.
    * Implement an intuitive sidebar with Streamlit widgets (`st.selectbox`, `st.slider`, etc.).
    * Fetch data from the MySQL database based on user selections.
    * Create various Plotly visualizations, including:
        * **Geo-maps (Choropleth maps):** To display state-wise and district-wise transaction and user data.
        * **Bar charts, Line charts:** For trends over time, top categories, etc.
        * **Pie charts:** For brand distribution.
    * Implement at least **10 distinct dropdown/selection options** for dynamic filtering:
        1.  Year
        2.  Quarter
        3.  Transaction Type (e.g., "Recharge & Bill Payments", "Peer-to-peer payments")
        4.  User Brand (e.g., "Xiaomi", "Samsung")
        5.  State selection for detailed district-level views
        6.  Metric Type (e.g., "Total Transactions", "Total Amount", "Registered Users", "App Openings")
        7.  Top N filter for top entities
        8.  Transaction Amount Range (slider)
        9.  Transaction Count Range (slider)
        10. Specific Pincode/District search (text input or selectbox)

5.  **Data Retrieval & Dynamic Updating:**
    * Database queries will be executed upon user interaction with dropdowns/filters.
    * The fetched data will then be used to render or update the Plotly charts dynamically.

6.  **Deployment:**
    * Ensure all dependencies are listed in `requirements.txt`.
    * Host the code on a public GitHub repository.
    * Deploy the Streamlit application to Streamlit Community Cloud for public accessibility.
    * Record a demo video and share on LinkedIn.

## Results & Features

The project will deliver a powerful and interactive dashboard with the following key features:

* **Live Geo-Visualization:** Interactive maps of India displaying transaction and user data at state and district levels.
* **Dynamic Filtering:** Users can filter data by year, quarter, transaction type, user brand, and more, providing granular insights.
* **Comprehensive Metrics:** Visualizations for total transactions, total amount, registered users, app openings, and top entities (states, districts, pincodes, brands).
* **User-Friendly Interface:** Built with Streamlit for an intuitive and responsive web experience.
* **Efficient Data Handling:** Data stored in MySQL for quick retrieval and analysis.
* **Actionable Insights:** Facilitates understanding of PhonePe's market penetration, user behavior, and regional trends.

## Dataset

The data for this project is sourced from the official PhonePe Pulse GitHub repository:
[https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse)

## Learning Outcomes

This project offers valuable learning opportunities in:

* **Data Engineering:** GitHub cloning, data extraction from complex JSON, data cleaning, transformation, and ETL processes.
* **Database Management:** MySQL setup, schema design, and efficient data insertion/retrieval using `mysql-connector-python`.
* **Data Visualization:** Creating compelling and interactive charts with Plotly, including advanced geo-spatial plots.
* **Web Application Development:** Building interactive data applications with Streamlit.
* **Software Engineering:** Modular coding, adherence to PEP 8, version control with Git/GitHub, and deployment strategies.
* **Problem Solving:** Breaking down a complex problem into manageable components and integrating various technologies.

## Project Structure

(Refer to the `Phonepe_Pulse_Data_Visualization/` directory structure at the beginning of this document.)

## Setup and Installation

Follow these steps to set up and run the project locally:

### Prerequisites

* Python 3.8+
* Git
* MySQL Server (e.g., XAMPP, Docker, or local installation)

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Phonepe_Pulse_Data_Visualization.git](https://github.com/YOUR_USERNAME/Phonepe_Pulse_Data_Visualization.git)
    cd Phonepe_Pulse_Data_Visualization
    ```
    (Replace `YOUR_USERNAME` with your actual GitHub username)

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **MySQL Database Setup:**
    * Ensure your MySQL server is running.
    * **Create a database:**
        Connect to your MySQL server (e.g., using MySQL Workbench, `mysql` CLI, or phpMyAdmin) and run:
        ```sql
        CREATE DATABASE phonepe_pulse_db;
        ```
    * **Create user and grant permissions (optional but good practice):**
        ```sql
        CREATE USER 'phonepe_user'@'localhost' IDENTIFIED BY 'your_password';
        GRANT ALL PRIVILEGES ON phonepe_pulse_db.* TO 'phonepe_user'@'localhost';
        FLUSH PRIVILEGES;
        ```
        (Replace `your_password` with a strong password)
    * **Configure Database Credentials:**
        Create a file named `.env` in the root directory of your project (e.g., `Phonepe_Pulse_Data_Visualization/.env`) and add your database credentials:
        ```
        DB_HOST=localhost
        DB_USER=phonepe_user
        DB_PASSWORD=your_password
        DB_NAME=phonepe_pulse_db
        ```
        **NOTE:** **NEVER commit `.env` or `config.ini` files to GitHub** as they contain sensitive information. Add them to your `.gitignore`.

5.  **Run Data Pipeline:**

    * **Extract Raw Data:**
        ```bash
        python src/data_extraction.py
        ```
        This script will clone the PhonePe Pulse GitHub repository into the `data/raw_data/` directory.

    * **Transform Data and Insert into MySQL:**
        ```bash
        python src/data_transformation.py
        python src/database_insertion.py
        ```
        *`data_transformation.py`* will read from `data/raw_data/`, clean and process it, and prepare it.
        *`database_insertion.py`* will connect to your MySQL database and insert the processed data.

        **Alternatively, you can run a single script that orchestrates all these steps, or combine `data_transformation.py` and `database_insertion.py` into one if preferred for simplicity in a smaller project.**

## Execution Workflow

1.  **Start MySQL Server:** Ensure your MySQL server is running.
2.  **Execute Data Pipeline:** Run the `data_extraction.py`, `data_transformation.py`, and `database_insertion.py` scripts in sequence to populate your database. This is a one-time process or run whenever new data is added to the PhonePe Pulse GitHub repo.
    ```bash
    python src/data_extraction.py
    python src/data_transformation.py
    python src/database_insertion.py
    ```
3.  **Run the Streamlit Dashboard:**
    ```bash
    streamlit run src/dashboard_app.py
    ```
    This will open the Streamlit application in your web browser, typically at `http://localhost:8501`.

## Database Schema

The MySQL database `phonepe_pulse_db` will contain the following tables:

* **`aggregated_transactions`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `transaction_type` (VARCHAR(255))
    * `transaction_count` (BIGINT)
    * `transaction_amount` (DECIMAL(18, 2))

* **`aggregated_users`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `brand` (VARCHAR(255))
    * `registered_users` (BIGINT)
    * `app_openings` (BIGINT)

* **`map_transactions`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `district` (VARCHAR(255))
    * `transaction_count` (BIGINT)
    * `transaction_amount` (DECIMAL(18, 2))

* **`map_users`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `district` (VARCHAR(255))
    * `registered_users` (BIGINT)
    * `app_openings` (BIGINT)

* **`top_transactions_state`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `pincode` (INT)
    * `transaction_count` (BIGINT)
    * `transaction_amount` (DECIMAL(18, 2))

* **`top_transactions_district`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `district` (VARCHAR(255))
    * `transaction_count` (BIGINT)
    * `transaction_amount` (DECIMAL(18, 2))

* **`top_transactions_pincode`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `pincode` (INT)
    * `transaction_count` (BIGINT)
    * `transaction_amount` (DECIMAL(18, 2))

* **`top_users_state`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `pincode` (INT)
    * `registered_users` (BIGINT)

* **`top_users_district`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `district` (VARCHAR(255))
    * `registered_users` (BIGINT)

* **`top_users_pincode`**
    * `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    * `state` (VARCHAR(255))
    * `year` (INT)
    * `quarter` (INT)
    * `pincode` (INT)
    * `registered_users` (BIGINT)

*(Note: The exact schema might be slightly adjusted based on the intricacies of the raw JSON data structure and normalization choices. The above is a strong starting point.)*

## Screenshots / Demo

*(Add screenshots of your Streamlit dashboard here to visually showcase its features. Include various views and interactive elements.)*

## Demo Video

[Link to your LinkedIn Demo Video] (e.g., `https://www.linkedin.com/feed/update/urn:li:activity:XXXXXXXXXX/`)

## Contributing

Feel free to fork this repository, create pull requests, or open issues for any suggestions or bugs.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contact

* **Your Name:** [Your LinkedIn Profile URL]
* **Email:** [Your Email Address]

---