import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from chatbot import shop_easy_reply
from database import query_order, search_products, fetch_all_orders, update_shipping_address, init_db

# Ensure DB is fresh
init_db()

# ==============================================================================
# 1. PAGE CONFIG & ENTERPRISE CSS DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="ShopEasy Customer Experience Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism + Neon Accents + Micro-Interactions)
st.markdown("""
<style>
    /* Glassmorphic Container Header */
    .hero-container {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(124, 58, 237, 0.12) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        backdrop-filter: blur(12px);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-sub {
        color: #94A3B8;
        font-size: 0.95rem;
    }
    
    /* Product Grid Cards */
    .product-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        border-color: #60A5FA;
        transform: translateY(-3px);
    }

    /* Live Badge Indicators */
    .pulse-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. STATE MANAGEMENT
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Welcome to ShopEasy Customer Support!** I am synchronized with our live orders and catalog database. How can I assist you today?",
            "time": datetime.datetime.now().strftime("%H:%M")
        }
    ]

if "tickets" not in st.session_state:
    st.session_state.tickets = []

def send_chat_message(prompt_text):
    t_stamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": prompt_text, "time": t_stamp})
    reply = shop_easy_reply(prompt_text)
    st.session_state.messages.append({"role": "assistant", "content": reply, "time": t_stamp})

# ==============================================================================
# 3. SIDEBAR CONTROL PANEL
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3081/3081559.png", width=42)
    st.markdown("### **ShopEasy Control Hub**")
    st.markdown('<span class="pulse-badge">🟢 SQLite DB Engine Active</span>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("#### ⚡ Rapid Query Pills")
    st.caption("Click any prompt to trigger a live query:")
    
    pills = [
        "Where is my order ORD1234?",
        "Track order ORD4499",
        "Cancel order ORD5678",
        "Do you have laptops in stock?",
        "Show 4K monitors",
        "What is your return policy?"
    ]
    
    for pill in pills:
        if st.button(f"💬 {pill}", use_container_width=True):
            send_chat_message(pill)
            st.rerun()

    st.markdown("---")
    st.markdown("#### 📋 Database Sample IDs")
    st.caption("Test order queries with these live record IDs:")
    
    sample_orders = fetch_all_orders()
    for o in sample_orders[:5]:
        st.code(f"{o[0]} -> {o[1]} ({o[2]})")

    st.markdown("---")
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# ==============================================================================
# 4. HERO HEADER & METRICS STRIP
# ==============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">ShopEasy Customer Experience Suite</div>
    <div class="hero-sub">AI Assistant Engine & Real-Time Relational Order Database Portal</div>
</div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Database Status", "10 Orders Seeded", delta="SQLite 3.x")
col_m2.metric("Catalog Inventory", "10 Products Active", delta="Live Stock")
col_m3.metric("Response Time", "0.02s", delta="-5ms")
col_m4.metric("Satisfaction Score", "4.9 / 5.0", delta="★ ★ ★ ★ ★")

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. TABBED WORKSPACE PLATFORM
# ==============================================================================
tab_chat, tab_catalog, tab_tracking, tab_ticket, tab_analytics = st.tabs([
    "💬 AI Assistant", 
    "🛍️ Catalog Explorer", 
    "📦 Order Tracking & Self-Service", 
    "🎫 VIP Ticket Portal", 
    "📊 System Analytics"
])

# ------------------------------------------------------------------------------
# TAB 1: AI CONCIERGE CHAT
# ------------------------------------------------------------------------------
with tab_chat:
    c_chat, c_sidebar = st.columns([2.8, 1.2])
    
    with c_chat:
        st.subheader("Interactive Support Stream")
        
        for msg in st.session_state.messages:
            avatar = "🤖" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                st.caption(f"_{msg.get('time', '')}_")

        if user_input := st.chat_input("Ask a question or enter an order ID (e.g., 'Where is ORD1234?' or 'Cancel ORD5678')..."):
            send_chat_message(user_input)
            st.rerun()

    with c_sidebar:
        st.subheader("📌 Helpful Context")
        st.info("💡 **Live Database Instructions:**\n\n* **Track Order:** Enter `ORD1234`, `ORD4499`, or `ORD9012`\n* **Cancel Order:** Enter `Cancel ORD5678`\n* **Search Items:** Ask `Show me headphones` or `laptops`")
        
        with st.expander("🛠️ Active Capabilities", expanded=True):
            st.markdown("""
            * **Order Lookup**: SQL query by Regex pattern
            * **Order Cancellation**: Real-time DB state update
            * **Inventory Query**: Multi-filter stock search
            * **Policy Engine**: Full-text policy routing
            """)

# ------------------------------------------------------------------------------
# TAB 2: CATALOG EXPLORER WITH FILTERS
# ------------------------------------------------------------------------------
with tab_catalog:
    st.subheader("🛍️ Real-Time Product Catalog Explorer")
    st.markdown("Filter and search products directly from our backend SQLite database.")
    
    # Filter Controls
    f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1.5, 1.5, 1])
    with f_col1:
        search_kw = st.text_input("🔍 Search Keyword", value="", placeholder="e.g. headphones, chair, laptop")
    with f_col2:
        cat_filter = st.selectbox("Category", ["All", "Audio", "Laptops", "Furniture", "Wearables", "Gaming", "Accessories", "Electronics", "Home"])
    with f_col3:
        max_p = st.slider("Max Price ($)", 0, 1500, 1500, step=50)
    with f_col4:
        in_stock = st.checkbox("In Stock Only", value=False)

    filtered_prods = search_products(search_kw, cat_filter, max_p, in_stock)
    
    st.markdown(f"Showing **{len(filtered_prods)}** products matching criteria:")
    
    p_col1, p_col2 = st.columns(2)
    for idx, prod in enumerate(filtered_prods):
        target_col = p_col1 if idx % 2 == 0 else p_col2
        with target_col:
            stock_badge = f"🟢 In Stock ({prod['stock']} left)" if prod['stock'] > 0 else "🔴 Out of Stock"
            st.markdown(f"""
            <div class="product-card">
                <h3>{prod['icon']} {prod['name']}</h3>
                <p><strong>Category:</strong> {prod['category']} | <strong>Rating:</strong> ⭐ {prod['rating']}/5.0</p>
                <p>{prod['description']}</p>
                <h4 style="color: #60A5FA;">${prod['price']:.2f} <span style="font-size: 0.8rem; color: #94A3B8;">({stock_badge})</span></h4>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ask AI about {prod['name']}", key=f"btn_p_{prod['id']}"):
                send_chat_message(f"Tell me more about {prod['name']}")
                st.rerun()

# ------------------------------------------------------------------------------
# TAB 3: ORDER TRACKER & SELF-SERVICE ADDRESS MUTATION
# ------------------------------------------------------------------------------
with tab_tracking:
    st.subheader("📦 Real-Time Order Stepper & Address Manager")
    st.markdown("Inspect order details and directly modify shipping addresses in the SQLite database.")
    
    all_ord_ids = [o[0] for o in fetch_all_orders()]
    
    track_col1, track_col2 = st.columns([1.2, 1.8])
    
    with track_col1:
        selected_id = st.selectbox("Select Order ID to Inspect:", all_ord_ids)
        order_info = query_order(selected_id)
        
        st.markdown("---")
        st.markdown("#### ✏️ Self-Service Address Update")
        with st.form("address_form"):
            new_addr = st.text_input("New Shipping Address", value=order_info["address"] if order_info else "")
            update_btn = st.form_submit_button("Update Shipping Address")
            
            if update_btn and order_info:
                if new_addr.strip():
                    success = update_shipping_address(selected_id, new_addr.strip())
                    if success:
                        st.success("Shipping address updated in SQLite database!")
                        st.rerun()
                    else:
                        st.error("Failed to update address.")

    with track_col2:
        if order_info:
            st.markdown(f"### Order `{order_info['order_id']}` — Customer: **{order_info['customer_name']}**")
            
            # Progress Stepper
            stages = ["Processing", "Shipped", "Out for Delivery", "Delivered"]
            status_map = {"Processing": 0, "Shipped": 1, "Out for Delivery": 2, "Delivered": 3, "On Hold": 0, "Cancelled": -1, "Refunded": -1}
            current_stage_idx = status_map.get(order_info["status"], 0)
            
            if current_stage_idx >= 0:
                st.progress((current_stage_idx + 1) / 4)
                s_cols = st.columns(4)
                for i, stage_name in enumerate(stages):
                    with s_cols[i]:
                        if i <= current_stage_idx:
                            st.markdown(f"✅ **{stage_name}**")
                        else:
                            st.markdown(f"⚪ <span style='color:gray;'>{stage_name}</span>", unsafe_allow_html=True)
            else:
                st.warning(f"Order Status: **{order_info['status']}**")
                        
            st.markdown("---")
            st.json(order_info)

# ------------------------------------------------------------------------------
# TAB 4: VIP TICKET PORTAL
# ------------------------------------------------------------------------------
with tab_ticket:
    st.subheader("🎫 Escalation Ticket Management")
    st.markdown("Submit a support ticket to human engineering support.")
    
    t_col1, t_col2 = st.columns([1.5, 1])
    
    with t_col1:
        with st.form("ticket_form"):
            email = st.text_input("Email Address")
            category = st.selectbox("Category", ["Order Issue", "Refund Status", "Damaged Delivery", "Other"])
            desc = st.text_area("Detailed Description")
            submit_ticket = st.form_submit_button("🚀 Submit Ticket")
            
            if submit_ticket:
                if email and desc:
                    t_id = f"TICK-{datetime.datetime.now().strftime('%d%H%M%S')}"
                    st.session_state.tickets.append({"ID": t_id, "Email": email, "Category": category, "Status": "Open"})
                    st.success(f"Ticket **{t_id}** submitted successfully!")
                else:
                    st.error("Please fill out all required fields.")

    with t_col2:
        st.markdown("#### Active Session Tickets")
        if st.session_state.tickets:
            st.dataframe(pd.DataFrame(st.session_state.tickets), use_container_width=True)
        else:
            st.info("No active tickets submitted in this session.")

# ------------------------------------------------------------------------------
# TAB 5: TELEMETRY & ANALYTICS DASHBOARD
# ------------------------------------------------------------------------------
with tab_analytics:
    st.subheader("📊 Operational Telemetry & Metrics")
    
    an_col1, an_col2 = st.columns(2)
    
    with an_col1:
        st.markdown("#### Order Status Distribution")
        raw_orders = fetch_all_orders()
        df_orders = pd.DataFrame(raw_orders, columns=["Order ID", "Customer", "Status", "Amount", "Carrier"])
        
        status_counts = df_orders["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        fig_donut = px.pie(status_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_donut, use_container_width=True)

    with an_col2:
        st.markdown("#### Order Value Breakdown by Carrier")
        fig_bar = px.bar(df_orders, x="Carrier", y="Amount", color="Status", template="plotly_dark", barmode="group")
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)