# SaaS Pricing Calculator

A Streamlit application for calculating SaaS pricing based on modular packages and order volume.

## Features

- **Modular Selection**: Choose from various modules like Marketplace, Installation, Analytics, etc.
- **Package Tiers**: Different pricing tiers based on order volume with overage fees
- **External Fees**: Calculate third-party service costs that are facilitated but not revenue-generating
- **Interactive Calculator**: Real-time cost calculation based on expected order volume
- **Cost Projections**: View cost breakdowns across different order volumes

## Project Structure

```
PrisBeregner/
├── app.py                    # Main Streamlit application
├── pricing_config.py         # Configuration for modules, packages, and external fees
├── pricing_calculator.py     # Business logic for price calculations
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd PrisBeregner
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the displayed URL (typically `http://localhost:8501`)

## Usage

### Step 1: Module Selection
- Choose from available modules (Marketplace, Installation, Analytics, etc.)
- Each module has a base monthly price
- Multiple modules can be selected

### Step 2: Package Selection
- Select a package tier based on expected order volume:
  - Starter (<25 orders): $49/month + $2.50 overage
  - Professional (<50 orders): $89/month + $2.25 overage
  - Business (<100 orders): $149/month + $2.00 overage
  - Enterprise (<250 orders): $299/month + $1.75 overage
  - Enterprise Plus (<500 orders): $499/month + $1.50 overage
  - Custom (500+ orders): $899/month + $1.25 overage

### Step 3: Cost Calculator
- Enter expected monthly order volume
- Select optional external fees
- View real-time cost breakdown
- See cost projections for different order volumes

## Configuration

### Adding New Modules
Edit `pricing_config.py` and add to the `MODULES` dictionary:

```python
"New Module": {
    "base_price": 199,
    "description": "Description of the new module"
}
```

### Adding New Package Tiers
Edit `pricing_config.py` and add to the `PACKAGE_SIZES` dictionary:

```python
"New Tier (<X orders)": {
    "monthly_fee": 199,
    "order_limit": 75,
    "overage_fee": 2.00
}
```

### Adding External Fees
Edit `pricing_config.py` and add to the `EXTERNAL_FEES` dictionary:

```python
"New External Fee": {
    "type": "fixed",  # or "per_order"
    "amount": 29,
    "description": "Description of the external fee"
}
```

## Cost Breakdown

The application calculates:

1. **Base Module Costs**: Sum of selected module monthly fees
2. **Package Fee**: Monthly fee for the selected package tier
3. **Overage Costs**: Additional fees for orders exceeding package limits
4. **External Fees**: Third-party service costs

**Total Monthly Cost** = Base Modules + Package Fee + Overage + External Fees

## Development

The application is built with:
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and display
- **Python**: Backend logic and calculations

To extend the application:
1. Modify `pricing_config.py` for pricing changes
2. Update `pricing_calculator.py` for new calculation logic
3. Enhance `app.py` for UI improvements
