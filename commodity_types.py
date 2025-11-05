"""
Commodity type mapping based on commodity names
"""

def get_commodity_type(commodity_name):
    """Map commodity name to type category"""
    name_upper = commodity_name.upper()

    # Metals
    if any(keyword in name_upper for keyword in ['GOLD', 'SILVER', 'COPPER', 'ALUMINUM', 'ALUMINIUM',
                                                  'PLATINUM', 'PALLADIUM', 'COBALT', 'LITHIUM', 'STEEL',
                                                  'SCRAP', 'HRC', 'HOT-ROLL']):
        return 'Metals'

    # Energy - Crude Oil & Products
    if any(keyword in name_upper for keyword in ['CRUDE', 'WTI', 'BRENT', 'GASOLINE', 'HEATING OIL',
                                                  'ULSD', 'USLD', 'PROPANE', 'ETHANE', 'BUTANE',
                                                  'NAPHTHA', 'FUEL OIL', 'JET', 'MARINE FUEL',
                                                  'RBOB', 'GASOLINE', 'CBOB', 'CRACK', 'BALMO']):
        return 'Energy - Oil & Products'

    # Natural Gas
    if any(keyword in name_upper for keyword in ['NATURAL GAS', 'NAT GAS', 'HENRY HUB', 'BASIS',
                                                  'INDEX', 'CITYGATE', 'FINANCIAL', 'PENULTIMATE',
                                                  'LD1', 'ICE', 'NYME']):
        return 'Natural Gas'

    # Power & Emissions
    if any(keyword in name_upper for keyword in ['ERCOT', 'PJM', 'NYISO', 'CAISO', 'MISO', 'ISONE',
                                                  'CARBON', 'RGGI', 'REC', 'AEC', 'COMPLIANCE',
                                                  'EMISSIONS', 'OFFSET', 'VINTAGE', 'DA PEAK',
                                                  'DA OFF', 'RT PK', 'RT OFF', 'DAY-AHEAD',
                                                  'REAL-TIME', 'HUB', 'ZONE', 'MONTH_OFF',
                                                  'MONTH_ON', 'OFF_DAP', 'ON_DAP']):
        return 'Power & Emissions'

    # Agricultural - Grains
    if any(keyword in name_upper for keyword in ['CORN', 'WHEAT', 'SOYBEAN', 'CANOLA', 'OATS',
                                                  'RICE', 'ROUGH RICE']):
        return 'Agricultural - Grains'

    # Agricultural - Softs
    if any(keyword in name_upper for keyword in ['COFFEE', 'COCOA', 'SUGAR', 'COTTON', 'ORANGE JUICE',
                                                  'FRZN CONCENTRATED']):
        return 'Agricultural - Softs'

    # Livestock
    if any(keyword in name_upper for keyword in ['CATTLE', 'FEEDER', 'HOGS', 'LEAN HOGS']):
        return 'Livestock'

    # Dairy
    if any(keyword in name_upper for keyword in ['MILK', 'CHEESE', 'BUTTER', 'WHEY', 'DRY MILK']):
        return 'Dairy'

    # Other Industrial
    if any(keyword in name_upper for keyword in ['LUMBER', 'RANDOM LENGTH', 'UREA', 'PALM OIL']):
        return 'Other Industrial'

    # Default to Other
    return 'Other'
