import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ses = boto3.client('ses')
CHARSET = "UTF-8"

def send_email_with_attachment(subject, body_text, to_address, from_address, attachment_path):
    """
    Sends an email with an attachment using AWS SES send_raw_email.

    Args:
        subject (str): The subject line of the email.
        body_text (str): The plain text body of the email.
        to_address (str): The recipient email address.
        from_address (str): The sender email address (must be verified with SES).
        attachment_path (str): The local path to the file to be attached.

    Returns:
        str: The message ID if the email was sent successfully, None otherwise.
    """
    if not os.path.exists(attachment_path):
        print(f"Error: Attachment file not found at {attachment_path}")
        return None

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Create the body of the message (a plain text part).
    # You could add an HTML part here as well inside 'alternative' if needed.
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(body_text.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)

    # Attach the body part to the main message.
    msg.attach(msg_body)

    # Define the attachment part and encode it using MIMEApplication.
    try:
        with open(attachment_path, 'rb') as f:
            att = MIMEApplication(f.read())
    except Exception as e:
        print(f"Error reading attachment file {attachment_path}: {e}")
        return None

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))

    # Attach the attachment to the main message.
    msg.attach(att)

    try:
        # Provide the contents of the email.
        response = ses.send_raw_email(
            Source=from_address,
            Destinations=[
                to_address
            ],
            RawMessage={
                'Data': msg.as_string(),
            }
            # If you need to use a configuration set, uncomment the following line
            # ConfigurationSetName="YourConfigSet" # Replace with your config set name if used
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_message = e.response.get('Error', {}).get('Message', 'No message available')
        print(f"SES ClientError sending email: {error_code} - {error_message}")
        # Specific handling for common errors
        if error_code == 'MessageRejected':
             print("Message was rejected. Check SES sandbox status and verified emails.")
        elif error_code == 'MailFromDomainNotVerifiedException':
             print(f"The sending domain for {from_address} is not verified.")
        elif error_code == 'ConfigurationSetDoesNotExistException':
             print("The specified Configuration Set does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred sending email: {e}")
        return None
    else:
        message_id = response.get('MessageId')
        if message_id:
             print(f"Email sent! Message ID: {message_id}")
             return message_id
        else:
             print("Email sent but no Message ID returned in response.")
             return None

        
