import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_document_email(smtp_host, smtp_port, sender_email, sender_password, recipient_email, subject, body, pdf_bytes, filename):
    """
    Sends an email containing a PDF document as an attachment using SMTP.
    Supports SSL and STARTTLS based on port number.
    
    Returns:
        tuple: (success (bool), message (str))
    """
    if not smtp_host or not smtp_port or not sender_email or not sender_password or not recipient_email:
        return False, "Missing SMTP credentials or recipient email address."

    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach the text body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach the PDF bytes
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)
        
        # Determine whether to use SSL or STARTTLS
        port = int(smtp_port)
        
        if port == 465:
            # Use SSL directly
            server = smtplib.SMTP_SSL(smtp_host, port, timeout=15)
        else:
            # Use STARTTLS (typically port 587 or 25)
            server = smtplib.SMTP(smtp_host, port, timeout=15)
            server.ehlo()
            server.starttls()
            server.ehlo()
            
        # Login and send
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        return True, f"Email delivered successfully to {recipient_email}!"
        
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication failed. Please verify your email and app password."
    except smtplib.SMTPConnectError:
        return False, "Failed to connect to the SMTP server. Please verify the host and port."
    except Exception as e:
        return False, f"An error occurred while sending the email: {str(e)}"
