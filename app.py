import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import pandas as pd
import joblib

# Set Page Configs for a wide dashboard layout
st.set_page_config(page_title="EcoForecast - Dashboard", layout="wide")
sns.set_theme(style='whitegrid')

# ==========================================
# PLACEHOLDERS FOR YOUR DATA LOADING
# Replace these with your actual data sources!
# ==========================================
@st.cache_data
def load_data():
    # 1. Load CSV files (setting the index column where appropriate)
    df_raw = pd.read_csv('raw_co2.csv', index_col=0)
    # Convert index to int (years) and reconstruct the dictionary of series
    df_raw.index = df_raw.index.astype(int)
    raw_co2 = {col: df_raw[col] for col in df_raw.columns}
    country_list = list(df_raw.columns)
    
    df_fwd_decouple = pd.read_csv('df_fwd_decouple.csv')
    df_league = pd.read_csv('df_league.csv')
    df_contrib = pd.read_csv('df_contrib.csv', index_col=0)
    
    # 2. Load the nested forecasts dictionary
    scenario_forecasts = joblib.load('scenario_forecasts.pkl')

    # 3. Define your analysis constants (adjust years if needed)
    TEST_END = 2022
    TRAIN_END = 2022
    
    DRIVER_LABELS = {
        'energy': 'Energy Intensity of GDP', 
        'gdp': 'GDP per Capita', 
        'pop': 'Population',
        'coal': 'Coal Share',
        'oil': 'Oil Share',
        'cement': 'Cement Activity'
    }
    
    CLR = {
        'energy': '#34495e', 
        'gdp': '#2980b9', 
        'pop': '#e67e22',
        'coal': '#7f8c8d',
        'oil': '#d35400',
        'cement': '#bdc3c7'
    }
    
    return country_list, raw_co2, TEST_END, TRAIN_END, scenario_forecasts, df_fwd_decouple, df_league, DRIVER_LABELS, df_contrib, CLR

# Unpack your actual Colab data structures
country_list, raw_co2, TEST_END, TRAIN_END, scenario_forecasts, df_fwd_decouple, df_league, DRIVER_LABELS, df_contrib, CLR = load_data()

# -- Colour constants ------------------------------------------
C_HIST     = '#2c3e50'

# -- Colour constants ------------------------------------------
C_HIST     = '#2c3e50'
C_B_BASE   = '#27ae60'
C_B_LOW    = '#3498db'
C_B_HIGH   = '#e74c3c'
C_A_BASE   = '#bdc3c7'
C_BAND     = '#27ae60'

STATUS_COLORS_DB = {
    'Absolute Decoupling': '#27ae60',
    'Relative Decoupling': '#2ecc71',
    'Weak Decoupling'    : '#f39c12',
    'Carbon-Locked'      : '#e74c3c',
    'Insufficient data'  : '#95a5a6',
}

# -- APP LAYOUT ------------------------------------------------
st.title("🌿EcoForecast  ASEAN CO2 2030 Interactive Dashboard")

# Create a clean configuration Sidebar instead of bulky grid boxes
st.sidebar.header("Dashboard Controls")

st.sidebar.subheader("Countries")
selected = []
for country in sorted(country_list):
    default_val = country in ['Malaysia', 'Indonesia', 'Vietnam']
    if st.sidebar.checkbox(country, value=default_val):
        selected.append(country)

scenario = st.sidebar.radio("Growth Scenario", options=['Low', 'Baseline', 'High'], index=1)

st.sidebar.subheader("Pathway Options")
show_b = st.sidebar.checkbox("Pathway B (recommended)", value=True)
show_a = st.sidebar.checkbox("Pathway A (ref only)", value=False)
show_bands = st.sidebar.checkbox("Show uncertainty bands", value=True)

yr_min, yr_max = st.sidebar.slider("Year Range", min_value=1990, max_value=2030, value=(2000, 2030))

# Tabs layout for main view
tab_choice = st.radio(
    "Select Analysis View", 
    options=['📈Forecast', '🔀Decoupling', '🏆League Table', '🔍Driver Attribution'],
    horizontal=True
)

# Guard rail clause
if not selected:
    st.warning("⚠️Select at least one country using the checkboxes in the sidebar.")
    st.stop()

# -- TAB 1: FORECAST -------------------------------------------
if tab_choice == '📈Forecast':
    n = len(selected)
    cols_count = min(n, 3)
    rows_count = int(np.ceil(n / cols_count))

    fig, axes = plt.subplots(rows_count, cols_count, figsize=(6 * cols_count, 4.5 * rows_count), squeeze=False)
    axes_flat = axes.flatten()

    for i, country in enumerate(selected):
        ax = axes_flat[i]
        hist = raw_co2[country]
        hist = hist[(hist.index >= yr_min) & (hist.index <= min(yr_max, TEST_END))]

        # Historical
        ax.plot(hist.index, hist.values, color=C_HIST, linewidth=2.5, label='Historical', zorder=5)

        # Pathway B
        if show_b:
            fc_b = scenario_forecasts['B'][scenario].get(country, pd.Series(dtype=float))
            fc_b = fc_b[fc_b.index <= yr_max]
            if not fc_b.empty:
                ax.plot(fc_b.index, fc_b.values, color=C_B_BASE, linewidth=2.2, linestyle='--', label=f'B {scenario}', zorder=4)

                if scenario == 'Baseline':
                    fc_b_low = scenario_forecasts['B']['Low'].get(country, pd.Series(dtype=float))
                    fc_b_low = fc_b_low[fc_b_low.index <= yr_max]
                    fc_b_high = scenario_forecasts['B']['High'].get(country, pd.Series(dtype=float))
                    fc_b_high = fc_b_high[fc_b_high.index <= yr_max]
                    
                    if not fc_b_low.empty:
                        ax.plot(fc_b_low.index, fc_b_low.values, color=C_B_LOW, linewidth=1.2, linestyle=':', label='B Low', zorder=3)
                    if not fc_b_high.empty:
                        ax.plot(fc_b_high.index, fc_b_high.values, color=C_B_HIGH, linewidth=1.2, linestyle=':', label='B High', zorder=3)

        # Pathway A
        if show_a:
            fc_a = scenario_forecasts['A'][scenario].get(country, pd.Series(dtype=float))
            fc_a = fc_a[fc_a.index <= yr_max]
            if not fc_a.empty:
                ax.plot(fc_a.index, fc_a.values, color=C_A_BASE, linewidth=1.2, linestyle=(0, (5, 2)), alpha=0.45, label='A (ref only)', zorder=2)

        ax.axvline(TRAIN_END, color='#bdc3c7', linestyle=':', linewidth=0.8)
        ax.set_title(country, fontweight='bold', fontsize=11)
        ax.set_ylabel('Mt CO2', fontsize=9)
        ax.set_xlim(yr_min, yr_max)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        if i == 0:
            ax.legend(fontsize=8, framealpha=0.8)

    for j in range(len(selected), len(axes_flat)):
        axes_flat[j].set_visible(False)

    plt.suptitle(f'CO2 Forecast  {scenario} Scenario', fontsize=14, fontweight='bold', y=1.01)
    plt.tight_layout()
    st.pyplot(fig)

    # Clean Streamlit Data Table alternative to command-line prints
    st.subheader("Summary Performance Data")
    summary_rows = []
    for country in selected:
        actual = raw_co2[country].get(2022, np.nan)
        fc30 = scenario_forecasts['B'][scenario].get(country, pd.Series(dtype=float)).get(2030, np.nan)
        growth = ((fc30 / actual) - 1) * 100 if actual > 0 and not np.isnan(fc30) else np.nan
        summary_rows.append({
            "Country": country,
            "2022 Actual (Mt)": round(actual, 2),
            "2030 Forecast B (Mt)": round(fc30, 2),
            "Growth %": f"{growth:+.1f}%" if not np.isnan(growth) else "N/A"
        })
    st.dataframe(pd.DataFrame(summary_rows), width='stretch')

# -- TAB 2: DECOUPLING -----------------------------------------
elif tab_choice == '🔀Decoupling':
    df_plot = df_fwd_decouple[df_fwd_decouple['Country'].isin(selected)].sort_values('Fwd_Gap_%pts')

    if df_plot.empty:
        st.warning("No decoupling data for selected countries.")
    else:
        fig, ax = plt.subplots(figsize=(11, max(4, len(df_plot) * 0.65)))
        colors = [STATUS_COLORS_DB.get(s, '#95a5a6') for s in df_plot['Forward_Status_2030']]
        bars = ax.barh(df_plot['Country'], df_plot['Fwd_Gap_%pts'], color=colors, edgecolor='white', linewidth=0.5)

        for bar, val in zip(bars, df_plot['Fwd_Gap_%pts']):
            x_pos = bar.get_width() + 0.05 if bar.get_width() >= 0 else bar.get_width() - 0.05
            ha = 'left' if bar.get_width() >= 0 else 'right'
            ax.text(x_pos, bar.get_y() + bar.get_height() / 2, f'{val:+.2f}%', va='center', ha=ha, fontsize=9)

        ax.axvline(0, color='black', linewidth=1.2)
        ax.set_xlabel('GDP CAGR - CO2 CAGR (% pts)', fontsize=10)
        ax.set_title('Forward Decoupling Index (20232030 Baseline)\nPositive = economy growing faster than emissions', fontweight='bold', fontsize=12)
        
        for status, color in STATUS_COLORS_DB.items():
            if status != 'Insufficient data':
                ax.barh([], [], color=color, label=status)
        ax.legend(fontsize=9, loc='lower right')
        sns.despine(ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.dataframe(df_plot, width='stretch')

# -- TAB 3: LEAGUE TABLE ---------------------------------------
elif tab_choice == '🏆League Table':
    df_lt = df_league[df_league['Country'].isin(selected)][[
        'Rank', 'Country', 'Actual_2022_Mt', 'B_Baseline_2030_Mt', 'B_Low_Mt', 'B_High_Mt', 'Growth_B_%', 'Fwd_Decoupling'
    ]].copy()

    if df_lt.empty:
        st.warning("No league table data for selected countries.")
    else:
        fig, ax = plt.subplots(figsize=(14, max(3, len(df_lt) * 0.6 + 1.2)))
        ax.axis('off')
        tbl = ax.table(cellText=df_lt.values, colLabels=['Rank', 'Country', '2022 Mt', 'B Base 2030', 'B Low', 'B High', 'Growth %', 'Fwd Status'], cellLoc='center', loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9)
        tbl.scale(1.2, 1.8)

        for col_idx in range(len(df_lt.columns)):
            tbl[0, col_idx].set_facecolor('#2c3e50')
            tbl[0, col_idx].set_text_props(color='white', fontweight='bold')

        st.pyplot(fig)
        st.dataframe(df_lt, width='stretch')

# -- TAB 4: DRIVER ATTRIBUTION ---------------------------------
elif tab_choice == '🔍Driver Attribution':
    driver_display_cols = [c for c in list(DRIVER_LABELS.values()) if c in df_contrib.columns]
    df_attr = df_contrib[df_contrib.index.isin(selected)][driver_display_cols].copy()

    if df_attr.empty:
        st.warning("No attribution data for selected countries.")
    else:
        driver_colors_list = [CLR.get(c.lower(), '#95a5a6') for c in driver_display_cols]
        fig, ax = plt.subplots(figsize=(13, max(4, len(df_attr) * 0.85)))
        bottom_pos = np.zeros(len(df_attr))
        bottom_neg = np.zeros(len(df_attr))
        pos = df_attr.clip(lower=0)
        neg = df_attr.clip(upper=0)

        for col, color in zip(driver_display_cols, driver_colors_list):
            ax.barh(df_attr.index, pos[col], left=bottom_pos, color=color, alpha=0.85, label=col, edgecolor='white', linewidth=0.4)
            bottom_pos += pos[col].values
            ax.barh(df_attr.index, neg[col], left=bottom_neg, color=color, alpha=0.85, edgecolor='white', linewidth=0.4)
            bottom_neg += neg[col].values

        ax.axvline(0, color='black', linewidth=1.2)
        ax.set_xlabel('Contribution to 2022?2030 CO2 growth (%)', fontsize=10)
        ax.set_title('Driver Attribution  What is pushing emissions toward 2030?', fontweight='bold', fontsize=12)
        ax.legend(fontsize=9, ncol=3, loc='lower right')
        sns.despine(ax=ax)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.dataframe(df_attr, width='stretch')