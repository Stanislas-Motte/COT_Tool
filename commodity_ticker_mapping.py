"""
Commodity name to Yahoo Finance ticker mapping.

This module maps commodity names from the COT data to Yahoo Finance ticker symbols.
Many commodities have multiple contracts (different months/years), so this mapping
provides the base ticker symbol which can be used to fetch the front month contract
or specific contract months.
"""

# Mapping from commodity name (as it appears in COT data) to Yahoo Finance ticker
# Format: 'COMMODITY NAME': ('FUTURES_TICKER', 'ETF_TICKER')
# Futures tickers use format like 'GC=F' for Gold futures
# ETF tickers are alternatives (e.g., 'GLD' for Gold ETF)
# Both options are provided, with futures preferred but ETF as fallback
COMMODITY_TICKER_MAPPING = {
    # Metals - (Futures, ETF)
    'GOLD': ('GC=F', 'GLD'),  # Gold Futures / Gold ETF
    'SILVER': ('SI=F', 'SLV'),  # Silver Futures / Silver ETF
    'COPPER': ('HG=F', 'CPER'),  # Copper Futures / Copper ETF
    'PLATINUM': ('PL=F', 'PPLT'),  # Platinum Futures / Platinum ETF
    'PALLADIUM': ('PA=F', 'PALL'),  # Palladium Futures / Palladium ETF

    # Energy - Crude Oil
    'CRUDE OIL, LIGHT SWEET': ('CL=F', 'USO'),  # WTI Crude Futures / Oil ETF
    'CRUDE OIL': ('CL=F', 'USO'),
    'WTI': ('CL=F', 'USO'),
    'BRENT CRUDE': ('BZ=F', 'BNO'),  # Brent Futures / Brent Oil ETF
    'BRENT': ('BZ=F', 'BNO'),

    # Energy - Products
    'GASOLINE': ('RB=F', 'UGA'),  # RBOB Gasoline Futures / Gasoline ETF
    'RBOB GASOLINE': ('RB=F', 'UGA'),
    'HEATING OIL': ('HO=F', 'UHN'),  # Heating Oil Futures / Heating Oil ETF
    'NATURAL GAS': ('NG=F', 'UNG'),  # Natural Gas Futures / Natural Gas ETF
    'NAT GAS': ('NG=F', 'UNG'),

    # Agricultural - Grains
    'CORN': ('ZC=F', 'CORN'),  # Corn Futures / Corn ETF
    'WHEAT': ('ZW=F', 'WEAT'),  # Wheat Futures / Wheat ETF
    'SOYBEANS': ('ZS=F', 'SOYB'),  # Soybean Futures / Soybean ETF
    'SOYBEAN OIL': ('ZL=F', None),  # Soybean Oil Futures
    'SOYBEAN MEAL': ('ZM=F', None),  # Soybean Meal Futures
    'OATS': ('ZO=F', None),
    'ROUGH RICE': ('ZR=F', None),
    'RICE': ('ZR=F', None),

    # Agricultural - Softs
    'COFFEE': ('KC=F', 'JO'),  # Coffee Futures / Coffee ETF
    'SUGAR': ('SB=F', 'CANE'),  # Sugar Futures / Sugar ETF
    'COTTON': ('CT=F', 'BAL'),  # Cotton Futures / Cotton ETF
    'ORANGE JUICE': ('OJ=F', None),
    'COCOA': ('CC=F', 'NIB'),  # Cocoa Futures / Cocoa ETF

    # Livestock
    'LIVE CATTLE': ('LE=F', 'COW'),  # Live Cattle Futures / Livestock ETF
    'CATTLE': ('LE=F', 'COW'),
    'FEEDER CATTLE': ('GF=F', None),
    'FEEDER': ('GF=F', None),
    'LEAN HOGS': ('HE=F', None),
    'HOGS': ('HE=F', None),

    # Dairy
    'MILK': ('DC=F', None),  # Class III Milk Futures
    'CHEESE': ('DA=F', None),
    'BUTTER': ('DB=F', None),

    # Other
    'LUMBER': ('LBS=F', None),
    'RANDOM LENGTH LUMBER': ('LBS=F', None),
}

# Alternative mappings for variations in commodity names
# This helps match commodity names that might have slight variations
COMMODITY_NAME_VARIANTS = {
    'CRUDE OIL, LIGHT SWEET': ['CRUDE OIL', 'WTI CRUDE', 'LIGHT SWEET CRUDE'],
    'GASOLINE': ['RBOB GASOLINE', 'GASOLINE RBOB'],
    'NATURAL GAS': ['NAT GAS', 'HENRY HUB', 'NATURAL GAS FINANCIAL'],
    'LIVE CATTLE': ['CATTLE', 'LIVE CATTLE FINANCIAL'],
    'FEEDER CATTLE': ['FEEDER', 'FEEDER CATTLE FINANCIAL'],
    'LEAN HOGS': ['HOGS', 'LEAN HOGS FINANCIAL'],
    'MILK': ['MILK, CLASS III', 'MILK CLASS III'],
    'CORN': ['CORN FINANCIAL'],
    'WHEAT': ['WHEAT FINANCIAL'],
    'SOYBEANS': ['SOYBEANS FINANCIAL'],
}


def get_ticker_for_commodity(commodity_name, prefer_futures=True):
    """
    Get Yahoo Finance ticker for a commodity name.

    Args:
        commodity_name: The commodity name from COT data
        prefer_futures: If True, prefer futures ticker; if False, prefer ETF ticker

    Returns:
        Yahoo Finance ticker symbol (e.g., 'GC=F') or None if not found
        Returns tuple of (futures_ticker, etf_ticker) if both available
    """
    # Try exact match first
    name_upper = commodity_name.upper()
    if name_upper in COMMODITY_TICKER_MAPPING:
        tickers = COMMODITY_TICKER_MAPPING[name_upper]
        if isinstance(tickers, tuple):
            futures_ticker, etf_ticker = tickers
            if prefer_futures and futures_ticker:
                return futures_ticker
            elif etf_ticker:
                return etf_ticker
            elif futures_ticker:
                return futures_ticker
            return None
        else:
            # Legacy format (string)
            return tickers

    # Try partial matching for common patterns
    for key, tickers in COMMODITY_TICKER_MAPPING.items():
        if key in name_upper:
            if isinstance(tickers, tuple):
                futures_ticker, etf_ticker = tickers
                if prefer_futures and futures_ticker:
                    return futures_ticker
                elif etf_ticker:
                    return etf_ticker
                elif futures_ticker:
                    return futures_ticker
            else:
                return tickers

    # Try variant matching
    for base_name, variants in COMMODITY_NAME_VARIANTS.items():
        if name_upper in variants or any(variant in name_upper for variant in variants):
            tickers = COMMODITY_TICKER_MAPPING.get(base_name)
            if tickers:
                if isinstance(tickers, tuple):
                    futures_ticker, etf_ticker = tickers
                    if prefer_futures and futures_ticker:
                        return futures_ticker
                    elif etf_ticker:
                        return etf_ticker
                    elif futures_ticker:
                        return futures_ticker
                else:
                    return tickers

    return None


def get_all_tickers_for_commodity(commodity_name):
    """
    Get all available tickers (futures and ETF) for a commodity.

    Args:
        commodity_name: The commodity name from COT data

    Returns:
        Dictionary with 'futures' and 'etf' keys, or None if not found
    """
    name_upper = commodity_name.upper()

    # Try exact match
    if name_upper in COMMODITY_TICKER_MAPPING:
        tickers = COMMODITY_TICKER_MAPPING[name_upper]
        if isinstance(tickers, tuple):
            return {'futures': tickers[0], 'etf': tickers[1]}
        else:
            return {'futures': tickers, 'etf': None}

    # Try partial matching
    for key, tickers in COMMODITY_TICKER_MAPPING.items():
        if key in name_upper:
            if isinstance(tickers, tuple):
                return {'futures': tickers[0], 'etf': tickers[1]}
            else:
                return {'futures': tickers, 'etf': None}

    return None


def normalize_commodity_name(commodity_name):
    """
    Normalize commodity name to improve matching.

    Args:
        commodity_name: Raw commodity name

    Returns:
        Normalized commodity name
    """
    name = commodity_name.upper().strip()

    # Remove common suffixes that don't affect ticker lookup
    suffixes_to_remove = [
        ' FINANCIAL',
        ' - FINANCIAL',
        ' - ICE',
        ' - CME',
        ' - NYMEX',
        ' - COMEX',
    ]

    for suffix in suffixes_to_remove:
        if name.endswith(suffix):
            name = name[:-len(suffix)]

    return name.strip()


def get_all_mapped_commodities():
    """
    Get list of all commodity names that have ticker mappings.

    Returns:
        List of commodity names
    """
    return list(COMMODITY_TICKER_MAPPING.keys())
