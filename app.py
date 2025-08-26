import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pricing_config import MODULES, PACKAGE_SIZES, EXTERNAL_FEES
from pricing_calculator import PricingCalculator

def main():
    st.set_page_config(
        page_title="Nordic Charge",
        page_icon="logo.png",  # Replace with your logo file path
        layout="wide"
    )

    # Header with logo
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            st.image("logo.png", width=1000)  # Adjust width as needed
        except:
            st.write("🏢")  # Fallback if logo not found
    with col2:
        st.title("")
    
    st.markdown("---")
    
    # Initialize session state
    if 'selected_modules' not in st.session_state:
        st.session_state.selected_modules = ["System Access"]  # Always include System Access
    elif "System Access" not in st.session_state.selected_modules:
        st.session_state.selected_modules.append("System Access")  # Ensure it's always present
    if 'selected_package' not in st.session_state:
        st.session_state.selected_package = "Starter (<25 orders)"
    
    # Single-step module and package selection
    show_pricing_configurator()

def show_pricing_configurator():
    st.header("Select your package tier and modules to see pricing")
    st.subheader("Note all prices are excluded VAT")
    
    # Create two columns for package selection and module selection
    col_package, col_modules = st.columns([1, 2])
    
    with col_package:
        st.subheader("📦 Select Package Tier")
        
        # Package selection
        package_options = list(PACKAGE_SIZES.keys())
        selected_package = st.selectbox(
            "Choose your package size:",
            options=package_options,
            index=package_options.index(st.session_state.selected_package),
            help="Higher tiers offer better overage rates and module pricing"
        )
        
        # Update session state
        st.session_state.selected_package = selected_package
        
        # Show package details
        package_info = PACKAGE_SIZES[selected_package]
        
        st.metric("Order Limit", f"{package_info['order_limit']} orders/month")
        st.metric("Overage Fee", f"DKK{package_info['overage_fee']}/order")
        
        # Show total monthly cost preview
        if st.session_state.selected_modules:
            total_module_cost = sum(MODULES[module]['prices'][selected_package] 
                                  for module in st.session_state.selected_modules)
            st.metric("**Monthly Module Cost**", f"**DKK{total_module_cost:,}**")
            st.caption(f"Based on {len(st.session_state.selected_modules)} selected modules")
        else:
            st.info("Select modules to see total cost")
    
    with col_modules:
        st.subheader("🔧 Select Modules")
        
        # Create a grid for modules
        col1, col2 = st.columns(2)
        
        selected_modules = st.session_state.selected_modules.copy()
        
        with col1:
            for i, (module_name, module_info) in enumerate(MODULES.items()):
                if i % 2 == 0:
                    module_price = module_info['prices'][selected_package]
                    
                    # Special handling for mandatory System Access module
                    if module_name == "System Access":
                        is_selected = st.checkbox(
                            f"**{module_name}** (Mandatory)",
                            key=f"module_{module_name}",
                            value=True,
                            disabled=True  # Cannot be deselected
                        )
                        # Always ensure System Access is in selected modules
                        if module_name not in selected_modules:
                            selected_modules.append(module_name)
                    else:
                        # Regular checkbox for optional modules
                        is_selected = st.checkbox(
                            f"**{module_name}**",
                            key=f"module_{module_name}",
                            value=module_name in st.session_state.selected_modules
                        )
                        
                        if is_selected and module_name not in selected_modules:
                            selected_modules.append(module_name)
                        elif not is_selected and module_name in selected_modules:
                            selected_modules.remove(module_name)
                    
                    if is_selected:
                        st.success(f" DKK{module_price:,}/month")
                    else:
                        st.write(f" DKK{module_price:,}/month")
                    
                    st.caption(module_info['description'])
                    st.markdown("---")
        
        with col2:
            for i, (module_name, module_info) in enumerate(MODULES.items()):
                if i % 2 == 1:
                    module_price = module_info['prices'][selected_package]
                    
                    # Special handling for mandatory System Access module
                    if module_name == "System Access":
                        is_selected = st.checkbox(
                            f"**{module_name}** (Mandatory)",
                            key=f"module_{module_name}",
                            value=True,
                            disabled=True  # Cannot be deselected
                        )
                        # Always ensure System Access is in selected modules
                        if module_name not in selected_modules:
                            selected_modules.append(module_name)
                    else:
                        # Regular checkbox for optional modules
                        is_selected = st.checkbox(
                            f"**{module_name}**",
                            key=f"module_{module_name}",
                            value=module_name in st.session_state.selected_modules
                        )
                        
                        if is_selected and module_name not in selected_modules:
                            selected_modules.append(module_name)
                        elif not is_selected and module_name in selected_modules:
                            selected_modules.remove(module_name)
                    
                    if is_selected:
                        st.success(f" DKK{module_price:,}/month")
                    else:
                        st.write(f" DKK{module_price:,}/month")
                    
                    st.caption(module_info['description'])
                    st.markdown("---")
        
        # Update session state
        st.session_state.selected_modules = selected_modules
    
    # Show detailed calculator since System Access is always selected
    st.markdown("---")
    show_pricing_calculator()

def show_pricing_calculator():
    st.header("Your Pricing Summary & Calculator")
    
    calculator = PricingCalculator(
        st.session_state.selected_modules,
        st.session_state.selected_package
    )
    
    # Show configuration summary
    with st.expander("📋 Configuration Summary", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Selected Modules:")
            for module in st.session_state.selected_modules:
                module_info = MODULES[module]
                module_price = module_info['prices'][st.session_state.selected_package]
                st.write(f"• **{module}**: DKK{module_price:,}/month")
            
            # Show total module cost
            total_module_cost = sum(MODULES[module]['prices'][st.session_state.selected_package] 
                                  for module in st.session_state.selected_modules)
            st.write(f"**Total Module Cost: DKK{total_module_cost:,}/month**")
        
        with col2:
            st.subheader("Package Details:")
            package_info = PACKAGE_SIZES[st.session_state.selected_package]
            st.write(f"**{st.session_state.selected_package}**")
            st.write(f"• Order limit: {package_info['order_limit']} orders")
            st.write(f"• Overage fee: DKK{package_info['overage_fee']}/order")
        
    # Customer Revenue Calculator
    st.markdown("---")
    st.header("💰 Customer Revenue Calculator")
    st.subheader("Calculate your potential revenue from charge point subscriptions:")
    
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        st.subheader("💵 Pricing Structure")
        monthly_subscription_fee = st.number_input(
            "Monthly subscription (DKK/customer):",
            min_value=0.0,
            value=39.0,
            step=10.0,
            help="How much you charge customers per charge point per month"
        )
        
        one_time_setup_fee = st.number_input(
            "Setup fee (DKK):",
            min_value=0.0,
            value=6000.0,
            step=100.0,
            help="Initial setup or installation fee charged to customers"
        )
        
        st.subheader("**⚡ Electricity Revenue**")
        kwh_addon_price = st.number_input(
            "kWh add-on (DKK/kWh):",
            min_value=0.0,
            value=0.00,
            step=0.05,
            help="Your markup/profit per kWh of electricity sold to customers"
        )
        
        kwh_per_customer_monthly = st.number_input(
            "kWh/customer/month:",
            min_value=0.0,
            value=400.0,
            step=50.0,
            help="Expected monthly electricity consumption per active customer"
        )
    
    with col2:
        st.subheader("📈 Business Forecast")
        existing_customers = st.number_input(
            "Current customers:",
            min_value=0,
            value=0,
            step=50,
            help="Number of customers you already have with active subscriptions"
        )
        
        customers_month_1 = st.number_input(
            "New customers Month 1:",
            min_value=0,
            value=20,
            step=5
        )
        
        monthly_growth_rate = st.number_input(
            "Growth rate (%):",
            min_value=0.0,
            value=5.0,
            step=1.0,
            help="Expected percentage growth in new customers each month"
        ) / 100
        
        growth_cap = st.number_input(
            "Growth cap (max new customers/month):",
            min_value=0,
            value=0,
            step=50,
            help="Maximum new customers per month (0 = no cap). Growth flattens when this limit is reached."
        )
        
        customer_retention_rate = st.number_input(
            "Retention rate (%):",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            help="Percentage of customers that continue their subscription each month"
        ) / 100
        
        forecast_months = st.number_input(
            "Forecast (months):",
            min_value=1,
            max_value=60,
            value=24,
            step=12
        )
        
        st.markdown("**🔌 Hardware**")
        charger_type = st.radio(
            "Charger type:",
            options=["NexBlue Edge", "Zaptec Go"],
            help="Choose which charger type you'll provide to new customers"
        )
        
        # Calculate variable costs per customer
        standard_installation_cost = EXTERNAL_FEES["Standard installation"]["amount"]
        charger_cost = EXTERNAL_FEES[charger_type]["amount"]
        variable_cost_per_customer = standard_installation_cost + charger_cost
        
        # Display variable cost breakdown
        st.caption(f"🔧 Installation: DKK{standard_installation_cost:,}")
        st.caption(f"⚡ {charger_type}: DKK{charger_cost:,}")
        st.metric("Variable Cost/Customer", f"DKK{variable_cost_per_customer:,}")
    
    with col3:
        # Calculate revenue projections
        st.subheader("📊 Revenue Projection")
        
        # Calculate monthly projections
        months = []
        new_customers = []
        total_active_customers = []
        monthly_recurring_revenue = []
        electricity_revenue = []  # New electricity revenue stream
        one_time_revenue = []
        total_monthly_revenue = []
        
        active_customers = existing_customers  # Start with existing customer base
        
        for month in range(1, forecast_months + 1):
            # Calculate new customers for this month with growth cap
            uncapped_new_cust = customers_month_1 * ((1 + monthly_growth_rate) ** (month - 1))
            
            # Apply growth cap if set (0 means no cap)
            if growth_cap > 0:
                new_cust = min(uncapped_new_cust, growth_cap)
            else:
                new_cust = uncapped_new_cust
                
            new_customers.append(int(new_cust))
            
            # Update active customers (existing/previous retained + new)
            active_customers = (active_customers * customer_retention_rate) + new_cust
            total_active_customers.append(int(active_customers))
            
            # Calculate revenues
            mrr = active_customers * monthly_subscription_fee
            electricity_rev = active_customers * kwh_per_customer_monthly * kwh_addon_price  # New electricity revenue
            one_time_rev = new_cust * one_time_setup_fee  # Only new customers pay setup fee
            total_rev = mrr + electricity_rev + one_time_rev
            
            months.append(month)
            monthly_recurring_revenue.append(mrr)
            electricity_revenue.append(electricity_rev)
            one_time_revenue.append(one_time_rev)
            total_monthly_revenue.append(total_rev)
        
        # Display key metrics
        total_revenue_full_period = sum(total_monthly_revenue)  # Fix: calculate total for full period
        final_mrr = monthly_recurring_revenue[-1]
        average_monthly_revenue = total_revenue_full_period / forecast_months  # Calculate average
        total_customers_end = total_active_customers[-1]
        
        # Calculate comprehensive totals for the forecast period
        total_recurring_revenue = sum(monthly_recurring_revenue)
        total_electricity_revenue = sum(electricity_revenue)
        total_one_time_revenue = sum(one_time_revenue)
        total_new_customers = sum(new_customers)
        
        # Verify total revenue calculation (should equal subscription + electricity + one-time)
        total_revenue_verification = total_recurring_revenue + total_electricity_revenue + total_one_time_revenue
        assert abs(total_revenue_full_period - total_revenue_verification) < 0.01, "Revenue calculation mismatch!"
        
        # Calculate platform costs (including overage) for each month
        total_platform_cost_period = 0
        total_variable_cost_period = 0
        
        for i in range(len(months)):
            new_customers_month = new_customers[i]
            
            # Platform cost based on new customers per month (with automatic package optimization)
            optimal_info = calculator.find_optimal_package(new_customers_month)
            monthly_platform_cost = optimal_info['cost_breakdown']['total']
            total_platform_cost_period += monthly_platform_cost
            
            # Variable costs based on new customers only
            monthly_variable_cost = new_customers_month * variable_cost_per_customer
            total_variable_cost_period += monthly_variable_cost
        
        total_cost_period = total_platform_cost_period + total_variable_cost_period
        
        # Display comprehensive metrics in a structured way
        st.markdown("### 📊 Complete Financial Overview")
        
        # Revenue metrics
        col_rev1, col_rev2 = st.columns(2)
        with col_rev1:
            st.metric("Total Revenue", f"DKK{total_revenue_full_period:,.0f}")
            st.caption(f"Over {forecast_months} months")
        with col_rev2:
            st.metric("Total Recurring Revenue", f"DKK{total_recurring_revenue + total_electricity_revenue:,.0f}")
            st.caption("Subscription + Electricity accumulated")
        
        col_rev3, col_rev4 = st.columns(2)
        with col_rev3:
            st.metric("Total Subscription Revenue", f"DKK{total_recurring_revenue:,.0f}")
            st.caption("Monthly subscriptions accumulated over period")
        with col_rev4:
            st.metric("Total Electricity Revenue", f"DKK{total_electricity_revenue:,.0f}")
            st.caption("Electricity sales accumulated over period")
        
        col_rev5, col_rev6 = st.columns(2)
        with col_rev5:
            st.metric("Total One-time Revenue", f"DKK{total_one_time_revenue:,.0f}")
            st.caption(f"From {total_new_customers:,.0f} new customers")
        with col_rev6:
            st.metric("Average Monthly Revenue", f"DKK{average_monthly_revenue:,.0f}")
            st.caption("Mean monthly revenue over period")
        
        st.markdown("---")
        
        # Cost metrics
        col_cost1, col_cost2 = st.columns(2)
        with col_cost1:
            st.metric("Total Cost", f"DKK{total_cost_period:,.0f}")
            st.caption(f"Over {forecast_months} months")
        with col_cost2:
            st.metric("Total Platform Cost", f"DKK{total_platform_cost_period:,.0f}")
            st.caption("Base + overage fees combined")
        
        col_cost3, col_cost4 = st.columns(2)
        with col_cost3:
            st.metric("Total Variable Cost", f"DKK{total_variable_cost_period:,.0f}")
            st.caption("Installation + charger costs")
        with col_cost4:
            # Calculate average platform cost over the period
            average_platform_cost = total_platform_cost_period / forecast_months
            st.metric("Average Platform Cost", f"DKK{average_platform_cost:,.0f}")
            st.caption("Mean monthly platform cost")
        
        st.markdown("---")
        
        # Profitability summary
        total_profit_period = total_revenue_full_period - total_cost_period
        profit_margin = (total_profit_period / total_revenue_full_period * 100) if total_revenue_full_period > 0 else 0
        
        col_profit1, col_profit2 = st.columns(2)
        with col_profit1:
            if total_profit_period >= 0:
                st.metric("Total Profit", f"DKK{total_profit_period:,.0f}", delta="Profitable")
            else:
                st.metric("Total Loss", f"DKK{abs(total_profit_period):,.0f}", delta="Loss")
        with col_profit2:
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
            if profit_margin > 10:
                st.caption("🟢 Healthy margin")
            elif profit_margin > 5:
                st.caption("🟡 Moderate margin") 
            else:
                st.caption("🔴 Low margin")
        
        if existing_customers > 0:
            st.caption(f"Starting with {existing_customers:,} existing customers")
        
        # Growth cap indicator
        if growth_cap > 0:
            # Check if growth cap was reached
            max_new_customers = max(new_customers) if new_customers else 0
            cap_reached_month = next((i+1 for i, val in enumerate(new_customers) if val >= growth_cap), None)
            
            if cap_reached_month:
                st.info(f"📈 **Growth Cap Applied**: Reached {growth_cap:,} new customers/month limit in Month {cap_reached_month}")
            else:
                st.info(f"📈 **Growth Cap Set**: Maximum {growth_cap:,} new customers/month (not reached in forecast period)")
    
    # Revenue visualization
    st.markdown("---")    
    st.subheader("📈 Revenue & Cost Analysis Charts")
    
    st.info("💡 **Smart Package Optimization**: The system automatically selects the most cost-effective package tier each month based on your **new customers per month**. When overage fees exceed the cost of upgrading to a higher tier, the system automatically chooses the cheaper option.")
    
    revenue_df = pd.DataFrame({
        'Month': months,
        'New Customers': new_customers,
        'Total Active Customers': total_active_customers,
        'Monthly Recurring Revenue': monthly_recurring_revenue,
        'Electricity Revenue': electricity_revenue,
        'One-time Revenue': one_time_revenue,
        'Total Monthly Revenue': total_monthly_revenue
    })
    
    # Fixed Components chart (full width)
    st.subheader("🔧 Fixed Components")
    fig_fixed = go.Figure()
    
    # Calculate platform costs including overage for each month
    fixed_platform_costs = []
    overage_costs = []
    optimal_packages_used = []  # Track which package is optimal for each month
    
    for i in range(len(months)):
        new_customers_month = new_customers[i]
        
        # Find optimal package for this month's new customers
        optimal_info = calculator.find_optimal_package(new_customers_month)
        optimal_package = optimal_info['optimal_package']
        optimal_packages_used.append(optimal_package)
        
        # Calculate costs using optimal package
        cost_breakdown = optimal_info['cost_breakdown']
        base_cost = cost_breakdown['base_modules']
        overage_cost = cost_breakdown['overage_cost']
        
        fixed_platform_costs.append(base_cost)
        overage_costs.append(overage_cost)
    
    # Base platform cost (red) - bottom layer
    fig_fixed.add_trace(go.Bar(
        name='Base Platform Cost',
        x=revenue_df['Month'],
        y=fixed_platform_costs,
        marker_color="#1111D6",
        offsetgroup=1,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Base Platform Cost: DKK%{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    # Overage fees (blue) - stacked on top of base platform cost
    fig_fixed.add_trace(go.Bar(
        name='Overage Fees',
        x=revenue_df['Month'],
        y=overage_costs,
        marker_color='#7C99F1',
        offsetgroup=1,
        base=fixed_platform_costs,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Overage Fees: DKK%{y:,.0f}<br>' +
                     'Orders over limit: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=[max(0, new_customers[i] - PACKAGE_SIZES[optimal_packages_used[i]]['order_limit']) for i in range(len(months))]
    ))
    
    # Monthly Recurring Revenue (separate group) - bottom layer
    fig_fixed.add_trace(go.Bar(
        name='Monthly Subscription Revenue',
        x=revenue_df['Month'],
        y=revenue_df['Monthly Recurring Revenue'],
        marker_color="#63BE63",
        offsetgroup=2,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Subscription Revenue: DKK%{y:,.0f}<br>' +
                     'Active Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['Total Active Customers']
    ))
    
    # Electricity Revenue (stacked on top of subscription revenue)
    fig_fixed.add_trace(go.Bar(
        name='Electricity Revenue',
        x=revenue_df['Month'],
        y=revenue_df['Electricity Revenue'],
        marker_color='#C7F0C0',
        offsetgroup=2,
        base=revenue_df['Monthly Recurring Revenue'],
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Electricity Revenue: DKK%{y:,.0f}<br>' +
                     'Active Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['Total Active Customers']
    ))
    
    fig_fixed.update_layout(
        title='Fixed: Subscription + Electricity Revenue vs Platform Cost (Auto-Optimized Packages)',
        xaxis_title='Month',
        xaxis=dict(
            tick0=1, 
            dtick=2,  # Show x-axis ticks every 2 months
            range=[0.5, forecast_months + 0.5]  # Set proper range from 1 to forecast_months
        ),
        yaxis_title='Amount (DKK)',
        height=500,
        barmode='group'
    )
    
    st.plotly_chart(fig_fixed, use_container_width=True)
    
    # Show package optimization summary
    with st.expander("📋 Package Optimization Summary", expanded=False):
        st.write("**Optimal packages used each month (based on new customers per month):**")
        package_changes = []
        current_pkg = None
        
        for i, pkg in enumerate(optimal_packages_used):
            month = i + 1
            new_cust = new_customers[i]
            if pkg != current_pkg:
                package_changes.append(f"• **Month {month}**: Upgraded to **{pkg}** ({new_cust:,} new customers)")
                current_pkg = pkg
            elif i == 0:  # First month
                package_changes.append(f"• **Month {month}**: Started with **{pkg}** ({new_cust:,} new customers)")
        
        for change in package_changes[:5]:  # Show first 5 changes
            st.write(change)
        
        if len(package_changes) > 5:
            st.write(f"... and {len(package_changes) - 5} more package optimizations")
        
        # Show final package
        final_pkg = optimal_packages_used[-1]
        final_new_customers = new_customers[-1]
        st.write(f"**Final package**: {final_pkg} for {final_new_customers:,} new customers per month")

    # Variable Components chart (full width)
    st.subheader("📊 Variable Components")
    fig_variable = go.Figure()
    
    # Calculate variable costs for each month (based on new customers)
    variable_costs_monthly = [new_customers[i] * variable_cost_per_customer for i in range(len(months))]
    
    fig_variable.add_trace(go.Bar(
        name='Variable Costs',
        x=revenue_df['Month'],
        y=variable_costs_monthly,
        marker_color='#FF8C00',
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Variable Costs: DKK%{y:,.0f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['New Customers']
    ))
    
    fig_variable.add_trace(go.Bar(
        name='One-time Revenue',
        x=revenue_df['Month'],
        y=revenue_df['One-time Revenue'],
        marker_color="#018001",
        hovertemplate='<b>Month %{x}</b><br>' +
                     'One-time Revenue: DKK%{y:,.0f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['New Customers']
    ))
    
    fig_variable.update_layout(
        title='Variable: One-time Revenue vs Variable Costs',
        xaxis_title='Month',
        xaxis=dict(
            tick0=1, 
            dtick=2,  # Show x-axis ticks every 2 months
            range=[0.5, forecast_months + 0.5]  # Set proper range from 1 to forecast_months
        ),
        yaxis_title='Amount (DKK)',
        height=500,
        barmode='group'
    )
    
    st.plotly_chart(fig_variable, use_container_width=True)
    
    # Total Overview section (full width below the two columns)
    st.subheader("💰 Total Overview")
    fig_total = go.Figure()
    
    # Calculate total costs for each month (including overage)
    total_platform_costs_monthly = []
    for i in range(len(months)):
        new_customers_month = new_customers[i]
        # Use optimal package for each month's new customers
        optimal_info = calculator.find_optimal_package(new_customers_month)
        platform_cost = optimal_info['cost_breakdown']['total']
        total_platform_costs_monthly.append(platform_cost)
    
    total_costs_monthly = [total_platform_costs_monthly[i] + variable_costs_monthly[i] for i in range(len(months))]
    
    # Total Revenue Stack (One-time + Electricity + Subscription) - Group 1
    fig_total.add_trace(go.Bar(
        name='One-time Revenue',
        x=revenue_df['Month'],
        y=revenue_df['One-time Revenue'],
        marker_color='#018001',
        offsetgroup=1,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'One-time Revenue: DKK%{y:,.0f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['New Customers']
    ))
    
    fig_total.add_trace(go.Bar(
        name='Electricity Revenue',
        x=revenue_df['Month'],
        y=revenue_df['Electricity Revenue'],
        marker_color="#63BE63",
        offsetgroup=1,
        base=revenue_df['One-time Revenue'],
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Electricity Revenue: DKK%{y:,.0f}<br>' +
                     'Active Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['Total Active Customers']
    ))
    
    # Calculate base for subscription revenue (one-time + electricity)
    onetime_plus_electricity = [revenue_df['One-time Revenue'].iloc[i] + revenue_df['Electricity Revenue'].iloc[i] for i in range(len(months))]
    
    fig_total.add_trace(go.Bar(
        name='Monthly Subscription Revenue',
        x=revenue_df['Month'],
        y=revenue_df['Monthly Recurring Revenue'],
        marker_color='#C7F0C0',
        offsetgroup=1,
        base=onetime_plus_electricity,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Subscription Revenue: DKK%{y:,.0f}<br>' +
                     'Active Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['Total Active Customers']
    ))
    
    # Total Costs Stack (Variable + Base Platform + Overage) - Group 2
    fig_total.add_trace(go.Bar(
        name='Variable Costs',
        x=revenue_df['Month'],
        y=variable_costs_monthly,
        marker_color='#FF8C00',
        offsetgroup=2,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Variable Costs: DKK%{y:,.0f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     'Total Cost'
                     '<extra></extra>',
        customdata=revenue_df['New Customers']
    ))
    
    fig_total.add_trace(go.Bar(
        name='Base Platform Cost',
        x=revenue_df['Month'],
        y=fixed_platform_costs,
        marker_color='#1111D6',
        offsetgroup=2,
        base=variable_costs_monthly,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Base Platform Cost: DKK%{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    # Variable costs + base platform costs for overage base
    variable_plus_platform = [variable_costs_monthly[i] + fixed_platform_costs[i] for i in range(len(months))]
    
    fig_total.add_trace(go.Bar(
        name='Overage Fees',
        x=revenue_df['Month'],
        y=overage_costs,
        marker_color="#7C99F1",
        offsetgroup=2,
        base=variable_plus_platform,
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Overage Fees: DKK%{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    # Add profit line
    profit_monthly = [revenue_df['Total Monthly Revenue'].iloc[i] - total_costs_monthly[i] for i in range(len(months))]
    fig_total.add_trace(go.Scatter(
        name='Monthly Profit',
        x=revenue_df['Month'],
        y=profit_monthly,
        mode='lines+markers',
        marker_color='#FFD700',
        line=dict(width=3),
        yaxis='y2',
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Monthly Profit: DKK%{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    fig_total.update_layout(
        title='Total: Revenue Stack (Subscription + Electricity + One-time) vs Cost Stack (Auto-Optimized Packages)',
        xaxis_title='Month',
        xaxis=dict(
            tick0=1, 
            dtick=2,  # Show x-axis ticks every 2 months
            range=[0.5, forecast_months + 0.5]  # Set proper range from 1 to forecast_months
        ),
        yaxis_title='Amount (DKK)',
        yaxis2=dict(
            title='Profit (DKK)',
            overlaying='y',
            side='right'
        ),
        height=500,
        barmode='group'  # Changed to group to show separate stacks
    )
    
    st.plotly_chart(fig_total, use_container_width=True)
    
    # Customer Growth Chart (separate row)
    st.subheader("👥 Customer Growth Overview")
    
    fig_customers = go.Figure()
    
    fig_customers.add_trace(go.Scatter(
        x=revenue_df['Month'],
        y=revenue_df['Total Active Customers'],
        mode='lines+markers',
        name='Total Active Customers',
        marker_color='#1f77b4',
        line=dict(width=3),
        hovertemplate='<b>Month %{x}</b><br>' +
                     'Active Customers: %{y:,.0f}<br>' +
                     'New Customers: %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=revenue_df['New Customers']
    ))
    
    fig_customers.add_trace(go.Bar(
        x=revenue_df['Month'],
        y=revenue_df['New Customers'],
        name='New Customers',
        marker_color="#168416",
        opacity=0.5,
        yaxis='y2',
        hovertemplate='<b>Month %{x}</b><br>' +
                     'New Customers: %{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    fig_customers.update_layout(
        title='Customer Acquisition & Growth',
        xaxis_title='Month',
        xaxis=dict(
            tick0=1, 
            dtick=2,  # Show x-axis ticks every 2 months
            range=[0.5, forecast_months + 0.5]  # Set proper range from 1 to forecast_months
        ),
        yaxis_title='Total Active Customers',
        yaxis2=dict(
            title='New Customers',
            overlaying='y',
            side='right'
        ),
        height=400
    )
    
    st.plotly_chart(fig_customers, use_container_width=True)

    # Restart button
    st.markdown("---")
    if st.button("🔄 Start Over", type="secondary"):
        st.session_state.selected_modules = []
        st.session_state.selected_package = "Starter (<25 orders)"
        st.rerun()

if __name__ == "__main__":
    main()
