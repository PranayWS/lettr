import streamlit as st
import datetime
from pdf_generator import (
    generate_offer_letter,
    generate_salary_slip,
    generate_internship_certificate,
    generate_nda,
    generate_experience_letter,
    generate_relieving_letter,
    number_to_words
)
from email_sender import send_document_email

# Set page configuration to wide and premium title
st.set_page_config(
    page_title="LETTR - Easiest Employee Document Hub",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Premium, Custom CSS for a beautiful visual design
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek gradient background */
    .stApp {
        background-color: #FAFAFB;
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1B4B 0%, #0F172A 100%);
        color: #F8FAFC;
        border-right: 1px solid #334155;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }
    
    /* Sidebar Input Styling */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
    }
    
    /* Form Card Container (Left Column) */
    .form-card {
        background: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #F3F4F6;
        margin-bottom: 20px;
    }
    
    /* Interactive Preview Container (Right Column) */
    .preview-card {
        background: #FFFFFF;
        padding: 35px 30px;
        border-radius: 8px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 1px solid #E5E7EB;
        border-top: 6px solid #7C3AED; /* Violet 600 Letterhead accent */
        min-height: 700px;
        color: #111827;
        line-height: 1.6;
    }
    
    .certificate-preview-card {
        background: #FFFFFF;
        padding: 40px 35px;
        border-radius: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border: 8px double #7C3AED;
        outline: 2px solid #F59E0B;
        outline-offset: -6px;
        min-height: 500px;
        color: #111827;
        text-align: center;
        margin-top: 20px;
    }
    
    /* Primary buttons styling */
    .stButton>button {
        background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(124, 58, 237, 0.2), 0 2px 4px -1px rgba(124, 58, 237, 0.1) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.3), 0 4px 6px -2px rgba(124, 58, 237, 0.15) !important;
    }
    
    /* Download Button override */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3) !important;
    }
    
    /* Secondary and standard inputs */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
    }
    
    /* Custom header branding */
    .main-logo-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Force main page labels to be dark slate for perfect contrast in both themes */
    .stApp label {
        color: #1E293B !important;
        font-weight: 600 !important;
    }
    
    /* Preserve white labels inside the sidebar */
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE STICKY VARIABLES -----------------
# Setup default values for Company info in session state to persist them
if "company_name" not in st.session_state:
    st.session_state.company_name = "AMP Elevated Social India Private Limited"
if "company_address" not in st.session_state:
    st.session_state.company_address = "#1, 161, CHANDRA SHEKHAR AZAD, Jhansi City, Jhansi, Jhansi - 284002, Uttar Pradesh"
if "company_cin" not in st.session_state:
    st.session_state.company_cin = "U85500UP2024PTC212408"
if "signer_name" not in st.session_state:
    st.session_state.signer_name = "Pranay Shrivastava"
if "signer_designation" not in st.session_state:
    st.session_state.signer_designation = "Director"
if "reporting_manager" not in st.session_state:
    st.session_state.reporting_manager = "CEO, Mr Pranay Shrivastava"

# Setup SMTP Settings session states
if "smtp_host" not in st.session_state:
    st.session_state.smtp_host = "smtp.gmail.com"
if "smtp_port" not in st.session_state:
    st.session_state.smtp_port = 587
if "smtp_email" not in st.session_state:
    st.session_state.smtp_email = ""
if "smtp_password" not in st.session_state:
    st.session_state.smtp_password = ""

# ----------------- SIDEBAR: BRANDING & SMTP SETTINGS -----------------
st.sidebar.markdown("<h1 style='text-align: center; margin-bottom: 2px;'>LETTR</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: #94A3B8; margin-top:0;'>Premium Document Hub</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 1. Company Branding
st.sidebar.subheader("🏢 Company Branding")
st.session_state.company_name = st.sidebar.text_input("Company Registered Name", value=st.session_state.company_name)
st.session_state.company_address = st.sidebar.text_area("Registered Address", value=st.session_state.company_address, height=70)
st.session_state.company_cin = st.sidebar.text_input("Company CIN (optional)", value=st.session_state.company_cin)

st.sidebar.markdown("---")

# Logo Uploader
st.sidebar.subheader("🎨 Logo & Branding")
logo_file = st.sidebar.file_uploader("Upload Logo Image", type=["png", "jpg", "jpeg"], help="Optional: Renders on the left corner of letterhead.")
logo_bytes = None
logo_ext = "png"
if logo_file:
    logo_bytes = logo_file.read()
    logo_ext = logo_file.name.split('.')[-1]

st.sidebar.markdown("---")

# Signatory details
st.sidebar.subheader("✍️ Authorized Signatory")
st.session_state.signer_name = st.sidebar.text_input("Signer Full Name", value=st.session_state.signer_name)
st.session_state.signer_designation = st.sidebar.text_input("Signer Designation", value=st.session_state.signer_designation)

st.sidebar.markdown("---")

# SMTP Server Settings (Collapsible)
with st.sidebar.expander("✉️ Outgoing Email Server (SMTP)", expanded=False):
    st.markdown("<p style='font-size: 11px; color:#94A3B8;'>Configure your SMTP to enable instant document mailing.</p>", unsafe_allow_html=True)
    st.session_state.smtp_host = st.text_input("SMTP Host", value=st.session_state.smtp_host)
    st.session_state.smtp_port = st.number_input("SMTP Port", value=st.session_state.smtp_port, step=1)
    st.session_state.smtp_email = st.text_input("Sender Email Address", value=st.session_state.smtp_email, placeholder="hr@yourcompany.com")
    st.session_state.smtp_password = st.text_input("App Password / Password", value=st.session_state.smtp_password, type="password", placeholder="••••••••••••••••")

# ----------------- MAIN INTERFACE -----------------

# Page header
col_logo, col_title = st.columns([1, 15])
with col_title:
    st.markdown('<span class="main-logo-header">LETTR</span>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 14px; color: #6B7280; margin-top:-10px;">The easiest way to generate, download, and email professional employee letters immediately.</p>', unsafe_allow_html=True)

st.markdown("---")

# Main Split screen: Form (Left) vs Live Visual Preview (Right)
col_form, col_preview = st.columns([4.2, 5.8])

with col_form:
    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
    st.subheader("📋 Document Builder Form")
    st.markdown("<p style='font-size: 12px; color: #6B7280; margin-top:-10px;'>Arrange key attributes. Fill items below; preview updates in real-time.</p>", unsafe_allow_html=True)
    
    # ---------------- HIERARCHY OF INPUTS: MOST COMMON FIRST ----------------
    
    # Block 1: Target Document Selection
    doc_options = [
        "Offer Letter",
        "Salary Slip",
        "Internship Certificate",
        "Non-Disclosure Agreement (NDA)",
        "Experience Letter / Exit Doc",
        "Relieving Letter"
    ]
    selected_doc = st.selectbox("Select Target Document to Generate", options=doc_options)
    
    # Block 2: Recipient / Employee Details (Most frequently modified)
    st.markdown("<h4 style='color: #4F46E5; margin-bottom: 5px; margin-top: 15px;'>1. Recipient Details</h4>", unsafe_allow_html=True)
    employee_name = st.text_input("Employee / Candidate Name", value="Aditya Sharma", placeholder="Enter full name")
    employee_role = st.text_input("Job Title / Role", value="Digital Marketing Intern", placeholder="e.g. Software Engineer Intern")
    employee_email = st.text_input("Destination Email Address (for immediate delivery)", value="", placeholder="employee@gmail.com")
    
    # Additional specific ID for salary slip
    employee_id = "EMP-2026-042"
    if selected_doc == "Salary Slip":
        employee_id = st.text_input("Employee ID", value="EMP-2026-042")
        
    # Block 3: Timeline & Financial Terms
    st.markdown("<h4 style='color: #4F46E5; margin-bottom: 5px; margin-top: 15px;'>2. Terms & Timelines</h4>", unsafe_allow_html=True)
    
    col_date1, col_date2 = st.columns(2)
    with col_date1:
        joining_date = st.text_input("Joining / Start Date", value="01/06/2026", placeholder="DD/MM/YYYY")
    with col_date2:
        doc_date = st.text_input("Document Issue Date", value=datetime.date.today().strftime("%d/%m/%Y"))
        
    # Specific fields based on doc type
    duration = "2 Months"
    reporting_manager = st.session_state.reporting_manager
    stipend_salary = "10,000"
    relieving_date = "31/07/2026"
    resignation_date = datetime.date.today().strftime("%d/%m/%Y")
    
    if selected_doc in ["Offer Letter", "Internship Certificate", "Non-Disclosure Agreement (NDA)"]:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            duration = st.text_input("Duration of Internship / Term", value="2 Months")
        with col_t2:
            stipend_salary = st.text_input("Stipend / Salary (Monthly)", value="10,000")
            
        reporting_manager = st.text_input("Reporting Manager Name & Title", value=st.session_state.reporting_manager)

    elif selected_doc == "Salary Slip":
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            month_year = st.text_input("Payslip Month & Year", value=datetime.date.today().strftime("%B %Y"))
        with col_s2:
            paid_days = st.text_input("Paid Days / Total Days", value="30")
            
        # Bank Details (Removed)
        bank_name = ""
        bank_account = ""
        ifsc_code = ""
            
        # Salary breakdown
        st.markdown("<p style='font-size: 12px; font-weight:600; color: #4B5563; margin-bottom: 0;'>Earnings Breakdown (INR)</p>", unsafe_allow_html=True)
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            basic_sal = st.number_input("Basic Salary", value=6000, step=100)
            hra_sal = st.number_input("HRA (House Rent)", value=2000, step=100)
        with col_e2:
            conv_sal = st.number_input("Conveyance Allowance", value=1000, step=100)
            spec_sal = st.number_input("Special Allowance", value=1000, step=100)
            
        st.markdown("<p style='font-size: 12px; font-weight:600; color: #4B5563; margin-bottom: 0;'>Deductions Breakdown (INR)</p>", unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(3)
        with col_d1:
            pf_ded = st.number_input("PF Deduct", value=0, step=50)
        with col_d2:
            pt_ded = st.number_input("PT (Professional Tax)", value=200, step=50)
        with col_d3:
            tds_ded = st.number_input("TDS / Income Tax", value=0, step=50)

    elif selected_doc in ["Experience Letter / Exit Doc", "Relieving Letter"]:
        col_exit1, col_exit2 = st.columns(2)
        with col_exit1:
            relieving_date = st.text_input("Relieving / Last Working Date", value="31/07/2026", placeholder="DD/MM/YYYY")
        with col_exit2:
            resignation_date = st.text_input("Resignation Date", value="30/06/2026", placeholder="DD/MM/YYYY")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------------- ACTION HUB ----------------
    st.subheader("⚡ Action Hub")
    st.markdown("<p style='font-size: 12px; color: #6B7280; margin-top:-10px;'>Instant PDF download and immediate emailing to destination ID.</p>", unsafe_allow_html=True)
    
    # Package data dictionary dynamically for generator
    data_payload = {
        "company_name": st.session_state.company_name,
        "company_address": st.session_state.company_address,
        "company_cin": st.session_state.company_cin,
        "employee_name": employee_name,
        "employee_role": employee_role,
        "employee_email": employee_email,
        "role": employee_role,
        "joining_date": joining_date,
        "date": doc_date,
        "signer_name": st.session_state.signer_name,
        "signer_designation": st.session_state.signer_designation,
    }
    
    # Append specific details based on doc selection
    if selected_doc == "Offer Letter":
        data_payload.update({
            "duration": duration,
            "stipend_salary": stipend_salary,
            "reporting_manager": reporting_manager
        })
        pdf_generator_fn = lambda: generate_offer_letter(data_payload, logo_bytes, logo_ext)
        file_prefix = f"Offer_Letter_{employee_name.replace(' ', '_')}"
        email_subject = f"Offer Letter & Internship Details - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nWe are pleased to share your Offer Letter for the {employee_role} position at {st.session_state.company_name}.\n\nPlease find the attached PDF containing all terms and conditions of your engagement.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    elif selected_doc == "Salary Slip":
        data_payload.update({
            "employee_id": employee_id,
            "bank_name": bank_name,
            "bank_account": bank_account,
            "ifsc": ifsc_code,
            "paid_days": paid_days,
            "month_year": month_year,
            "basic": basic_sal,
            "hra": hra_sal,
            "conveyance": conv_sal,
            "special": spec_sal,
            "pf": pf_ded,
            "pt": pt_ded,
            "tds": tds_ded
        })
        pdf_generator_fn = lambda: generate_salary_slip(data_payload, logo_bytes, logo_ext)
        file_prefix = f"Salary_Slip_{month_year.replace(' ', '_')}_{employee_name.replace(' ', '_')}"
        email_subject = f"Payslip / Salary Slip for {month_year} - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nPlease find attached your Salary Slip / Payslip for the month of {month_year}.\n\nFor any clarifications regarding deductions or calculations, please get in touch with the Finance / HR Team.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    elif selected_doc == "Internship Certificate":
        data_payload.update({
            "duration": duration,
            "relieving_date": relieving_date
        })
        pdf_generator_fn = lambda: generate_internship_certificate(data_payload, logo_bytes, logo_ext)
        file_prefix = f"Internship_Certificate_{employee_name.replace(' ', '_')}"
        email_subject = f"Internship Completion Certificate - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nCongratulations on successfully completing your internship at {st.session_state.company_name}!\n\nPlease find attached your official Certificate of Internship.\n\nWe appreciate your hard work and dedication, and wish you all the best in your career.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    elif selected_doc == "Non-Disclosure Agreement (NDA)":
        data_payload.update({
            "duration": duration,
            "stipend_salary": stipend_salary
        })
        pdf_generator_fn = lambda: generate_nda(data_payload, logo_bytes, logo_ext)
        file_prefix = f"NDA_{employee_name.replace(' ', '_')}"
        email_subject = f"Non-Disclosure Agreement (NDA) - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nPlease find attached the Employee Non-Disclosure Agreement (NDA) from {st.session_state.company_name}.\n\nYou are requested to review the confidentiality terms, sign a copy, and return it back to the HR department.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    elif selected_doc == "Experience Letter / Exit Doc":
        data_payload.update({
            "relieving_date": relieving_date
        })
        pdf_generator_fn = lambda: generate_experience_letter(data_payload, logo_bytes, logo_ext)
        file_prefix = f"Experience_Certificate_{employee_name.replace(' ', '_')}"
        email_subject = f"Experience Certificate & Letter of Service - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nThank you for your valuable services and contributions to {st.session_state.company_name}.\n\nPlease find attached your official Experience Certificate.\n\nWe wish you great success in all your future endeavors.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    elif selected_doc == "Relieving Letter":
        data_payload.update({
            "resignation_date": resignation_date,
            "relieving_date": relieving_date
        })
        pdf_generator_fn = lambda: generate_relieving_letter(data_payload, logo_bytes, logo_ext)
        file_prefix = f"Relieving_Letter_{employee_name.replace(' ', '_')}"
        email_subject = f"Relieving Letter & Resignation Acceptance - {st.session_state.company_name}"
        email_body = f"Dear {employee_name},\n\nWe write to formally accept your resignation and officially relieve you from your duties as {employee_role} at {st.session_state.company_name}.\n\nPlease find attached the Relieving Letter. Your full & final settlement accounts are fully cleared.\n\nWe wish you all the best in your career.\n\nBest regards,\n{st.session_state.signer_name}\n{st.session_state.company_name}"

    # Pre-render PDF in memory for instant actions
    try:
        generated_pdf_bytes = pdf_generator_fn()
        pdf_filename = f"{file_prefix}.pdf"
        
        # Two side-by-side premium actions
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            # Native Streamlit download button (100% works in any iframe sandbox!)
            st.download_button(
                label="📥 Download PDF",
                data=generated_pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )
            
        with col_btn2:
            # Email delivery button
            email_triggered = st.button("📧 Send via Email", use_container_width=True)
            
        if email_triggered:
            if not employee_email:
                st.error("⚠️ Email address is empty. Please enter a 'Destination Email Address' under Recipient Details first.")
            elif not st.session_state.smtp_email or not st.session_state.smtp_password:
                st.error("⚠️ SMTP Credentials are not configured. Please fill in the Outgoing Email Server (SMTP) credentials in the sidebar expander first.")
            else:
                with st.spinner("Delivering email to employee..."):
                    success, msg = send_document_email(
                        smtp_host=st.session_state.smtp_host,
                        smtp_port=st.session_state.smtp_port,
                        sender_email=st.session_state.smtp_email,
                        sender_password=st.session_state.smtp_password,
                        recipient_email=employee_email,
                        subject=email_subject,
                        body=email_body,
                        pdf_bytes=generated_pdf_bytes,
                        filename=pdf_filename
                    )
                    if success:
                        st.success(f"📧 {msg}")
                        st.balloons()
                    else:
                        st.error(f"❌ Email error: {msg}")
                        
    except Exception as ex:
        st.error(f"⚠️ Error preparing document: {ex}")
        st.info("Check console logs or verify inputs.")


# ----------------- RIGHT COLUMN: LIVE VISUAL PREVIEW -----------------
with col_preview:
    st.subheader("👁️ Live Visual Preview")
    st.markdown("<p style='font-size: 12px; color: #6B7280; margin-top:-10px;'>This updates in real-time as you fill the form fields.</p>", unsafe_allow_html=True)
    
    # Choose visual layout depending on the type of document selected
    if selected_doc == "Internship Certificate":
        # Landscape elegant certificate preview
        st.markdown(f"""
        <div class="certificate-preview-card">
            <h5 style="color: #6B7280; font-size: 13px; font-weight: 500; text-transform: uppercase; margin-bottom: 2px;">{st.session_state.company_name.upper()}</h5>
            <span style="font-size: 8px; color: #9CA3AF; display: block; margin-bottom: 15px;">{st.session_state.company_address}</span>
            
            <h2 style="color: #7C3AED; font-family: Georgia, serif; font-size: 26px; font-weight: 700; margin-bottom: 5px;">Certificate of Internship</h2>
            <div style="width: 80px; height: 1.5px; background-color: #F59E0B; margin: 0 auto 15px auto;"></div>
            
            <p style="font-family: Georgia, serif; font-style: italic; font-size: 13px; color: #4B5563; margin-bottom: 5px;">This is proudly presented to</p>
            <h3 style="font-size: 20px; font-weight: 700; color: #111827; margin-bottom: 12px;">{employee_name}</h3>
            
            <p style="font-size: 12.5px; line-height: 1.6; color: #374151; padding: 0 15px; margin-bottom: 15px;">
                for successfully completing a <b>{duration}</b> professional internship as a <b>{employee_role}</b> 
                at <b>{st.session_state.company_name}</b> from <b>{joining_date}</b> to <b>{relieving_date}</b>.
            </p>
            
            <p style="font-size: 12.5px; line-height: 1.6; color: #374151; padding: 0 15px; margin-bottom: 30px;">
                During this period, their work was reviewed and found to be exemplary, 
                exhibiting remarkable professional standards, sincerity, and high dedication.
            </p>
            
            <table style="width: 100%; border: none; font-size: 12px;">
                <tr>
                    <td style="text-align: left; color: #6B7280; padding-left: 20px;">
                        Date of Issue: <b>{doc_date}</b>
                    </td>
                    <td style="text-align: right; padding-right: 20px;">
                        <span style="display: block; font-weight: 700; color: #111827;">{st.session_state.signer_name}</span>
                        <span style="font-size: 10.5px; color: #6B7280;">{st.session_state.signer_designation}</span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    elif selected_doc == "Salary Slip":
        # Payslip elegant preview grid
        try:
            b_s = float(basic_sal)
            h_s = float(hra_sal)
            c_s = float(conv_sal)
            s_s = float(spec_sal)
            total_e = b_s + h_s + c_s + s_s
            
            p_d = float(pf_ded)
            t_d = float(pt_ded)
            i_d = float(tds_ded)
            total_d = p_d + t_d + i_d
            
            net_s = total_e - total_d
            net_words = number_to_words(int(net_s))
        except Exception:
            total_e = 0
            total_d = 0
            net_s = 0
            net_words = "N/A"
            
        st.markdown(f"""
        <div class="preview-card">
            <!-- Header -->
            <table style="width:100%; border:none; margin-bottom:15px;">
                <tr>
                    <td style="width:70%;">
                        <h4 style="margin:0; font-weight:700; color:#111827;">{st.session_state.company_name}</h4>
                        <span style="font-size:9px; color:#6B7280;">{st.session_state.company_address}</span><br/>
                        <span style="font-size:9px; color:#6B7280;">CIN: {st.session_state.company_cin}</span>
                    </td>
                    <td style="text-align:right; vertical-align:top; width:30%;">
                        <h5 style="margin:0; color:#7C3AED; font-weight:700;">SALARY SLIP</h5>
                        <span style="font-size:10px; color:#4B5563; font-weight:600;">{month_year}</span>
                    </td>
                </tr>
            </table>
            
            <hr style="border:0; border-top:1px solid #E5E7EB; margin:10px 0;"/>
            
            <!-- Employee Info Grid -->
            <table style="width:100%; border:none; font-size:11px; background-color:#F9FAFB; padding:10px; border-radius:6px; margin-bottom:15px; line-height:1.8;">
                <tr>
                    <td><b>Employee Name:</b></td><td>{employee_name}</td>
                    <td><b>Joining Date:</b></td><td>{joining_date}</td>
                </tr>
                <tr>
                    <td><b>Employee ID:</b></td><td>{employee_id}</td>
                    <td><b>Designation:</b></td><td>{employee_role}</td>
                </tr>
                <tr>
                    <td><b>Paid Days:</b></td><td>{paid_days}</td>
                    <td></td><td></td>
                </tr>
            </table>
            
            <!-- Earnings and Deductions tables -->
            <table style="width:100%; border-collapse:collapse; font-size:11px; margin-bottom:15px;">
                <tr style="color:#FFFFFF; font-weight:700; text-align:left;">
                    <th style="background-color:#7C3AED; padding:5px; width:35%;">EARNINGS</th>
                    <th style="background-color:#7C3AED; padding:5px; text-align:right; width:15%;">AMOUNT (INR)</th>
                    <th style="background-color:#1F2937; padding:5px; width:35%;">DEDUCTIONS</th>
                    <th style="background-color:#1F2937; padding:5px; text-align:right; width:15%;">AMOUNT (INR)</th>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;">
                    <td style="padding:5px;">Basic Salary</td><td style="text-align:right; padding:5px;">{b_s:,.2f}</td>
                    <td style="padding:5px;">Provident Fund (PF)</td><td style="text-align:right; padding:5px;">{p_d:,.2f}</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;">
                    <td style="padding:5px;">House Rent Allowance (HRA)</td><td style="text-align:right; padding:5px;">{h_s:,.2f}</td>
                    <td style="padding:5px;">Professional Tax (PT)</td><td style="text-align:right; padding:5px;">{t_d:,.2f}</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;">
                    <td style="padding:5px;">Conveyance Allowance</td><td style="text-align:right; padding:5px;">{c_s:,.2f}</td>
                    <td style="padding:5px;">TDS / Income Tax</td><td style="text-align:right; padding:5px;">{i_d:,.2f}</td>
                </tr>
                <tr style="border-bottom:1px solid #E5E7EB;">
                    <td style="padding:5px;">Special Allowance</td><td style="text-align:right; padding:5px;">{s_s:,.2f}</td>
                    <td style="padding:5px;">-</td><td style="text-align:right; padding:5px;">0.00</td>
                </tr>
                <tr style="background-color:#F3F4F6; font-weight:700;">
                    <td style="padding:6px;">Total Earnings (A)</td><td style="text-align:right; padding:6px;">{total_e:,.2f}</td>
                    <td style="padding:6px;">Total Deductions (B)</td><td style="text-align:right; padding:6px;">{total_d:,.2f}</td>
                </tr>
            </table>
            
            <!-- Net Pay Box -->
            <div style="background-color:#EDE9FE; border:1px solid #C084FC; padding:10px; border-radius:6px; margin-bottom:20px;">
                <span style="font-size:12px; font-weight:700; color:#6D28D9; display:block;">NET TAKE HOME: INR {net_s:,.2f}</span>
                <span style="font-size:10px; font-style:italic; color:#4B5563;">In Words: {net_words}</span>
            </div>
            
            <!-- Signatures -->
            <table style="width:100%; border:none; font-size:11px; margin-top:20px;">
                <tr>
                    <td style="width:50%;">_____________________________<br/>Employee Signature</td>
                    <td style="text-align:right; width:50%;">
                        _____________________________<br/>
                        <b>Authorized Signatory</b><br/>
                        <span style="font-weight:600; color:#111827;">{st.session_state.signer_name}</span><br/>
                        <span style="font-size:9.5px; color:#6B7280;">{st.session_state.signer_designation}</span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Standard elegant letters layout (Offer Letter, NDA, Experience, Relieving)
        body_text = ""
        doc_header_title = selected_doc.upper()
        
        if selected_doc == "Offer Letter":
            stipend_text = f"INR {stipend_salary}/- per month" if str(stipend_salary).strip().isdigit() else stipend_salary
            body_text = f"""
            <p>To,<br/><b>{employee_name}</b><br/>{f"Email: {employee_email}" if employee_email else ""}</p>
            <p style="text-align: right; margin-top:-35px;">Date: {doc_date}</p>
            
            <p>Dear {employee_name},</p>
            
            <p>We are pleased to offer you a <b>{duration}</b> Internship at <b>{st.session_state.company_name}</b> reporting to <b>{reporting_manager}</b>. Looking forward to working as a team.</p>
            
            <p>We expect you to join on <b>{joining_date}</b> and your job responsibilities will be as discussed and mutually agreed upon.</p>
            
            <p>You will get conveyance allowance, Experience Certificate and a stipend of <b>{stipend_text}</b> as discussed at the completion of this Internship.</p>
            
            <p>We hope you will enjoy your role and make a significant contribution to the success of the business.</p>
            
            <p>Please sign and return a copy of this letter as a token of your acceptance of the offer.</p>
            """
        
        elif selected_doc == "Non-Disclosure Agreement (NDA)":
            body_text = f"""
            <h4 style="text-align:center; color:#7C3AED;">EMPLOYEE NON-DISCLOSURE AGREEMENT</h4>
            <p>This Non-Disclosure Agreement (the "Agreement") is entered into on this <b>{doc_date}</b> by and between <b>{st.session_state.company_name}</b> (referred to as "Employer") and <b>{employee_name}</b> (referred to as "Employee").</p>
            
            <p><b>1. Definition of Confidential Information:</b> For purposes of this Agreement, "Confidential Information" shall include all information or material that has or could have commercial value or other utility in the business in which Employer is engaged, including trade secrets, software code, customer data, and strategical plans.</p>
            
            <p><b>2. Obligations of Employee:</b> Employee shall hold and maintain the Confidential Information in strictest confidence for the sole and exclusive benefit of the Employer. Employee shall not, without prior written approval of Employer, use for Employee's own benefit, copy, or otherwise disclose to others, any Confidential Information.</p>
            
            <p><b>3. Term:</b> The non-disclosure provisions of this Agreement shall survive the termination of Employee's engagement and shall remain in effect for a period of <b>two (2) years</b> after the engagement ends.</p>
            """
            
        elif selected_doc == "Experience Letter / Exit Doc":
            doc_header_title = "TO WHOMSOEVER IT MAY CONCERN"
            body_text = f"""
            <p style="text-align: right;">Date: {doc_date}</p>
            
            <p>This is to certify that <b>{employee_name}</b> has been employed / engaged with <b>{st.session_state.company_name}</b> in the capacity of <b>{employee_role}</b> from <b>{joining_date}</b> to <b>{relieving_date}</b>.</p>
            
            <p>During the tenure of their engagement, we found them to be extremely diligent, highly motivated, and sincere in their duties. They managed their responsibilities professionally and proved to be an excellent team player.</p>
            
            <p>The employee has been relieved of their services and all full and final settlements have been fully cleared. There are no outstanding liabilities.</p>
            
            <p>We wish them the absolute best in all their future career endeavors.</p>
            """
            
        elif selected_doc == "Relieving Letter":
            resignation_dt = resignation_date if resignation_date else doc_date
            body_text = f"""
            <p>To,<br/><b>{employee_name}</b><br/>{f"Email: {employee_email}" if employee_email else ""}</p>
            <p style="text-align: right; margin-top:-35px;">Date: {doc_date}</p>
            
            <p>Dear {employee_name},</p>
            <p><b>Subject: Resignation Acceptance & Relieving from services as {employee_role}</b></p>
            
            <p>This is in reference to your formal resignation letter dated <b>{resignation_dt}</b>. We wish to inform you that your resignation has been accepted by the management and you are officially relieved of your duties as <b>{employee_role}</b> at <b>{st.session_state.company_name}</b> at the close of business hours on <b>{relieving_date}</b>.</p>
            
            <p>We further confirm that you have returned all company property, assets, and credentials under your custody. Your Full & Final Settlement accounts have been settled successfully and no dues remain outstanding.</p>
            
            <p>We thank you for the service rendered during your tenure and wish you the very best in all your future professional pursuits.</p>
            """
            
        # Draw the virtual paper document preview
        st.markdown(f"""
        <div class="preview-card">
            <!-- Letterhead Header -->
            <table style="width:100%; border:none; margin-bottom:15px;">
                <tr>
                    <td>
                        <h3 style="margin:0; color:#111827; font-weight:700;">{st.session_state.company_name}</h3>
                        <span style="font-size:9px; color:#6B7280;">{st.session_state.company_address}</span>
                        {f"<br/><span style='font-size:9px; color:#6B7280;'>CIN: {st.session_state.company_cin}</span>" if st.session_state.company_cin else ""}
                    </td>
                    <td style="text-align:right; vertical-align:top; font-size:12px; font-weight:700; color:#7C3AED;">
                        {doc_header_title}
                    </td>
                </tr>
            </table>
            
            <hr style="border:0; border-top:1px solid #7C3AED; height:1px; margin-bottom:15px;"/>
            
            <!-- Document Body -->
            <div style="font-size:11.5px; color:#374151; line-height:1.6; min-height:350px;">
                {body_text}
            </div>
            
            <!-- Sign-off -->
            <div style="margin-top:40px; font-size:11.5px;">
                <p>Yours sincerely,</p>
                <p style="margin-top:15px; font-weight:700; color:#111827; margin-bottom:0;">{st.session_state.signer_name}</p>
                <p style="color:#6B7280; margin-top:0;">{st.session_state.signer_designation}<br/><b>{st.session_state.company_name}</b></p>
            </div>
            
            <!-- Specific Acceptance block for Offer Letter -->
            {'''
            <div style="margin-top:20px; background-color:#F9FAFB; border:1px solid #E5E7EB; padding:10px; border-radius:6px; font-size:10.5px;">
                <b>Acceptance:</b><br/>
                <span style="font-style:italic; color:#4B5563;">I accept the aforesaid terms & conditions and this offer.</span>
                <table style="width:100%; border:none; margin-top:10px;">
                    <tr>
                        <td>Signature: ______________________</td>
                        <td>Date: ______________________</td>
                    </tr>
                </table>
            </div>
            ''' if selected_doc == "Offer Letter" else ""}
        </div>
        """, unsafe_allow_html=True)
