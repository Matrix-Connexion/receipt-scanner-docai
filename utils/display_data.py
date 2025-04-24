import streamlit as st

def display_receipt_data(data):
    if not data:
        st.warning("No data to display.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Receipt Details")
        for key, value in data.get("receipt_details", {}).items():
            display_key = key.replace("_", " ").title()
            st.write(f"**{display_key}:** {value or 'N/A'}")

    with col2:
        st.subheader("Purchased Items")
        for i, item in enumerate(data.get("line_items", [])):
            desc = item.get("description", f"Item {i+1}") or f"Item {i+1}"
            price = item.get("total_price", "N/A")
            with st.expander(f"{desc} - {price}"):
                st.write(f"**Description:** {desc}")
                st.write(f"**Quantity:** {item.get('quantity', 'N/A')}")
                st.write(f"**Unit Price:** {item.get('unit_price', 'N/A')}")
                st.write(f"**Total Price:** {price}")

        st.divider()
        st.subheader("Summary")
        st.write(f"**Subtotal:** {data.get('subtotal', 'N/A')}")
        st.write(f"**Tax:** {data.get('total_tax_amount', 'N/A')}")
        if data.get("total_discount_amount"):
            st.write(f"**Discount:** {data['total_discount_amount']}")
        st.write(f"**Total Amount:** {data.get('total_amount', 'N/A')}")

    with st.expander("View Raw Extracted JSON Data"):
        st.json(data)