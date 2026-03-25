# 💰 AI Expense Analyzer

An AI-powered tool that automatically categorizes your bank statement transactions and visualizes your spending habits.

## Features

- 📤 Upload CSV bank statements
- 🤖 Auto-categorization using keyword matching
- 🥧 Pie chart - spending distribution
- 📊 Bar chart - monthly spending trends
- 🚀 Deployed and ready to use

## Demo

Try the live app: https://expense-analyzer-cyhwkhy4czftfjivq7vgeb.streamlit.app/

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/expense-analyzer.git
cd expense-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## Usage

1. Export your bank statement as CSV
2. Upload it to the app
3. View automatic categorization and charts

## CSV Format

Your CSV should have these columns:
- Date
- Description
- Amount (negative for expenses, positive for income)

## Tech Stack

- **Python** - Programming language
- **Streamlit** - Web framework
- **Pandas** - Data processing
- **Plotly** - Data visualization

## Contributing

Feel free to fork this project and submit pull requests!

## License

MIT
