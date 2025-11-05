"""
Yahoo Finance price fetching module.

This module provides functions to fetch historical commodity prices from Yahoo Finance
using the yfinance library.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import time
from commodity_ticker_mapping import get_ticker_for_commodity, normalize_commodity_name


def fetch_historical_prices(ticker: str, start_date: Optional[str] = None,
                            end_date: Optional[str] = None, period: Optional[str] = None) -> pd.DataFrame:
    """
    Fetch historical prices for a Yahoo Finance ticker.

    Args:
        ticker: Yahoo Finance ticker symbol (e.g., 'GC=F' for Gold)
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)
        period: Alternative to dates: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'

    Returns:
        DataFrame with columns: Date, Open, High, Low, Close, Volume, Dividends, Stock Splits
        Returns empty DataFrame if ticker not found or error occurs
    """
    try:
        stock = yf.Ticker(ticker)

        if period:
            hist = stock.history(period=period)
        elif start_date and end_date:
            hist = stock.history(start=start_date, end=end_date)
        elif start_date:
            hist = stock.history(start=start_date)
        else:
            # Default: 1 year of data
            hist = stock.history(period='1y')

        if hist.empty:
            return pd.DataFrame()

        # Reset index to make Date a column
        hist.reset_index(inplace=True)

        # Rename columns to standard format
        hist.columns = [col.replace(' ', '_').upper() if isinstance(col, str) else col
                        for col in hist.columns]

        return hist

    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()


def fetch_commodity_price(commodity_name: str, start_date: Optional[str] = None,
                         end_date: Optional[str] = None, period: Optional[str] = None,
                         prefer_futures: bool = True, try_etf_fallback: bool = True) -> pd.DataFrame:
    """
    Fetch historical prices for a commodity by name.

    Args:
        commodity_name: Commodity name from COT data
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)
        period: Alternative to dates: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
        prefer_futures: If True, try futures ticker first
        try_etf_fallback: If True, try ETF ticker if futures fails

    Returns:
        DataFrame with historical prices, or empty DataFrame if commodity not found
    """
    # Normalize commodity name
    normalized_name = normalize_commodity_name(commodity_name)

    # Get ticker
    ticker = get_ticker_for_commodity(normalized_name, prefer_futures=prefer_futures)

    if not ticker:
        print(f"No ticker mapping found for commodity: {commodity_name}")
        return pd.DataFrame()

    # Try fetching with preferred ticker
    df = fetch_historical_prices(ticker, start_date, end_date, period)

    # If failed and we should try ETF fallback
    if df.empty and try_etf_fallback:
        from commodity_ticker_mapping import get_all_tickers_for_commodity
        all_tickers = get_all_tickers_for_commodity(normalized_name)
        if all_tickers:
            etf_ticker = all_tickers.get('etf')
            if etf_ticker and etf_ticker != ticker:
                print(f"  Trying ETF ticker {etf_ticker} as fallback...")
                df = fetch_historical_prices(etf_ticker, start_date, end_date, period)

    return df


def fetch_multiple_commodities(commodity_names: List[str], start_date: Optional[str] = None,
                              end_date: Optional[str] = None, period: Optional[str] = None,
                              delay: float = 0.5) -> Dict[str, pd.DataFrame]:
    """
    Fetch historical prices for multiple commodities.

    Args:
        commodity_names: List of commodity names
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)
        period: Alternative to dates: '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
        delay: Delay between requests in seconds (to avoid rate limiting)

    Returns:
        Dictionary mapping commodity names to DataFrames with historical prices
    """
    results = {}

    for commodity_name in commodity_names:
        print(f"Fetching prices for: {commodity_name}")
        df = fetch_commodity_price(commodity_name, start_date, end_date, period)

        if not df.empty:
            results[commodity_name] = df
            print(f"  ✓ Successfully fetched {len(df)} days of data")
        else:
            print(f"  ✗ No data found")

        # Add delay to avoid rate limiting
        if delay > 0:
            time.sleep(delay)

    return results


def fetch_all_available_commodities(commodity_list: List[str], start_date: Optional[str] = None,
                                    end_date: Optional[str] = None, period: Optional[str] = None,
                                    delay: float = 0.5) -> Dict[str, pd.DataFrame]:
    """
    Fetch prices for all commodities that have ticker mappings.
    Only fetches commodities that can be mapped to Yahoo Finance tickers.

    Args:
        commodity_list: List of all commodity names to check
        start_date: Start date in 'YYYY-MM-DD' format (optional)
        end_date: End date in 'YYYY-MM-DD' format (optional)
        period: Alternative to dates
        delay: Delay between requests in seconds

    Returns:
        Dictionary mapping commodity names to DataFrames with historical prices
    """
    from commodity_ticker_mapping import get_ticker_for_commodity, normalize_commodity_name

    # Filter to only commodities that have ticker mappings
    mapped_commodities = []
    for commodity in commodity_list:
        normalized = normalize_commodity_name(commodity)
        ticker = get_ticker_for_commodity(normalized)
        if ticker:
            mapped_commodities.append(commodity)

    print(f"Found {len(mapped_commodities)} commodities with ticker mappings out of {len(commodity_list)} total")

    return fetch_multiple_commodities(mapped_commodities, start_date, end_date, period, delay)


def save_prices_to_database(prices_dict: Dict[str, pd.DataFrame], db_path: str = 'commodities.db'):
    """
    Save fetched prices to SQLite database.

    Args:
        prices_dict: Dictionary mapping commodity names to price DataFrames
        db_path: Path to SQLite database
    """
    import sqlite3

    conn = sqlite3.connect(db_path)

    for commodity_name, df in prices_dict.items():
        if df.empty:
            continue

        # Add commodity name column
        df['Commodity_Name'] = commodity_name

        # Ensure DATE column exists
        if 'DATE' not in df.columns:
            if 'Date' in df.columns:
                df.rename(columns={'Date': 'DATE'}, inplace=True)

        # Save to database (create table if it doesn't exist)
        table_name = 'commodity_prices'
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Saved {len(df)} records for {commodity_name} to {table_name}")

    # Create index for better query performance
    conn.execute('''
        CREATE INDEX IF NOT EXISTS idx_commodity_price_date
        ON commodity_prices(Commodity_Name, DATE)
    ''')

    conn.close()
    print(f"All prices saved to {db_path}")


def get_commodity_prices_from_db(commodity_name: Optional[str] = None,
                                 db_path: str = 'commodities.db') -> pd.DataFrame:
    """
    Retrieve commodity prices from database.

    Args:
        commodity_name: Specific commodity name (optional, if None returns all)
        db_path: Path to SQLite database

    Returns:
        DataFrame with price data
    """
    import sqlite3

    conn = sqlite3.connect(db_path)

    # Check if table exists
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='commodity_prices'
    """)
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        conn.close()
        return pd.DataFrame()

    if commodity_name:
        query = "SELECT * FROM commodity_prices WHERE Commodity_Name = ? ORDER BY DATE"
        df = pd.read_sql_query(query, conn, params=(commodity_name,))
    else:
        query = "SELECT * FROM commodity_prices ORDER BY Commodity_Name, DATE"
        df = pd.read_sql_query(query, conn)

    conn.close()

    if not df.empty and 'DATE' in df.columns:
        df['DATE'] = pd.to_datetime(df['DATE'])

    return df


if __name__ == '__main__':
    # Example usage
    print("Testing Yahoo Finance price fetching...")

    # Test single commodity
    print("\n1. Testing single commodity fetch:")
    gold_prices = fetch_commodity_price('GOLD', period='1mo')
    if not gold_prices.empty:
        print(f"Gold prices fetched: {len(gold_prices)} days")
        print(gold_prices.head())

    # Test multiple commodities
    print("\n2. Testing multiple commodities:")
    commodities = ['GOLD', 'SILVER', 'CRUDE OIL', 'NATURAL GAS']
    prices = fetch_multiple_commodities(commodities, period='1mo')
    print(f"\nSuccessfully fetched prices for {len(prices)} commodities")
