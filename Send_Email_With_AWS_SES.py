import smtplib
import os
import mimetypes
import time

from tqdm import tqdm #прогресс бар при обработке файлов
from email import encoders
from email.mime.text import MIMEText  # позволяет на русском письмо отправить
from email.mime.multipart import MIMEMultipart  # позволяет файлы прикрепить к письму
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
# -----------------------------
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_with_aws_ses():
    SENDER = 'XXXX@gmail.com'
    SENDERNAME = 'John Doe'
    RECIPIENT = 'YYYYY@gmail.com'

    USERNAME_SMTP = 'XXXXXXXXXXXXXXXXXX'
    PASSWORD_SMTP = 'XXxXXxxXXXxxxXXXXXXXXXX+XXXXXXXXXX'

    CONFIGURATION_SET = "ConfigSet"

    HOST = 'email-smtp.eu-central-1.amazonaws.com'
    PORT = 587

    SUBJECT = "HELOOOO AWSSSSSS"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )

    BODY_HTML = """<html>
    <head></head>
    <body>
      <h1>Amazon SES Test (SDK for Python)</h1>
      <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
    """

    try:
        with open("email_template.html") as file:
            BODY_HTML = file.read()

    except IOError:
        return "[-] the template file doesn't found!"

    # The HTML body of the email.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    # msg.add_header('X-SES-CONFIGURATION-SET', CONFIGURATION_SET)

    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')

    msg.attach(part1)
    msg.attach(part2)
    # --------------------- Attached Files ---------------------------
    for file in tqdm(os.listdir("attachments")):
        time.sleep(0.4)
        filename = os.path.basename(file)
        ftype, encoding = mimetypes.guess_type(file)  # определим тип файла
        file_type, subtype = ftype.split("/")  # application pdf

        if file_type == "text":
            with open(f"attachments/{file}", encoding='UTF-8') as f:
                file = MIMEText(f.read())
        elif file_type == "image":
            with open(f"attachments/{file}", "rb") as f:
                file = MIMEImage(f.read(), subtype)
        elif file_type == "audio":
            with open(f"attachments/{file}", "rb") as f:
                file = MIMEAudio(f.read(), subtype)
        elif file_type == "application":
            with open(f"attachments/{file}", "rb") as f:
                file = MIMEApplication(f.read(), subtype)
        else:
            with open(f"attachments/{file}", "rb") as f:
                file = MIMEBase(f.read(), subtype)
                file.set_payload(f.read())
                encoders.encode_base64(file)

        # with open(f"attachments/{file}", "rb") as f:
        #     file = MIMEBase(f.read(), subtype)
        #     file.set_payload(f.read())
        #     encoders.encode_base64(file)

        file.add_header('content-disposition', 'attachment', filename=filename)
        msg.attach(file)
    # ---------------------------------------------------
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()

        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    except Exception as e:
        return f'Error: {e}'
    else:
        return f'Email sent!'

def main():
    print(send_email_with_aws_ses())


if __name__ == '__main__':
    main()