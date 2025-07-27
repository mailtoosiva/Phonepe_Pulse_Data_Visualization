import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from utils import get_db_connection, close_db_connection
import json
import os # For getting current script directory to load geojson

# Load Indian states GeoJSON data (you might need to download this file and place it in the same directory as dashboard_app.py)
# A good source for Indian state boundaries in GeoJSON format is often from GADM or similar open data projects.
# For simplicity, you might embed it or provide a direct link for download in README.
# Assuming 'india_states.geojson' is in the 'data' folder or same as app.py
try:
    script_dir = os.path.dirname(__file__)
    geojson_path = os.path.join(script_dir, '..', 'data', 'india_states.geojson') # Adjust path as needed
    with open(geojson_path) as f:
        india_geojson = json.load(f)
except FileNotFoundError:
    st.error("Error: india_states.geojson not found. Please ensure it's in the 'data' directory relative to the app.")
    st.stop() # Stop the app if geojson is missing
except Exception as e:
    st.error(f"Error loading geojson: {e}")
    st.stop()


st.set_page_config(layout="wide", page_title="PhonePe Pulse Data Visualization")

st.title("💰 PhonePe Pulse Data Visualization and Exploration")
st.markdown("---")

# --- Helper function for fetching data from MySQL ---
@st.cache_data(ttl=3600) # Cache data for 1 hour
def fetch_data_from_db(query):
    """Fetches data from MySQL database using the provided query."""
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return pd.DataFrame()
        finally:
            close_db_connection(conn, None) # Cursor is handled by pd.read_sql
    return pd.DataFrame()

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

year_options = sorted(fetch_data_from_db("SELECT DISTINCT year FROM aggregated_transactions ORDER BY year").iloc[:, 0].tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options, index=len(year_options) - 1)

quarter_options = sorted(fetch_data_from_db("SELECT DISTINCT quarter FROM aggregated_transactions WHERE year = %s ORDER BY quarter" % selected_year).iloc[:, 0].tolist())
selected_quarter = st.sidebar.selectbox("Select Quarter", quarter_options, index=0)

state_options_df = fetch_data_from_db("SELECT DISTINCT state FROM aggregated_transactions ORDER BY state")
if not state_options_df.empty:
    state_options = ['All India'] + sorted(state_options_df.iloc[:, 0].tolist())
else:
    state_options = ['All India']
selected_state = st.sidebar.selectbox("Select State", state_options)

# --- Dynamic Dropdowns based on Context ---
page_selection = st.sidebar.radio("Select Data Type", ["Transactions", "Users"])

if page_selection == "Transactions":
    st.sidebar.subheader("Transaction Filters")
    transaction_type_options_df = fetch_data_from_db("SELECT DISTINCT transaction_type FROM aggregated_transactions ORDER BY transaction_type")
    if not transaction_type_options_df.empty:
        transaction_type_options = ['All Transaction Types'] + sorted(transaction_type_options_df.iloc[:, 0].tolist())
    else:
        transaction_type_options = ['All Transaction Types']
    selected_transaction_type = st.sidebar.selectbox("Select Transaction Type", transaction_type_options)

    # Metric for Transactions
    transaction_metric_options = ["Total Transactions", "Total Amount"]
    selected_transaction_metric = st.sidebar.selectbox("Select Transaction Metric", transaction_metric_options)

    st.sidebar.subheader("Top/Bottom Filters (Transactions)")
    top_n_trans = st.sidebar.slider("Show Top/Bottom N States/Districts", 1, 30, 10)
    top_bottom_trans_type = st.sidebar.radio("Top/Bottom Type", ["Top", "Bottom"])


elif page_selection == "Users":
    st.sidebar.subheader("User Filters")
    brand_options_df = fetch_data_from_db("SELECT DISTINCT brand FROM aggregated_users WHERE brand IS NOT NULL ORDER BY brand")
    if not brand_options_df.empty:
        brand_options = ['All Brands'] + sorted(brand_options_df.iloc[:, 0].tolist())
    else:
        brand_options = ['All Brands']
    selected_brand = st.sidebar.selectbox("Select Brand", brand_options)

    # Metric for Users
    user_metric_options = ["Registered Users", "App Openings"]
    selected_user_metric = st.sidebar.selectbox("Select User Metric", user_metric_options)

    st.sidebar.subheader("Top/Bottom Filters (Users)")
    top_n_users = st.sidebar.slider("Show Top/Bottom N States/Districts", 1, 30, 10)
    top_bottom_users_type = st.sidebar.radio("Top/Bottom Type", ["Top", "Bottom"])

# --- Main Content Area ---
st.header(f"{page_selection} Overview - {selected_year} Q{selected_quarter}")

# --- Geo Visualization ---
st.subheader(f"Geographical Distribution of {page_selection}")
if selected_state == "All India":
    if page_selection == "Transactions":
        query = f"""
            SELECT state, SUM(transaction_count) as total_count, SUM(transaction_amount) as total_amount
            FROM map_transactions
            WHERE year = {selected_year} AND quarter = {selected_quarter}
            GROUP BY state
        """
        df_geo = fetch_data_from_db(query)
        if not df_geo.empty:
            color_column = 'total_amount' if selected_transaction_metric == "Total Amount" else 'total_count'
            fig_geo = px.choropleth(
                df_geo,
                geojson=india_geojson,
                featureidkey="properties.st_nm", # This needs to match the GeoJSON property for state name
                locations="state",
                color=color_column,
                color_continuous_scale="Viridis",
                hover_name="state",
                hover_data={"state":False, color_column: True},
                title=f'{selected_transaction_metric} by State in {selected_year} Q{selected_quarter}',
                height=600
            )
            fig_geo.update_geos(fitbounds="locations", visible=False)
            fig_geo.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
            st.plotly_chart(fig_geo, use_container_width=True)
        else:
            st.warning("No geographical transaction data found for the selected filters.")

    elif page_selection == "Users":
        query = f"""
            SELECT state, SUM(registered_users) as total_registered_users, SUM(app_openings) as total_app_openings
            FROM map_users
            WHERE year = {selected_year} AND quarter = {selected_quarter}
            GROUP BY state
        """
        df_geo = fetch_data_from_db(query)
        if not df_geo.empty:
            color_column = 'total_app_openings' if selected_user_metric == "App Openings" else 'total_registered_users'
            fig_geo = px.choropleth(
                df_geo,
                geojson=india_geojson,
                featureidkey="properties.st_nm",
                locations="state",
                color=color_column,
                color_continuous_scale="Plasma",
                hover_name="state",
                hover_data={"state":False, color_column: True},
                title=f'{selected_user_metric} by State in {selected_year} Q{selected_quarter}',
                height=600
            )
            fig_geo.update_geos(fitbounds="locations", visible=False)
            fig_geo.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
            st.plotly_chart(fig_geo, use_container_width=True)
        else:
            st.warning("No geographical user data found for the selected filters.")

else: # Specific state selected, show district-wise
    st.subheader(f"District-wise {page_selection} in {selected_state}")
    if page_selection == "Transactions":
        query = f"""
            SELECT district, SUM(transaction_count) as total_count, SUM(transaction_amount) as total_amount
            FROM map_transactions
            WHERE year = {selected_year} AND quarter = {selected_quarter} AND state = '{selected_state}'
            GROUP BY district
            ORDER BY total_amount DESC
        """
        df_district = fetch_data_from_db(query)
        if not df_district.empty:
            metric_col = 'total_amount' if selected_transaction_metric == "Total Amount" else 'total_count'
            fig_district = px.bar(
                df_district.sort_values(by=metric_col, ascending=False).head(top_n_trans),
                x="district",
                y=metric_col,
                title=f'{top_bottom_trans_type} {top_n_trans} Districts by {selected_transaction_metric} in {selected_state}',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_district, use_container_width=True)
        else:
            st.warning(f"No district-wise transaction data found for {selected_state} with the selected filters.")

    elif page_selection == "Users":
        query = f"""
            SELECT district, SUM(registered_users) as total_registered_users, SUM(app_openings) as total_app_openings
            FROM map_users
            WHERE year = {selected_year} AND quarter = {selected_quarter} AND state = '{selected_state}'
            GROUP BY district
            ORDER BY total_registered_users DESC
        """
        df_district = fetch_data_from_db(query)
        if not df_district.empty:
            metric_col = 'total_app_openings' if selected_user_metric == "App Openings" else 'total_registered_users'
            fig_district = px.bar(
                df_district.sort_values(by=metric_col, ascending=False).head(top_n_users),
                x="district",
                y=metric_col,
                title=f'{top_bottom_users_type} {top_n_users} Districts by {selected_user_metric} in {selected_state}',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_district, use_container_width=True)
        else:
            st.warning(f"No district-wise user data found for {selected_state} with the selected filters.")

# --- Other Visualizations (e.g., Trends, Top Lists) ---

st.markdown("---")
st.subheader("Trends and Top Statistics")

if page_selection == "Transactions":
    # Trend over time (Years)
    st.markdown("##### Transaction Trends Over Years")
    trans_trend_query = f"""
        SELECT year, SUM(transaction_amount) as total_amount, SUM(transaction_count) as total_count
        FROM aggregated_transactions
        WHERE 1=1
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        {"AND transaction_type = '%s'" % selected_transaction_type if selected_transaction_type != "All Transaction Types" else ""}
        GROUP BY year
        ORDER BY year
    """
    df_trans_trend = fetch_data_from_db(trans_trend_query)
    if not df_trans_trend.empty:
        fig_trans_trend = px.line(
            df_trans_trend,
            x="year",
            y="total_amount",
            title=f"Total Transaction Amount Trend {'in ' + selected_state if selected_state != 'All India' else ''}"
        )
        st.plotly_chart(fig_trans_trend, use_container_width=True)
    else:
        st.info("No transaction trend data available for selected filters.")

    # Top Transaction Types
    st.markdown("##### Top Transaction Types")
    top_type_query = f"""
        SELECT transaction_type, SUM(transaction_amount) as total_amount
        FROM aggregated_transactions
        WHERE year = {selected_year} AND quarter = {selected_quarter}
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        GROUP BY transaction_type
        ORDER BY total_amount DESC
        LIMIT 10
    """
    df_top_type = fetch_data_from_db(top_type_query)
    if not df_top_type.empty:
        fig_top_type = px.pie(
            df_top_type,
            values='total_amount',
            names='transaction_type',
            title=f'Top Transaction Types by Amount in {selected_year} Q{selected_quarter} {"in " + selected_state if selected_state != "All India" else ""}',
            hole=0.3
        )
        st.plotly_chart(fig_top_type, use_container_width=True)
    else:
        st.info("No transaction type data available for selected filters.")


elif page_selection == "Users":
    # Registered Users Trend over time (Years)
    st.markdown("##### Registered Users Trend Over Years")
    user_trend_query = f"""
        SELECT year, SUM(registered_users) as total_registered_users
        FROM aggregated_users
        WHERE 1=1
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        {"AND brand = '%s'" % selected_brand if selected_brand != "All Brands" else ""}
        GROUP BY year
        ORDER BY year
    """
    df_user_trend = fetch_data_from_db(user_trend_query)
    if not df_user_trend.empty:
        fig_user_trend = px.line(
            df_user_trend,
            x="year",
            y="total_registered_users",
            title=f"Total Registered Users Trend {'in ' + selected_state if selected_state != 'All India' else ''}"
        )
        st.plotly_chart(fig_user_trend, use_container_width=True)
    else:
        st.info("No registered user trend data available for selected filters.")

    # Top Brands
    st.markdown("##### User Distribution by Brand")
    top_brand_query = f"""
        SELECT brand, SUM(registered_users) as total_registered_users
        FROM aggregated_users
        WHERE year = {selected_year} AND quarter = {selected_quarter} AND brand IS NOT NULL
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        GROUP BY brand
        ORDER BY total_registered_users DESC
        LIMIT 10
    """
    df_top_brand = fetch_data_from_db(top_brand_query)
    if not df_top_brand.empty:
        fig_top_brand = px.bar(
            df_top_brand,
            x='brand',
            y='total_registered_users',
            title=f'Top User Brands by Registered Users in {selected_year} Q{selected_quarter} {"in " + selected_state if selected_state != "All India" else ""}',
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        st.plotly_chart(fig_top_brand, use_container_width=True)
    else:
        st.info("No user brand data available for selected filters.")

# --- Additional Dropdown Options (Examples) ---
st.markdown("---")
st.subheader("More Granular Data Views")

# Example: Top Pincodes for Transactions
if page_selection == "Transactions":
    st.markdown("##### Top Pincodes by Transactions")
    pincode_query = f"""
        SELECT pincode, SUM(transaction_amount) as total_amount, SUM(transaction_count) as total_count
        FROM top_transactions_pincode
        WHERE year = {selected_year} AND quarter = {selected_quarter}
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        GROUP BY pincode
        ORDER BY total_amount DESC
        LIMIT {top_n_trans}
    """
    df_pincodes = fetch_data_from_db(pincode_query)
    if not df_pincodes.empty:
        st.dataframe(df_pincodes.set_index('pincode'))
    else:
        st.info("No pincode data for transactions found.")

# Example: Top Pincodes for Users
elif page_selection == "Users":
    st.markdown("##### Top Pincodes by Registered Users")
    pincode_query = f"""
        SELECT pincode, SUM(registered_users) as total_registered_users
        FROM top_users_pincode
        WHERE year = {selected_year} AND quarter = {selected_quarter}
        {"AND state = '%s'" % selected_state if selected_state != "All India" else ""}
        GROUP BY pincode
        ORDER BY total_registered_users DESC
        LIMIT {top_n_users}
    """
    df_pincodes = fetch_data_from_db(pincode_query)
    if not df_pincodes.empty:
        st.dataframe(df_pincodes.set_index('pincode'))
    else:
        st.info("No pincode data for users found.")

# Example: Transaction/User Count/Amount Range Sliders (Illustrative - requires more complex SQL filtering)
st.sidebar.markdown("---")
st.sidebar.subheader("Numerical Filters (Illustrative)")
min_trans_val = st.sidebar.number_input("Min Transaction Amount (Millions)", min_value=0.0, value=0.0, step=0.1)
max_trans_val = st.sidebar.number_input("Max Transaction Amount (Millions)", min_value=0.0, value=100.0, step=0.1)

if page_selection == "Transactions":
    st.markdown("##### Transactions within Amount Range")
    # This query would need to be adapted to fetch relevant data based on the sliders
    # For a real implementation, you'd integrate min_trans_val and max_trans_val into the WHERE clause
    st.info(f"Displaying transactions with amount between {min_trans_val}M and {max_trans_val}M will require a specific query.")

st.markdown("---")
st.caption("Data provided by PhonePe Pulse. Developed using Streamlit, Plotly, and MySQL.")