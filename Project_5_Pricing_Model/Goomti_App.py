# ── Goomti Restaurant — Streamlit Dashboard ──
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── Page config ──
st.set_page_config(
    page_title="Goomti Restaurant Analytics",
    page_icon="🍛",
    layout="wide"
)

# ── Load data ──
@st.cache_data
def load_data():
    df_overview = pd.read_csv('fact_sales_overview.csv')
    df_menu = pd.read_csv('dim_menu_items.csv')
    df_channels = pd.read_csv('dim_channels.csv')
    df_categories = pd.read_csv('dim_categories.csv')
    df_overview['Date'] = pd.to_datetime(df_overview['Date'])
    df_overview = df_overview.dropna(subset=['Date'])
    df_overview['Orders'] = pd.to_numeric(
        df_overview['Orders'].astype(str).str.replace(',',''),
        errors='coerce')
    df_overview['AOV'] = (df_overview['Net_Sales'] /
                          df_overview['Orders'].replace(0,1)).round(2)
    return df_overview, df_menu, df_channels, df_categories

df_overview, df_menu, df_channels, df_categories = load_data()

# ── Header ──
st.title("🍛 Goomti Restaurant — Sales Analytics")
st.markdown("**Interactive dashboard · May–June 2026 · "
            "All channels**")
st.divider()

# ── Sidebar filters ──
st.sidebar.title("🔧 Filters")
day_filter = st.sidebar.multiselect(
    "Filter by Day of Week",
    options=df_overview['Day_of_Week'].unique().tolist(),
    default=df_overview['Day_of_Week'].unique().tolist()
)

min_revenue = st.sidebar.slider(
    "Minimum daily revenue (£)",
    min_value=0,
    max_value=int(df_overview['Net_Sales'].max()),
    value=0,
    step=100
)

# Apply filters
df_filtered = df_overview[
    (df_overview['Day_of_Week'].isin(day_filter)) &
    (df_overview['Net_Sales'] >= min_revenue)
].copy()

# ── KPI Row ──
st.subheader("📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Net Sales",
              f"£{df_filtered['Net_Sales'].sum():,.0f}")
with col2:
    st.metric("Total Orders",
              f"{df_filtered['Orders'].sum():,.0f}")
with col3:
    st.metric("Avg Order Value",
              f"£{df_filtered['AOV'].mean():,.2f}")
with col4:
    weekend = df_filtered[
        df_filtered['Day_of_Week'].isin(
            ['Friday','Saturday','Sunday'])]['Net_Sales'].sum()
    st.metric("Weekend Revenue",
              f"£{weekend:,.0f}")
with col5:
    st.metric("Trading Days",
              f"{len(df_filtered)}")

st.divider()

# ── Page tabs ──
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "📡 Channels",
    "🍛 Menu",
    "💡 Insights"
])

# ── TAB 1: Overview ──
with tab1:
    st.subheader("Daily Revenue Trend")
    fig, ax = plt.subplots(figsize=(14, 5))
    df_sorted = df_filtered.sort_values('Date')
    ax.plot(df_sorted['Date'], df_sorted['Net_Sales'],
            color='#2563eb', linewidth=2,
            marker='o', markersize=4)
    ax.fill_between(df_sorted['Date'],
                    df_sorted['Net_Sales'],
                    alpha=0.1, color='#2563eb')
    rolling = df_sorted['Net_Sales'].rolling(
        window=7, min_periods=1).mean()
    ax.plot(df_sorted['Date'], rolling,
            color='#c9a96e', linewidth=2,
            linestyle='--', label='7-day avg')
    ax.set_ylabel('Net Sales (£)')
    ax.legend()
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Day of Week")
        dow_avg = df_filtered.groupby(
            'Day_of_Week')['Net_Sales'].mean()
        dow_order = ['Monday','Wednesday','Thursday',
                     'Friday','Saturday','Sunday']
        dow_avg = dow_avg.reindex(
            [d for d in dow_order if d in dow_avg.index])
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        colors = ['#dc2626' if d in
                  ['Friday','Saturday','Sunday']
                  else '#2563eb' for d in dow_avg.index]
        ax2.bar(range(len(dow_avg)), dow_avg.values,
                color=colors, edgecolor='white')
        ax2.set_xticks(range(len(dow_avg)))
        ax2.set_xticklabels(dow_avg.index, rotation=15)
        ax2.set_ylabel('Avg Revenue (£)')
        ax2.grid(True, alpha=0.2, axis='y')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    with col2:
        st.subheader("AOV by Day of Week")
        aov_dow = df_filtered.groupby(
            'Day_of_Week')['AOV'].mean()
        aov_dow = aov_dow.reindex(
            [d for d in dow_order if d in aov_dow.index])
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        ax3.bar(range(len(aov_dow)), aov_dow.values,
                color='#7c3aed', edgecolor='white')
        ax3.set_xticks(range(len(aov_dow)))
        ax3.set_xticklabels(aov_dow.index, rotation=15)
        ax3.set_ylabel('Avg Order Value (£)')
        ax3.grid(True, alpha=0.2, axis='y')
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

# ── TAB 2: Channels ──
with tab2:
    st.subheader("Revenue by Channel")
    col1, col2 = st.columns(2)

    with col1:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        ch_colors = ['#059669','#2563eb','#0891b2',
                     '#d97706','#7c3aed','#9ca3af']
        ax4.bar(range(len(df_channels)),
                df_channels['Net_Sales'],
                color=ch_colors, edgecolor='white')
        ax4.set_xticks(range(len(df_channels)))
        ax4.set_xticklabels(df_channels['Channel'],
                            rotation=15, fontsize=9)
        ax4.set_ylabel('Net Sales (£)')
        ax4.grid(True, alpha=0.2, axis='y')
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

    with col2:
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        ax5.pie(df_channels['Net_Sales'],
                labels=df_channels['Channel'],
                colors=ch_colors,
                autopct='%1.1f%%',
                startangle=90)
        plt.tight_layout()
        st.pyplot(fig5)
        plt.close()

    st.subheader("Platform Fee Impact")
    platform_fees = {
        'POS / Dine-in': 0.00, 'Uber Eats': 0.30,
        'Deliveroo': 0.30, 'Just Eat': 0.25,
        'Web': 0.05, 'Kiosk': 0.00
    }
    df_ch = df_channels.copy()
    df_ch['Fee_Pct'] = df_ch['Channel'].map(platform_fees)
    df_ch['Fee_Cost'] = (df_ch['Net_Sales'] *
                         df_ch['Fee_Pct']).round(2)
    df_ch['Net_After_Fees'] = (df_ch['Net_Sales'] -
                                df_ch['Fee_Cost']).round(2)
    st.dataframe(df_ch[['Channel','Net_Sales',
                         'Fee_Pct','Fee_Cost',
                         'Net_After_Fees']],
                 use_container_width=True)
    st.error(f"💸 Total platform fees: "
             f"£{df_ch['Fee_Cost'].sum():,.2f} "
             f"(13.3% of revenue)")

# ── TAB 3: Menu ──
with tab3:
    st.subheader("Menu Performance")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top 10 by Revenue**")
        top_rev = df_menu.nlargest(10, 'Net_Sales')
        fig6, ax6 = plt.subplots(figsize=(8, 6))
        ax6.barh(range(len(top_rev)),
                 top_rev['Net_Sales'],
                 color='#059669', edgecolor='white')
        ax6.set_yticks(range(len(top_rev)))
        ax6.set_yticklabels(top_rev['Item'], fontsize=9)
        ax6.invert_yaxis()
        ax6.set_xlabel('Net Sales (£)')
        ax6.grid(True, alpha=0.2, axis='x')
        plt.tight_layout()
        st.pyplot(fig6)
        plt.close()

    with col2:
        st.markdown("**Top 10 by Volume**")
        top_vol = df_menu.nlargest(10, 'Items_Sold')
        fig7, ax7 = plt.subplots(figsize=(8, 6))
        ax7.barh(range(len(top_vol)),
                 top_vol['Items_Sold'],
                 color='#2563eb', edgecolor='white')
        ax7.set_yticks(range(len(top_vol)))
        ax7.set_yticklabels(top_vol['Item'], fontsize=9)
        ax7.invert_yaxis()
        ax7.set_xlabel('Items Sold')
        ax7.grid(True, alpha=0.2, axis='x')
        plt.tight_layout()
        st.pyplot(fig7)
        plt.close()

    st.subheader("Full Menu Table")
    search = st.text_input("🔍 Search menu items")
    df_menu_display = df_menu.copy()
    if search:
        df_menu_display = df_menu_display[
            df_menu_display['Item'].str.contains(
                search, case=False, na=False)]
    st.dataframe(
        df_menu_display[['Item','Category',
                         'Items_Sold','Net_Sales',
                         'Avg_Price']].sort_values(
            'Net_Sales', ascending=False),
        use_container_width=True)

# ── TAB 4: Insights ──
with tab4:
    st.subheader("💡 Key Business Insights")

    st.success("⭐ **Grand Maharaja Thali** generates "
               "£1,039 from just 14 covers — "
               "19% of all dine-in revenue at £74.24 avg price.")

    st.error("⚠️ **Platform fees** cost £2,511/month — "
             "13.3% of total revenue. "
             "Uber Eats alone: £1,404.")

    st.warning("📉 **Retention crisis** — 87% of customers "
               "never return. Winning back 10% = "
               "+£487/month at zero acquisition cost.")

    st.info("📅 **Weekend effect** — Fri/Sat/Sun generates "
            "£12,889 (68% of revenue). "
            "Saturday avg £1,148/day vs £434 Wednesday.")

    st.divider()
    st.subheader("📋 Pricing Recommendations")

    data = {
        'Item/Category': [
            'Goomti Signatures',
            'Artisanal Breads',
            'Delivery → Web',
            'Tuesday Opening'
        ],
        'Current': [
            '£13.31 avg',
            '£3.13 avg',
            '£8,430 delivery',
            'Closed'
        ],
        'Recommendation': [
            'Increase to £16-18',
            'Increase to £3.75',
            'Push direct web orders',
            'Consider opening'
        ],
        'Est. Monthly Impact': [
            '+£39/month',
            '+£222/month',
            'Save £250 in fees',
            '+£2,000/month'
        ]
    }
    st.dataframe(pd.DataFrame(data),
                 use_container_width=True)

    st.divider()
    st.caption("Dashboard built by [Your Name] | "
               "Data Science Portfolio | June 2026 | "
               "Tools: Python, Pandas, Streamlit, "
               "Scikit-learn, Matplotlib")