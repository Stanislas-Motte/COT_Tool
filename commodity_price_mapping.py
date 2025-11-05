"""
Commodity to Price Data Mapping.

This module manages the mapping between COT commodity names and their corresponding
Yahoo Finance tickers/prices. The mappings are stored in a SQLite database for
persistence and can be checked/corrected.
"""

import sqlite3
import pandas as pd
from typing import Optional, Dict, List
from commodity_ticker_mapping import get_ticker_for_commodity, normalize_commodity_name, get_all_tickers_for_commodity


def init_price_mapping_db(db_path='commodities.db'):
    """
    Initialize the price mapping table in the database.

    Args:
        db_path: Path to SQLite database
    """
    conn = sqlite3.connect(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS commodity_price_mapping (
            commodity_name TEXT PRIMARY KEY,
            ticker_symbol TEXT,
            ticker_type TEXT,
            auto_mapped INTEGER DEFAULT 0,
            verified INTEGER DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.execute('''
        CREATE INDEX IF NOT EXISTS idx_price_mapping_ticker
        ON commodity_price_mapping(ticker_symbol)
    ''')

    conn.commit()
    conn.close()


def auto_map_commodities(db_path='commodities.db', overwrite_existing=False):
    """
    Automatically map commodities to tickers and save to database.

    Args:
        db_path: Path to SQLite database
        overwrite_existing: If True, overwrite existing mappings
    """
    init_price_mapping_db(db_path)

    # Get all unique commodities from COT data
    conn = sqlite3.connect(db_path)
    query = "SELECT DISTINCT Commodity_Name FROM cot_data ORDER BY Commodity_Name"
    commodities_df = pd.read_sql_query(query, conn)
    conn.close()

    all_commodities = commodities_df['Commodity_Name'].tolist()

    # Map each commodity
    mappings = []
    for commodity in all_commodities:
        normalized = normalize_commodity_name(commodity)
        ticker = get_ticker_for_commodity(normalized, prefer_futures=True)

        if ticker:
            # Determine ticker type
            ticker_type = 'futures' if '=F' in ticker else 'etf'

            mappings.append({
                'commodity_name': commodity,
                'ticker_symbol': ticker,
                'ticker_type': ticker_type,
                'auto_mapped': 1,
                'verified': 0
            })

    # Save to database
    conn = sqlite3.connect(db_path)
    for mapping in mappings:
        if overwrite_existing:
            conn.execute('''
                INSERT OR REPLACE INTO commodity_price_mapping
                (commodity_name, ticker_symbol, ticker_type, auto_mapped, verified, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                mapping['commodity_name'],
                mapping['ticker_symbol'],
                mapping['ticker_type'],
                mapping['auto_mapped'],
                mapping['verified']
            ))
        else:
            # Only insert if doesn't exist
            conn.execute('''
                INSERT OR IGNORE INTO commodity_price_mapping
                (commodity_name, ticker_symbol, ticker_type, auto_mapped, verified)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                mapping['commodity_name'],
                mapping['ticker_symbol'],
                mapping['ticker_type'],
                mapping['auto_mapped'],
                mapping['verified']
            ))

    conn.commit()
    conn.close()

    return len(mappings)


def get_price_mapping(commodity_name: str, db_path='commodities.db') -> Optional[Dict]:
    """
    Get price mapping for a commodity.

    Args:
        commodity_name: COT commodity name
        db_path: Path to SQLite database

    Returns:
        Dictionary with mapping info or None if not found
    """
    init_price_mapping_db(db_path)

    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM commodity_price_mapping WHERE commodity_name = ?"
    cursor = conn.execute(query, (commodity_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        columns = ['commodity_name', 'ticker_symbol', 'ticker_type', 'auto_mapped',
                  'verified', 'notes', 'created_at', 'updated_at']
        return dict(zip(columns, row))

    return None


def update_price_mapping(commodity_name: str, ticker_symbol: Optional[str] = None,
                         ticker_type: Optional[str] = None, verified: bool = False,
                         notes: Optional[str] = None, db_path='commodities.db'):
    """
    Update price mapping for a commodity.

    Args:
        commodity_name: COT commodity name
        ticker_symbol: Yahoo Finance ticker symbol (None to clear mapping)
        ticker_type: 'futures' or 'etf'
        verified: Whether the mapping has been verified
        notes: Optional notes about the mapping
        db_path: Path to SQLite database
    """
    init_price_mapping_db(db_path)

    conn = sqlite3.connect(db_path)

    if ticker_symbol is None:
        # Delete mapping
        conn.execute("DELETE FROM commodity_price_mapping WHERE commodity_name = ?",
                    (commodity_name,))
    else:
        # Update or insert
        conn.execute('''
            INSERT OR REPLACE INTO commodity_price_mapping
            (commodity_name, ticker_symbol, ticker_type, verified, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (commodity_name, ticker_symbol, ticker_type, 1 if verified else 0, notes))

    conn.commit()
    conn.close()


def get_all_mappings(db_path='commodities.db', verified_only=False) -> pd.DataFrame:
    """
    Get all price mappings.

    Args:
        db_path: Path to SQLite database
        verified_only: If True, only return verified mappings

    Returns:
        DataFrame with all mappings
    """
    init_price_mapping_db(db_path)

    conn = sqlite3.connect(db_path)

    if verified_only:
        query = "SELECT * FROM commodity_price_mapping WHERE verified = 1 ORDER BY commodity_name"
    else:
        query = "SELECT * FROM commodity_price_mapping ORDER BY commodity_name"

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def get_ticker_for_commodity_from_db(commodity_name: str, db_path='commodities.db') -> Optional[str]:
    """
    Get ticker symbol for a commodity from the database mapping.

    Args:
        commodity_name: COT commodity name
        db_path: Path to SQLite database

    Returns:
        Ticker symbol or None if not found
    """
    mapping = get_price_mapping(commodity_name, db_path)
    if mapping and mapping['ticker_symbol']:
        return mapping['ticker_symbol']
    return None


if __name__ == '__main__':
    # Initialize and auto-map
    print("Initializing price mapping database...")
    init_price_mapping_db()

    print("\nAuto-mapping commodities...")
    count = auto_map_commodities()
    print(f"✓ Mapped {count} commodities")

    # Show summary
    print("\n" + "="*60)
    print("Price Mapping Summary")
    print("="*60)
    mappings_df = get_all_mappings()

    if not mappings_df.empty:
        print(f"\nTotal mappings: {len(mappings_df)}")
        print(f"Verified: {mappings_df['verified'].sum()}")
        print(f"Auto-mapped: {mappings_df['auto_mapped'].sum()}")

        print("\nSample mappings:")
        print(mappings_df[['commodity_name', 'ticker_symbol', 'ticker_type', 'verified']].head(10))
    else:
        print("No mappings found")
