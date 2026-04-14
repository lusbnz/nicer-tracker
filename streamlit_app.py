import streamlit as st
import pandas as pd
import re
import os
from datetime import datetime
import plotly.express as px

# --- Constants & Configuration ---
DATA_FILE = "transactions_data.csv"

st.set_page_config(
    page_title="Nicer",
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
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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

def handle_csv_upload(uploaded_file):
    try:
        new_df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        # Basic validation: check if required columns exist
        required_cols = ['Amount', 'Bank', 'Time', 'Content']
        if not all(col in new_df.columns for col in required_cols):
            st.error(f"File CSV thiếu cột. Cần có: {', '.join(required_cols)}")
            return 0
        
        added = 0
        for _, row in new_df.iterrows():
            try:
                val = float(row['Amount'])
                bank = str(row['Bank']).strip()
                # Use pd.to_datetime to normalize various date formats
                time_val = pd.to_datetime(row['Time'])
                time_str = time_val.strftime("%Y-%m-%d %H:%M:%S")
                content = str(row['Content']).strip()
                
                entry = {'Amount': val, 'Bank': bank, 'Time': time_str, 'Content': content}
                
                # Duplicate check based on Amount AND Time
                # We normalize the stored time to string for comparison
                is_duplicate = any(
                    t['Amount'] == val and 
                    (pd.to_datetime(t['Time']).strftime("%Y-%m-%d %H:%M:%S") == time_str)
                    for t in st.session_state.transactions
                )
                
                if not is_duplicate:
                    st.session_state.transactions.append(entry)
                    added += 1
            except: continue
            
        if added > 0:
            save_data(st.session_state.transactions)
            
        return added
    except Exception as e:
        st.error(f"Lỗi khi xử lý file CSV: {e}")
        return 0

# --- UI Components ---

st.markdown("""
<div class="hero-section">
    <h1>Nicer</h1>
</div>
""", unsafe_allow_html=True)

with st.container():
    input_expanded = not bool(st.session_state.transactions)
    with st.expander("📥 Dán dữ liệu giao dịch mới", expanded=input_expanded):
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

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### ⚙️ Cài đặt")
    monthly_goal = st.number_input("Mục tiêu doanh thu (đ)", min_value=0, value=500000000, step=1000000, format="%d")
    
    st.markdown("---")
    st.markdown("### 📥 Import dữ liệu")
    uploaded_file = st.file_uploader("Tải lên file CSV", type=["csv"])
    if uploaded_file:
        if st.button("Xác nhận Import 🚀", use_container_width=True, type="primary"):
            new_count = handle_csv_upload(uploaded_file)
            if new_count:
                st.balloons()
                st.toast(f"Đã thêm {new_count} giao dịch!", icon='✅')
                st.rerun()
            else:
                st.toast("Không tìm thấy dữ liệu mới.", icon='⚠️')
    
    # Download template always available
    template_df = pd.DataFrame(columns=['Amount', 'Bank', 'Time', 'Content'])
    template_csv = template_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📄 Tải file mẫu CSV",
        data=template_csv,
        file_name="template_nicer.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("### 📤 Export dữ liệu")
    if st.session_state.transactions:
        csv_data = pd.DataFrame(st.session_state.transactions).to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải xuống CSV",
            data=csv_data,
            file_name=f"nicer_transactions_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Chưa có dữ liệu để xuất.")

if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values('Time')
    
    # CALCULATE CUMULATIVE BALANCE
    df['Balance'] = df['Amount'].cumsum()

    # --- Calculations for Metrics ---
    today = datetime.now()
    current_date = today.date()
    current_month = today.month
    current_year = today.year
    
    # Yesterday for comparison (optional but good for context)
    yesterday_date = current_date - pd.Timedelta(days=1)
    
    # Today's data
    mask_today = df['Time'].dt.date == current_date
    today_df = df[mask_today]
    total_today = today_df['Amount'].sum()
    count_today = len(today_df)
    
    # Yesterday's data
    mask_yesterday = df['Time'].dt.date == yesterday_date
    yesterday_df = df[mask_yesterday]
    total_yesterday = yesterday_df['Amount'].sum()
    count_yesterday = len(yesterday_df)
    
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

    # Daily target calculation
    last_day = (pd.Timestamp(current_year, current_month, 1) + pd.offsets.MonthEnd(0)).day
    current_day = today.day
    days_rem = last_day - current_day + 1
    days_left = max(0, last_day - current_day)
    # Actually, more simple: (monthly_goal / last_day) is the baseline daily target. 
    # Or: Remaining goal / days left.
    daily_target = monthly_goal / last_day
    
    # Today's progress
    progress_today = min(1.0, total_today / daily_target) if daily_target > 0 else (1.0 if total_today > 0 else 0)
    
    # Growth today vs yesterday
    growth_today = total_today - total_yesterday
    growth_count = count_today - count_yesterday

    # --- Today Summary Row ---
    st.markdown("### Hôm nay")
    t1, t2, t3 = st.columns(3)
    
    delta_today_val = total_today - daily_target
    
    with t1:
        st.metric("Doanh thu hôm nay", f"{total_today:,.0f} đ", delta=f"{growth_today:+,.0f} đ" if total_yesterday > 0 else None)
    with t2:
        st.metric("Lượt vào hôm nay", f"{count_today}", delta=f"{growth_count:+d} lượt" if count_yesterday > 0 else None)
    with t3:
        st.metric("Tiến độ hôm nay", f"{progress_today*100:.1f}%", delta=f"{delta_today_val:,.0f} đ so với mục tiêu")
    
    st.progress(progress_today)
    st.write("")

    # --- Monthly Metrics ---
    st.markdown("### Hiệu suất tháng")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Doanh thu tháng này", f"{total_this_month:,.0f} đ", delta=f"{growth:.1f}% vs tháng trước" if last_month_upto_today > 0 else None)
    with m2: st.metric("Tổng lượt vào", f"{len(df)}")
    with m3: st.metric("Tiền vào TB", f"{df['Amount'].mean():,.0f} đ")

    # --- Goal Progress ---
    progress = min(1.0, total_this_month / monthly_goal) if monthly_goal > 0 else 0
    
    st.markdown(f"**Tiến độ mục tiêu tháng {current_month}: {progress*100:.1f}%** ({total_this_month:,.0f} / {monthly_goal:,.0f} đ)")
    st.progress(progress)
    
    # Prediction Logic
    avg_daily = total_this_month / current_day if current_day > 0 else 0
    predicted_end = df['Balance'].iloc[-1] + (avg_daily * days_left)
    
    # Row 1: Forecast
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 20px; border-radius: 16px; color: white; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);">
        <div style="font-size: 0.8rem; opacity: 0.9; font-weight: 500;">Dự báo doanh thu cuối tháng ({today.strftime('%m/%Y')})</div>
        <div style="font-size: 2rem; font-weight: 800; margin-top: 5px;">{predicted_end:,.0f} đ</div>
        <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 5px;">Tốc độ doanh thu: {avg_daily:,.0f} đ/ngày</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 2: Target & Daily Need
    pred_col1, pred_col2 = st.columns(2)
    
    with pred_col1:
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

    with pred_col2:
        days_rem = last_day - current_day + 1
        daily_needed = max(0, monthly_goal - total_this_month) / days_rem if days_rem > 0 else 0
        
        st.markdown(f"""
        <div style="background: white; border: 1px solid #f3f4f6; padding: 20px; border-radius: 16px; height: 100%;">
            <div style="font-size: 0.8rem; color: #6b7280;">Doanh thu cần đạt trong ngày</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #6366f1; margin-top: 5px;">{daily_needed:,.0f} đ/ngày</div>
            <div style="font-size: 0.7rem; color: #9ca3af; margin-top: 5px;">Còn lại {days_rem} ngày</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Tabs
    tab_balance, tab_daily, tab_list = st.tabs(["📉 Biến động doanh thu", "📊 Doanh thu theo ngày", "📝 Danh sách giao dịch"])
    
    with tab_balance:
        fig_balance = px.area(df, x='Time', y='Balance', title="Xu hướng doanh thu lũy kế",
                              labels={'Balance': 'Tổng doanh thu (đ)', 'Time': 'Thời gian'},
                              line_shape='spline', color_discrete_sequence=['#6366f1'])
        fig_balance.update_traces(mode="lines+markers", hovertemplate="<b>Thời gian:</b> %{x}<br><b>Tổng:</b> %{y:,.0f} đ")
        fig_balance.update_layout(hovermode="x unified", margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_balance, use_container_width=True)

    with tab_daily:
        st.markdown("#### Phân tích doanh thu hàng ngày")
        df_daily = df.copy()
        df_daily['Date'] = df_daily['Time'].dt.date
        daily_revenue = df_daily.groupby('Date')['Amount'].sum().reset_index()
        
        fig_daily = px.bar(daily_revenue, x='Date', y='Amount', 
                           title="Biểu đồ doanh thu theo ngày",
                           labels={'Amount': 'Doanh thu (đ)', 'Date': 'Ngày'},
                           color_discrete_sequence=['#6366f1'])
        
        # Format the look and feel
        fig_daily.update_traces(
            hovertemplate="<b>Ngày:</b> %{x}<br><b>Doanh thu:</b> %{y:,.0f} đ",
            marker_color='#6366f1',
            marker_line_color='#4f46e5',
            marker_line_width=1,
            opacity=0.9
        )
        
        fig_daily.update_layout(
            hovermode="x unified",
            margin=dict(t=50, b=0, l=0, r=0),
            xaxis_title="",
            yaxis_title="Doanh thu (VNĐ)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        # Add a mean line for better context if there's enough data
        if len(daily_revenue) > 1:
            mean_rev = daily_revenue['Amount'].mean()
            fig_daily.add_hline(y=mean_rev, line_dash="dash", line_color="#a855f7", 
                                annotation_text=f"Trung bình: {mean_rev:,.0f} đ", 
                                annotation_position="top right")

        st.plotly_chart(fig_daily, use_container_width=True)

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
            # Standardize Time back to string format
            new_df_sync = edited_df[['Amount', 'Bank', 'Time', 'Content']].copy()
            new_df_sync['Time'] = new_df_sync['Time'].dt.strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.transactions = new_df_sync.to_dict('records')
            save_data(st.session_state.transactions)
            st.rerun()

        # Handled in sidebar now
        pass

else:
    st.write("")
    col_empty1, col_empty2, col_empty3 = st.columns([1, 2, 1])
    with col_empty2:
        st.info("💡 Hệ thống đang sẵn sàng. Hãy dán giao dịch 'Nicer' của bạn để xem biểu đồ biến động số dư theo thời gian!")
        st.image("https://illustrations.popsy.co/blue/digital-marketing-analysis.svg")
