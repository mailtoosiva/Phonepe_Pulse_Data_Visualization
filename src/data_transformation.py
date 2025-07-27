import pandas as pd
import os
import json
import re

# Configuration (or load from config.ini if you set that up)
RAW_DATA_DIR = "data/raw_data/"
PROCESSED_DATA_DIR = "data/processed_data/" # For optional CSVs, not strictly needed for DB insertion

def create_processed_data_dir():
    """Creates directory for processed data if it doesn't exist.
    This is mainly for debugging/optional CSV outputs.
    """
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

def clean_state_name(state_name):
    """Cleans state names for consistency (e.g., removing '-', converting to title case)."""
    # Remove file extensions, then replace hyphens, then title case
    base_name = os.path.splitext(state_name)[0]
    return base_name.replace('-', ' ').title()

def extract_year_quarter(json_file_name):
    """Extracts quarter from the JSON file name.
    Assumes file name is like '1.json' for quarter 1.
    Year is taken from the parent folder name.
    """
    try:
        quarter = int(os.path.splitext(json_file_name)[0])
        return quarter
    except ValueError:
        return None

def extract_and_transform_aggregated_transactions():
    """Extracts and transforms aggregated transaction data."""
    data_list = []
    # Path: data/aggregated/transaction/country/india/state/{state}/{year}/{quarter}.json
    agg_trans_base_path = os.path.join(RAW_DATA_DIR, "data", "aggregated", "transaction", "country", "india", "state")

    if not os.path.exists(agg_trans_base_path):
        print(f"Warning: Aggregated transaction path not found: {agg_trans_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(agg_trans_base_path):
        state_path = os.path.join(agg_trans_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                # Check for expected data structure
                                if 'data' in data and 'transactionData' in data['data']:
                                    for item in data['data']['transactionData']:
                                        payment_instruments = item.get('paymentInstruments')
                                        if payment_instruments and isinstance(payment_instruments, list) and len(payment_instruments) > 0:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'transaction_type': item.get('name'),
                                                'transaction_count': payment_instruments[0].get('count', 0),
                                                'transaction_amount': payment_instruments[0].get('amount', 0.0)
                                            })
                                        else:
                                            print(f"Warning: Missing or invalid 'paymentInstruments' in {file_path} for item: {item.get('name', 'Unknown')}. Skipping item.")
                                else:
                                    print(f"Warning: Missing 'data' or 'transactionData' in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)

def extract_and_transform_aggregated_users():
    """Extracts and transforms aggregated user data."""
    data_list = []
    # Path: data/aggregated/user/country/india/state/{state}/{year}/{quarter}.json
    agg_user_base_path = os.path.join(RAW_DATA_DIR, "data", "aggregated", "user", "country", "india", "state")

    if not os.path.exists(agg_user_base_path):
        print(f"Warning: Aggregated user path not found: {agg_user_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(agg_user_base_path):
        state_path = os.path.join(agg_user_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                if 'data' in data:
                                    aggregated_by = data['data'].get('aggregatedBy', {})
                                    total_registered_users_overall = aggregated_by.get('userRegistered', 0)
                                    total_app_openings_overall = aggregated_by.get('appOpens', 0)

                                    if 'userDevices' in data['data'] and data['data']['userDevices']:
                                        for item in data['data']['userDevices']:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'brand': item.get('brand', 'Unknown'),
                                                'registered_users': item.get('count', 0),
                                                'app_openings': item.get('percentage', 0.0)
                                            })
                                    else:
                                        data_list.append({
                                            'state': cleaned_state,
                                            'year': year,
                                            'quarter': quarter,
                                            'brand': 'Overall',
                                            'registered_users': total_registered_users_overall,
                                            'app_openings': total_app_openings_overall
                                        })
                                else:
                                    print(f"Warning: Missing 'data' key in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)

def extract_and_transform_map_transactions():
    """Extracts and transforms map transaction data (state/district)."""
    data_list = []
    # Path: data/map/transaction/hover/country/india/state/{state}/{year}/{quarter}.json
    map_trans_base_path = os.path.join(RAW_DATA_DIR, "data", "map", "transaction", "hover", "country", "india", "state")

    if not os.path.exists(map_trans_base_path):
        print(f"Warning: Map transaction path not found: {map_trans_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(map_trans_base_path):
        state_path = os.path.join(map_trans_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder) # <--- THIS IS THE LINE THAT WAS LIKELY WRONG BEFORE
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                # Crucial check for 'hoverDataList'
                                if 'data' in data and 'hoverDataList' in data['data'] and data['data']['hoverDataList']:
                                    for item in data['data']['hoverDataList']:
                                        district_name_raw = item.get('name')
                                        district = re.sub(r'\s*\(\d+\)$', '', district_name_raw) if district_name_raw else "Unknown District"

                                        metric_data = item.get('metric')
                                        if metric_data and isinstance(metric_data, list) and len(metric_data) > 0:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'district': district,
                                                'transaction_count': metric_data[0].get('count', 0),
                                                'transaction_amount': metric_data[0].get('amount', 0.0)
                                            })
                                        else:
                                            print(f"Warning: Missing or invalid 'metric' data in {file_path}, item: {item.get('name', 'Unknown')}. Skipping item.")
                                elif 'data' in data and 'hoverDataList' in data['data'] and not data['data']['hoverDataList']:
                                     print(f"Info: 'hoverDataList' is empty in {file_path}. Skipping file.")
                                else:
                                    print(f"Warning: Missing 'data' or 'hoverDataList' in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)

def extract_and_transform_map_users():
    """Extracts and transforms map user data (state/district)."""
    data_list = []
    # Path: data/map/user/hover/country/india/state/{state}/{year}/{quarter}.json
    map_user_base_path = os.path.join(RAW_DATA_DIR, "data", "map", "user", "hover", "country", "india", "state")

    if not os.path.exists(map_user_base_path):
        print(f"Warning: Map user path not found: {map_user_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(map_user_base_path):
        state_path = os.path.join(map_user_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                # Crucial check for 'hoverDataList'
                                if 'data' in data and 'hoverDataList' in data['data'] and data['data']['hoverDataList']:
                                    for item in data['data']['hoverDataList']:
                                        district_name_raw = item.get('name')
                                        district = re.sub(r'\s*\(\d+\)$', '', district_name_raw) if district_name_raw else "Unknown District"

                                        metric_data = item.get('metric')
                                        if metric_data and isinstance(metric_data, list) and len(metric_data) > 0:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'district': district,
                                                'registered_users': metric_data[0].get('registeredUsers', 0),
                                                'app_openings': metric_data[0].get('appOpens', 0) # appOpens might be missing or 0 in some data
                                            })
                                        else:
                                            print(f"Warning: Missing or invalid 'metric' data in {file_path}, item: {item.get('name', 'Unknown')}. Skipping item.")
                                elif 'data' in data and 'hoverDataList' in data['data'] and not data['data']['hoverDataList']:
                                    print(f"Info: 'hoverDataList' is empty in {file_path}. Skipping file.")
                                else:
                                    print(f"Warning: Missing 'data' or 'hoverDataList' in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)


def extract_and_transform_top_transactions_pincode():
    """Extracts and transforms top transaction data (state/pincode)."""
    data_list = []
    # Path: data/top/transaction/country/india/state/{state}/{year}/{quarter}.json
    top_trans_base_path = os.path.join(RAW_DATA_DIR, "data", "top", "transaction", "country", "india", "state")

    if not os.path.exists(top_trans_base_path):
        print(f"Warning: Top transaction path not found: {top_trans_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(top_trans_base_path):
        state_path = os.path.join(top_trans_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                if 'data' in data and 'pincodes' in data['data'] and data['data']['pincodes']:
                                    for item in data['data']['pincodes']:
                                        metric_data = item.get('metric')
                                        if metric_data:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'pincode': item.get('entityName'), # This is the pincode
                                                'transaction_count': metric_data.get('count', 0),
                                                'transaction_amount': metric_data.get('amount', 0.0)
                                            })
                                        else:
                                            print(f"Warning: Missing 'metric' data in {file_path}, item: {item.get('entityName', 'Unknown')}. Skipping item.")
                                elif 'data' in data and 'pincodes' in data['data'] and not data['data']['pincodes']:
                                    print(f"Info: 'pincodes' list is empty in {file_path}. Skipping file.")
                                else:
                                    print(f"Warning: Missing 'data' or 'pincodes' in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)

def extract_and_transform_top_users_pincode():
    """Extracts and transforms top user data (state/pincode)."""
    data_list = []
    # Path: data/top/user/country/india/state/{state}/{year}/{quarter}.json
    top_user_base_path = os.path.join(RAW_DATA_DIR, "data", "top", "user", "country", "india", "state")

    if not os.path.exists(top_user_base_path):
        print(f"Warning: Top user path not found: {top_user_base_path}. Returning empty DataFrame.")
        return pd.DataFrame()

    for state_folder in os.listdir(top_user_base_path):
        state_path = os.path.join(top_user_base_path, state_folder)
        if os.path.isdir(state_path):
            cleaned_state = clean_state_name(state_folder)
            for year_folder in os.listdir(state_path):
                # Corrected path construction for year_path
                year_path = os.path.join(state_path, year_folder)
                if os.path.isdir(year_path):
                    for json_file in os.listdir(year_path):
                        if json_file.endswith(".json"):
                            file_path = os.path.join(year_path, json_file)
                            try:
                                with open(file_path, 'r') as f:
                                    data = json.load(f)

                                year = int(year_folder)
                                quarter = extract_year_quarter(json_file)
                                if quarter is None:
                                    print(f"Warning: Could not extract quarter from {json_file}. Skipping file.")
                                    continue

                                if 'data' in data and 'pincodes' in data['data'] and data['data']['pincodes']:
                                    for item in data['data']['pincodes']:
                                        metric_data = item.get('metric')
                                        if metric_data:
                                            data_list.append({
                                                'state': cleaned_state,
                                                'year': year,
                                                'quarter': quarter,
                                                'pincode': item.get('entityName'), # This is pincode
                                                'registered_users': metric_data.get('registeredUsers', 0)
                                            })
                                        else:
                                            print(f"Warning: Missing 'metric' data in {file_path}, item: {item.get('entityName', 'Unknown')}. Skipping item.")
                                elif 'data' in data and 'pincodes' in data['data'] and not data['data']['pincodes']:
                                    print(f"Info: 'pincodes' list is empty in {file_path}. Skipping file.")
                                else:
                                    print(f"Warning: Missing 'data' or 'pincodes' in {file_path}. Skipping file.")

                            except json.JSONDecodeError:
                                print(f"Error decoding JSON from file: {file_path}. Skipping file.")
                            except Exception as e:
                                print(f"An unexpected error occurred processing {file_path}: {e}. Skipping file.")

    return pd.DataFrame(data_list)

def create_top_transactions_district_from_map_transactions(df_map_transactions):
    """Aggregates map transactions to get top transactions by district."""
    if df_map_transactions.empty:
        print("Warning: df_map_transactions is empty. Cannot create top_transactions_district.")
        return pd.DataFrame()

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
    if df_map_users.empty:
        print("Warning: df_map_users is empty. Cannot create top_users_district.")
        return pd.DataFrame()

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
    create_processed_data_dir() # Ensures the directory exists for optional CSVs

    print("Extracting and transforming aggregated transactions...")
    df_agg_trans = extract_and_transform_aggregated_transactions()
    # Optional: df_agg_trans.to_csv(os.path.join(PROCESSED_DATA_DIR, 'agg_transaction.csv'), index=False)
    print(f"Done: aggregated_transactions. Rows processed: {len(df_agg_trans)}")

    print("Extracting and transforming aggregated users...")
    df_agg_users = extract_and_transform_aggregated_users()
    # Optional: df_agg_users.to_csv(os.path.join(PROCESSED_DATA_DIR, 'agg_users.csv'), index=False)
    print(f"Done: aggregated_users. Rows processed: {len(df_agg_users)}")

    print("Extracting and transforming map transactions...")
    df_map_trans = extract_and_transform_map_transactions()
    # Optional: df_map_trans.to_csv(os.path.join(PROCESSED_DATA_DIR, 'map_transactions.csv'), index=False)
    print(f"Done: map_transactions. Rows processed: {len(df_map_trans)}")

    print("Extracting and transforming map users...")
    df_map_users = extract_and_transform_map_users()
    # Optional: df_map_users.to_csv(os.path.join(PROCESSED_DATA_DIR, 'map_users.csv'), index=False)
    print(f"Done: map_users. Rows processed: {len(df_map_users)}")

    print("Extracting and transforming top transactions (pincode)...")
    df_top_trans_pincode = extract_and_transform_top_transactions_pincode()
    # Optional: df_top_trans_pincode.to_csv(os.path.join(PROCESSED_DATA_DIR, 'top_transactions_pincode.csv'), index=False)
    print(f"Done: top_transactions_pincode. Rows processed: {len(df_top_trans_pincode)}")

    print("Extracting and transforming top users (pincode)...")
    df_top_users_pincode = extract_and_transform_top_users_pincode()
    # Optional: df_top_users_pincode.to_csv(os.path.join(PROCESSED_DATA_DIR, 'top_users_pincode.csv'), index=False)
    print(f"Done: top_users_pincode. Rows processed: {len(df_top_users_pincode)}")

    # Create derived dataframes
    print("Creating top transactions by district from map transactions...")
    df_top_trans_district = create_top_transactions_district_from_map_transactions(df_map_trans)
    print(f"Done: top_transactions_district. Rows processed: {len(df_top_trans_district)}")

    print("Creating top users by district from map users...")
    df_top_users_district = create_top_users_district_from_map_users(df_map_users)
    print(f"Done: top_users_district. Rows processed: {len(df_top_users_district)}")

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
    # You can add more prints or checks here for debugging purposes
    print("\n--- Sample DataFrames Head ---")
    for df_name, df in transformed_dataframes.items():
        if not df.empty:
            print(f"\n{df_name}:")
            print(df.head())
        else:
            print(f"\n{df_name}: (Empty DataFrame)")