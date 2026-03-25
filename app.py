import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expense Analyzer", page_icon="💰")

st.title("💰 AI Expense Analyzer")

st.sidebar.title("⚙️ Settings")
show_income = st.sidebar.toggle("Show Income", value=True)

uploaded_file = st.file_uploader("Upload your bank statement (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    def categorize(description):
        desc = str(description).lower()

        if any(word in desc for word in ["salary", "payroll", "deposit", "transfer", "refund", "dividend", "interest earned"]):
            return "Income"

        if any(word in desc for word in ["uber", "lyft", "taxi", "gas", "fuel", "shell", "parking"]):
            return "Transportation"

        if any(word in desc for word in ["grocery", "whole foods", "trader joe", "safeway", "kroger", "walmart", "target"]):
            return "Groceries"

        if any(word in desc for word in ["restaurant", "cafe", "coffee", "starbucks", "mcdonald", "doordash", "uber eats"]):
            return "Food & Dining"

        if any(word in desc for word in ["rent", "mortgage", "utility", "electric", "water", "internet"]):
            return "Housing"
        if any(word in desc for word in ["amazon", "clothing", "shoes", "apple", "electronics"]):
            return "Shopping"

        if any(word in desc for word in ["netflix", "spotify", "movie", "game", "entertainment"]):
            return "Entertainment"

        if any(word in desc for word in ["pharmacy", "doctor", "hospital", "medical", "dental"]):
            return "Healthcare"

        return "Other"

    df["Category"] = df["Description"].apply(categorize)

    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    income = df[df["Amount"] > 0].copy()
    expenses = df[df["Amount"] < 0].copy()
    expenses["Amount"] = expenses["Amount"].abs()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💳 Expenses", "💰 Income", "📤 Export"])

    with tab1:
        st.write("### Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Income", f"${income['Amount'].sum():.2f}")
        with col2:
            st.metric("Total Expenses", f"${expenses['Amount'].sum():.2f}")
        with col3:
            savings = income['Amount'].sum() - expenses['Amount'].sum()
            savings_rate = (savings / income['Amount'].sum() * 100) if income['Amount'].sum() > 0 else 0
            st.metric("Savings Rate", f"{savings_rate:.1f}%")

        st.write("### Spending Distribution")
        if not expenses.empty:
            fig = px.pie(expenses, values="Amount", names="Category",
                        title="Where your money goes")
            st.plotly_chart(fig, use_container_width=True)

        st.write("### Monthly Trend")
        if not expenses.empty:
            expenses["Date"] = pd.to_datetime(expenses["Date"], errors="coerce")
            expenses["Month"] = expenses["Date"].dt.to_period("M").astype(str)
            monthly = expenses.groupby("Month")["Amount"].sum().reset_index()
            fig2 = px.bar(monthly, x="Month", y="Amount", title="Monthly Spending",
                         color_discrete_sequence=["#FF4B4B"])
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.write("### Expense Breakdown")
        if not expenses.empty:
            cat_sum = expenses.groupby("Category")["Amount"].sum().reset_index()
            cat_sum = cat_sum.sort_values("Amount", ascending=False)
            fig3 = px.bar(cat_sum, x="Category", y="Amount", title="Expenses by Category",
                         color_discrete_sequence=["#FF4B4B"])
            st.plotly_chart(fig3, use_container_width=True)

            st.write("### Categorized Transactions")
            st.dataframe(expenses[["Date", "Description", "Category", "Amount"]], use_container_width=True)

    with tab3:
        st.write("### Income Breakdown")
        if not income.empty:
            income["Date"] = pd.to_datetime(income["Date"], errors="coerce")
            income["Month"] = income["Date"].dt.to_period("M").astype(str)
            monthly_income = income.groupby("Month")["Amount"].sum().reset_index()

            fig4 = px.bar(monthly_income, x="Month", y="Amount", title="Monthly Income",
                         color_discrete_sequence=["#00CC96"])
            st.plotly_chart(fig4, use_container_width=True)

            st.write("### Income Sources")
            income_by_source = income.groupby("Category")["Amount"].sum().reset_index()
            st.dataframe(income_by_source, use_container_width=True)
        else:
            st.write("No income detected in your statements.")

    with tab4:
        st.write("### Export Data")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Categorized Data (CSV)",
            data=csv,
            file_name="categorized_expenses.csv",
            mime="text/csv"
        )

        st.write("---")
        st.write("### Receipt Upload (Coming Soon)")
        st.info("Upload images of receipts and AI will extract the data! (Feature in development)")

else:
    st.info("👆 Upload a CSV file to get started!")
    st.write("### Sample CSV Format")
    sample_data = pd.DataFrame({
        "Date": ["2024-01-15", "2024-01-16", "2024-01-17", "2024-01-18"],
        "Description": ["Uber", "Whole Foods", "Salary", "Netflix"],
        "Amount": [-15.50, -85.20, 3000.00, -15.99]
    })
    st.dataframe(sample_data)

st.sidebar.write("---")
st.sidebar.write("### Add Custom Category")
new_category = st.sidebar.text_input("Category name")
new_keywords = st.sidebar.text_input("Keywords (comma separated)")
if st.sidebar.button("Add Category") and new_category and new_keywords:
    st.sidebar.success(f"Added: {new_category}")
