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
    
    /* Progress Bar Custom */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #6366f1 , #a855f7);
    }
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
    
    # --- Sidebar Configuration ---
    with st.sidebar:
        st.markdown("### 🎯 Mục tiêu tháng")
        monthly_goal = st.number_input("Mục tiêu doanh thu (đ)", min_value=0, value=50000000, step=1000000, format="%d")
        st.divider()

    # --- Calculations for Metrics ---
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    # Current month data
    mask_current = (df['Time'].dt.month == current_month) & (df['Time'].dt.year == current_year)
    this_month_df = df[mask_current]
    total_this_month = this_month_df['Amount'].sum()
    
    # Last month data (for comparison)
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    # For a fair comparison, look at last month up to the same day
    mask_last = (df['Time'].dt.month == last_month) & (df['Time'].dt.year == last_month_year)
    last_month_df = df[mask_last]
    last_month_upto_today = last_month_df[last_month_df['Time'].dt.day <= today.day]['Amount'].sum()
    
    growth = 0
    if last_month_upto_today > 0:
        growth = ((total_this_month - last_month_upto_today) / last_month_upto_today) * 100

    # Stats Row
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Số dư hiện tại", f"{df['Balance'].iloc[-1]:,.0f} đ")
    with m2: st.metric("Doanh thu tháng này", f"{total_this_month:,.0f} đ", delta=f"{growth:.1f}% vs tháng trước" if last_month_upto_today > 0 else None)
    with m3: st.metric("Tổng lượt vào", f"{len(df)}")
    with m4: st.metric("Tiền vào TB", f"{df['Amount'].mean():,.0f} đ")

    # --- Goal Progress ---
    progress = min(1.0, total_this_month / monthly_goal) if monthly_goal > 0 else 0
    
    st.markdown(f"**Tiến độ mục tiêu tháng {current_month}: {progress*100:.1f}%** ({total_this_month:,.0f} / {monthly_goal:,.0f} đ)")
    st.progress(progress)
    
    # Prediction Logic
    last_day = (pd.Timestamp(current_year, current_month, 1) + pd.offsets.MonthEnd(0)).day
    current_day = today.day
    days_left = max(0, last_day - current_day)
    
    avg_daily = total_this_month / current_day if current_day > 0 else 0
    predicted_end = df['Balance'].iloc[-1] + (avg_daily * days_left)
    
    predict_col1, predict_col2 = st.columns([2, 1])
    with predict_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);">
            <div style="font-size: 0.8rem; opacity: 0.9; font-weight: 500;">Dự kiến số dư cuối tháng ({today.strftime('%m/%Y')})</div>
            <div style="font-size: 2rem; font-weight: 800; margin-top: 5px;">{predicted_end:,.0f} đ</div>
            <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 5px;">Tốc độ trung bình: {avg_daily:,.0f} đ/ngày</div>
        </div>
        """, unsafe_allow_html=True)
    
    with predict_col2:
        if total_this_month < monthly_goal and avg_daily > 0:
            remaining = monthly_goal - total_this_month
            days_to_goal = remaining / avg_daily
            target_date = today + pd.Timedelta(days=days_to_goal)
            
            status_color = "#10b981" if days_to_goal <= days_left else "#f59e0b"
            st.markdown(f"""
            <div style="background: white; border: 1px solid #f3f4f6; padding: 20px; border-radius: 16px; height: 100%;">
                <div style="font-size: 0.8rem; color: #6b7280;">Dự kiến đạt mục tiêu</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: {status_color}; margin-top: 5px;">{target_date.strftime('%d/%m/%Y')}</div>
                <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 5px;">{'Sớm hơn dự kiến' if days_to_goal <= days_left else 'Cần tăng tốc!'}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #ecfdf5; border: 1px solid #10b981; padding: 20px; border-radius: 16px; height: 100%; display: flex; align-items: center; justify-content: center; text-align: center;">
                <div style="font-weight: 700; color: #059669;">🎉 Đã đạt mục tiêu!</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    
    # Tabs
    tab_balance, tab_daily, tab_time, tab_list = st.tabs(["📉 Biến động", "📊 Theo ngày", "⏰ Phân tích giờ", "📝 Quản lý"])
    
    with tab_balance:
        fig_balance = px.area(df, x='Time', y='Balance', title="Xu hướng số dư lũy kế",
                              labels={'Balance': 'Số dư (đ)', 'Time': 'Thời gian'},
                              line_shape='spline', color_discrete_sequence=['#6366f1'])
        fig_balance.update_traces(mode="lines+markers", hovertemplate="<b>Thời gian:</b> %{x}<br><b>Số dư:</b> %{y:,.0f} đ")
        fig_balance.update_layout(hovermode="x unified", margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_balance, use_container_width=True)
        
    with tab_daily:
        df['Date'] = df['Time'].dt.date
        daily_income = df.groupby('Date')['Amount'].sum().reset_index()
        
        fig_daily = px.bar(daily_income, x='Date', y='Amount', title="Tổng tiền vào mỗi ngày",
                           labels={'Amount': 'Tiền vào (đ)', 'Date': 'Ngày'},
                           color_discrete_sequence=['#8b5cf6'])
        fig_daily.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_daily, use_container_width=True)

    with tab_time:
        df['Hour'] = df['Time'].dt.hour
        df['DayOfWeek'] = df['Time'].dt.day_name()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        c1, c2 = st.columns(2)
        with c1:
            hour_dist = df.groupby('Hour').size().reset_index(name='Count')
            fig_hour = px.bar(hour_dist, x='Hour', y='Count', title="Phân bổ giao dịch theo giờ",
                              labels={'Hour': 'Giờ trong ngày', 'Count': 'Số lượng GD'},
                              color_discrete_sequence=['#f59e0b'])
            st.plotly_chart(fig_hour, use_container_width=True)
        with c2:
            day_dist = df.groupby('DayOfWeek').size().reindex(days_order).reset_index(name='Count')
            fig_day = px.bar(day_dist, x='DayOfWeek', y='Count', title="Giao dịch theo thứ",
                             labels={'DayOfWeek': 'Thứ', 'Count': 'Số lượng GD'},
                             color_discrete_sequence=['#10b981'])
            st.plotly_chart(fig_day, use_container_width=True)

    with tab_list:
        st.markdown("#### Quản lý & Tìm kiếm")
        search_query = st.text_input("🔍 Tìm kiếm theo nội dung...", placeholder="Nhập từ khóa...")
        
        display_df = df.copy().sort_values('Time', ascending=False)
        if search_query:
            display_df = display_df[display_df['Content'].str.contains(search_query, case=False, na=False)]
        
        # Using data_editor for editing/deleting
        edited_df = st.data_editor(
            display_df[['Time', 'Amount', 'Bank', 'Content', 'Balance']],
            column_config={
                "Amount": st.column_config.NumberColumn("Số tiền", format="%d đ"),
                "Balance": st.column_config.NumberColumn("Số dư sau GD", format="%d đ"),
                "Time": st.column_config.DatetimeColumn("Thời gian"),
                "Bank": "Ngân hàng",
                "Content": "Nội dung"
            },
            use_container_width=True, 
            hide_index=True,
            num_rows="dynamic" # This allows deleting rows
        )
        
        # Handle updates from data_editor
        if len(edited_df) != len(display_df):
            # Row was deleted or something changed. 
            # Simplified logic: sync back the entire session state from edited_df
            # Note: This is a simple sync. For large datasets, more complex logic is needed.
            new_data = edited_df[['Amount', 'Bank', 'Time', 'Content']].to_dict('records')
            # Add back non-displayed data if any, but here we cover all fields.
            st.session_state.transactions = new_data
            save_data(st.session_state.transactions)
            st.rerun()

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
