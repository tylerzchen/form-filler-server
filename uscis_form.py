import boto3
import datetime
import json
from fillpdf import fillpdfs
import os
import uuid
from send_email import send_email_with_attachment

s3 = boto3.client('s3')
ses = boto3.client('ses')

# S3 Configuration
bucket_name = 'caucustest'
s3_key_prefix = 'documents/casework-forms'
input_pdf_s3_key = os.path.join(s3_key_prefix, 'uscis-privacy-release.pdf')

from_address = os.environ.get('FROM_ADDRESS')
password = os.environ.get('pas')
to_address = os.environ.get('TO_ADDRESS')

def get_cors_headers():
   """
   Returns CORS headers
   """
   return {
       'Access-Control-Allow-Origin': '*',
       'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
       'Access-Control-Allow-Methods': 'POST, OPTIONS'
   }


def fill_form(event, context):
  
   # Define temporary local file paths
   # Using unique names to avoid potential conflicts if the function runs concurrently
   request_id = uuid.uuid4()
   local_input_path = f"/tmp/{request_id}_input.pdf"
   local_output_path = f"/tmp/{request_id}_filled.pdf"
  
   try:
       body = json.loads(event.get('body', '{}'))


       # 1. Download the PDF template from S3 to /tmp
       print(f"Downloading {input_pdf_s3_key} from bucket {bucket_name} to {local_input_path}")
       s3.download_file(bucket_name, input_pdf_s3_key, local_input_path)
       print("Download complete.")


       # Extract form data from the request body
       member_of_congress = body.get('congressMember', '')
       petitioner_name = body.get('petitionerName', '')
       petitioner_dob = body.get('petitionerDOB', '')
       petitioner_alien_number = body.get('petitionerAlienNumber', '')
       petitioner_country_of_birth = body.get('petitionerCountryOfBirth', '')
       beneficiary_name = body.get('beneficiaryName', '')
       beneficiary_dob = body.get('beneficiaryDOB', '')
       beneficiary_alien_number = body.get('beneficiaryAlienNumber', '')
       beneficiary_country_of_birth = body.get('beneficiaryCountryOfBirth', '')
       uscis_number = body.get('uscisNumber', '')
       filing_date = body.get('filingDate', '')
       filing_place = body.get('filingPlace', '')
       form_types = body.get('formTypes', {})
       other_form_type = body.get('otherFormType', '')
       issue_description = body.get('issueDescription', '')
       staff_member = body.get('staffMember', '')
       staff_phone = body.get('staffPhone', '')
       staff_email = body.get('staffEmail', '')
       subject_name = body.get('subjectName', '')
       authorized_congress_member = body.get('authorizedCongressMember', '')
       signature_date = body.get('signatureDate', '')
       address = body.get('address', '')
       phone = body.get('phone', '')
       email = body.get('email', '')


       # Create mapping for form fields
       data_dict = {
           'Member of Congress': member_of_congress,
           'Name': petitioner_name,
           'Date of Birth': petitioner_dob,
           'Alien number if any': petitioner_alien_number,
           'Country of Birth': petitioner_country_of_birth,
           'Name_2': beneficiary_name,
           'Date of Birth_2': beneficiary_dob,
           'Alien number if any_2': beneficiary_alien_number,
           'Country of Birth_2': beneficiary_country_of_birth,
           'USCIS receipt number or tracking number no Social Security numbers': uscis_number,
           'Date of filing': filing_date,
           'Place of filing': filing_place,
           'Other': other_form_type,
           'Description': issue_description,
           'Staff Member print': staff_member,
           'Phone': staff_phone,
           'Email': staff_email,
           'I print your name': subject_name,
           'permitted by law to SenatorRepresentative': authorized_congress_member,
           'Date': signature_date,
           'Address': address,
           'Phone_2': phone,
           'Email_2': email
       }
      
       # Add form type checkboxes
       form_type_fields = {
           'G-639': 'G639',
           'I-90': 'I90',
           'I-129': 'I129',
           'I-129F': 'I129F',
           'I-130': 'I130',
           'I-131': 'I131',
           'I-140': 'I140',
           'I-212': 'I212',
           'I-290B': 'I290B',
           'I-360': 'I360',
           'I-485': 'I485',
           'I-526': 'I526',
           'I-539': 'I539',
           'I-589': 'I589',
           'I-590': 'I590',
           'I-600A': 'I600A',
           'I-600': 'I600',
           'I-601': 'I601',
           'I-612': 'I612',
           'I-690': 'I690',
           'I-730': 'I730',
           'I-751': 'I751',
           'I-765': 'I765',
           'I-821': 'I821',
           'I-824': 'I824',
           'I-829': 'I829',
           'I-914': 'I914 Supplement A B or C',
           'I-918': 'I918',
           'I-924': 'I924',
           'I-929': 'I929',
           'N-400': 'N400',
           'N-600': 'N600',
           'N-565': 'N565',
           'N-644': 'N644'
       }
      
       # Set checkbox values
       for form_key, pdf_field in form_type_fields.items():
           data_dict[pdf_field] = 'On' if form_types.get(form_key, False) else 'Off'
      
       print("Form data to be filled:", data_dict)
      
       # 2. Write the filled PDF to /tmp
       print(f"Filling PDF from {local_input_path} to {local_output_path}")
       fillpdfs.write_fillable_pdf(
           input_pdf_path=local_input_path,
           output_pdf_path=local_output_path,
           data_dict=data_dict
       )
       print("PDF filling complete.")


       # 3. Upload the filled PDF to S3
       # Use a unique name for the output file, e.g., timestamp or UUID
       timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
       output_pdf_s3_key = os.path.join(s3_key_prefix, f"uscis-privacy-release-filled-{timestamp}-{request_id}.pdf")
       print(f"Uploading filled PDF {local_output_path} to s3://{bucket_name}/{output_pdf_s3_key}")
       s3.upload_file(local_output_path, bucket_name, output_pdf_s3_key)
       print("Upload complete.")
       
       # Prepare email content
       subject = f'{member_of_congress} Privacy Release Form for {petitioner_name}'
       body_text = f'Hello,\r\nPlease find attached the privacy release form for {petitioner_name} filed on {filing_date} at {filing_place}. \n {petitioner_name} had the following description of the issue: \n {issue_description}\n Regards, Caucus Digital Constituent Assistant'

       # Send email with attachment using the new function
       print(f"Attempting to send email notification to {to_address} from {from_address} with attachment {local_output_path}")
       message_id = send_email_with_attachment(
           subject=subject,
           body_text=body_text,
           to_address=to_address,
           from_address=from_address,
           attachment_path=local_output_path
       )

       if message_id:
           print(f"Email sent successfully. Message ID: {message_id}")
       else:
           print("Failed to send email notification.")
           # Decide if failure to send email should be a 500 error or just logged
           # For now, we continue and return 200 as the form was processed and uploaded

       return {
           'statusCode': 200,
           'headers': get_cors_headers(),
           'body': json.dumps({
               'message': 'Form filled successfully and uploaded to S3',
               's3_path': f"s3://{bucket_name}/{output_pdf_s3_key}"
           })
       }


   except Exception as e:
       print(f"Error processing request: {e}")
       # Log the full exception traceback for debugging
       import traceback
       traceback.print_exc()
       return {
           'statusCode': 500,
           'headers': get_cors_headers(),
           'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
       }


   finally:
       # 4. Clean up local temporary files regardless of success or failure
       if os.path.exists(local_input_path):
           try:
               os.remove(local_input_path)
               print(f"Removed temporary input file: {local_input_path}")
           except OSError as e:
               print(f"Error removing temporary input file {local_input_path}: {e}")
       if os.path.exists(local_output_path):
           try:
               os.remove(local_output_path)
               print(f"Removed temporary output file: {local_output_path}")
           except OSError as e:
               print(f"Error removing temporary output file {local_output_path}: {e}")





