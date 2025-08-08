# email_sender.py
import smtplib, ssl, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email: str, app_password: str, receiver_email: str,
               cc_list: list, bcc_list: list, subject: str, body: str,
               email_format: str, attachment_path: str) -> bool:
    """
    Sends an email using Gmail's SMTP server with advanced options.
    """
    try:
        smtp_server = "smtp.gmail.com"
        port = 465  # For SSL

        # Create the root message object
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        
        # Add Cc recipients if any
        if cc_list:
            message["Cc"] = ", ".join(cc_list)
        
        # The list of all recipients for the sendmail command includes To, Cc, and Bcc
        all_recipients = [receiver_email] + cc_list + bcc_list
        
        # Attach the body of the email based on the selected format
        message.attach(MIMEText(body, email_format))
        
        # Handle the attachment if a path is provided
        if attachment_path and os.path.exists(attachment_path):
            print(f"   -> Attaching file: {os.path.basename(attachment_path)}")
            with open(attachment_path, "rb") as attachment_file:
                # Create a MIMEBase object
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment_file.read())
            
            # Encode the attachment in base64
            encoders.encode_base64(part)
            
            # Add a header to the attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            
            # Attach the part to the root message
            message.attach(part)
            
        # Create a secure SSL context and send the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, all_recipients, message.as_string())
            
        print("2. Email sent successfully.")
        return True

    except FileNotFoundError:
        print("   -> ERROR: Attachment file not found. Email not sent.")
        return False
    except Exception as e:
        print(f"   -> ERROR sending email: {e}")
        return False