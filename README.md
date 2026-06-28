# Goomti Restaurant — Data Analytics Portfolio

Five end-to-end data projects built on real sales data from an Indian restaurant. The data came from the restaurant's Flipdish POS system and covers about 30 days of trading across dine-in, Uber Eats, Deliveroo, Just Eat, and web ordering.

The goal was simple: take raw exports from a real business and build something actually useful — not a cleaned-up Kaggle dataset with a known answer, but messy real-world data with missing fields, grand total rows baked in, and cold takeaway items logged at £0 skewing the menu analysis.

---

## The Projects

### Project 1 — Power BI Sales Dashboard
An interactive 4-page business review covering revenue, channel performance, menu highlights and customer retention. Built in Power BI Desktop with DAX measures, a star schema data model, and a documented data cleaning step for the outlier removal.

The HTML version is hosted here and opens in any browser — no Power BI needed.

**Key finding:** 87% of online customers never placed a second order. A re-engagement campaign targeting just 10% of dormant customers would generate ~£487/month at zero acquisition cost.

### Project 2 — Menu Engineering & Revenue Analysis
A full EDA on 112 dine-in menu items using the Boston Matrix framework. Items classified as Stars, Plowhorses, Puzzles and Dogs based on revenue vs volume. Outliers handled two ways: business logic removal (cold takeaway items with £0 revenue) and IQR statistical detection — with a documented decision to *keep* the IQR outliers because they turned out to be the best-performing dishes.

**Key finding:** Grand Maharaja Thali generates £1,039 from just 14 covers — 19% of all dine-in revenue at £74.24 average price. The top 37% of menu items generate 80% of revenue, which is weaker than the classic 80/20 rule and suggests the menu is too broad.

### Project 3 — RFM Segmentation with K-Means
Day-level RFM scoring (Recency, Frequency, Monetary) on 25 trading days, clustered into 4 segments using K-Means. Optimal k chosen using the Elbow method and Silhouette score (k=4, score=0.371). Features scaled with StandardScaler before clustering.

**Segments found:** Peak Days (Fri/Sat/Sun, £1,271 avg), Good Days, Average Days, Quiet Days — with tailored staffing and marketing strategies per segment.

### Project 4 — Revenue Forecasting
Time series decomposition to extract trend, seasonality and residual components from daily revenue. ADF stationarity test applied (p=0.133, non-stationary). ARIMA attempted but ruled out due to insufficient data points (25 days vs 50+ needed) — this decision is documented. Weighted Moving Average with day-of-week seasonality used instead, achieving a MAPE of 26.1%.

**7-day forecast:** £4,528 forecast for 23–29 June 2026, with confidence intervals and a staffing recommendation (weekends need 2.5x more cover than midweek).

### Project 5 — Multi-Channel Pricing Model + Streamlit App
Multiple linear regression to identify revenue drivers. Data leakage caught and documented (Delivery + Dine-in revenue summed to Net Sales, causing R²=1.0). Fixed model achieved R²=-0.38 — correctly flagged as unreliable with 25 data points and documented as a limitation. Price elasticity analysis and platform fee impact modelling completed as more appropriate alternatives.

**Key finding:** £2,511/month lost to platform fees (13.3% of total revenue). Uber Eats alone costs £1,404. Weekend average order value (£58.23) is 77% higher than weekday (£32.84).

Live Streamlit app with sidebar filters, interactive charts and a pricing recommendations table.

---

## Data Notes

All data came from Flipdish POS exports. A few things worth knowing:

- Cold Takeaway Food items (1,103 units, £0 revenue) were removed from menu analysis — they're pre-packaged cold items logged in the system but contributing nothing to revenue
- A grand total row was baked into one of the exports, which caused all KPI measures to double until caught and removed
- Customer data covers online/delivery only — walk-in dine-in customers without accounts aren't captured
- COGS is £0 throughout — not populated in the source system

---

## Stack

Python · Pandas · Scikit-learn · Matplotlib · Seaborn · Statsmodels · Streamlit · Power BI · DAX

---

## Files

```
├── Project_1_PowerBI/
│   ├── Goomti_Dashboard.html          ← open in any browser
│   ├── fact_sales_overview.csv
│   ├── fact_daily_sales.csv
│   ├── fact_hourly_sales.csv
│   ├── dim_menu_items.csv
│   ├── dim_categories.csv
│   └── dim_channels.csv
├── Project_2_Menu_Engineering/
│   ├── Goomti_Menu_Engineering.ipynb
│   ├── pareto_chart.png
│   ├── menu_quadrant.png
│   ├── category_performance.png
│   └── price_efficiency.png
├── Project_3_RFM_Segmentation/
│   ├── Goomti_RFM_Segmentation.ipynb
│   ├── elbow_method.png
│   └── rfm_clusters.png
├── Project_4_Revenue_Forecasting/
│   ├── Goomti_Revenue_Forecasting.ipynb
│   ├── time_series_overview.png
│   ├── decomposition.png
│   └── revenue_forecast.png
└── Project_5_Pricing_Model/
    ├── Goomti_Pricing_Model.ipynb
    ├── goomti_app.py
    └── pricing_analysis.png
```
