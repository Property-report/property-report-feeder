import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders
from src import config
from botocore.client import Config
from smtplib import SMTP
from jinja2 import Environment, FileSystemLoader


# from flask import render_template, Flask
# import os
# from flask_mail import Mail, Message

keyId = config.AWS_ACCESS_KEY
sKeyId = config.AWS_SECRET_KEY

# app = Flask(__name__)

client = boto3.client('s3',
                      aws_access_key_id=keyId,
                      aws_secret_access_key=sKeyId,
                      config=Config(signature_version='s3v4'),
                      region_name='eu-west-2')

# app = Flask(__name__)
# app.config.update(
#     MAIL_SERVER='smtp.ionos.com',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=False,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME=config.email
# )
# mail = Mail(app)


def send_email_with_s3_attachment_and_html(created_doc, email, formatted_address):
    # Fetch the PDF from S3
    file_object = client.get_object(Bucket=config.BUCKET_ID, Key=config.BUCKET_NAME +
                                    '/property_reports/' + created_doc['document_name']+'.pdf')
    file_content = file_object['Body'].read()

    # Create the Jinja2 environment
    template_loader = FileSystemLoader(searchpath=config.doc_location)
    env = Environment(loader=template_loader)

    # Load the template
    template = env.get_template(f'/report_email.html')

    rendered_template = template.render(

    )

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = config.email
    msg['To'] = email
    msg['Subject'] = f"your property report for {formatted_address}"

    # Attach the HTML content
    html_content = MIMEText(rendered_template, 'html')
    msg.attach(html_content)

    # Attach the PDF
    pdf_attachment = MIMEApplication(file_content, 'octet-stream')
    pdf_attachment.add_header(
        'Content-Disposition', 'attachment', filename=created_doc['document_name'])
    msg.attach(pdf_attachment)

    # Send the email
    with SMTP('smtp.ionos.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(config.email, config.email_password)
        smtp.send_message(msg)
