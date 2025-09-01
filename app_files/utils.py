import streamlit as st

def format_currency(amount, currency_symbol="$"):
    """Format amount as currency string"""
    return f"{currency_symbol}{amount:,.2f}"

def reset_session_state():
    """Reset all session state variables"""
    keys_to_reset = ['step', 'selected_modules', 'selected_package']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

def calculate_savings(base_cost, discounted_cost):
    """Calculate savings percentage"""
    if base_cost == 0:
        return 0
    return ((base_cost - discounted_cost) / base_cost) * 100

def format_percentage(percentage):
    """Format percentage for display"""
    return f"{percentage:.1f}%"

def validate_order_input(orders):
    """Validate order input"""
    if orders < 0:
        st.error("Order count cannot be negative")
        return False
    if orders > 10000:
        st.warning("Very high order count - please verify this is correct")
    return True
