import streamlit as st
import pandas as pd
import re
import os
from datetime import datetime
import plotly.express as px

# --- Constants & Configuration ---
DATA_FILE = "transactions_data.csv"

st.set_page_config(
    page_title="Nicer Analytics",
    page_icon="💎",
    layout="wide",
)

# --- Custom Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #4f46e5;
        --bg-light: #f9fafb;
        --text-main: #111827;
        --text-sub: #6b7280;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    .stApp { background-color: white; }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #f3f4f6;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        color: var(--primary) !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .hero-section {
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero-section h1 { font-weight: 800; letter-spacing: -0.025em; margin-bottom: 0.5rem; }
    .hero-section p { color: var(--text-sub); font-size: 1.1rem; }

    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- Persistence Logic ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE, encoding='utf-8-sig').to_dict('records')
        except: return []
    return []

def save_data(data_list):
    try:
        pd.DataFrame(data_list).to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
    except: pass

# --- Initialize State ---
if 'transactions' not in st.session_state:
    st.session_state.transactions = load_data()

# --- Analysis Logic ---
def parse_text(text):
    chunks = re.split(r'Tiền vào ae Nicer ơi!|-------------|==== TÀI KHOẢN DOANH NGHIỆP ====', text)
    added = 0
    for chunk in chunks:
        if not chunk.strip(): continue
        amt = re.search(r'Amount:\s*([\+\-][\d,]+)\s*đ', chunk)
        bnk = re.search(r'Bank:\s*([^\n\r]*)', chunk)
        tme = re.search(r'Time:\s*([^\n\r]*)', chunk)
        cnt = re.search(r'Content:\s*([^\n\r]*)', chunk)
        
        if amt and bnk:
            try:
                clean_amt = re.sub(r'[^\d\+\-]', '', amt.group(1))
                val = float(clean_amt)
                bank = bnk.group(1).strip()
                time_str = tme.group(1).strip() if tme else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                content = cnt.group(1).strip() if cnt else ""
                
                entry = {'Amount': val, 'Bank': bank, 'Time': time_str, 'Content': content}
                
                if not any(t['Amount'] == val and t['Time'] == time_str for t in st.session_state.transactions):
                    st.session_state.transactions.append(entry)
                    added += 1
            except: continue
    
    if added > 0:
        save_data(st.session_state.transactions)
    return added

# --- UI Components ---

st.markdown("""
<div class="hero-section">
    <h1>💎 Nicer Analytics</h1>
    <p>Biến các tin nhắn thông báo thành biểu đồ số dư trực quan.</p>
</div>
""", unsafe_allow_html=True)

with st.container():
    input_expanded = not bool(st.session_state.transactions)
    with st.expander("📥 Nhập dữ liệu giao dịch mới", expanded=input_expanded):
        col1, col2 = st.columns([4, 1])
        with col1:
            raw_input = st.text_area("Dán nội dung giao dịch...", height=120, label_visibility="collapsed", placeholder="Dán nội dung 'Tiền vào ae Nicer ơi!'...")
        with col2:
            st.write("")
            if st.button("Phân tích ✨", use_container_width=True, type="primary"):
                if raw_input:
                    new_count = parse_text(raw_input)
                    if new_count:
                        st.balloons()
                        st.toast(f"Đã thêm {new_count} giao dịch!", icon='✅')
                        st.rerun()
                    else: st.toast("Không tìm thấy dữ liệu mới.", icon='⚠️')

if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values('Time')
    
    # CALCULATE CUMULATIVE BALANCE
    df['Balance'] = df['Amount'].cumsum()
    
    # Stats
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Số dư hiện tại", f"{df['Balance'].iloc[-1]:,.0f} đ")
    with m2: st.metric("Tổng lượt vào", f"{len(df)}")
    with m3: st.metric("Tiền vào TB", f"{df['Amount'].mean():,.0f} đ")

    # --- Prediction Logic ---
    today = datetime.now()
    last_day = (pd.Timestamp(today.year, today.month, 1) + pd.offsets.MonthEnd(0)).day
    current_day = today.day
    days_left = last_day - current_day
    
    # Calculate daily average income
    # Filter for current month AND year to be more accurate
    current_month_df = df[(df['Time'].dt.month == today.month) & (df['Time'].dt.year == today.year)]
    if not current_month_df.empty:
        avg_daily = current_month_df['Amount'].sum() / current_day
    else:
        avg_daily = 0
        
    predicted_end = df['Balance'].iloc[-1] + (avg_daily * max(0, days_left))
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);">
        <div style="font-size: 0.9rem; opacity: 0.9; font-weight: 500;">Dự kiến số dư cuối tháng ({today.strftime('%m/%Y')})</div>
        <div style="font-size: 2.2rem; font-weight: 800; margin-top: 5px;">{predicted_end:,.0f} đ</div>
        <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 10px;">Dựa trên trung bình {avg_daily:,.0f} đ/ngày hiện tại</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # Tabs
    tab_balance, tab_daily, tab_list = st.tabs(["📉 Biến động số dư", "📊 Thống kê hàng ngày", "📝 Nhật ký"])
    
    with tab_balance:
        # Balance over time chart (Premium line chart)
        fig_balance = px.area(df, x='Time', y='Balance', title="Biểu đồ biến động số dư lũy kế",
                              labels={'Balance': 'Số dư (đ)', 'Time': 'Thời gian'},
                              line_shape='spline', color_discrete_sequence=['#6366f1'])
        
        # Add hover data for extra detail
        fig_balance.update_traces(mode="lines+markers", hovertemplate="<b>Thời gian:</b> %{x}<br><b>Số dư:</b> %{y:,.0f} đ")
        fig_balance.update_layout(hovermode="x unified", margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_balance, use_container_width=True)
        
    with tab_daily:
        df['Date'] = df['Time'].dt.date
        daily_income = df.groupby('Date')['Amount'].sum().reset_index()
        
        fig_daily = px.bar(daily_income, x='Date', y='Amount', title="Tổng tiền vào theo ngày",
                           labels={'Amount': 'Tổng tiền (đ)', 'Date': 'Ngày'},
                           color_discrete_sequence=['#8b5cf6'])
        fig_daily.update_traces(hovertemplate="<b>Ngày:</b> %{x}<br><b>Tổng:</b> %{y:,.0f} đ")
        fig_daily.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_daily, use_container_width=True)

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            # Count transactions per day
            daily_count = df.groupby('Date').size().reset_index(name='Counts')
            fig_count = px.line(daily_count, x='Date', y='Counts', title="Số lượng giao dịch theo ngày",
                                 markers=True, color_discrete_sequence=['#ec4899'])
            st.plotly_chart(fig_count, use_container_width=True)
        with col_d2:
            st.markdown("#### Chi tiết theo ngày")
            st.dataframe(daily_income.sort_values('Date', ascending=False), use_container_width=True, hide_index=True)

    with tab_list:
        st.dataframe(
            df.sort_values('Time', ascending=False),
            column_config={
                "Amount": st.column_config.NumberColumn("Số tiền", format="%d đ"),
                "Balance": st.column_config.NumberColumn("Số dư sau GD", format="%d đ"),
                "Time": "Thời gian",
                "Bank": "Ngân hàng",
                "Content": "Nội dung"
            },
            use_container_width=True, hide_index=True
        )
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Xuất file CSV", data=csv, file_name="history.csv", mime="text/csv")

else:
    st.write("")
    col_empty1, col_empty2, col_empty3 = st.columns([1, 2, 1])
    with col_empty2:
        st.info("💡 Hệ thống đang sẵn sàng. Hãy dán giao dịch 'Nicer' của bạn để xem biểu đồ biến động số dư theo thời gian!")
        st.image("https://illustrations.popsy.co/blue/digital-marketing-analysis.svg")

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎛️ Quản lý")
    if st.button("🗑️ Xóa sạch toàn bộ lịch sử", use_container_width=True):
        st.session_state.transactions = []
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.rerun()
    st.divider()
    st.caption("Dữ liệu được lưu tại local: %s" % DATA_FILE)
    st.caption("Sử dụng kỹ thuật tính toán lũy kế (Cumulative Sum) để vẽ biểu đồ biến động.")
