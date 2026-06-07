import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

# ------------------------
# Load Data
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/clean_supply_chain.csv")

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Shipment_Date"] = pd.to_datetime(df["Shipment_Date"])

    return df

df = load_data()

st.sidebar.header("Filters")

selected_warehouse = st.sidebar.multiselect(
    "Warehouse",
    options=df["Warehouse"].unique(),
    default=df["Warehouse"].unique()
)

selected_category = st.sidebar.multiselect(
    "Product Category",
    options=df["Product_Category"].unique(),
    default=df["Product_Category"].unique()
)

selected_priority = st.sidebar.multiselect(
    "Order Priority",
    options=df["Order_Priority"].unique(),
    default=df["Order_Priority"].unique()
)

df = df[
    (df["Warehouse"].isin(selected_warehouse))
    &
    (df["Product_Category"].isin(selected_category))
    &
    (df["Order_Priority"].isin(selected_priority))
]

# ------------------------
# Sidebar
# ------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Executive Overview",
        "Warehouse Analysis",
        "Supplier Analysis",
        "Inventory Analysis",
        "Demand & Fulfillment"
    ]
)

# ------------------------
# EXECUTIVE OVERVIEW
# ------------------------
if page == "Executive Overview":

    st.title("📦 Supply Chain Analytics Dashboard")

    total_orders = len(df)
    total_revenue = df["Revenue"].sum()
    avg_lead_time = df["Lead_Time"].mean()

    stockout_rate = (
        (df["Stockout_Flag"] > 0).mean() * 100
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col2.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

    col3.metric(
        "Avg Lead Time",
        f"{avg_lead_time:.2f} Days"
    )

    col4.metric(
        "Stockout Rate",
        f"{stockout_rate:.2f}%"
    )

    st.divider()

    category_rev = (
        df.groupby("Product_Category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_rev,
        x="Product_Category",
        y="Revenue",
        title="Revenue by Product Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    warehouse_rev = (
        df.groupby("Warehouse")["Revenue"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        warehouse_rev,
        x="Warehouse",
        y="Revenue",
        title="Revenue by Warehouse"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    monthly_rev = (
        df.groupby(
            df["Order_Date"].dt.to_period("M")
        )["Revenue"]
        .sum()
        .reset_index()
    )

    monthly_rev["Order_Date"] = (
        monthly_rev["Order_Date"]
        .astype(str)
    )

    fig3 = px.line(
        monthly_rev,
        x="Order_Date",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ------------------------
# WAREHOUSE ANALYSIS
# ------------------------
elif page == "Warehouse Analysis":

    st.title("🏭 Warehouse Analysis")

    warehouse_perf = (
        df.groupby("Warehouse")
        .agg(
            Orders=("Product_ID", "count"),
            Revenue=("Revenue", "sum"),
            Avg_Lead_Time=("Lead_Time", "mean"),
            Stockout_Rate=("Stockout_Flag", "mean"),
            Backorder_Rate=("Backorder_Flag", "mean")
        )
        .reset_index()
    )

    st.dataframe(warehouse_perf)

    fig = px.bar(
        warehouse_perf,
        x="Warehouse",
        y="Revenue",
        title="Revenue by Warehouse"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig2 = px.bar(
        warehouse_perf,
        x="Warehouse",
        y="Avg_Lead_Time",
        title="Average Lead Time by Warehouse"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    warehouse_perf["Stockout_Rate"] *= 100

    fig3 = px.bar(
        warehouse_perf,
        x="Warehouse",
        y="Stockout_Rate",
        title="Stockout Rate by Warehouse (%)"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ------------------------
# SUPPLIER ANALYSIS
# ------------------------
elif page == "Supplier Analysis":

    st.title("🚚 Supplier Analysis")

    supplier_perf = (
        df.groupby("Supplier_ID")
        .agg(
            Avg_Lead_Time=("Lead_Time", "mean"),
            Revenue=("Revenue", "sum")
        )
        .reset_index()
        .sort_values(
            by="Avg_Lead_Time",
            ascending=False
        )
    )

    st.subheader("Top 10 Slowest Suppliers")

    st.dataframe(
        supplier_perf.head(10)
    )

    fig = px.bar(
        supplier_perf.head(10),
        x="Supplier_ID",
        y="Avg_Lead_Time",
        title="Top 10 Slowest Suppliers"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Top 10 Fastest Suppliers")

    st.dataframe(
        supplier_perf.sort_values(
            "Avg_Lead_Time"
        ).head(10)
    )

# ------------------------
# INVENTORY ANALYSIS
# ------------------------
elif page == "Inventory Analysis":

    st.title("📊 Inventory Analysis")

    df['Inventory_Coverage'] = (
        df['Inventory_Level']/ df['Demand_Forecast']
    )
    inventory = (
        df.groupby("Product_Category")
        ["Inventory_Coverage"]
        .mean()
        .reset_index()
    )

    st.dataframe(inventory)

    fig = px.bar(
        inventory,
        x="Product_Category",
        y="Inventory_Coverage",
        title="Inventory Coverage by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    df['Demand_Gap'] = (
        df['Demand_Forecast']
        - df['Shipment_Quantity']
    )

    gap_analysis = (
        df.groupby("Product_Category")
        ["Demand_Gap"]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        gap_analysis,
        x="Product_Category",
        y="Demand_Gap",
        title="Average Demand Gap by Category"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ------------------------
# DEMAND & FULFILLMENT
# ------------------------
elif page == "Demand & Fulfillment":

    st.title("📈 Demand & Fulfillment Analysis")

    fulfillment = (
        df.groupby("Product_Category")
        .agg(
            Demand=("Demand_Forecast", "sum"),
            Shipped=("Shipment_Quantity", "sum")
        )
        .reset_index()
    )

    st.dataframe(fulfillment)

    fig = px.bar(
        fulfillment,
        x="Product_Category",
        y=["Demand", "Shipped"],
        barmode="group",
        title="Demand vs Shipment Quantity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


