import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("💰 Expense Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type="csv")

if uploaded_file is not None:
    # Read the CSV
    df = pd.read_csv(uploaded_file)

    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()

    # Show raw data
    st.write("### Raw Data")
    st.dataframe(df)

    # --- CATEGORIZATION LOGIC ---
    def categorize(description):
        desc = str(description).lower()

        # Transportation
        if any(word in desc for word in ["uber", "lyft", "taxi", "gas", "fuel", "parking"]):
            return "Transportation"

        # Groceries
        if any(word in desc for word in ["grocery", "whole foods", "trader joe", "safeway", "kroger", "walmart", "target"]):
            return "Groceries"

        # Food & Dining
        if any(word in desc for word in ["restaurant", "cafe", "coffee", "starbucks", "mcdonald", "doordash", "uber eats"]):
            return "Food & Dining"

        # Housing
        if any(word in desc for word in ["rent", "mortgage", "utility", "electric", "water", "internet"]):
            return "Housing"

        # Shopping
        if any(word in desc for word in ["amazon", "clothing", "shoes", "apple", "electronics"]):
            return "Shopping"

        # Entertainment
        if any(word in desc for word in ["netflix", "spotify", "movie", "game", "entertainment"]):
            return "Entertainment"

        return "Other"

    # Apply categorization
    df["Category"] = df["Description"].apply(categorize)

    st.write("### Categorized Data")
    st.dataframe(df)

    # --- VISUALIZATIONS ---
    st.write("### Spending by Category")

    # Filter for expenses only (negative amounts)
    expenses = df[df["Amount"] < 0].copy()
    expenses["Amount"] = expenses["Amount"].abs()  # Make positive for display

    if not expenses.empty:
        # Pie chart
        fig = px.pie(expenses, values="Amount", names="Category",
                     title="Spending Distribution")
        st.plotly_chart(fig)

        # Bar chart
        st.write("### Monthly Spending")
        expenses["Date"] = pd.to_datetime(expenses["Date"])
        expenses["Month"] = expenses["Date"].dt.to_period("M").astype(str)

        monthly = expenses.groupby("Month")["Amount"].sum().reset_index()
        fig2 = px.bar(monthly, x="Month", y="Amount", title="Monthly Trend")
        st.plotly_chart(fig2)

        # Summary
        st.write("### Summary")
        st.write(f"Total Spending: ${expenses['Amount'].sum():.2f}")
    else:
        st.write("No expenses found. Make sure your CSV has negative amounts for spending.")
