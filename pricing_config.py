# Pricing Configuration for SaaS Calculator

# Package size definitions - different tiers based on order volume
PACKAGE_SIZES = {
    "Starter (<25 orders)": {
        "order_limit": 25,
        "overage_fee": 500
    },
    "Professional (<100 orders)": {
        "order_limit": 100,
        "overage_fee": 400
    },
    "Business (<200 orders)": {
        "order_limit": 200,
        "overage_fee": 300
    },
    "Enterprise (<500 orders)": {
        "order_limit": 250,
        "overage_fee": 200
    }
}

# Module definitions with tiered pricing based on package size
MODULES = {
    "System Access": {
        "description": "Mandatory system access for all users",
        "prices": {
            "Starter (<25 orders)": 7000,
            "Professional (<100 orders)": 19000,
            "Business (<200 orders)": 32000,
            "Enterprise (<500 orders)": 41000
        }
    },
    "API Integration": {
        "description": "Access to the Nordic Charge API",
        "prices": {
            "Starter (<25 orders)": 1000,
            "Professional (<100 orders)": 1500,
            "Business (<200 orders)": 2000,
            "Enterprise (<500 orders)": 2000
        }
    },
    "Charge Point Transfer": {
        "description": "Integrated transfer module of charge point service subscriptions",
        "prices": {
            "Starter (<25 orders)": 2000,
            "Professional (<100 orders)": 4000,
            "Business (<200 orders)": 6000,
            "Enterprise (<500 orders)": 8000
        }
    },
    "Inventory Management": {
        "description": "Storage handling and inventory tracking system",
        "prices": {
            "Starter (<25 orders)": 1500,
            "Professional (<100 orders)": 3000,
            "Business (<200 orders)": 5000,
            "Enterprise (<500 orders)": 7500
        }
    },
    "Return Management": {
        "description": "Return handling system for return orders of used chargers",
        "prices": {
            "Starter (<25 orders)": 2000,
            "Professional (<100 orders)": 4000,
            "Business (<200 orders)": 6000,
            "Enterprise (<500 orders)": 8000
        }
    },
        "Technical Support": {
        "description": "Technical support services for charger related issues",
        "prices": {
            "Starter (<25 orders)": 2000,
            "Professional (<100 orders)": 2000,
            "Business (<200 orders)": 2000,
            "Enterprise (<500 orders)": 2000
        }
    },
    "Installation Network": {
        "description": "Access to the Nordic Charge installation network",
        "prices": {
            "Starter (<25 orders)": 2000,
            "Professional (<100 orders)": 2000,
            "Business (<200 orders)": 2000,
            "Enterprise (<500 orders)": 2000
        }
    },
    "Marketplace": {
        "description": "Access to the Nordic Charge marketplace for hardware procurement",
        "prices": {
            "Starter (<25 orders)": 2000,
            "Professional (<100 orders)": 2000,
            "Business (<200 orders)": 2000,
            "Enterprise (<500 orders)": 2000
        }
    }
}

# External fees - third-party services that we facilitate but don't receive revenue from
EXTERNAL_FEES = {
    "Standard installation": {
        "type": "per_order",
        "amount": 2600,
        "description": "Standard installation cost per charger"
    },
    "NexBlue Edge": {
        "type": "per_order",
        "amount": 2500,
        "description": "SMS notifications for order updates"
    },
    "Zaptec Go": {
        "type": "per_order",
        "amount": 3019,
        "description": "Monthly email service subscription"
    }
}
