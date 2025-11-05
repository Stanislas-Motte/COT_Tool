import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from column_mapping import COLUMN_MAPPING, get_short_name, get_description, get_column_mapping_df
from fetch_prices import fetch_commodity_price, get_commodity_prices_from_db
from commodity_price_mapping import get_price_mapping

# Page config
st.set_page_config(page_title="Commodities COT Data", layout="wide")

# Compatibility: Use cache_data if available, otherwise use cache
if hasattr(st, 'cache_data'):
    cache_data = st.cache_data
else:
    # Fallback for older Streamlit versions
    cache_data = st.cache

# Database path
DB_PATH = 'commodities.db'

# Load available commodities with types and OI stats
@cache_data
def get_commodities_with_stats():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        Commodity_Name,
        Exchange_Name,
        CFTC_Commodity_Code,
        Commodity_Type,
        MIN(Open_Interest_All) as Min_OI,
        MAX(Open_Interest_All) as Max_OI,
        AVG(Open_Interest_All) as Avg_OI
    FROM cot_data
    GROUP BY Commodity_Name, Exchange_Name, CFTC_Commodity_Code, Commodity_Type
    ORDER BY Commodity_Name
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Get unique commodity types
@cache_data
def get_commodity_types():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT DISTINCT Commodity_Type FROM cot_data ORDER BY Commodity_Type"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['Commodity_Type'].tolist()

# Get commodities with price mapping info
@cache_data
def get_commodities_with_price_info():
    """
    Get commodities with information about whether they have price mappings.
    """
    commodities_df = get_commodities_with_stats().copy()

    # Get all commodities that have price mappings
    from commodity_price_mapping import get_all_mappings
    mappings_df = get_all_mappings(DB_PATH)

    # Create a set of commodities with price mappings
    commodities_with_prices = set(mappings_df['commodity_name'].unique()) if not mappings_df.empty else set()

    # Add column indicating if price mapping exists
    commodities_df['Has_Price_Data'] = commodities_df['Commodity_Name'].isin(commodities_with_prices)

    return commodities_df

# Load data for selected commodity
@cache_data
def load_commodity_data(commodity_name, date_range=None):
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT * FROM cot_data
    WHERE Commodity_Name = ?
    """
    params = [commodity_name]

    if date_range:
        query += " AND As_of_Date_In_Form_YYMMDD BETWEEN ? AND ?"
        params.extend(date_range)

    query += " ORDER BY As_of_Date_In_Form_YYMMDD"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    # Convert date column if it's not already datetime
    if 'As_of_Date_In_Form_YYMMDD' in df.columns:
        df['As_of_Date_In_Form_YYMMDD'] = pd.to_datetime(df['As_of_Date_In_Form_YYMMDD'], errors='coerce')

    return df

# Main app
st.title("📊 Commodities COT Data Visualization")

# Create tabs
tab1, tab2 = st.tabs(["📈 Visualization", "📋 Column Reference"])

# Initialize price mappings in the background
from commodity_price_mapping import init_price_mapping_db
init_price_mapping_db(DB_PATH)

# Column Reference Tab
with tab2:
    st.header("Column Reference Guide")
    st.markdown("""
    This table shows the mapping between technical column names and their user-friendly short names,
    along with descriptions of what each column represents.
    """)

    mapping_df = get_column_mapping_df()
    st.dataframe(mapping_df)

    st.markdown("""
    ### Key Terms:
    - **Producer/Merchant**: Commercial traders who use futures markets to hedge their business activities
    - **Swap Dealer**: Entities that deal in swaps and use futures markets to hedge swap transactions
    - **Money Manager**: Managed money traders including commodity trading advisors, commodity pool operators, and hedge funds
    - **Other Reportable**: Other large traders who don't fit into the above categories
    - **Non-Reportable**: Smaller traders whose positions are below reporting thresholds
    - **Open Interest**: Total number of outstanding contracts
    """)

# Visualization Tab
with tab1:
    # Sidebar for filters
    st.sidebar.header("Filters")

    # Get commodities with stats
    commodities_df = get_commodities_with_stats().copy()

    # Commodity Type Filter
    commodity_types = get_commodity_types()
    selected_types = st.sidebar.multiselect(
        "Commodity Type",
        options=commodity_types,
        default=[]  # Empty means show all
    )

    # Price Data Filter
    st.sidebar.subheader("Price Data Filter")
    price_filter = st.sidebar.selectbox(
        "Price Data Availability",
        options=["All", "With Price Data", "Without Price Data"],
        index=0,
        help="Filter commodities based on whether price data is available"
    )

    # Open Interest Filter
    st.sidebar.subheader("Open Interest Filter")
    oi_min = st.sidebar.number_input(
        "Min Open Interest",
        min_value=0,
        value=0,
        step=1000
    )
    oi_max_value = int(commodities_df['Max_OI'].max()) if len(commodities_df) > 0 and 'Max_OI' in commodities_df.columns else 10000000
    oi_max = st.sidebar.number_input(
        "Max Open Interest",
        min_value=0,
        value=oi_max_value,
        step=10000
    )

    # Get commodities with price info
    commodities_with_price_info = get_commodities_with_price_info()

    # Filter commodities based on selected criteria
    filtered_commodities_df = commodities_with_price_info.copy()

    # Filter by price data availability
    if price_filter == "With Price Data":
        filtered_commodities_df = filtered_commodities_df[filtered_commodities_df['Has_Price_Data'] == True]
    elif price_filter == "Without Price Data":
        filtered_commodities_df = filtered_commodities_df[filtered_commodities_df['Has_Price_Data'] == False]

    # Filter by type
    if selected_types:
        filtered_commodities_df = filtered_commodities_df[
            filtered_commodities_df['Commodity_Type'].isin(selected_types)
        ]

    # Filter by Open Interest range
    filtered_commodities_df = filtered_commodities_df[
        (filtered_commodities_df['Max_OI'] >= oi_min) &
        (filtered_commodities_df['Max_OI'] <= oi_max)
    ]

    commodity_list = filtered_commodities_df['Commodity_Name'].unique().tolist()

    # Commodity selector (now filtered)
    if commodity_list:
        selected_commodity = st.sidebar.selectbox(
            "Select Commodity",
            options=commodity_list,
            index=0
        )
        st.sidebar.caption(f"{len(commodity_list)} commodities match filters")
    else:
        selected_commodity = None
        st.sidebar.warning("No commodities match the selected filters")

    if selected_commodity:
        # Load data
        data = load_commodity_data(selected_commodity).copy()

        if not data.empty:
            # Date range filter
            min_date = data['As_of_Date_In_Form_YYMMDD'].min()
            max_date = data['As_of_Date_In_Form_YYMMDD'].max()

            date_range = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            # Filter by date if range selected
            if isinstance(date_range, tuple) and len(date_range) == 2:
                filtered_data = data[
                    (data['As_of_Date_In_Form_YYMMDD'] >= pd.Timestamp(date_range[0])) &
                    (data['As_of_Date_In_Form_YYMMDD'] <= pd.Timestamp(date_range[1]))
                ].copy()
            else:
                filtered_data = data.copy()

            # Column selectors for dual axes
            numeric_columns = filtered_data.select_dtypes(include=['number']).columns.tolist()

            # Create mapping from short names to technical names for display
            short_to_technical = {}
            technical_to_short = {}
            for col in numeric_columns:
                short = get_short_name(col)
                short_to_technical[short] = col
                technical_to_short[col] = short


            st.sidebar.subheader("Left Y-Axis (Primary)")

            # Formula input for left axis
            left_formula = st.sidebar.text_input(
                "Formula (e.g., Prod/Merc Long + Prod/Merc Short)",
                key="left_formula",
                help="Use short column names with +, -, *, /, and parentheses. Example: (MM Long - MM Short) / Open Interest"
            )

            # Regular column selector for left axis (show short names)
            left_axis_options = {get_short_name(col): col for col in numeric_columns}
            left_axis_selected_short = st.sidebar.multiselect(
                "Or select columns for left axis",
                options=list(left_axis_options.keys()),
                default=[get_short_name('Open_Interest_All')] if 'Open_Interest_All' in numeric_columns else []
            )
            left_axis_columns = [left_axis_options[short] for short in left_axis_selected_short]

            st.sidebar.subheader("Right Y-Axis (Secondary)")

            # Formula input for right axis
            right_formula = st.sidebar.text_input(
                "Formula (e.g., % OI MM Long - % OI MM Short)",
                key="right_formula",
                help="Use short column names with +, -, *, /, and parentheses"
            )

            # Regular column selector for right axis (show short names)
            right_axis_options = {get_short_name(col): col for col in numeric_columns}
            right_axis_selected_short = st.sidebar.multiselect(
                "Or select columns for right axis",
                options=list(right_axis_options.keys()),
                default=[get_short_name('Pct_of_OI_M_Money_Long_All'), get_short_name('Pct_of_OI_M_Money_Short_All')]
                if all(col in numeric_columns for col in ['Pct_of_OI_M_Money_Long_All', 'Pct_of_OI_M_Money_Short_All']) else []
            )
            right_axis_columns = [right_axis_options[short] for short in right_axis_selected_short]

            # Get exchange name and type for this commodity
            exchange_info = filtered_commodities_df[filtered_commodities_df['Commodity_Name'] == selected_commodity]
            exchange_name = exchange_info['Exchange_Name'].iloc[0] if not exchange_info.empty else ''
            commodity_type = exchange_info['Commodity_Type'].iloc[0] if not exchange_info.empty else ''

            st.subheader(f"{selected_commodity}")
            if commodity_type:
                st.caption(f"Type: {commodity_type}")
            if exchange_name:
                st.caption(f"Exchange: {exchange_name}")
            st.caption(f"Data from {filtered_data['As_of_Date_In_Form_YYMMDD'].min().strftime('%Y-%m-%d')} to {filtered_data['As_of_Date_In_Form_YYMMDD'].max().strftime('%Y-%m-%d')}")

            # Function to convert short names to technical names in formulas
            def convert_short_names_to_technical(formula, short_to_technical_map):
                """Convert short names in formula to technical column names"""
                import re
                # Sort short names by length (longest first) to avoid partial matches
                sorted_short_names = sorted(short_to_technical_map.items(), key=lambda x: len(x[0]), reverse=True)

                converted_formula = formula
                # Replace short names with technical names, starting with longest matches first
                for short_name, technical_name in sorted_short_names:
                    # Use word boundaries but allow for special chars in short names like "/"
                    # Escape special regex characters in short_name
                    escaped_short = re.escape(short_name)
                    # Match whole word (allowing for / and spaces in column names)
                    pattern = r'\b' + escaped_short + r'\b'
                    converted_formula = re.sub(pattern, technical_name, converted_formula, flags=re.IGNORECASE)

                return converted_formula

            # Function to safely evaluate formulas
            def evaluate_formula(formula, data, short_to_technical_map):
                """Evaluate a formula safely and return (result, error) tuple"""
                if not formula or not formula.strip():
                    return None, None

                original_formula = formula.strip()

                # Convert short names to technical names
                formula = convert_short_names_to_technical(original_formula, short_to_technical_map)

                # Validate formula contains only allowed characters and column names
                # Allow division operator /, spaces, and alphanumeric with underscores
                allowed_chars = set('+-*/()[].,0123456789_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
                if not all(c in allowed_chars for c in formula):
                    return None, "Invalid characters in formula"

                # Extract potential column names (words with underscores)
                import re
                potential_columns = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', formula)

                # Check if all referenced columns exist
                missing_columns = [col for col in potential_columns if col not in data.columns]
                if missing_columns:
                    # Filter out common Python keywords and operators
                    actual_missing = [col for col in missing_columns if col not in ['min', 'max', 'sum', 'abs', 'round']]
                    if actual_missing:
                        return None, f"Columns not found: {', '.join(actual_missing)}"

                try:
                    # Use pandas eval for safe evaluation
                    # Replace any remaining spaces around operators for cleaner eval
                    formula = re.sub(r'\s*([+\-*/])\s*', r'\1', formula)
                    result = data.eval(formula)
                    return result, None
                except Exception as e:
                    return None, f"Formula error: {str(e)}. Make sure to use proper column names and operators (+, -, *, /)"

            # Evaluate formulas if provided
            left_formula_result = None
            right_formula_result = None
            left_formula_error = None
            right_formula_error = None

            if left_formula:
                result, error = evaluate_formula(left_formula, filtered_data, short_to_technical)
                if error:
                    left_formula_error = error
                else:
                    left_formula_result = result

            if right_formula:
                result, error = evaluate_formula(right_formula, filtered_data, short_to_technical)
                if error:
                    right_formula_error = error
                else:
                    right_formula_result = result

            # Plot with dual axes
            has_left_data = left_axis_columns or left_formula_result is not None
            has_right_data = right_axis_columns or right_formula_result is not None

            if has_left_data or has_right_data:
                fig = go.Figure()

                # Convert datetime to numpy array to avoid deprecation warnings
                date_values = np.array(filtered_data['As_of_Date_In_Form_YYMMDD'].values)

                # Add traces for left axis (formulas first, then regular columns)
                if left_formula_result is not None:
                    fig.add_trace(go.Scatter(
                        x=date_values,
                        y=left_formula_result,
                        mode='lines',
                        name=f"Formula: {left_formula}",
                        line=dict(width=2, color='#1f77b4'),
                        yaxis='y'
                    ))

                for col in left_axis_columns:
                    fig.add_trace(go.Scatter(
                        x=date_values,
                        y=filtered_data[col],
                        mode='lines',
                        name=get_short_name(col),
                        line=dict(width=2),
                        yaxis='y'
                    ))

                # Add traces for right axis (formulas first, then regular columns)
                if right_formula_result is not None:
                    fig.add_trace(go.Scatter(
                        x=date_values,
                        y=right_formula_result,
                        mode='lines',
                        name=f"Formula: {right_formula}",
                        line=dict(width=2, color='#ff7f0e'),
                        yaxis='y2'
                    ))

                for col in right_axis_columns:
                    fig.add_trace(go.Scatter(
                        x=date_values,
                        y=filtered_data[col],
                        mode='lines',
                        name=get_short_name(col),
                        line=dict(width=2),
                        yaxis='y2'
                    ))

                fig.update_layout(
                    xaxis=dict(
                        title="Date",
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(128, 128, 128, 0.2)'
                    ),
                    yaxis=dict(
                        title="Left Axis",
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(128, 128, 128, 0.2)',
                        side='left'
                    ),
                    yaxis2=dict(
                        title="Right Axis",
                        overlaying='y',
                        side='right',
                        showgrid=False
                    ),
                    hovermode='x unified',
                    height=700,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    margin=dict(l=60, r=60, t=20, b=60)
                )

                st.plotly_chart(fig, use_container_width=True)

                # Show formula errors if any
                if left_formula_error:
                    st.error(f"Left axis formula error: {left_formula_error}")
                if right_formula_error:
                    st.error(f"Right axis formula error: {right_formula_error}")
            else:
                st.info("Select columns or enter formulas in the sidebar to visualize")

            # Price data section - right after the main chart
            st.markdown("---")
            st.subheader("💰 Price Data")

            # Check if price mapping exists
            price_mapping = get_price_mapping(selected_commodity, DB_PATH)

            if price_mapping and price_mapping['ticker_symbol']:
                ticker = price_mapping['ticker_symbol']
                ticker_type = price_mapping['ticker_type']
                verified = price_mapping['verified']

                # Status indicator
                status_icon = "✅" if verified else "⚠️"
                st.caption(f"{status_icon} Ticker: {ticker} ({ticker_type})")

                # Try to get price data from database first
                price_data = get_commodity_prices_from_db(selected_commodity, DB_PATH)

                # If no price data in DB, try fetching
                if price_data.empty:
                    with st.spinner("Fetching price data..."):
                        try:
                            # Get date range from COT data
                            price_start = filtered_data['As_of_Date_In_Form_YYMMDD'].min()
                            price_end = filtered_data['As_of_Date_In_Form_YYMMDD'].max()

                            # Use the ticker we already have from the price mapping
                            from fetch_prices import fetch_historical_prices
                            price_data = fetch_historical_prices(
                                ticker,
                                start_date=price_start.strftime('%Y-%m-%d'),
                                end_date=price_end.strftime('%Y-%m-%d')
                            )

                            # Ensure DATE column exists (yfinance might return it as Date or Datetime)
                            if not price_data.empty:
                                if 'DATE' not in price_data.columns:
                                    # Try to find date column with different names
                                    for col in ['Date', 'Datetime', 'DATETIME']:
                                        if col in price_data.columns:
                                            price_data.rename(columns={col: 'DATE'}, inplace=True)
                                            break

                                # Ensure DATE is datetime type
                                if 'DATE' in price_data.columns:
                                    price_data['DATE'] = pd.to_datetime(price_data['DATE'], errors='coerce')

                                # Save to database if fetched
                                from fetch_prices import save_prices_to_database
                                save_prices_to_database({selected_commodity: price_data}, DB_PATH)
                        except Exception as e:
                            st.error(f"Could not fetch price data for ticker {ticker}: {str(e)}")

                if not price_data.empty:
                    # Filter price data to match COT date range
                    price_data_filtered = price_data[
                        (price_data['DATE'] >= pd.Timestamp(date_range[0])) &
                        (price_data['DATE'] <= pd.Timestamp(date_range[1]))
                    ] if isinstance(date_range, tuple) and len(date_range) == 2 else price_data

                    if not price_data_filtered.empty and 'CLOSE' in price_data_filtered.columns:
                        # Get date range from COT data for alignment
                        cot_date_min = filtered_data['As_of_Date_In_Form_YYMMDD'].min()
                        cot_date_max = filtered_data['As_of_Date_In_Form_YYMMDD'].max()

                        # Create price chart with aligned date range
                        price_fig = go.Figure()

                        # Convert datetime to numpy array to avoid deprecation warnings
                        price_date_values = np.array(price_data_filtered['DATE'].values)

                        price_fig.add_trace(go.Scatter(
                            x=price_date_values,
                            y=price_data_filtered['CLOSE'],
                            mode='lines',
                            name='Close Price',
                            line=dict(width=2, color='green'),
                            fill='tozeroy',
                            fillcolor='rgba(0, 255, 0, 0.1)'
                        ))

                        # Convert date range to Python datetime to avoid deprecation warnings
                        date_range_min = cot_date_min if isinstance(cot_date_min, pd.Timestamp) else pd.Timestamp(cot_date_min)
                        date_range_max = cot_date_max if isinstance(cot_date_max, pd.Timestamp) else pd.Timestamp(cot_date_max)

                        price_fig.update_layout(
                            title=f'{selected_commodity} Price Chart',
                            xaxis_title='Date',
                            yaxis_title='Price ($)',
                            height=400,
                            hovermode='x unified',
                            xaxis=dict(
                                range=[date_range_min, date_range_max],
                                showgrid=True,
                                gridwidth=1,
                                gridcolor='rgba(128, 128, 128, 0.2)'
                            )
                        )

                        st.plotly_chart(price_fig, use_container_width=True)

                        # Show price stats
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Latest Price", f"${price_data_filtered['CLOSE'].iloc[-1]:.2f}")
                        with col2:
                            st.metric("Min Price", f"${price_data_filtered['CLOSE'].min():.2f}")
                        with col3:
                            st.metric("Max Price", f"${price_data_filtered['CLOSE'].max():.2f}")
                        with col4:
                            price_change = price_data_filtered['CLOSE'].iloc[-1] - price_data_filtered['CLOSE'].iloc[0]
                            price_change_pct = (price_change / price_data_filtered['CLOSE'].iloc[0]) * 100
                            st.metric("Change", f"${price_change:.2f}", f"{price_change_pct:.1f}%")
                    else:
                        st.info("Price data available but no data for selected date range")
                else:
                    st.info("No price data available. The ticker may not be valid or Yahoo Finance API may be unavailable.")
            else:
                st.info("No price mapping found for this commodity. Price mappings are managed in the backend.")

            # Export button
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_commodity.replace(' ', '_')}_cot_data.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"No data available for {selected_commodity}")
    else:
        st.info("Select a commodity from the sidebar to begin")
