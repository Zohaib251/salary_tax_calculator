// IRIS Tables - Generate Table 1 (Detailed) and Table 2 (Summary)

function generateIrisTables(calculationData) {
    // Define field mappings with IRIS codes
    const fieldMappings = [
        // Gross Salary Section
        { field: "Basic Salary", code: "1009", value: calculationData.basic_salary || 0 },
        { field: "Utility Allowance", code: "1049", value: calculationData.utility || 0 },
        { field: "House Rent Allowance (HRA)", code: "1049", value: calculationData.house_rent || 0 },
        { field: "Medical Allowance", code: "1049", value: calculationData.medical || 0 },
        { field: "Other Allowances", code: "1049", value: calculationData.other_allowances || 0 },
        
        // Pension Section
        { field: "Pension Amount Received", code: "1008", value: calculationData.pension_amount || 0 },
        
        // Cash Benefits Section
        { field: "Leave Fare Assistance (LFA)", code: "1049", value: calculationData.lfa || 0 },
        { field: "Bonus", code: "1009", value: calculationData.bonus || 0 },
        { field: "Fuel Allowance", code: "1049", value: calculationData.fuel_allowance || 0 },
        { field: "Special Work Condition Allowance", code: "1049", value: calculationData.special_work_allowance || 0 },
        { field: "Overtime", code: "1049", value: calculationData.overtime || 0 },
        { field: "Lump Sum for Vehicle Purchase", code: "1059", value: calculationData.vehicle_purchase || 0 },
        { field: "House Loan Mark-up Subsidy", code: "1099", value: calculationData.house_loan_subsidy || 0 },
        { field: "Employee's Obligation Paid by Employer", code: "1059", value: calculationData.obligations_paid || 0 },
        { field: "Fixed Salary Tax Paid by Employer", code: "1009", value: calculationData.salary_tax_paid || 0 },
        { field: "Termination / Severance Amount", code: "1099", value: calculationData.termination_amount || 0 },
        { field: "Other Cash Benefits", code: "1049", value: calculationData.other_cash || 0 },
        
        // Perks Section
        { field: "Servant/Driver/Maid Salaries Paid", code: "1089", value: calculationData.servant_salary_paid || 0 },
        { field: "Kids Education Reimbursement", code: "1059", value: calculationData.kids_education || 0 },
        { field: "Car Lease / Ijara Rentals Reimbursement", code: "1059", value: calculationData.car_lease || 0 },
        { field: "Utility Bills Reimbursement", code: "1059", value: calculationData.utility_reimbursement || 0 },
        
        // Company Car (5% or 10% of car cost based on usage)
        { field: "Company Car Benefit", code: "1009", value: calculationData.company_car_value || 0 },
        
        // Provident Fund
        { field: "Employer PF Contribution", code: "1009", value: calculationData.employer_pf_contribution || 0 },
        { field: "PF Interest Received", code: "1009", value: calculationData.pf_interest || 0 },
        { field: "PF Accumulated Balance (Unrecognized)", code: "1009", value: calculationData.pf_accumulated_balance || 0 },
        
        // Housing & Loan
        { field: "Housing Facility (Fair Market Rent)", code: "1009", value: calculationData.housing_facility || 0 },
        { field: "Concessional Loan Benefit", code: "1009", value: calculationData.concessional_loan || 0 },
        
        // Other Perks
        { field: "Asset Transfer Value", code: "1009", value: calculationData.asset_transfer || 0 },
        { field: "Any Other Perk", code: "1009", value: calculationData.any_other_perk || 0 },
        
        // Deductions
        { field: "Zakat Paid", code: "9001", value: calculationData.zakat || 0 },
        { field: "Number of Children", code: "900801", value: calculationData.num_children || 0 },
        { field: "Tuition Fees Paid", code: "9008", value: calculationData.education_expenses || 0 },
        { field: "Medical Allowance Exemption", code: "1049", value: calculationData.medical_exemption || 0 },
        
        // Tax Credits
        { field: "Charitable Contribution Credit", code: "9311", value: calculationData.charity_credit || 0 },
        { field: "Pension Fund Contribution Credit", code: "9313", value: calculationData.pension_credit || 0 },
        { field: "House Loan Interest Credit", code: "", value: calculationData.house_loan_credit || 0 },
        
        // Adjustable Taxes
        { field: "Annual Token Tax", code: "64130003", value: calculationData.annual_token_tax || 0 },
        { field: "Vehicle Purchase Tax", code: "64100301", value: calculationData.vehicle_purchase_tax || 0 },
        { field: "Cash Withdrawal Tax", code: "64100101", value: calculationData.cash_withdrawal_tax || 0 },
        { field: "Electricity Bill Tax", code: "64140101", value: calculationData.electricity_bill_tax || 0 },
        { field: "Property Purchase Tax", code: "64151101", value: calculationData.property_purchase_tax || 0 },
        { field: "Property Sale Tax", code: "64150301", value: calculationData.property_sale_tax || 0 },
        { field: "Foreign Card Transactions Tax", code: "64151905", value: calculationData.foreign_txn_tax || 0 },
        { field: "Telecom Tax", code: "64150001", value: calculationData.telecom_tax || 0 },
        { field: "Functions/Gatherings Tax", code: "64150407", value: calculationData.function_tax || 0 },
        { field: "Salary of Employees u/s 149", code: "64020004", value: calculationData.salary_tax_paid || 0 }
    ];
    
    // Group by code for Table 2
    const groupedData = {};
    
    fieldMappings.forEach(item => {
        const code = item.code || "no_code";
        if (!groupedData[code]) {
            groupedData[code] = {
                code: item.code,
                fields: [],
                total: 0
            };
        }
        groupedData[code].fields.push(item.field);
        groupedData[code].total += item.value;
    });
    
    // Generate Table 1 HTML
    const detailedTableBody = document.getElementById("detailedTableBody");
    if (detailedTableBody) {
        detailedTableBody.innerHTML = "";
        fieldMappings.forEach(item => {
            const row = detailedTableBody.insertRow();
            row.insertCell(0).textContent = item.field;
            row.insertCell(1).textContent = item.code || "-";
            row.insertCell(2).textContent = item.value.toLocaleString();
        });
        console.log("Table 1 generated with", fieldMappings.length, "rows");
    } else {
        console.error("detailedTableBody not found");
    }
    
    // Generate Table 2 HTML
    const summaryTableBody = document.getElementById("summaryTableBody");
    if (summaryTableBody) {
        summaryTableBody.innerHTML = "";
        
        // Sort by code
        const sortedGroups = Object.keys(groupedData).sort();
        
        sortedGroups.forEach(code => {
            const group = groupedData[code];
            const row = summaryTableBody.insertRow();
            
            // Group name (list of fields or custom name)
            let groupName = "";
            if (code === "1009") groupName = "Total Salary, Bonus & Benefits";
            else if (code === "1049") groupName = "Total Allowances & Benefits";
            else if (code === "1059") groupName = "Total Reimbursements";
            else if (code === "1099") groupName = "Total Subsidies";
            else if (code === "1008") groupName = "Pension Received";
            else if (code === "1089") groupName = "Servant Salaries";
            else if (code === "9001") groupName = "Zakat Paid";
            else if (code === "9008") groupName = "Education Expenses";
            else if (code === "900801") groupName = "Number of Children";
            else if (code === "9311") groupName = "Charity Credit";
            else if (code === "9313") groupName = "Pension Credit";
            else if (code === "no_code") groupName = "House Loan Interest Credit (No IRIS Code)";
            else if (code === "64130003") groupName = "Annual Token Tax";
            else if (code === "64100301") groupName = "Vehicle Purchase Tax";
            else if (code === "64100101") groupName = "Cash Withdrawal Tax";
            else if (code === "64140101") groupName = "Electricity Bill Tax";
            else if (code === "64151101") groupName = "Property Purchase Tax";
            else if (code === "64150301") groupName = "Property Sale Tax";
            else if (code === "64151905") groupName = "Foreign Card Tax";
            else if (code === "64150001") groupName = "Telecom Tax";
            else if (code === "64150407") groupName = "Functions Tax";
            else if (code === "64020004") groupName = "Salary of Employees";
            else groupName = group.fields.slice(0, 2).join(", ") + (group.fields.length > 2 ? "..." : "");
            
            row.insertCell(0).textContent = groupName;
            row.insertCell(1).textContent = group.code || "-";
            row.insertCell(2).textContent = group.total.toLocaleString();
        });
        console.log("Table 2 generated with", sortedGroups.length, "groups");
    } else {
        console.error("summaryTableBody not found");
    }
}

// Function to setup toggle button
function setupIrisToggle(calculationData) {
    const toggleBtn = document.getElementById("toggleIrisTables");
    const container = document.getElementById("irisTablesContainer");
    
    // Store the data globally for access when button is clicked
    window.irisCalculationData = calculationData;
    
    if (toggleBtn && container) {
        const newBtn = toggleBtn.cloneNode(true);
        toggleBtn.parentNode.replaceChild(newBtn, toggleBtn);
        
        newBtn.addEventListener("click", function() {
            console.log("Button clicked! Using data:", window.irisCalculationData);
            if (container.style.display === "none" || container.style.display === "") {
                // Generate tables using the stored data
                generateIrisTables(window.irisCalculationData);
                container.style.display = "block";
                newBtn.textContent = "Hide IRIS Portal Mapping";
                newBtn.classList.add("active");
            } else {
                container.style.display = "none";
                newBtn.textContent = "Show IRIS Portal Mapping";
                newBtn.classList.remove("active");
            }
        });
    }
}

// Make functions available globally
window.generateIrisTables = generateIrisTables;
window.setupIrisToggle = setupIrisToggle;