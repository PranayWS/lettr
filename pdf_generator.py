import io
import os
import tempfile
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class CustomPDF(FPDF):
    def __init__(self, logo_bytes=None, logo_ext="png", company_name="", company_address="", company_cin="", doc_title="", is_certificate=False):
        orientation = 'L' if is_certificate else 'P'
        super().__init__(orientation=orientation, unit='mm', format='A4')
        self.logo_bytes = logo_bytes
        self.logo_ext = logo_ext
        self.company_name = company_name if company_name else "LETTR DEMO COMPANY"
        self.company_address = company_address if company_address else "123, Tech Park, Silicon Valley, India"
        self.company_cin = company_cin
        self.doc_title = doc_title
        self.is_certificate = is_certificate
        
        # Temp file for logo if provided as bytes
        self.temp_logo_path = None
        if self.logo_bytes:
            try:
                self.temp_logo_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{self.logo_ext}")
                self.temp_logo_file.write(self.logo_bytes)
                self.temp_logo_file.close()
                self.temp_logo_path = self.temp_logo_file.name
            except Exception as e:
                print("Failed to save temp logo file:", e)
                self.temp_logo_path = None

    def __del__(self):
        if hasattr(self, 'temp_logo_path') and self.temp_logo_path and os.path.exists(self.temp_logo_path):
            try:
                os.remove(self.temp_logo_path)
            except Exception:
                pass

    def header(self):
        if self.is_certificate:
            # Draw beautiful border for Certificate
            self.set_draw_color(124, 58, 237) # Elegant Violet border
            self.set_line_width(1.5)
            self.rect(8, 8, 281, 194) # outer border
            
            self.set_draw_color(245, 158, 11) # Gold inner border
            self.set_line_width(0.5)
            self.rect(10, 10, 277, 190) # inner border
            return

        # Regular document Header
        # Left margin 20mm, Right margin 20mm
        self.set_y(15)
        
        logo_w = 28
        has_logo = False
        if self.temp_logo_path and os.path.exists(self.temp_logo_path):
            try:
                self.image(self.temp_logo_path, x=20, y=14, w=logo_w)
                has_logo = True
            except Exception as e:
                print("Failed to render logo image in PDF:", e)
                has_logo = False
        
        # Company Info text block
        if has_logo:
            self.set_x(20 + logo_w + 6)
        else:
            self.set_x(20)
            
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(17, 24, 39) # Slate 900
        self.cell(0, 6, self.company_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        if has_logo:
            self.set_x(20 + logo_w + 6)
        else:
            self.set_x(20)
            
        self.set_font('helvetica', '', 8)
        self.set_text_color(107, 114, 128) # Gray 500
        self.multi_cell(110 if has_logo else 170, 4, self.company_address)
        
        if self.company_cin:
            if has_logo:
                self.set_x(20 + logo_w + 6)
            else:
                self.set_x(20)
            self.cell(0, 4, f"CIN: {self.company_cin}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
        # Draw a beautiful gradient-colored header rule
        self.set_y(36)
        self.set_draw_color(124, 58, 237) # Violet 600
        self.set_line_width(0.8)
        self.line(20, self.get_y(), 190, self.get_y())
        
        # Subtle gray line right below the violet line
        self.set_draw_color(229, 231, 235) # Gray 200
        self.set_line_width(0.3)
        self.line(20, self.get_y() + 0.8, 190, self.get_y() + 0.8)
        
        # Header spacing
        self.set_y(44)
        self.set_text_color(0, 0, 0) # reset text color to black

    def footer(self):
        if self.is_certificate:
            return
            
        self.set_y(-18)
        self.set_draw_color(229, 231, 235) # Gray 200
        self.set_line_width(0.3)
        self.line(20, self.get_y(), 190, self.get_y())
        
        self.set_y(self.get_y() + 2)
        self.set_font('helvetica', 'I', 7)
        self.set_text_color(156, 163, 175) # Gray 400
        self.cell(0, 4, f"Generated automatically by LETTR Employee System on {datetime.now().strftime('%Y-%m-%d %H:%M')}", align='L')
        self.set_x(-40)
        self.cell(20, 4, f"Page {self.page_no()}", align='R')


def number_to_words(number):
    """Converts a positive integer into Indian Rupee words standard."""
    try:
        num = int(number)
    except (ValueError, TypeError):
        return "Zero Only"
    
    if num == 0:
        return "Zero Only"
        
    under_20 = [
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
        "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_chunk(n):
        c_words = []
        if n >= 100:
            c_words.append(under_20[n // 100] + " Hundred")
            n %= 100
        if n >= 20:
            c_words.append(tens[n // 10])
            n %= 10
        if n > 0:
            c_words.append(under_20[n])
        return " ".join(c_words)

    words = []
    # Crores (1,00,00,000)
    if num >= 10000000:
        crore_part = num // 10000000
        words.append(convert_chunk(crore_part) + " Crore")
        num %= 10000000
    # Lakhs (1,00,000)
    if num >= 100000:
        lakh_part = num // 100000
        words.append(convert_chunk(lakh_part) + " Lakh")
        num %= 100000
    # Thousands (1,000)
    if num >= 1000:
        thousand_part = num // 1000
        words.append(convert_chunk(thousand_part) + " Thousand")
        num %= 1000
    # Rest
    if num > 0:
        words.append(convert_chunk(num))
        
    return "Rupees " + " ".join(words) + " Only"


def setup_standard_margins(pdf):
    pdf.set_margins(20, 25, 20)
    pdf.set_auto_page_break(True, margin=20)


def generate_offer_letter(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        doc_title="Offer Letter"
    )
    setup_standard_margins(pdf)
    pdf.add_page()
    
    # Document Metadata
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(124, 58, 237) # Violet 600
    pdf.cell(0, 10, "OFFER LETTER", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    
    # Target Address & Date
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(17, 24, 39)
    
    # Addressed to employee
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(100, 5, "To,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(100, 5, data.get('employee_name', '_________________'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    if data.get('employee_email'):
        pdf.set_font('helvetica', 'I', 9)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(100, 5, f"Email: {data.get('employee_email')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(17, 24, 39)
        
    pdf.ln(3)
    
    # Date on the right side
    pdf.set_y(pdf.get_y() - 15)
    pdf.set_x(140)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 5, f"Date: {data.get('date', datetime.now().strftime('%d/%m/%Y'))}", align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(pdf.get_y() + 10)
    pdf.ln(5)
    
    # Salutation
    pdf.set_font('helvetica', '', 10.5)
    pdf.cell(0, 5, f"Dear {data.get('employee_name', 'Candidate')},", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    
    # Paragraph 1
    duration = data.get('duration', '2 Months')
    role = data.get('role', 'Intern')
    comp_brand = data.get('company_name', 'our Organization')
    manager = data.get('reporting_manager', 'the Management')
    stipend_val = data.get('stipend_salary', '0')
    joining_date = data.get('joining_date', '_________________')
    
    p1 = (f"We are pleased to offer you a {duration} Internship at {comp_brand} "
          f"reporting to {manager}. Looking forward to working as a team.")
    pdf.multi_cell(0, 5.5, p1)
    pdf.ln(3)
    
    # Paragraph 2
    p2 = (f"We expect you to join on {joining_date} and your job responsibilities will be "
          f"as discussed and mutually agreed upon.")
    pdf.multi_cell(0, 5.5, p2)
    pdf.ln(3)
    
    # Paragraph 3
    stipend_text = f"INR {stipend_val}/- per month" if str(stipend_val).strip().isdigit() else stipend_val
    p3 = (f"You will get conveyance allowance, Experience Certificate and a stipend of {stipend_text} "
          f"as discussed at the completion of this Internship.")
    pdf.multi_cell(0, 5.5, p3)
    pdf.ln(3)
    
    # Paragraph 4
    p4 = "We hope you will enjoy your role and make a significant contribution to the success of the business."
    pdf.multi_cell(0, 5.5, p4)
    pdf.ln(3)
    
    # Paragraph 5
    p5 = "Please sign and return a copy of this letter as a token of your acceptance of the offer."
    pdf.multi_cell(0, 5.5, p5)
    pdf.ln(8)
    
    # Signatures
    pdf.set_font('helvetica', '', 10.5)
    pdf.cell(100, 5, "Yours sincerely,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(8)
    
    # Signer details
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.cell(100, 5, data.get('signer_name', 'Authorized Signatory'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 9.5)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(100, 4, data.get('signer_designation', 'HR Manager'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(100, 4, comp_brand, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(12)
    
    # Acceptance Block
    pdf.set_draw_color(229, 231, 235)
    pdf.set_fill_color(249, 250, 251)
    pdf.set_line_width(0.3)
    
    # Draw nice box for acceptance
    start_y = pdf.get_y()
    pdf.rect(20, start_y, 170, 24, 'DF')
    
    pdf.set_y(start_y + 3)
    pdf.set_x(24)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 4, "Acceptance:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(24)
    pdf.set_font('helvetica', 'I', 9.5)
    pdf.cell(0, 4.5, "I accept the aforesaid terms & conditions and this offer.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(1)
    pdf.set_x(24)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(80, 5, "Signature: _______________________")
    pdf.cell(80, 5, "Date: _______________________")
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()


def generate_salary_slip(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        doc_title="Salary Slip"
    )
    setup_standard_margins(pdf)
    pdf.add_page()
    
    # Document Title
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "PAYSLIP / SALARY SLIP", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    month_val = data.get('month_year', datetime.now().strftime('%B %Y'))
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 5, f"For the Month of {month_val}", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    # Employee details grid
    pdf.set_text_color(17, 24, 39)
    pdf.set_draw_color(229, 231, 235)
    pdf.set_fill_color(249, 250, 251)
    pdf.set_line_width(0.3)
    
    # Grid background rect
    start_y = pdf.get_y()
    pdf.rect(20, start_y, 170, 36, 'DF')
    
    # Populate Employee Details
    pdf.set_y(start_y + 3)
    
    details = [
        [("Employee Name:", data.get('employee_name', 'N/A')), ("Joining Date:", data.get('joining_date', 'N/A'))],
        [("Employee ID:", data.get('employee_id', 'EMP-LETTR-01')), ("Designation / Role:", data.get('role', 'N/A'))],
        [("Bank Name:", data.get('bank_name', 'N/A')), ("Paid Days:", data.get('paid_days', '30'))],
        [("Bank A/C No:", data.get('bank_account', 'N/A')), ("IFSC Code:", data.get('ifsc', 'N/A'))]
    ]
    
    for row in details:
        # Col 1
        pdf.set_x(24)
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(32, 4.5, row[0][0])
        pdf.set_font('helvetica', '', 9)
        pdf.cell(50, 4.5, str(row[0][1]))
        
        # Col 2
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(32, 4.5, row[1][0])
        pdf.set_font('helvetica', '', 9)
        pdf.cell(50, 4.5, str(row[1][1]))
        
        pdf.ln(7.5)
        
    pdf.ln(2)
    
    # Earnings & Deductions Table Header
    table_y = pdf.get_y()
    pdf.set_draw_color(124, 58, 237)
    pdf.set_fill_color(124, 58, 237)
    pdf.rect(20, table_y, 85, 7, 'DF') # Earnings header
    
    pdf.set_fill_color(31, 41, 55)
    pdf.set_draw_color(31, 41, 55)
    pdf.rect(105, table_y, 85, 7, 'DF') # Deductions header
    
    pdf.set_y(table_y + 1.5)
    pdf.set_font('helvetica', 'B', 9)
    pdf.set_text_color(255, 255, 255)
    
    # Labels
    pdf.set_x(24)
    pdf.cell(55, 4, "EARNINGS")
    pdf.cell(26, 4, "AMOUNT (INR)", align='R')
    
    pdf.set_x(109)
    pdf.cell(55, 4, "DEDUCTIONS")
    pdf.cell(26, 4, "AMOUNT (INR)", align='R')
    
    pdf.ln(5.5)
    pdf.set_text_color(17, 24, 39)
    
    # Table rows
    # Convert amounts safely
    def clean_amt(v):
        try:
            return float(v)
        except (ValueError, TypeError):
            return 0.0
            
    basic_val = clean_amt(data.get('basic', 0))
    hra_val = clean_amt(data.get('hra', 0))
    conv_val = clean_amt(data.get('conveyance', 0))
    spec_val = clean_amt(data.get('special', 0))
    
    pf_val = clean_amt(data.get('pf', 0))
    pt_val = clean_amt(data.get('pt', 0))
    tds_val = clean_amt(data.get('tds', 0))
    
    earnings_list = [
        ("Basic Salary", basic_val),
        ("House Rent Allowance (HRA)", hra_val),
        ("Conveyance Allowance", conv_val),
        ("Special Allowance", spec_val)
    ]
    
    deductions_list = [
        ("Provident Fund (PF)", pf_val),
        ("Professional Tax (PT)", pt_val),
        ("TDS / Income Tax", tds_val),
        ("-", 0.0) # spacer
    ]
    
    pdf.set_draw_color(229, 231, 235)
    pdf.set_line_width(0.3)
    
    for i in range(4):
        curr_y = pdf.get_y()
        # Row outline box
        pdf.rect(20, curr_y, 85, 8)
        pdf.rect(105, curr_y, 85, 8)
        
        pdf.set_y(curr_y + 2)
        
        # Col 1 (Earnings)
        pdf.set_x(24)
        pdf.set_font('helvetica', '', 9)
        pdf.cell(55, 4, earnings_list[i][0])
        pdf.cell(26, 4, f"{earnings_list[i][1]:,.2f}" if earnings_list[i][1] > 0 else "0.00", align='R')
        
        # Col 2 (Deductions)
        pdf.set_x(109)
        pdf.cell(55, 4, deductions_list[i][0])
        if deductions_list[i][0] != "-":
            pdf.cell(26, 4, f"{deductions_list[i][1]:,.2f}" if deductions_list[i][1] > 0 else "0.00", align='R')
        else:
            pdf.cell(26, 4, "", align='R')
            
        pdf.ln(6)
        
    # Totals Row
    curr_y = pdf.get_y()
    pdf.set_fill_color(243, 244, 246)
    pdf.rect(20, curr_y, 85, 8, 'DF')
    pdf.rect(105, curr_y, 85, 8, 'DF')
    
    total_earnings = basic_val + hra_val + conv_val + spec_val
    total_deductions = pf_val + pt_val + tds_val
    net_salary = total_earnings - total_deductions
    
    pdf.set_y(curr_y + 2)
    pdf.set_font('helvetica', 'B', 9)
    
    pdf.set_x(24)
    pdf.cell(55, 4, "Total Earnings (A)")
    pdf.cell(26, 4, f"{total_earnings:,.2f}", align='R')
    
    pdf.set_x(109)
    pdf.cell(55, 4, "Total Deductions (B)")
    pdf.cell(26, 4, f"{total_deductions:,.2f}", align='R')
    
    pdf.ln(9)
    
    # Net Pay Display Box
    box_y = pdf.get_y()
    pdf.set_fill_color(237, 233, 254) # Light violet fill
    pdf.set_draw_color(139, 92, 246) # Violet 500 border
    pdf.rect(20, box_y, 170, 16, 'DF')
    
    pdf.set_y(box_y + 3)
    pdf.set_x(24)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(109, 40, 217) # Dark purple
    pdf.cell(100, 5, f"NET TAKE HOME SALARY:   INR {net_salary:,.2f}")
    
    pdf.set_y(box_y + 8.5)
    pdf.set_x(24)
    pdf.set_font('helvetica', 'I', 9.5)
    pdf.set_text_color(75, 85, 99)
    words = number_to_words(int(net_salary))
    pdf.cell(0, 5, f"In Words: {words}")
    
    pdf.ln(12)
    pdf.set_text_color(17, 24, 39)
    
    # Signatures
    pdf.ln(6)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(110, 5, "Employee Signature", align='L')
    pdf.cell(60, 5, "Authorized Signatory", align='R')
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(156, 163, 175)
    pdf.cell(0, 4, "This is a computer-generated salary slip and does not require a physical signature.", align='C')
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()


def generate_internship_certificate(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        is_certificate=True
    )
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    
    # Outer visual layout
    pdf.set_y(22)
    
    # Logo rendering (centered at the top of landscape certificate)
    logo_w = 32
    if pdf.temp_logo_path and os.path.exists(pdf.temp_logo_path):
        try:
            pdf.image(pdf.temp_logo_path, x=132.5, y=20, w=logo_w)
            pdf.set_y(20 + 16 + 5)
        except Exception:
            pdf.set_y(25)
    else:
        pdf.set_y(25)
        
    # Company Name Header
    comp_brand = data.get('company_name', 'LETTR ORGANIZATION').upper()
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(0, 6, comp_brand, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Address (optional small)
    if data.get('company_address'):
        pdf.set_font('helvetica', '', 7.5)
        pdf.set_text_color(156, 163, 175)
        pdf.cell(0, 4, data.get('company_address'), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
    pdf.ln(5)
    
    # "CERTIFICATE OF COMPLETION"
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(124, 58, 237) # Violet
    pdf.cell(0, 10, "CERTIFICATE OF INTERNSHIP", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Subtle line decoration
    pdf.ln(2)
    pdf.set_draw_color(245, 158, 11) # Gold Accent
    pdf.set_line_width(0.8)
    pdf.line(118, pdf.get_y(), 178, pdf.get_y())
    
    pdf.ln(6)
    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(55, 65, 81) # Gray 700
    pdf.cell(0, 6, "This is proudly presented to", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    
    # Name
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(17, 24, 39) # Dark 900
    pdf.cell(0, 8, data.get('employee_name', '________________________'), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(4)
    
    # Description Body
    pdf.set_font('helvetica', '', 11.5)
    pdf.set_text_color(55, 65, 81)
    
    role = data.get('role', 'Software Development Intern')
    joining_date = data.get('joining_date', '___________')
    duration = data.get('duration', '2 Months')
    end_date = data.get('relieving_date') or data.get('date') or datetime.now().strftime('%d/%m/%Y')
    
    body = (f"for successfully completing a {duration} professional internship as a {role} "
            f"at {data.get('company_name', 'our company')}. The tenure of the internship was "
            f"from {joining_date} to {end_date}.")
    
    pdf.set_x(35)
    pdf.multi_cell(227, 6, body, align='C')
    
    pdf.ln(3)
    
    body2 = ("During this period, their work was reviewed and found to be exemplary, "
             "exhibiting remarkable professional standards, sincerity, and high dedication.")
    pdf.set_x(35)
    pdf.multi_cell(227, 6, body2, align='C')
    
    pdf.ln(12)
    
    # Footer signatures in landscape
    # Left: Issue Date, Right: Authorized Signatory
    pdf.set_y(155)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(107, 114, 128)
    
    # Left Col (Date)
    pdf.set_x(40)
    pdf.cell(80, 5, f"Date of Issue: {data.get('date', datetime.now().strftime('%d/%m/%Y'))}")
    
    # Right Col (Signatory)
    pdf.set_x(180)
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(80, 5, data.get('signer_name', 'Authorized Signatory'), align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(180)
    pdf.set_font('helvetica', '', 9.5)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(97, 4.5, data.get('signer_designation', 'HR Lead'), align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Visual Certificate Stamp/Badge placeholder
    pdf.set_y(150)
    pdf.set_x(138.5)
    pdf.set_draw_color(245, 158, 11)
    pdf.set_fill_color(254, 243, 199)
    pdf.set_line_width(0.5)
    pdf.circle(148.5, 158, 12, 'DF')
    
    pdf.set_y(153.5)
    pdf.set_x(138.5)
    pdf.set_font('helvetica', 'B', 7)
    pdf.set_text_color(217, 119, 6)
    pdf.cell(20, 4, "VERIFIED", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(138.5)
    pdf.cell(20, 3, "EXCELLENCE", align='C')
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()


def generate_nda(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        doc_title="Non-Disclosure Agreement"
    )
    setup_standard_margins(pdf)
    pdf.add_page()
    
    # Title
    pdf.set_font('helvetica', 'B', 13)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 8, "MUTUAL NON-DISCLOSURE AGREEMENT", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    
    # Preamble
    pdf.set_font('helvetica', '', 9.5)
    pdf.set_text_color(17, 24, 39)
    
    date_val = data.get('date', datetime.now().strftime('%d/%m/%Y'))
    company = data.get('company_name', '[Company Name]')
    employee = data.get('employee_name', '[Employee Name]')
    role = data.get('role', '[Designation]')
    
    preamble = (
        f"This Non-Disclosure Agreement (the \"Agreement\") is entered into on this {date_val} (the \"Effective Date\"), "
        f"by and between {company}, represented by its Authorized Signatory (hereinafter referred to as \"Employer\"), "
        f"and {employee}, residing at the address registered with the company (hereinafter referred to as \"Employee\")."
    )
    pdf.multi_cell(0, 5, preamble)
    pdf.ln(3.5)
    
    # Recitals
    pdf.set_font('helvetica', 'B', 9.5)
    pdf.cell(0, 4.5, "WHEREAS:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 9.5)
    recital_text = (
        f"A. The Employee is hired / engaged as a {role} at the Employer's business operations.\n"
        f"B. In connection with such engagement, the Employee will have access to certain proprietary, confidential, "
        f"technical, financial, and strategic information belonging to the Employer.\n"
        f"C. To protect such proprietary assets, both parties agree to execute this Non-Disclosure Agreement."
    )
    pdf.multi_cell(0, 5, recital_text)
    pdf.ln(4)
    
    # Sections
    sections = [
        ("1. Definition of Confidential Information",
         "For purposes of this Agreement, \"Confidential Information\" shall include all information or material that has or "
         "could have commercial value or other utility in the business in which Employer is engaged. If Information is in "
         "written form, the Employer shall label or stamp the materials with the word \"Confidential\" or some similar warning. "
         "If Information is transmitted orally, the Employer shall promptly provide writing that such oral communication "
         "constituted Confidential Information. This includes software code, designs, algorithms, customer databases, and strategies."),
        
        ("2. Exclusions from Confidentiality",
         "Employee's obligations under this Agreement do not extend to information that is: (a) publicly known at the time of "
         "disclosure or subsequently becomes publicly known through no fault of the Employee; (b) discovered or created by "
         "the Employee before disclosure by Employer; (c) learned by the Employee through legitimate means other than from "
         "the Employer; or (d) is disclosed by Employee with Employer's prior written consent."),
        
        ("3. Obligations of Employee",
         "Employee shall hold and maintain the Confidential Information in strictest confidence for the sole and exclusive "
         "benefit of the Employer. Employee shall carefully restrict access to Confidential Information to third parties. "
         "Employee shall not, without prior written approval of Employer, use for Employee's own benefit, publish, copy, or "
         "otherwise disclose to others, or permit the use by others for their benefit or to the detriment of Employer, "
         "any Confidential Information. Upon termination of engagement, all physical and digital copies must be returned."),
        
        ("4. Term and Termination",
         "The non-disclosure provisions of this Agreement shall survive the termination of Employee's engagement and "
         "Employee's duty to hold Confidential Information in confidence shall remain in effect for a period of two (2) years "
         "after engagement ends, or until such time as Employer releases Employee from such obligation in writing."),
        
        ("5. Governing Law and Remedies",
         "This Agreement shall be construed in accordance with the laws of India. In the event of a breach or threatened "
         "breach of this Agreement, the Employer shall be entitled to seek an injunction restraining the Employee from "
         "disclosing such information, in addition to seeking damage recovery and legal expenses.")
    ]
    
    for title, text in sections:
        pdf.set_font('helvetica', 'B', 10)
        pdf.set_text_color(124, 58, 237)
        pdf.cell(0, 5, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('helvetica', '', 9.5)
        pdf.set_text_color(17, 24, 39)
        pdf.multi_cell(0, 4.5, text)
        pdf.ln(3.5)
        
    pdf.ln(5)
    
    # Sign-off Blocks
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(85, 5, "For Employer:")
    pdf.cell(85, 5, "Employee:")
    pdf.ln(12)
    
    pdf.set_font('helvetica', '', 9.5)
    pdf.set_x(20)
    pdf.cell(85, 4, f"Name: {data.get('signer_name', 'Authorized Signer')}")
    pdf.cell(85, 4, f"Name: {employee}")
    pdf.ln(4.5)
    
    pdf.set_x(20)
    pdf.cell(85, 4, f"Title: {data.get('signer_designation', 'HR Manager')}")
    pdf.cell(85, 4, "Title: Employee / Intern")
    pdf.ln(4.5)
    
    pdf.set_x(20)
    pdf.cell(85, 4, "Signature: ______________________")
    pdf.cell(85, 4, "Signature: ______________________")
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()


def generate_experience_letter(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        doc_title="Experience Certificate"
    )
    setup_standard_margins(pdf)
    pdf.add_page()
    
    # Document title
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 10, "TO WHOMSOEVER IT MAY CONCERN", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(4)
    
    # Date on the right
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(17, 24, 39)
    pdf.set_x(140)
    pdf.cell(50, 5, f"Date: {data.get('date', datetime.now().strftime('%d/%m/%Y'))}", align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(6)
    
    # Body text
    pdf.set_font('helvetica', '', 11)
    
    employee = data.get('employee_name', '________________')
    company = data.get('company_name', '[Company Name]')
    role = data.get('role', 'Intern')
    joining_date = data.get('joining_date', '____________')
    relieving_date = data.get('relieving_date', '____________')
    
    body1 = (f"This is to certify that {employee} has been employed/engaged with {company} "
             f"in the capacity of {role} from {joining_date} to {relieving_date}.")
    pdf.multi_cell(0, 6, body1)
    pdf.ln(4)
    
    body2 = ("During the tenure of their engagement, we found them to be extremely diligent, "
             "highly motivated, and sincere in their duties. They managed their responsibilities "
             "professionally and proved to be an excellent team player.")
    pdf.multi_cell(0, 6, body2)
    pdf.ln(4)
    
    body3 = "The employee has been relieved of their services and all full and final settlements have been fully cleared. There are no outstanding liabilities."
    pdf.multi_cell(0, 6, body3)
    pdf.ln(4)
    
    body4 = "We wish them the absolute best in all their future career endeavors."
    pdf.multi_cell(0, 6, body4)
    
    pdf.ln(12)
    
    # Signatures
    pdf.set_font('helvetica', '', 11)
    pdf.cell(100, 5, "For " + company + ",", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(100, 5, data.get('signer_name', 'Authorized Signatory'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(100, 4.5, data.get('signer_designation', 'HR Manager'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()


def generate_relieving_letter(data, logo_bytes=None, logo_ext="png"):
    pdf = CustomPDF(
        logo_bytes=logo_bytes, 
        logo_ext=logo_ext,
        company_name=data.get('company_name'),
        company_address=data.get('company_address'),
        company_cin=data.get('company_cin'),
        doc_title="Relieving Letter"
    )
    setup_standard_margins(pdf)
    pdf.add_page()
    
    # Title
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(124, 58, 237)
    pdf.cell(0, 10, "RELIEVING LETTER", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.ln(4)
    
    # Addressed To
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(100, 5, "To,", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(100, 5, data.get('employee_name', '_________________'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if data.get('employee_email'):
        pdf.set_font('helvetica', 'I', 9.5)
        pdf.set_text_color(107, 114, 128)
        pdf.cell(100, 4.5, f"Email: {data.get('employee_email')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(17, 24, 39)
        
    pdf.ln(3)
    
    # Date on the right
    pdf.set_y(pdf.get_y() - 15)
    pdf.set_x(140)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 5, f"Date: {data.get('date', datetime.now().strftime('%d/%m/%Y'))}", align='R', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(pdf.get_y() + 10)
    pdf.ln(5)
    
    # Salutation
    pdf.set_font('helvetica', '', 11)
    pdf.cell(0, 5, f"Dear {data.get('employee_name', 'Employee')},", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)
    
    # Subject
    pdf.set_font('helvetica', 'B', 10.5)
    pdf.cell(0, 5, f"Subject: Resignation Acceptance & Relieving from services as {data.get('role', 'Intern')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)
    
    # Body text
    pdf.set_font('helvetica', '', 11)
    company = data.get('company_name', '[Company Name]')
    resignation_dt = data.get('resignation_date') or data.get('date') or datetime.now().strftime('%d/%m/%Y')
    relieving_dt = data.get('relieving_date', '___________')
    role = data.get('role', 'Intern')
    
    body1 = (f"This is in reference to your formal resignation letter dated {resignation_dt}. "
             f"We wish to inform you that your resignation has been accepted by the management and you are "
             f"officially relieved of your duties as {role} at {company} at the close of business hours on {relieving_dt}.")
    pdf.multi_cell(0, 6, body1)
    pdf.ln(4)
    
    body2 = ("We further confirm that you have returned all company property, technical assets, documents, and credentials "
             "under your custody. Your Full & Final Settlement accounts have been settled successfully and "
             "no dues remain outstanding.")
    pdf.multi_cell(0, 6, body2)
    pdf.ln(4)
    
    body3 = "We thank you for the service rendered during your employment/internship and wish you the very best in all your future professional pursuits."
    pdf.multi_cell(0, 6, body3)
    
    pdf.ln(12)
    
    # Signatures
    pdf.cell(100, 5, f"For {company},", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(100, 5, data.get('signer_name', 'Authorized Signatory'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(100, 4.5, data.get('signer_designation', 'HR Manager'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # Output PDF as bytes
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    return pdf_buffer.getvalue()
