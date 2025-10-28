#!/usr/bin/env python3

import os
import email
import smtplib
import random
import zipfile
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import make_msgid

# List of recipients (name, email address)
RECIPIENTS = [
#    ('Albra Welch', 'aw@pmcuda.com')
#   ('Avery Kim', 'akim@barracudademo.com'),
    ('Jordan Reyes', 'jreyes@barracudademo.com'),
    ('Morgan Patel', 'mpatel@barracudademo.com'),
    ('Riley Chen', 'rchen@barracudademo.com'),
    ('Taylor Alvarez', 'talvarez@barracudademo.com')
   ]

# Configuration pmcuda.com
#SMTP_SERVER = 'd337206.a.ess.de.barracudanetworks.com'
# Configuration barracudademo.com
SMTP_SERVER = 'd348911a.ess.barracudanetworks.com'
SMTP_PORT = 25
#MAX_RECIPIENTS = 1
MAX_RECIPIENTS = 4
DELAY_BETWEEN_EMAILS = 1  # seconds
EMAILS_PER_BATCH = 5
PAUSE_DURATION = 60  # seconds

def resend_email(original_msg, recipients, replace_from_name=False):
    for name, email_address in recipients:
        smtp = None
        try:
            # Create a new message
            new_msg = MIMEMultipart('alternative')
            new_msg['Subject'] = original_msg['Subject']
            
            # Include Date header
            new_msg['Date'] = email.utils.formatdate()

            # Include Message-ID
            new_msg['Message-ID'] = make_msgid()

            # Keep original From address
            new_msg['From'] = original_msg['From']

            # Include "Reply-To" header if available in the original message
            reply_to = original_msg.get('Reply-To')
            if reply_to:
                new_msg['Reply-To'] = reply_to

            # Extract email content
            for part in original_msg.walk():
                if part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                    try:
                        # Try different encodings
                        payload = part.get_payload(decode=True)
                        for encoding in ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
                            try:
                                decoded_content = payload.decode(encoding)
                                # Create MIMEText part with correct content type
                                mime_part = MIMEText(decoded_content, part.get_content_type().split('/')[1], encoding)
                                # Copy Content-Type header from original part
                                if 'Content-Type' in part:
                                    mime_part.replace_header('Content-Type', part['Content-Type'])
                                new_msg.attach(mime_part)
                                break
                            except UnicodeDecodeError:
                                continue
                        else:
                            # If no encoding worked, try with 'replace' error handler
                            decoded_content = payload.decode('utf-8', errors='replace')
                            new_msg.attach(MIMEText(decoded_content, part.get_content_type().split('/')[1], 'utf-8'))
                    except Exception as e:
                        print(f"Warning: Could not decode email content: {str(e)}")
                        # Fallback: attach the original part
                        new_msg.attach(part)
                elif part.get_content_maintype() == 'multipart':
                    continue
                else:
                    try:
                        attachment = MIMEBase(part.get_content_maintype(), part.get_content_subtype())
                        attachment.set_payload(part.get_payload(decode=True))
                        encoders.encode_base64(attachment)
                        filename = part.get_filename()
                        if filename:
                            attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                        new_msg.attach(attachment)
                    except Exception as e:
                        print(f"Warning: Could not process attachment: {str(e)}")

            new_msg['To'] = email_address

            # Create new SMTP connection for each recipient
            smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp.connect(SMTP_SERVER, SMTP_PORT)
            
            try:
                smtp.sendmail(original_msg['From'], email_address, new_msg.as_string().encode('utf-8'))
                print(f"Email sent successfully to {name} ({email_address})")
            except smtplib.SMTPException as e:
                print(f"Error sending email to {name} ({email_address}): {str(e)}")
        except Exception as e:
            print(f"Error sending email to {name} ({email_address}): {str(e)}")
        finally:
            if smtp:
                try:
                    smtp.quit()
                except:
                    pass

def main():
    # Check if zip file path is provided
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <zip_file_path>")
        sys.exit(1)

    zip_file_path = sys.argv[1]

    # Verify if the zip file exists
    if not os.path.exists(zip_file_path):
        print(f"Error: Zip file '{zip_file_path}' not found")
        sys.exit(1)

    email_counter = 0
    
    try:
        # Open the zip file and get the list of email filenames
        email_filenames = []
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            password = input("Enter the password for the zip file: ").encode('utf-8')
            zip_ref.setpassword(password)

            for name in zip_ref.namelist():
                if not name.endswith('/') and name.endswith('.eml') and not os.path.basename(name).startswith('.'):
                    email_filenames.append(name)

        if not email_filenames:
            print("No .eml files found in the zip file")
            sys.exit(1)

        # Iterate over email filenames and process each email
        for filename in email_filenames:
            print(f"\nReading email from file: {filename}")
            # Read the email content
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.setpassword(password)
                with zip_ref.open(filename) as email_file:
                    raw_email = email_file.read()

            # Parse the original email
            original_msg = email.message_from_bytes(raw_email)

            # Print sender and subject
            sender = original_msg['From']
            subject = original_msg['Subject']
            print(f"Sending email from: {sender}") 
            print(f"Subject: {subject}")

            # Choose a random number of recipients
            num_recipients = random.randint(1, min(MAX_RECIPIENTS, len(RECIPIENTS)))

            # Select random recipients
            selected_recipients = random.sample(RECIPIENTS, num_recipients)
            print(f"Number of recipients: {num_recipients}")

            # Resend the email to the randomly selected recipients
            resend_email(original_msg, selected_recipients, replace_from_name=True)

            # Increment email counter
            email_counter += 1

            # Check if we need to pause after batch
            if email_counter % EMAILS_PER_BATCH == 0:
                print(f"\nScript execution done - bye, buy...")
            else:
                time.sleep(DELAY_BETWEEN_EMAILS)


    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except zipfile.BadZipFile:
        print("Error: Invalid or corrupted zip file")
    except zipfile.BadPasswordError:
        print("Error: Incorrect password for zip file")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"\nEmail blast completed. Total emails sent: {email_counter}")
        sys.exit(0)

if __name__ == "__main__":
    main()