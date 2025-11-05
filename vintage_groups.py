"""
Vintage commodity groups mapping.

This file contains mappings of commodity groups that share the same base name
but have different vintage specifications (e.g., V2024, V2025, etc.).

Vintage groups are organized by exchange to avoid mixing contracts from different
exchanges that represent the same underlying commodity.

Each group maps to a base name, exchange, and lists all commodity names that belong to that group.
"""

# Exchange-specific vintage groups
# Structure: (base_name, exchange) -> group data
VINTAGE_GROUPS = {
    # California Carbon Allowance - Exchange 1 (e.g., ICE)
    ('CALIF CARBON ALLOWANCE', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'CALIF CARBON ALLOWANCE',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'CALIF CARBON ALLOWANCE V2022',
            'CALIF CARBON ALLOWANCE V2023',
            'CALIF CARBON ALLOWANCE V2024',
            'CALIF CARBON ALLOWANCE V2025',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'California Carbon Allowance with vintage years'
    },

    # California Carbon Allowance - Exchange 2 (e.g., CME)
    ('CALIF CARBON ALLOWANCE', 'CHICAGO MERCANTILE EXCHANGE'): {
        'base_name': 'CALIF CARBON ALLOWANCE',
        'exchange': 'CHICAGO MERCANTILE EXCHANGE',
        'commodities': [
            'CALIF CARBON ALLOWANCE V2022',
            'CALIF CARBON ALLOWANCE V2023',
            'CALIF CARBON ALLOWANCE V2024',
            'CALIF CARBON ALLOWANCE V2025',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'California Carbon Allowance with vintage years'
    },

    # California Carbon All
    ('CALIF CARBON ALL', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'CALIF CARBON ALL',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'CALIF CARBON ALL VINTAGE 2025',
            'CALIF CARBON ALL VINTAGE 2026',
        ],
        'vintage_pattern': 'VINTAGE {YYYY}',
        'description': 'California Carbon All vintage series'
    },

    # California Carbon (various formats, excluding CURRENT AUCTION)
    ('CALIF CARBON', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'CALIF CARBON',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'CALIF CARBON 21',
            'CALIF CARBON 22',
            'CALIF CARBON 23',
            'CALIF CARBON ALL VINTAGE 2025',
            'CALIF CARBON ALL VINTAGE 2026',
            'CALIF CARBON ALLOWANCE V2022',
            'CALIF CARBON ALLOWANCE V2023',
            'CALIF CARBON ALLOWANCE V2024',
            'CALIF CARBON ALLOWANCE V2025',
            'CALIF CARBON VINTAGE 2021',
            'CALIF CARBON VINTAGE SPEC 2028',
            # Note: CALIF CARBON CURRENT AUCTION is excluded - it's a contract of its own
        ],
        'vintage_pattern': 'Mixed (V{YYYY}, {YY}, VINTAGE {YYYY})',
        'description': 'California Carbon - various vintage formats'
    },

    # RGGI - ICE Exchange
    ('RGGI', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'RGGI',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'RGGI VINTAGE 2021',
            'RGGI V2022-ICE',
            'RGGI VINTAGE 2022',
            'RGGI V2023',
            'RGGI V2024',
            'RGGI V2025',
            'RGGI V2026',
        ],
        'vintage_pattern': 'V{YYYY} or VINTAGE {YYYY}',
        'description': 'Regional Greenhouse Gas Initiative credits'
    },

    # New Jersey RECs Class 2
    ('NEW JERSEY RECs CLASS 2', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'NEW JERSEY RECs CLASS 2',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'NEW JERSEY RECs CLASS 2 V2025',
            'NEW JERSEY RECs CLASS 2 V2026',
            'NEW JERSEY RECs CLASS 2 V2027',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'New Jersey Renewable Energy Certificates Class 2'
    },

    # Pennsylvania AEC Tier 2
    ('PENNSYLVANIA AEC TIER 2', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'PENNSYLVANIA AEC TIER 2',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'PENNSYLVANIA AEC TIER 2-V2024',
            'PENNSYLVANIA AEC TIER 2-V2025',
            'PENNSYLVANIA AEC TIER 2-V2026',
            'PENNSYLVANIA AEC TIER 2-V2027',
            'PENNSYLVANIA AEC TIER 2-V2028',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'Pennsylvania Alternative Energy Credit Tier 2'
    },

    # PJM Tri-Q RECs Class 1
    ('PJM TRI-Q RECs CLASS 1', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'PJM TRI-Q RECs CLASS 1',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'PJM TRI-Q RECs CLASS 1 V2022',
            'PJM TRI-Q RECs CLASS 1 V2023',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'PJM Tri-Qualified Renewable Energy Certificates Class 1'
    },

    # Texas Green-E REC
    ('TX GREEN-E REC', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'TX GREEN-E REC',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'TX GREEN-E REC V22 BACK HALF',
            'TX GREEN-E REC V22 FRONT HALF',
            'TX GREEN-E REC V23 BACK HALF',
            'TX GREEN-E REC V23 FRONT HALF',
            'TX GREEN-E REC V24 BACK HALF',
            'TX GREEN-E REC V24 FRONT HALF',
            'TX GREEN-E REC V25 BACK HALF',
            'TX GREEN-E REC V25 FRONT HALF',
        ],
        'vintage_pattern': 'V{YY} {HALF}',
        'description': 'Texas Green-E Renewable Energy Certificates with vintage and half-year'
    },

    # Texas REC CRS
    ('TX REC CRS', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'TX REC CRS',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'TX REC CRS V26 BACK HALF',
            'TX REC CRS V26 FRONT HALF',
            'TX REC CRS V27 BACK HALF',
            'TX REC CRS V27 FRONT HALF',
            'TX REC CRS V28 BACK HALF',
            'TX REC CRS V28 FRONT HALF',
            'TX REC CRS V29 BACK HALF',
            'TX REC CRS V29 FRONT HALF',
            'TX REC CRS V30 BACK HALF',
            'TX REC CRS V30 FRONT HALF',
        ],
        'vintage_pattern': 'V{YY} {HALF}',
        'description': 'Texas Renewable Energy Credit CRS with vintage and half-year'
    },

    # Washington Carbon
    ('WASHINGTON CARBON', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'WASHINGTON CARBON',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'WASHINGTON CARBON V2023',
            'WASHINGTON CARBON V2024',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'Washington Carbon Allowance'
    },

    # Washington Carbon All
    ('WASHINGTON CARBON ALL', 'ICE FUTURES ENERGY DIV'): {
        'base_name': 'WASHINGTON CARBON ALL',
        'exchange': 'ICE FUTURES ENERGY DIV',
        'commodities': [
            'WASHINGTON CARBON ALL V2024',
            'WASHINGTON CARBON ALL V2025',
        ],
        'vintage_pattern': 'V{YYYY}',
        'description': 'Washington Carbon All vintage series'
    },
}

# Cross-exchange commodity mapping
# Maps base commodity names to their equivalent commodities on different exchanges
# This allows users to view combined data across exchanges or filter by specific exchange
CROSS_EXCHANGE_COMMODITIES = {
    'CALIF CARBON ALLOWANCE': {
        'exchanges': [
            'ICE FUTURES ENERGY DIV',
            'CHICAGO MERCANTILE EXCHANGE',
        ],
        'description': 'California Carbon Allowance traded on multiple exchanges',
        'base_commodity': 'CALIF CARBON ALLOWANCE'
    },
    # Add more cross-exchange commodities as needed
    # Example:
    # 'RGGI': {
    #     'exchanges': ['ICE FUTURES ENERGY DIV', 'OTHER EXCHANGE'],
    #     'description': 'RGGI traded on multiple exchanges',
    #     'base_commodity': 'RGGI'
    # },
}

# Reverse mapping: (commodity_name, exchange) -> group key
COMMODITY_EXCHANGE_TO_GROUP = {}

for group_key, group_data in VINTAGE_GROUPS.items():
    base_name, exchange = group_key
    for commodity in group_data['commodities']:
        # Store mapping with exchange
        COMMODITY_EXCHANGE_TO_GROUP[(commodity, exchange)] = group_key


def get_vintage_group(commodity_name, exchange=None):
    """
    Get the vintage group key for a given commodity name and exchange.

    Args:
        commodity_name: The full commodity name
        exchange: Optional exchange name. If provided, returns exchange-specific group.
                  If not provided, returns first matching group (may be ambiguous).

    Returns:
        Group key (base_name, exchange) if found, None otherwise
    """
    if exchange:
        return COMMODITY_EXCHANGE_TO_GROUP.get((commodity_name, exchange))
    else:
        # Without exchange, return first match (for backward compatibility)
        # This may be ambiguous if commodity trades on multiple exchanges
        for (comm, exch), group_key in COMMODITY_EXCHANGE_TO_GROUP.items():
            if comm == commodity_name:
                return group_key
    return None


def is_vintage_commodity(commodity_name, exchange=None):
    """
    Check if a commodity belongs to a vintage group.

    Args:
        commodity_name: The full commodity name
        exchange: Optional exchange name for more precise matching

    Returns:
        True if commodity is in a vintage group, False otherwise
    """
    if exchange:
        return (commodity_name, exchange) in COMMODITY_EXCHANGE_TO_GROUP
    else:
        # Check if commodity exists in any exchange
        return any(
            comm == commodity_name for comm, _ in COMMODITY_EXCHANGE_TO_GROUP.keys()
        )


def get_group_commodities(group_key):
    """
    Get all commodities in a vintage group.

    Args:
        group_key: The vintage group key (base_name, exchange) tuple

    Returns:
        List of commodity names in the group, or empty list if group not found
    """
    if group_key in VINTAGE_GROUPS:
        return VINTAGE_GROUPS[group_key]['commodities']
    return []


def get_exchanges_for_commodity(base_commodity_name):
    """
    Get all exchanges where a base commodity is traded.

    Args:
        base_commodity_name: The base commodity name (e.g., 'CALIF CARBON ALLOWANCE')

    Returns:
        List of exchange names where this commodity is traded
    """
    exchanges = set()
    for (base_name, exchange), _ in VINTAGE_GROUPS.items():
        if base_name == base_commodity_name:
            exchanges.add(exchange)
    return sorted(list(exchanges))


def get_cross_exchange_commodities(base_commodity_name):
    """
    Get cross-exchange mapping information for a commodity.

    Args:
        base_commodity_name: The base commodity name

    Returns:
        Dictionary with exchange information if commodity trades on multiple exchanges,
        None otherwise
    """
    return CROSS_EXCHANGE_COMMODITIES.get(base_commodity_name)


def extract_vintage_year(commodity_name):
    """
    Extract vintage year from commodity name.

    Args:
        commodity_name: The full commodity name

    Returns:
        Vintage year as string (e.g., '2024'), or None if not found
    """
    import re

    # Try patterns in order of specificity
    patterns = [
        (r'V(\d{4})', 4),  # V2024
        (r'VINTAGE\s+(\d{4})', 4),  # VINTAGE 2024
        (r'V(\d{2})\s+', 2),  # V22 or V23 followed by space (for BACK/FRONT HALF)
        (r'V(\d{2})$', 2),  # V22 or V23 at end
        (r'\b(\d{4})\b', 4),  # 2024 (standalone 4-digit)
        (r'\b(\d{2})\b', 2),  # 22 or 23 (standalone 2-digit, like CALIF CARBON 21)
    ]

    for pattern, digits in patterns:
        match = re.search(pattern, commodity_name, re.IGNORECASE)
        if match:
            year = match.group(1)
            # Convert 2-digit to 4-digit if needed
            if digits == 2:
                year_int = int(year)
                if year_int >= 20 and year_int <= 99:  # Assume 2000s for years 20-99
                    return f'20{year}'
                elif year_int < 20:  # Years 00-19 assume 2000s
                    return f'20{year:02d}'
            return year

    return None


if __name__ == '__main__':
    # Print summary
    print(f"Total vintage groups: {len(VINTAGE_GROUPS)}")
    print(f"Total unique commodities in vintage groups: {len(COMMODITY_EXCHANGE_TO_GROUP)}")
    print(f"Total cross-exchange commodities: {len(CROSS_EXCHANGE_COMMODITIES)}")
    print("\n" + "="*80)
    print("VINTAGE GROUPS SUMMARY (by exchange):")
    print("="*80)

    for group_key, group_data in sorted(VINTAGE_GROUPS.items()):
        base_name, exchange = group_key
        print(f"\n{base_name} - {exchange}:")
        print(f"  Description: {group_data['description']}")
        print(f"  Pattern: {group_data['vintage_pattern']}")
        print(f"  Commodities ({len(group_data['commodities'])}):")
        for comm in group_data['commodities']:
            vintage = extract_vintage_year(comm)
            print(f"    - {comm} (vintage: {vintage})")

    print("\n" + "="*80)
    print("CROSS-EXCHANGE COMMODITIES:")
    print("="*80)
    for base_comm, cross_info in sorted(CROSS_EXCHANGE_COMMODITIES.items()):
        print(f"\n{base_comm}:")
        print(f"  Exchanges: {', '.join(cross_info['exchanges'])}")
        print(f"  Description: {cross_info['description']}")
