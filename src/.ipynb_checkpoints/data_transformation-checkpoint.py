import pandas as pd
import os
import json
import re

RAW_DATA_DIR = "data/raw_data/"
PROCESSED_DATA_DIR = "data/processed_data/" # For optional CSVs

def create_processed_data_dir():
    """Creates directory for processed data if it doesn't exist."""
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def clean_state_name(state_name):
    """Cleans state names for consistency (e.g., removing '-')."""
    return state_name.replace('-', ' ').title()

def extract_and_transform_aggregated_transactions():
    """Extracts and transforms aggregated transaction data."""
    data_list = []
    agg_trans_path = os.path.join(RAW_DATA_DIR, "data", "aggregated", "transaction", "country", "india", "state")
    for state_folder in os.listdir(agg_trans_path):
        state_path = os.path.join(agg_trans_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                # Quarter is typically 1, 2, 3, 4 based on filename
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                for item in data['data']['transactionData']:
                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'transaction_type': item['name'],
                                        'transaction_count': item['paymentInstruments'][0]['count'],
                                        'transaction_amount': item['paymentInstruments'][0]['amount']
                                    })
    return pd.DataFrame(data_list)

def extract_and_transform_aggregated_users():
    """Extracts and transforms aggregated user data."""
    data_list = []
    agg_user_path = os.path.join(RAW_DATA_DIR, "data", "aggregated", "user", "country", "india", "state")
    for state_folder in os.listdir(agg_user_path):
        state_path = os.path.join(agg_user_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                # Check if 'userRegistered' exists and 'userDevice'
                                registered_users = data['data'].get('aggregatedBy', {}).get('userRegistered', 0)
                                app_openings = data['data'].get('aggregatedBy', {}).get('appOpens', 0) # This might be less consistently available

                                if 'userDevices' in data['data']:
                                    for item in data['data']['userDevices']:
                                        data_list.append({
                                            'state': cleaned_state,
                                            'year': year,
                                            'quarter': quarter,
                                            'brand': item['brand'],
                                            'registered_users': item['count'],
                                            'app_openings': item['percentage'] # This is percentage, need to convert or decide
                                        })
                                else: # Handle cases where userDevices might be missing but overall user data exists
                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'brand': 'Unknown', # Default if no brand data
                                        'registered_users': registered_users,
                                        'app_openings': app_openings
                                    })
    # Post-process app_openings if it's percentage-based
    df = pd.DataFrame(data_list)
    # If app_openings is percentage, you might need to re-calculate total openings per state/year/quarter based on registered_users
    # Or, if data['data']['aggregatedBy']['appOpens'] is reliable, use that.
    # For now, let's assume `item['percentage']` is `app_openings` for the brand.
    # A more robust transformation might be needed here based on actual data values.
    return df


def extract_and_transform_map_transactions():
    """Extracts and transforms map transaction data (state/district)."""
    data_list = []
    map_trans_path = os.path.join(RAW_DATA_DIR, "data", "map", "transaction", "hover", "country", "india", "state")
    for state_folder in os.listdir(map_trans_path):
        state_path = os.path.join(map_trans_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                for item in data['data']['hoverDataList']:
                                    # Extract district name (e.g., 'district name (count)' -> 'district name')
                                    district_name_raw = item['name']
                                    district = re.sub(r'\s*\(\d+\)$', '', district_name_raw)

                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'district': district,
                                        'transaction_count': item['metric'][0]['count'],
                                        'transaction_amount': item['metric'][0]['amount']
                                    })
    return pd.DataFrame(data_list)

def extract_and_transform_map_users():
    """Extracts and transforms map user data (state/district)."""
    data_list = []
    map_user_path = os.path.join(RAW_DATA_DIR, "data", "map", "user", "hover", "country", "india", "state")
    for state_folder in os.listdir(map_user_path):
        state_path = os.path.join(map_user_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                for item in data['data']['hoverDataList']:
                                    district_name_raw = item['name']
                                    district = re.sub(r'\s*\(\d+\)$', '', district_name_raw)

                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'district': district,
                                        'registered_users': item['metric'][0]['registeredUsers'],
                                        'app_openings': item['metric'][0].get('appOpens', 0) # appOpens might be missing in some older data
                                    })
    return pd.DataFrame(data_list)

def extract_and_transform_top_transactions_pincode():
    """Extracts and transforms top transaction data (state/pincode)."""
    data_list = []
    top_trans_path = os.path.join(RAW_DATA_DIR, "data", "top", "transaction", "country", "india", "state")
    for state_folder in os.listdir(top_trans_path):
        state_path = os.path.join(top_trans_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                for item in data['data']['pincodes']:
                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'pincode': item['entityName'], # This is actually the pincode
                                        'transaction_count': item['metric']['count'],
                                        'transaction_amount': item['metric']['amount']
                                    })
    return pd.DataFrame(data_list)

def extract_and_transform_top_users_pincode():
    """Extracts and transforms top user data (state/pincode)."""
    data_list = []
    top_user_path = os.path.join(RAW_DATA_DIR, "data", "top", "user", "country", "india", "state")
    for state_folder in os.listdir(top_user_path):
        state_path = os.path.join(top_user_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                year = int(year_folder)
                                quarter = int(re.search(r'(\d+)\.json', json_file).group(1))

                                for item in data['data']['pincodes']:
                                    data_list.append({
                                        'state': cleaned_state,
                                        'year': year,
                                        'quarter': quarter,
                                        'pincode': item['entityName'], # This is pincode
                                        'registered_users': item['metric']['registeredUsers']
                                    })
    return pd.DataFrame(data_list)

def create_top_transactions_district_from_map_transactions(df_map_transactions):
    """Aggregates map transactions to get top transactions by district."""
    # Group by state, year, quarter, district and sum transaction count/amount
    df_top_dist_trans = df_map_transactions.groupby(
        ['state', 'year', 'quarter', 'district']
    ).agg(
        transaction_count=('transaction_count', 'sum'),
        transaction_amount=('transaction_amount', 'sum')
    ).reset_index()
    return df_top_dist_trans

def create_top_users_district_from_map_users(df_map_users):
    """Aggregates map users to get top users by district."""
    # Group by state, year, quarter, district and sum registered users/app openings
    df_top_dist_users = df_map_users.groupby(
        ['state', 'year', 'quarter', 'district']
    ).agg(
        registered_users=('registered_users', 'sum'),
        app_openings=('app_openings', 'sum')
    ).reset_index()
    return df_top_dist_users

def run_data_transformation():
    """Orchestrates the data extraction and transformation process."""
    create_processed_data_dir()

    print("Extracting and transforming aggregated transactions...")
    df_agg_trans = extract_and_transform_aggregated_transactions()
    # df_agg_trans.to_csv(os.path.join(PROCESSED_DATA_DIR, 'agg_transaction.csv'), index=False)
    print("Done: aggregated_transactions")

    print("Extracting and transforming aggregated users...")
    df_agg_users = extract_and_transform_aggregated_users()
    # df_agg_users.to_csv(os.path.join(PROCESSED_DATA_DIR, 'agg_users.csv'), index=False)
    print("Done: aggregated_users")

    print("Extracting and transforming map transactions...")
    df_map_trans = extract_and_transform_map_transactions()
    # df_map_trans.to_csv(os.path.join(PROCESSED_DATA_DIR, 'map_transactions.csv'), index=False)
    print("Done: map_transactions")

    print("Extracting and transforming map users...")
    df_map_users = extract_and_transform_map_users()
    # df_map_users.to_csv(os.path.join(PROCESSED_DATA_DIR, 'map_users.csv'), index=False)
    print("Done: map_users")

    print("Extracting and transforming top transactions (pincode)...")
    df_top_trans_pincode = extract_and_transform_top_transactions_pincode()
    # df_top_trans_pincode.to_csv(os.path.join(PROCESSED_DATA_DIR, 'top_transactions_pincode.csv'), index=False)
    print("Done: top_transactions_pincode")

    print("Extracting and transforming top users (pincode)...")
    df_top_users_pincode = extract_and_transform_top_users_pincode()
    # df_top_users_pincode.to_csv(os.path.join(PROCESSED_DATA_DIR, 'top_users_pincode.csv'), index=False)
    print("Done: top_users_pincode")

    print("Creating top transactions by district from map transactions...")
    df_top_trans_district = create_top_transactions_district_from_map_transactions(df_map_trans)
    print("Done: top_transactions_district")

    print("Creating top users by district from map users...")
    df_top_users_district = create_top_users_district_from_map_users(df_map_users)
    print("Done: top_users_district")

    print("All data transformations complete.")
    return {
        'agg_transactions': df_agg_trans,
        'agg_users': df_agg_users,
        'map_transactions': df_map_trans,
        'map_users': df_map_users,
        'top_transactions_pincode': df_top_trans_pincode,
        'top_users_pincode': df_top_users_pincode,
        'top_transactions_district': df_top_trans_district,
        'top_users_district': df_top_users_district
    }

if __name__ == "__main__":
    transformed_dataframes = run_data_transformation()
    # You can inspect dataframes here or save them to CSVs if needed for debugging
    # For example:
    # print(transformed_dataframes['agg_transactions'].head())