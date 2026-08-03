# 🛍️ ShopEasy AI Customer Support Suite

An enterprise-grade, real-time e-commerce customer support platform built with **Streamlit**, **SQLite**, **Plotly**, and **Hugging Face Transformers**.

This application moves beyond basic static chatbots by combining **regex pattern matching**, **a live relational database engine**, **self-service order management**, and **interactive analytics dashboards** into a single glassmorphic workspace.

---

## 🌟 Key Features

### 🤖 1. Smart AI Support Concierge
* **Regex Pattern Extraction**: Detects and extracts 7-character Order IDs (e.g., `ORD1234`, `ORD4499`) anywhere within natural text.
* **Live Relational Database Queries**: Queries actual SQLite tables for order telemetry, carriers, tracking numbers, and live product stock.
* **AI Fallback Pipeline**: Uses Hugging Face's `google/flan-t5-base` model to answer policy questions contextually.
* **Order Cancellations**: Processes live order cancellations directly from the chat interface.

### 📦 2. Real-Time Order Stepper & Self-Service Portal
* **Visual Delivery Stepper**: Displays live progress stages (*Processing → Shipped → Out for Delivery → Delivered*).
* **Address Modification Engine**: Allows customers to update their shipping address directly in the backend SQLite database.

### 🛍️ 3. Interactive Catalog Explorer
* Multi-parameter product search engine with category filters, price range sliders, and stock availability toggles.
* One-click **"Ask AI"** buttons that automatically trigger contextual inquiries.

### 🎫 4. VIP Escalation Ticket Portal
* Direct dispatch channel for users requiring human helpdesk intervention.
* Session-persistent ticket logging and reference ID generation.

### 📊 5. Operational Telemetry & Analytics
* Plotly dark-themed interactive visualizations for query topic distributions and order carrier breakdowns.
* Live metric cards displaying database health, latency, and catalog stock.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, Custom Glassmorphism CSS |
| **Data Visualization** | Plotly Express, Pandas |
| **Database Engine** | SQLite 3 (Relational) |
| **NLP & AI Engine** | Hugging Face Transformers (`google/flan-t5-base`), PyTorch, Regex Engine |
| **Language** | Python 3.9+ |

---

## 📁 Project Architecture

```text
ShopEasy-Support-Portal/
├── app.py           # Streamlit UI, multi-tab layout, custom CSS & Plotly dashboard
├── chatbot.py       # Smart NLP router, regex pattern matcher & query builder
├── database.py      # SQLite database initialization, 10+ seeded records & mutations
├── policies.py      # Core store policies & fallback data dictionary
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
