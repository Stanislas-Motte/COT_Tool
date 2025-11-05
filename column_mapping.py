"""
Column name mapping from technical names to user-friendly short names
"""

COLUMN_MAPPING = {
    # Identification
    'As_of_Date_In_Form_YYMMDD': {
        'short_name': 'Date',
        'description': 'Report date in YYMMDD format'
    },
    'Report_Date_as_MM_DD_YYYY': {
        'short_name': 'Report Date',
        'description': 'Report date in MM/DD/YYYY format'
    },
    'CFTC_Contract_Market_Code': {
        'short_name': 'Market Code',
        'description': 'CFTC contract market code'
    },
    'CFTC_Commodity_Code': {
        'short_name': 'Commodity Code',
        'description': 'CFTC commodity classification code'
    },
    'Contract_Units': {
        'short_name': 'Contract Units',
        'description': 'Number of units per contract'
    },

    # Core Position Data
    'Open_Interest_All': {
        'short_name': 'Open Interest',
        'description': 'Total open interest for all contracts'
    },

    # Producer/Merchant Positions
    'Prod_Merc_Positions_Long_ALL': {
        'short_name': 'Prod/Merc Long',
        'description': 'Producer/Merchant long positions (all contracts)'
    },
    'Prod_Merc_Positions_Short_ALL': {
        'short_name': 'Prod/Merc Short',
        'description': 'Producer/Merchant short positions (all contracts)'
    },

    # Swap Dealer Positions
    'Swap_Positions_Long_All': {
        'short_name': 'Swap Long',
        'description': 'Swap dealer long positions (all contracts)'
    },
    'Swap__Positions_Short_All': {
        'short_name': 'Swap Short',
        'description': 'Swap dealer short positions (all contracts)'
    },
    'Swap__Positions_Spread_All': {
        'short_name': 'Swap Spread',
        'description': 'Swap dealer spread positions (all contracts)'
    },

    # Money Manager Positions
    'M_Money_Positions_Long_ALL': {
        'short_name': 'MM Long',
        'description': 'Money Manager (Managed Money) long positions (all contracts)'
    },
    'M_Money_Positions_Short_ALL': {
        'short_name': 'MM Short',
        'description': 'Money Manager (Managed Money) short positions (all contracts)'
    },
    'M_Money_Positions_Spread_ALL': {
        'short_name': 'MM Spread',
        'description': 'Money Manager spread positions (all contracts)'
    },

    # Other Reportable Positions
    'Other_Rept_Positions_Long_ALL': {
        'short_name': 'Other Rept Long',
        'description': 'Other reportable long positions (all contracts)'
    },
    'Other_Rept_Positions_Short_ALL': {
        'short_name': 'Other Rept Short',
        'description': 'Other reportable short positions (all contracts)'
    },
    'Other_Rept_Positions_Spread_ALL': {
        'short_name': 'Other Rept Spread',
        'description': 'Other reportable spread positions (all contracts)'
    },

    # Total Reportable Positions
    'Tot_Rept_Positions_Long_All': {
        'short_name': 'Total Rept Long',
        'description': 'Total reportable long positions (all contracts)'
    },
    'Tot_Rept_Positions_Short_All': {
        'short_name': 'Total Rept Short',
        'description': 'Total reportable short positions (all contracts)'
    },

    # Non-Reportable Positions
    'NonRept_Positions_Long_All': {
        'short_name': 'Non-Rept Long',
        'description': 'Non-reportable long positions (all contracts)'
    },
    'NonRept_Positions_Short_All': {
        'short_name': 'Non-Rept Short',
        'description': 'Non-reportable short positions (all contracts)'
    },

    # Percentages of Open Interest
    'Pct_of_OI_Prod_Merc_Long_All': {
        'short_name': '% OI Prod/Merc Long',
        'description': 'Producer/Merchant long positions as percentage of open interest'
    },
    'Pct_of_OI_Prod_Merc_Short_All': {
        'short_name': '% OI Prod/Merc Short',
        'description': 'Producer/Merchant short positions as percentage of open interest'
    },
    'Pct_of_OI_Swap_Long_All': {
        'short_name': '% OI Swap Long',
        'description': 'Swap dealer long positions as percentage of open interest'
    },
    'Pct_of_OI_Swap_Short_All': {
        'short_name': '% OI Swap Short',
        'description': 'Swap dealer short positions as percentage of open interest'
    },
    'Pct_of_OI_M_Money_Long_All': {
        'short_name': '% OI MM Long',
        'description': 'Money Manager long positions as percentage of open interest'
    },
    'Pct_of_OI_M_Money_Short_All': {
        'short_name': '% OI MM Short',
        'description': 'Money Manager short positions as percentage of open interest'
    },
    'Pct_of_OI_Tot_Rept_Long_All': {
        'short_name': '% OI Total Rept Long',
        'description': 'Total reportable long positions as percentage of open interest'
    },
    'Pct_of_OI_Tot_Rept_Short_All': {
        'short_name': '% OI Total Rept Short',
        'description': 'Total reportable short positions as percentage of open interest'
    },
}

def get_short_name(column_name):
    """Get short name for a column, or return the original if not mapped"""
    return COLUMN_MAPPING.get(column_name, {}).get('short_name', column_name)

def get_description(column_name):
    """Get description for a column"""
    return COLUMN_MAPPING.get(column_name, {}).get('description', 'No description available')

def get_column_mapping_df():
    """Get a DataFrame with all column mappings"""
    import pandas as pd
    mapping_data = []
    for col_name, info in COLUMN_MAPPING.items():
        mapping_data.append({
            'Column Name': col_name,
            'Short Name': info['short_name'],
            'Description': info['description']
        })
    return pd.DataFrame(mapping_data)
