import re
from database import query_order, search_products, get_policy, cancel_order_in_db, init_db

init_db()

def shop_easy_reply(user_message: str) -> str:
    text = user_message.strip()
    text_lower = text.lower()

    # 1. Regex Match Order ID (e.g., ORD1234, ORD9900)
    order_match = re.search(r'\bORD\d{4}\b', text, re.IGNORECASE)
    
    # Cancellation Request Intent
    if "cancel" in text_lower and order_match:
        found_id = order_match.group(0).upper()
        success = cancel_order_in_db(found_id)
        if success:
            return f"✅ **Order {found_id} has been successfully cancelled.** If you were charged, a refund will be issued within 3-5 business days."
        else:
            order_info = query_order(found_id)
            if order_info and order_info["status"] in ["Shipped", "Delivered", "Out for Delivery"]:
                return f"⚠️ **Cannot Cancel Order {found_id}:** This order is already **{order_info['status']}**. Please wait for delivery and initiate a return."
            return f"❌ Order `{found_id}` could not be cancelled or was not found."

    # General Order Lookup
    if order_match:
        order_id = order_match.group(0).upper()
        data = query_order(order_id)
        
        if data:
            items_str = ", ".join(data["items"])
            return (
                f"📦 **Live Order Telemetry for `{data['order_id']}`**\n\n"
                f"* **Customer:** {data['customer_name']}\n"
                f"* **Status:** `{data['status']}`\n"
                f"* **Items:** {items_str}\n"
                f"* **Total Value:** ${data['total']:.2f}\n"
                f"* **Logistics Partner:** {data['carrier']} (`{data['tracking_number']}`)\n"
                f"* **Estimated Arrival:** **{data['delivery']}**\n"
                f"* **Shipping Destination:** {data['address']}"
            )
        else:
            return f"❌ I searched our live database, but could not locate Order ID **{order_id}**. Please verify your order number."

    # 2. General Order Tracking Intent
    if any(p in text_lower for p in ["where is my order", "track my order", "order status", "track order"]):
        return "I can query our live shipping database! Please provide your Order ID (e.g., `ORD1234`, `ORD5678`, `ORD9012`, or `ORD4499`)."

    # 3. Product Catalog Queries
    product_keywords = ["laptop", "phone", "headphone", "chair", "watch", "keyboard", "speaker", "mouse", "monitor", "lamp", "mic", "product", "buy", "stock"]
    if any(k in text_lower for k in product_keywords):
        target_kw = ""
        for kw in ["laptop", "headphone", "chair", "watch", "keyboard", "speaker", "mouse", "monitor", "lamp", "mic"]:
            if kw in text_lower:
                target_kw = kw
                break
                
        found = search_products(target_kw)
        if found:
            reply = "🛍️ **Here are the matching items from our real-time catalog:**\n\n"
            for p in found[:3]:
                stock_label = f"✅ In Stock ({p['stock']} left)" if p['stock'] > 0 else "❌ Out of Stock"
                reply += f"* **{p['icon']} {p['name']}** — **${p['price']:.2f}** | Rating: ⭐ {p['rating']}/5\n  _{p['description']}_ ({stock_label})\n\n"
            return reply

    # 4. Dynamic Policy Routing
    if "return" in text_lower:
        return f"🔄 **Return Policy:**\n\n{get_policy('returns')}"

    if "refund" in text_lower:
        return f"💰 **Refund Terms:**\n\n{get_policy('refunds')}"

    if any(k in text_lower for k in ["delivery", "shipping", "how long", "ship"]):
        return f"🚚 **Shipping Information:**\n\n{get_policy('shipping')}"

    if any(k in text_lower for k in ["payment", "upi", "cod", "credit card", "apple pay", "klarna"]):
        return f"💳 **Supported Payment Gateways:**\n\n{get_policy('payments')}"

    # 5. Human Escalation Intent
    if any(k in text_lower for k in ["human", "agent", "contact", "support", "person"]):
        return "👨‍💼 **Escalating to Live Human Agent...**\n\nYou can reach our priority helpdesk at **support@shopeasy.com** or call **1-800-555-EASY**. Alternatively, use the **VIP Support Ticket** tab above!"

    # Fallback
    return (
        "🤖 **ShopEasy Customer Assistant**\n\n"
        "I didn't quite catch that. Here is what I can do in real-time:\n"
        "* 📦 **Track Order:** Type `Where is ORD1234?` or `ORD4499`\n"
        "* ❌ **Cancel Order:** Type `Cancel order ORD5678`\n"
        "* 🔍 **Search Items:** Type `Do you have 4K monitors?` or `Show laptops`\n"
        "* 📑 **Check Policies:** Ask about `returns`, `refunds`, or `shipping`"
    )

def get_order_status(order_id: str) -> str:
    return shop_easy_reply(order_id)