import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page layout configuration
st.set_page_config(page_title="TrueBalance | Loan Payment Simulator", page_icon="https://notion-emojis.s3-us-west-2.amazonaws.com/prod/svg-twitter/1f4b5.svg", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Croissant+One&family=Marcellus&display=swap');

    /* 1. Base App Structure & Dark Background */
    .stApp {
        background: #0f172a;
        color: #ffffff !important;
    }

    /* 2. Custom Typography Overrides */
    /* Croissant One for Title and App Name branding */
    .app-title, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        font-family: 'Croissant One', cursive !important;
        color: #ffffff !important;
    }
    
    /* Marcellus for all Header and Subheader tags */
    h1, h2, h3, h4, h5, h6, .subheader-text {
        font-family: 'Marcellus', serif !important;
        color: #ffffff !important;
    }

    /* 3. Enforce Strict White Text Everywhere */
    p, span, label, div, li, .stMarkdown, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }

    /* 4. Glassmorphism UI Components */
    div[data-testid="stMetric"], .stInfo, div[data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
    }

    /* Fix table cell text visibility inside dataframes */
    div[data-testid="stDataFrame"] td, div[data-testid="stDataFrame"] th {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Header utilizing the custom font class
st.markdown('<h1 class="app-title" style="font-size: 2.5rem; margin-bottom: 0;">Loan Payment Simulator</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="margin-top: 0; font-weight: 300;">Phase 2 Project | FinTech Roadmap</h3>', unsafe_allow_html=True)
st.write("A complete interactive loan amortization simulator built with Python, NumPy, Pandas and Matplotlib.")
st.write("---")

st.sidebar.markdown('<h2 style="font-size: 1.5rem;">Adjust Loan Parameters</h2>', unsafe_allow_html=True)

principal = st.sidebar.number_input(
    "Loan Amount (₹)", 
    min_value=1000.0, 
    value=200000.0, 
    step=5000.0, 
    format="%.2f"
)

annual_rate = st.sidebar.slider(
    "Annual Interest Rate (%)", 
    min_value=1.0, 
    max_value=25.0, 
    value=8.5, 
    step=0.1
)

tenure = st.sidebar.slider(
    "Loan Tenure (months)", 
    min_value=3, 
    max_value=360, 
    value=24, 
    step=1
)

years = tenure // 12
months = tenure % 12
time_str = f"{years} years " if years > 0 else ""
time_str += f"{months} months" if months > 0 else ""
st.sidebar.caption(f"Equivalent Tenure: **{time_str}**")


rate = annual_rate / (12 * 100)
common_factor = pow((1 + rate), tenure)
emi = principal * rate * (common_factor / (common_factor - 1))

total_payment = emi * tenure
total_interest = total_payment - principal


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Monthly EMI", value=f"₹{emi:,.2f}")
with col2:
    st.metric(label="Total Amount Paid", value=f"₹{total_payment:,.2f}")
with col3:
    st.metric(label="Total Interest Paid", value=f"₹{total_interest:,.2f}")

st.write("---")

balance = principal
records = []

for i in range(1, int(tenure) + 1):
    monthly_interest = balance * rate
    monthly_principal = emi - monthly_interest
    opening_balance = balance
    
    
    if i == int(tenure):
        monthly_principal = opening_balance
        emi = monthly_principal + monthly_interest
        balance = 0.0
    else:
        balance = opening_balance - monthly_principal
        if balance < 0:
            balance = 0.0

    records.append({
        'Month': i,
        'Opening Bal': round(opening_balance, 2),
        'EMI': round(emi, 2),
        'Interest': round(monthly_interest, 2),
        'Principal': round(monthly_principal, 2),
        'Closing Bal': round(balance, 2)
    })

df = pd.DataFrame(records)


st.markdown('<h3 class="subheader-text">Visual Analytics</h3>', unsafe_allow_html=True)
viz_col1, viz_col2 = st.columns([2, 1])

# Set up matplotlib universal parameters for dark/white configuration
plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'axes.edgecolor': '#334155',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'figure.facecolor': '#0f172a',
    'axes.facecolor': '#1e293b'
})

with viz_col1:
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Month'], df['Principal'], label='Principal', color='#10b981', linewidth=2)
    ax.plot(df['Month'], df['Interest'], label='Interest', color='#ef4444', linewidth=2)
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount (₹)')
    ax.set_title('Principal vs Interest Allocation Component Trend', color='white', fontname='Marcellus')
    ax.legend(facecolor='#0f172a', edgecolor='#334155')
    ax.grid(True, linestyle='--', alpha=0.1)
    plt.tight_layout()
    st.pyplot(fig)

with viz_col2:
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax2.pie(
        [principal, total_interest],
        labels=['Principal', 'Total Interest'],
        autopct='%1.1f%%',
        colors=['#10b981', '#ef4444'],
        startangle=90,
        textprops=dict(color="white")
    )
    for autotext in autotexts:
        autotext.set_color('white')
    ax2.set_title('Total Cost Breakdown Structure Split', color='white', fontname='Marcellus')
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown('<h4 class="subheader-text">Balance Decay Over Time</h4>', unsafe_allow_html=True)
st.bar_chart(df.set_index('Month')['Closing Bal'])

st.write("---")

grid_col, insight_col = st.columns([2, 1])

with grid_col:
    st.markdown('<h3 class="subheader-text">Amortization Schedule Data</h3>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Full Schedule as CSV",
        data=csv_data,
        file_name="loan_amortization_schedule.csv",
        mime="text/csv"
    )

with insight_col:
    st.markdown('<h3 class="subheader-text">Key Insights</h3>', unsafe_allow_html=True)
    st.info(f"""
    * **Average Monthly Interest:** ₹{df['Interest'].mean():,.2f}
    * **Average Monthly Principal:** ₹{df['Principal'].mean():,.2f}
    * **Peak Monthly Interest Cost:** ₹{df['Interest'].max():,.2f} *(Month {int(df['Interest'].idxmax() + 1)})*
    * **Lowest Monthly Interest Cost:** ₹{df['Interest'].min():,.2f} *(Month {int(df['Interest'].idxmin() + 1)})*
    * **Interest Burden Ratio:** Over the lifetime of this loan, interest accounts for **{(total_interest / total_payment) * 100:.1f}%** of your total overall payments.
    """)