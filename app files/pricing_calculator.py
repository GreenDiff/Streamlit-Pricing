from pricing_config import MODULES, PACKAGE_SIZES

class PricingCalculator:
    
    def __init__(self, selected_modules, selected_package):
        self.selected_modules = selected_modules
        self.selected_package = selected_package
        self.package_info = PACKAGE_SIZES[selected_package]
    
    def calculate_cost_for_package(self, package_name, expected_orders):
        """Calculate total cost for a specific package and order volume"""
        package_info = PACKAGE_SIZES[package_name]
        
        # Calculate base module costs for this package
        base_modules = 0
        for module_name in self.selected_modules:
            if module_name in MODULES:
                module_price = MODULES[module_name]['prices'][package_name]
                base_modules += module_price
        
        # Calculate overage costs
        order_limit = package_info['order_limit']
        overage_fee = package_info['overage_fee']
        
        if expected_orders > order_limit:
            overage_orders = expected_orders - order_limit
            overage_cost = overage_orders * overage_fee
        else:
            overage_orders = 0
            overage_cost = 0
        
        total_cost = base_modules + overage_cost
        
        return {
            'package_name': package_name,
            'base_modules': base_modules,
            'overage_orders': overage_orders,
            'overage_cost': overage_cost,
            'total': total_cost
        }
    
    def find_optimal_package(self, expected_orders):
        """Find the most cost-effective package for the given order volume"""
        package_costs = {}
        package_names = list(PACKAGE_SIZES.keys())
        
        # Calculate costs for all packages
        for package_name in package_names:
            cost_info = self.calculate_cost_for_package(package_name, expected_orders)
            package_costs[package_name] = cost_info
        
        # Find the package with minimum total cost
        optimal_package = min(package_costs.keys(), key=lambda pkg: package_costs[pkg]['total'])
        
        return {
            'optimal_package': optimal_package,
            'cost_breakdown': package_costs[optimal_package],
            'all_package_costs': package_costs,
            'savings': self._calculate_savings(package_costs, optimal_package)
        }
    
    def _calculate_savings(self, package_costs, optimal_package):
        """Calculate savings compared to other packages"""
        optimal_cost = package_costs[optimal_package]['total']
        savings_info = {}
        
        for package_name, cost_info in package_costs.items():
            if package_name != optimal_package:
                savings = cost_info['total'] - optimal_cost
                if savings > 0:
                    savings_info[package_name] = {
                        'monthly_savings': savings,
                        'yearly_savings': savings * 12,
                        'percentage': (savings / cost_info['total']) * 100
                    }
        
        return savings_info
    
    def should_upgrade_package(self, expected_orders):
        """Check if current package should be upgraded for better cost efficiency"""
        current_cost = self.calculate_monthly_cost(expected_orders)
        optimal_info = self.find_optimal_package(expected_orders)
        
        optimal_package = optimal_info['optimal_package']
        optimal_cost = optimal_info['cost_breakdown']['total']
        
        should_upgrade = optimal_package != self.selected_package
        
        if should_upgrade:
            monthly_savings = current_cost['total'] - optimal_cost
            return {
                'should_upgrade': True,
                'current_package': self.selected_package,
                'recommended_package': optimal_package,
                'current_cost': current_cost['total'],
                'recommended_cost': optimal_cost,
                'monthly_savings': monthly_savings,
                'yearly_savings': monthly_savings * 12,
                'savings_percentage': (monthly_savings / current_cost['total']) * 100,
                'upgrade_reason': self._get_upgrade_reason(current_cost, optimal_info['cost_breakdown'])
            }
        else:
            return {
                'should_upgrade': False,
                'current_package': self.selected_package,
                'current_cost': current_cost['total']
            }
    
    def _get_upgrade_reason(self, current_cost, optimal_cost):
        """Generate human-readable reason for package upgrade"""
        if optimal_cost['overage_cost'] < current_cost['overage_cost']:
            return f"High overage fees (DKK{current_cost['overage_cost']:,.0f}) make upgrade cost-effective"
        elif optimal_cost['base_modules'] + optimal_cost['overage_cost'] < current_cost['total']:
            return "Better module pricing at higher tier reduces total cost"
        else:
            return "Overall cost optimization through package upgrade"
    
    def calculate_base_module_cost(self):
        total = 0
        for module_name in self.selected_modules:
            if module_name in MODULES:
                # Get the price for this module at the selected package tier
                module_price = MODULES[module_name]['prices'][self.selected_package]
                total += module_price
        return total
    
    def calculate_overage_cost(self, actual_orders):
        order_limit = self.package_info['order_limit']
        overage_fee = self.package_info['overage_fee']
        
        if actual_orders > order_limit:
            overage_orders = actual_orders - order_limit
            overage_cost = overage_orders * overage_fee
        else:
            overage_orders = 0
            overage_cost = 0
        
        return {
            'overage_orders': overage_orders,
            'overage_cost': overage_cost
        }
    
    def calculate_monthly_cost(self, expected_orders):
        # Base module costs
        base_modules = self.calculate_base_module_cost()
        
        # Overage costs
        overage_info = self.calculate_overage_cost(expected_orders)
        
        # Total calculation (no package fee anymore)
        total = base_modules + overage_info['overage_cost']
        
        return {
            'base_modules': base_modules,
            'overage_orders': overage_info['overage_orders'],
            'overage_cost': overage_info['overage_cost'],
            'total': total
        }
    
    def get_package_details(self):
        return {
            'name': self.selected_package,
            'order_limit': self.package_info['order_limit'],
            'overage_fee': self.package_info['overage_fee']
        }
    
    def get_selected_modules_info(self):
        modules_info = {}
        for module_name in self.selected_modules:
            if module_name in MODULES:
                modules_info[module_name] = MODULES[module_name]
        return modules_info
    
    def calculate_yearly_cost(self, expected_orders):
        monthly_costs = self.calculate_monthly_cost(expected_orders)
        
        return {
            'base_modules_yearly': monthly_costs['base_modules'] * 12,
            'overage_cost_yearly': monthly_costs['overage_cost'] * 12,
            'total_yearly': monthly_costs['total'] * 12
        }
