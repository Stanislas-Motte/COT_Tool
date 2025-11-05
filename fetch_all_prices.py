"""
Script to fetch historical prices for all commodities in the database.

This script:
1. Reads all unique commodity names from the database
2. Attempts to map them to Yahoo Finance tickers
3. Fetches historical prices for mapped commodities
4. Saves prices to the database
"""

import sqlite3
import pandas as pd
from fetch_prices import (
    fetch_all_available_commodities,
    save_prices_to_database,
    get_commodity_prices_from_db
)
from commodity_ticker_mapping import get_ticker_for_commodity, normalize_commodity_name
from datetime import datetime, timedelta


def get_all_commodities_from_db(db_path='commodities.db'):
    """
    Get list of all unique commodity names from the database.

    Args:
        db_path: Path to SQLite database

    Returns:
        List of commodity names
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT DISTINCT Commodity_Name FROM cot_data ORDER BY Commodity_Name"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['Commodity_Name'].tolist()


def find_mappable_commodities(commodity_list):
    """
    Find which commodities can be mapped to Yahoo Finance tickers.

    Args:
        commodity_list: List of commodity names

    Returns:
        Dictionary with 'mapped' and 'unmapped' lists
    """
    mapped = []
    unmapped = []

    for commodity in commodity_list:
        normalized = normalize_commodity_name(commodity)
        ticker = get_ticker_for_commodity(normalized)
        if ticker:
            mapped.append(commodity)
        else:
            unmapped.append(commodity)

    return {
        'mapped': mapped,
        'unmapped': unmapped
    }


def main():
    """Main function to fetch prices for all commodities."""
    print("=" * 80)
    print("Commodity Price Fetcher")
    print("=" * 80)

    # Get all commodities from database
    print("\n1. Reading commodities from database...")
    all_commodities = get_all_commodities_from_db()
    print(f"   Found {len(all_commodities)} unique commodities")

    # Find which ones can be mapped
    print("\n2. Checking ticker mappings...")
    mapping_result = find_mappable_commodities(all_commodities)
    mapped = mapping_result['mapped']
    unmapped = mapping_result['unmapped']

    print(f"   ✓ {len(mapped)} commodities have ticker mappings")
    print(f"   ✗ {len(unmapped)} commodities cannot be mapped")

    if unmapped:
        print(f"\n   Unmapped commodities (first 10):")
        for comm in unmapped[:10]:
            print(f"     - {comm}")
        if len(unmapped) > 10:
            print(f"     ... and {len(unmapped) - 10} more")

    if not mapped:
        print("\n   No commodities found with ticker mappings. Exiting.")
        return

    # Ask for date range
    print("\n3. Setting date range...")
    print("   Options:")
    print("   a) Use period (e.g., '1y', '5y', 'max')")
    print("   b) Use specific date range")

    choice = input("   Enter choice (a/b) or press Enter for default '1y': ").strip().lower()

    start_date = None
    end_date = None
    period = '1y'  # Default

    if choice == 'b':
        start_input = input("   Enter start date (YYYY-MM-DD) or press Enter for 1 year ago: ").strip()
        if start_input:
            start_date = start_input
        else:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        end_input = input("   Enter end date (YYYY-MM-DD) or press Enter for today: ").strip()
        if end_input:
            end_date = end_input
        else:
            end_date = datetime.now().strftime('%Y-%m-%d')

        period = None
        print(f"   Using date range: {start_date} to {end_date}")
    else:
        period_input = input("   Enter period (or press Enter for '1y'): ").strip()
        if period_input:
            period = period_input
        print(f"   Using period: {period}")

    # Fetch prices
    print(f"\n4. Fetching prices for {len(mapped)} commodities...")
    print("   This may take a while due to rate limiting...")

    prices = fetch_all_available_commodities(
        mapped,
        start_date=start_date,
        end_date=end_date,
        period=period,
        delay=0.5  # 0.5 second delay between requests
    )

    print(f"\n5. Results:")
    print(f"   ✓ Successfully fetched prices for {len(prices)} commodities")

    if prices:
        # Show summary
        print("\n   Summary:")
        for commodity, df in prices.items():
            if not df.empty:
                print(f"     {commodity}: {len(df)} days of data")
                if 'CLOSE' in df.columns:
                    latest_price = df['CLOSE'].iloc[-1]
                    print(f"       Latest close: ${latest_price:.2f}")

        # Ask to save
        save_choice = input("\n6. Save prices to database? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_prices_to_database(prices)
            print("\n   ✓ Prices saved to database!")
        else:
            print("\n   Prices not saved.")
    else:
        print("\n   No prices were successfully fetched.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
        import traceback
        traceback.print_exc()
