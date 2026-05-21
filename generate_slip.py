import os
from datetime import datetime
from pdf_generator import generate_salary_slip

# Define details for Ritka Dubey's Salary Slip
data_payload = {
    "company_name": "AMP Elevated Social India Private Limited",
    "company_address": "#1, 161, CHANDRA SHEKHAR AZAD, Jhansi City, Jhansi, Jhansi - 284002, Uttar Pradesh",
    "company_cin": "U85500UP2024PTC212408",
    "employee_name": "Ritka Dubey",
    "employee_id": "EMP-2026-044",
    "role": "Digital Marketing Intern",
    "joining_date": "21/05/2026",
    "month_year": "May 2026",
    "paid_days": "30",
    "basic": 6000,
    "hra": 2000,
    "conveyance": 1000,
    "special": 1000,
    "pf": 0,
    "pt": 200,
    "tds": 0,
    "signer_name": "Pranay Shrivastava",
    "signer_designation": "Director",
}

try:
    print("Generating Salary Slip for Ritka Dubey...")
    pdf_bytes = generate_salary_slip(data_payload)
    
    # Save the generated PDF bytes to a file
    output_filename = "Salary_Slip_Ritka_Dubey.pdf"
    output_path = os.path.join(os.getcwd(), output_filename)
    
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)
        
    print(f"Success! Salary Slip saved successfully as a PDF at:\n{output_path}")
except Exception as e:
    print(f"Error generating PDF: {e}")
