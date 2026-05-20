import streamlit as st
import pandas as pd

# ======================
# CONFIGURATION
# ======================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOAD DATA (avec cache)
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("../data/cleaned_superstore.csv")

    # Normalisation GLOBALE : supprime espaces + Title Case
    # "order date" -> "Order Date", "region" -> "Region", etc.
    df.columns = df.columns.str.strip().str.title()

    # Détection flexible de la colonne date
    date_col_candidates = [c for c in df.columns if "Date" in c and "Order" in c]
    if not date_col_candidates:
        st.error(f"❌ Aucune colonne 'Order Date' trouvée. Colonnes disponibles : {list(df.columns)}")
        st.stop()

    date_col = date_col_candidates[0]
    if date_col != "Order Date":
        df = df.rename(columns={date_col: "Order Date"})

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")

    # Renommage des colonnes avec underscores vers les noms attendus
    df = df.rename(columns={
        "Order_Id": "Order ID",
        "Product_Name": "Product Name",
    })

    return df

df = load_data()

# Vérification des colonnes requises
required_cols = {"Region", "Category", "Sales", "Profit", "Order ID", "Order Date", "Product Name"}
missing = required_cols - set(df.columns)
if missing:
    st.error(f"❌ Colonnes manquantes dans le CSV : {missing}\n\nColonnes trouvées : {list(df.columns)}")
    st.stop()

st.title("📊 Sales Analytics Dashboard")

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ======================
# GESTION FILTRE VIDE
# ======================
if filtered_df.empty:
    st.warning("⚠️ Aucune donnée pour les filtres sélectionnés. Veuillez ajuster vos critères.")
    st.stop()

# ======================
# KPIs
# ======================
st.subheader("Key Metrics")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = filtered_df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Total Orders", f"{total_orders:,}")

st.divider()

# ======================
# SALES OVER TIME (mensuel)
# ======================
st.subheader("📈 Sales Over Time (Monthly)")

sales_time = (
    filtered_df
    .resample("ME", on="Order Date")["Sales"]
    .sum()
    .reset_index()
    .rename(columns={"Order Date": "Month"})
    .set_index("Month")
)

st.line_chart(sales_time)

st.divider()

# ======================
# TOP PRODUCTS & REGION
# ======================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏆 Top 10 Products by Sales")
    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_products)

with col_right:
    st.subheader("🌍 Sales by Region")
    region_sales = filtered_df.groupby("Region")["Sales"].sum()
    st.bar_chart(region_sales)

st.divider()

# ======================
# PROFIT PAR CATEGORIE
# ======================
st.subheader("💰 Profit by Category")

profit_category = (
    filtered_df.groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

st.dataframe(
    profit_category.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
    use_container_width=True,
    hide_index=True
)

# ======================
# RAW DATA (optionnel)
# ======================
with st.expander("🔍 Voir les données brutes"):
    st.dataframe(filtered_df, use_container_width=True)
    st.caption(f"{len(filtered_df):,} lignes affichées")