# tax_calculations.py
# All tax calculation logic in ONE place

def get_float(value_str):
    """Convert string to float, handling commas and empty values"""
    if not value_str:
        return 0.0
    value_str = str(value_str).replace(',', '')
    try:
        return float(value_str)
    except ValueError:
        return 0.0

def calculate_tax_slab(taxable_income):
    """Calculate tax based on NEW tax slabs"""
    if taxable_income <= 600000:
        return 0
    elif taxable_income <= 1200000:
        return (taxable_income - 600000) * 0.01
    elif taxable_income <= 2200000:
        return 6000 + (taxable_income - 1200000) * 0.11
    elif taxable_income <= 3200000:
        return 116000 + (taxable_income - 2200000) * 0.23
    elif taxable_income <= 4100000:
        return 346000 + (taxable_income - 3200000) * 0.30
    else:
        return 616000 + (taxable_income - 4100000) * 0.35

def calculate_tax_credit(tax_before_credits, taxable_income, amount, limit_percentage):
    """Calculate tax credit using formula: (A/B) × C"""
    if taxable_income <= 0 or tax_before_credits <= 0:
        return 0
    
    A = tax_before_credits
    B = taxable_income
    C = min(amount, taxable_income * (limit_percentage / 100))
    
    tax_credit = (A / B) * C
    return min(tax_credit, tax_before_credits)

def calculate_pension_tax(pension_amount, age, retirement_status):
    """Calculate pension tax based on rules"""
    pension_tax = 0
    
    if retirement_status == 'retired':
        if age >= 70:
            pension_tax = 0
        elif pension_amount > 10000000:
            pension_tax = pension_amount * 0.05
        else:
            pension_tax = 0
    else:
        pension_tax = 0
    
    return pension_tax

def calculate_advance_tax_logic(form_data):
    """
    Main tax calculation logic.
    Takes form data dictionary, returns response dictionary.
    """
    try:
        # --- GROSS SALARY COMPONENTS ---
        basic_salary = get_float(form_data.get('salary', '0'))
        utility = get_float(form_data.get('utility', '0'))
        house_rent = get_float(form_data.get('house_rent', '0'))
        medical = get_float(form_data.get('medical', '0'))
        other_allowances = get_float(form_data.get('other_allowances', '0'))
        
        total_gross = basic_salary + utility + house_rent + medical + other_allowances
        
        # --- CASH BENEFITS ---
        lfa = get_float(form_data.get('lfa', '0'))
        bonus = get_float(form_data.get('bonus', '0'))
        fuel_allowance = get_float(form_data.get('fuel_allowance', '0'))
        special_work_allowance = get_float(form_data.get('special_work_allowance', '0'))
        overtime = get_float(form_data.get('overtime', '0'))
        vehicle_purchase = get_float(form_data.get('vehicle_purchase', '0'))
        house_loan_subsidy = get_float(form_data.get('house_loan_subsidy', '0'))
        obligations_paid = get_float(form_data.get('obligations_paid', '0'))
        salary_tax_paid = get_float(form_data.get('salary_tax_paid', '0'))
        termination_amount = get_float(form_data.get('termination_amount', '0'))
        other_cash = get_float(form_data.get('other_cash', '0'))
        
        total_cash = (lfa + bonus + fuel_allowance + special_work_allowance + 
                     overtime + vehicle_purchase + house_loan_subsidy + 
                     obligations_paid + salary_tax_paid + termination_amount + 
                     other_cash)
        
        # --- PERKS (AUTOMATIC CALCULATIONS) ---
        # 1. Servant Salaries
        servant_salary_paid = get_float(form_data.get('servant_salary_paid', '0'))
        servant_employee_contribution = get_float(form_data.get('servant_employee_contribution', '0'))
        servant_salary = max(0, servant_salary_paid - servant_employee_contribution)
        
        # 2. Kids Education
        kids_education = get_float(form_data.get('kids_education', '0'))
        
        # 3. Car Lease
        car_lease = get_float(form_data.get('car_lease', '0'))
        
        # 4. Utility Reimbursement
        utility_reimbursement = get_float(form_data.get('utility_reimbursement', '0'))
        
        # 5. Company Car (Note #2) - Fixed: Only if vehicle provided
        vehicle_cost = get_float(form_data.get('vehicle_cost', '0'))
        vehicle_usage_type = form_data.get('vehicle_usage_type', 'personal_only')
        company_car_value = 0

        if vehicle_cost > 0:
            if vehicle_usage_type == 'personal_only':
                company_car_value = vehicle_cost * 0.10
            else:  # mixed_use
                company_car_value = vehicle_cost * 0.05

        # ===== COMPLETE PROVIDENT FUND CALCULATION =====
        # Get PF type and amounts
        pf_type = form_data.get('pf_type', 'government')
        employer_pf_contribution = get_float(form_data.get('employer_pf_contribution', '0'))
        pf_interest = get_float(form_data.get('pf_interest', '0'))
        pf_accumulated_balance = get_float(form_data.get('pf_accumulated_balance', '0'))

        # Initialize total taxable from PF
        provident_fund_taxable = 0

        if pf_type == 'government':
            # Government PF: ALL amounts 100% exempt
            provident_fund_taxable = 0
            
        elif pf_type == 'recognized':
            # Recognized PF by FBR
            
            # 1. EMPLOYER CONTRIBUTION (Clause 3a)
            # Exempt up to LOWER of: 150,000 OR 10% of basic salary
            exemption_employer = min(150000, basic_salary * 0.10)
            taxable_employer = max(0, employer_pf_contribution - exemption_employer)
            
            # 2. INTEREST ON PF
            # Exempt up to HIGHER of: 
            #   - 16% yearly interest on accumulated balance
            #   - 1/3 of basic salary
            interest_exempt_option1 = pf_accumulated_balance * 0.16  # 16% of balance
            interest_exempt_option2 = basic_salary * (1/3)  # 1/3 of basic salary
            exemption_interest = max(interest_exempt_option1, interest_exempt_option2)
            taxable_interest = max(0, pf_interest - exemption_interest)
            
            # Total taxable from Recognized PF
            provident_fund_taxable = taxable_employer + taxable_interest
            
        elif pf_type == 'unrecognized':
            # Unrecognized PF: Entire balance received is taxable
            provident_fund_taxable = pf_accumulated_balance

        # For backward compatibility
        provident_fund_excess = provident_fund_taxable
        
        # 7. Housing Facility (Note #1) - Fixed: Only if housing provided
        fair_market_rent = get_float(form_data.get('fair_market_rent', '0'))
        housing_facility = 0
        
        if fair_market_rent > 0:
            housing_facility = max(fair_market_rent, basic_salary * 0.45)
        
        # 8. Concessional Loan (Note #5)
        loan_amount = get_float(form_data.get('loan_amount', '0'))
        actual_interest_rate = get_float(form_data.get('actual_interest_rate', '0')) / 100
        concessional_loan = 0

        if loan_amount > 0:  # Only if there's a loan
            benchmark_rate = 0.10  # FBR 10% benchmark
            
            if actual_interest_rate < benchmark_rate:
                # Calculate difference between 10% and actual rate
                rate_difference = benchmark_rate - actual_interest_rate
                concessional_loan = rate_difference * loan_amount
        
        # 9. Asset Transfer
        asset_transfer = get_float(form_data.get('asset_transfer', '0'))
        
        # 10. Any Other Perk
        any_other_perk = get_float(form_data.get('any_other_perk', '0'))
        
        # Total Perks
        total_perks = (servant_salary + kids_education + car_lease + 
                      utility_reimbursement + company_car_value + 
                      provident_fund_excess + housing_facility + 
                      concessional_loan + asset_transfer + any_other_perk)
        
        # --- GET PENSION DATA EARLIER ---
        pension_amount = get_float(form_data.get('pension_amount', '0'))
        age = get_float(form_data.get('age', '0'))
        retirement_status = form_data.get('retirement_status', 'retired')
        receiving_pension = form_data.get('receiving_pension', 'no')  # Add this field to HTML
        
        # --- CALCULATE TAXABLE INCOME (with pension if employed) ---
        # Initial taxable income
        taxable_income_before = total_gross + total_cash + total_perks
        
        # ADD PENSION TO TAXABLE INCOME IF:
        # 1. Person is still employed AND
        # 2. They are receiving pension
        if retirement_status == 'still_employed' and receiving_pension == 'yes':
            taxable_income_before += pension_amount
        
        # --- DEDUCTIONS/EXEMPTIONS ---
        zakat = get_float(form_data.get('zakat', '0'))

        # Education Expenses (Section 60D)
        education_expenses_input = get_float(form_data.get('education_expenses', '0'))
        num_children = int(form_data.get('num_children', '0'))

        # Initialize education deduction
        education_expenses = 0

        # Rule: Only if taxable income ≤ Rs 1.5 million
        if taxable_income_before <= 1500000:  # 1.5 million
            # Calculate the THREE limits
            limit1 = education_expenses_input * 0.05      # 5% of fee paid
            limit2 = taxable_income_before * 0.25         # 25% of taxable income
            limit3 = 60000 * num_children                 # Rs 60,000 × number of children
            
            # Allowed amount is the LOWEST of three limits
            allowed_amount = min(limit1, limit2, limit3)
            
            # Actual deduction (cannot exceed amount paid)
            education_expenses = min(education_expenses_input, allowed_amount)
        else:
            # If income > 1.5 million, NO deduction allowed
            education_expenses = 0

        # Medical Expenses (Clause 139)
        medical_expenses_input = get_float(form_data.get('medical_expenses', '0'))
        medical_exemption_limit = basic_salary * 0.10
        medical_expenses = min(medical_expenses_input, medical_exemption_limit)

        total_exemptions = zakat + education_expenses + medical_expenses
        
        # --- TAX CREDITS INPUT ---
        charity_input = get_float(form_data.get('charity_credit', '0'))
        pension_input = get_float(form_data.get('pension_credit', '0'))
        house_loan_input = get_float(form_data.get('house_loan_interest_credit', '0'))
        
        # --- ADJUSTABLE TAXES ---
        annual_token_tax = get_float(form_data.get('annual_token_tax', '0'))
        vehicle_purchase_tax = get_float(form_data.get('vehicle_purchase_tax', '0'))
        cash_withdrawal_tax = get_float(form_data.get('cash_withdrawal_tax', '0'))
        electricity_bill_tax = get_float(form_data.get('electricity_bill_tax', '0'))
        property_purchase_tax = get_float(form_data.get('property_purchase_tax', '0'))
        property_sale_tax = get_float(form_data.get('property_sale_tax', '0'))
        foreign_txn_tax = get_float(form_data.get('foreign_txn_tax', '0'))
        telecom_tax = get_float(form_data.get('telecom_tax', '0'))
        function_tax = get_float(form_data.get('function_tax', '0'))
        
        total_adjustments = (annual_token_tax + vehicle_purchase_tax + 
                           cash_withdrawal_tax + electricity_bill_tax + 
                           property_purchase_tax + property_sale_tax + 
                           foreign_txn_tax + telecom_tax + function_tax)
        
        # --- MAIN CALCULATIONS ---
        # Apply deductions to get final taxable income
        taxable_income_after = max(0, taxable_income_before - total_exemptions)
        
        # Calculate tax on taxable income
        regular_tax = calculate_tax_slab(taxable_income_after)
        
        # Tax credits (FIXED: House loan is 30%, not 20%)
        charity_credit = calculate_tax_credit(regular_tax, taxable_income_after, charity_input, 30)  # 30% - Correct
        pension_credit = calculate_tax_credit(regular_tax, taxable_income_after, pension_input, 20)  # 20% - Correct
        house_loan_credit = calculate_tax_credit(regular_tax, taxable_income_after, house_loan_input, 30)  # 30% - FIXED
        
        total_credits = charity_credit + pension_credit + house_loan_credit
        tax_after_credits = max(0, regular_tax - total_credits)
        
        # Pension tax (only for retired people)
        pension_tax_amount = 0
        if retirement_status == 'retired':
            pension_tax_amount = calculate_pension_tax(pension_amount, age, retirement_status)
        
        # Total tax
               # Total tax liability before adjustments
        total_tax_liability = tax_after_credits + pension_tax_amount
        
        # SIMPLE FIX: Allow negative values (refund) in net_tax
        net_tax = total_tax_liability - total_adjustments
        
        # Prepare response
        response = {
            'total_gross': round(total_gross, 2),
            'total_cash': round(total_cash, 2),
            'total_perks': round(total_perks, 2),
            'total_exemptions': round(total_exemptions, 2),
            'total_credits': round(total_credits, 2),
            'total_adjustments': round(total_adjustments, 2),
            'taxable_income_before': round(taxable_income_before, 2),
            'taxable_income_after': round(taxable_income_after, 2),
            'tax': round(regular_tax, 2),
            'tax_after_credits': round(tax_after_credits, 2),
            'pension_tax': round(pension_tax_amount, 2),
            'total_tax_liability': round(total_tax_liability, 2),
            'net_tax': round(net_tax, 2),
            'charity_credit': round(charity_credit, 2),
            'pension_credit': round(pension_credit, 2),
            'house_loan_credit': round(house_loan_credit, 2),
            'pension_amount': round(pension_amount, 2),
            'age': int(age),
            'retirement_status': retirement_status,
            'receiving_pension': receiving_pension,  # Add this to response
            'auto_calculated': True
        }
        
        return response
        
    except Exception as e:
        import traceback
        error_msg = f"Calculation error: {str(e)}\n{traceback.format_exc()}"
        raise Exception(error_msg)