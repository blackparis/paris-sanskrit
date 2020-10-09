from application import envs
import os

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def validate_username(username):
    if len(username) > 18 or len(username) < 4:
        return False
    if not username[0].isalnum() or not username[-1].isalnum():
        return False
    for c in username:
        if not c.isalnum():
            if c != '.' and c != '_' and c != '-':
                return False
    return True


def validate_password(password):
    if not password[0].isalnum() or not password[-1].isalnum():
        return False

    if len(password) < 8:
        return False

    spchar = False
    alpha = False
    number = False

    for c in password:
        if c == " ":
            return False
        if c.isalpha():
             alpha = True
        if c.isnumeric():
            number = True
        if not c.isalnum():
            spchar = True

    if spchar and alpha and number:
        return True
    
    return False


def validate_email(emailaddress):
    pos_AT = 0
    count_AT = 0
    count_DT = 0
    if emailaddress[0] == '@' or emailaddress[-1] == '@':
        return False
    if emailaddress[0] == '.' or emailaddress[-1] == '.':
        return False
    for c in range(len(emailaddress)):
        if emailaddress[c] == '@':
            pos_AT = c
            count_AT = count_AT + 1
    if count_AT != 1:
        return False
        
    username = emailaddress[0:pos_AT]
    if not username[0].isalnum() or not username[-1].isalnum():
        return False
    for d in range(len(emailaddress)):
        if emailaddress[d] == '.':
            if d == (pos_AT+1):
                return False
            if d > pos_AT:
                word = emailaddress[(pos_AT+1):d]
                if not word.isalnum():
                    return False
                pos_AT = d
                count_DT = count_DT + 1
    if count_DT < 1 or count_DT > 2:
        return False
        
    return True


def sendemail(email, content):
    return True
    subject = content["subject"]
    message = content["message"]
    msg = MIMEMultipart("alternative")
    msg["From"] = envs.SANSKRIT_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'html'))
    try:
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(envs.SANSKRIT_EMAIL, envs.SANSKRIT_PASSWORD)
        server.sendmail(envs.SANSKRIT_EMAIL, email, msg.as_string())
        server.quit()
    except:
        return False
    else:
        return True


def getVerificationEmailContent(code):
    subject = "Verify Your Email Address"
    message = f"""
    <html>
        <head></head>
        <body style="text-align: center; padding: 50px;">
            <h2>Verification Code</h2>
            <h4>{code}</h4>
            <br>
            <p>Note, this e-mail was sent from an address that cannot accept incoming e-mails.</p>
        </body>
    </html>
                """

    return {
        "subject": subject,
        "message": message
    }


def random_hex_bytes(n_bytes):
    """Create a hex encoded string of random bytes"""
    return os.urandom(n_bytes).hex()


def validate_mobile(mobile):
    if len(mobile) < 10:
        return False

    if mobile[0] == "+":
        m = mobile[1:]
    else:
        m = mobile[:]

    for c in m:
        if not c.isnumeric():
            if c == " " or c == "-":
                pass
            else:
                return False
    
    return True


def get_secret_email(email):
    e = email[0]
    d = email.split('@')
    em = d[0]
    dm = d[1]
    for _ in range(len(em)-1):
        e = e + '*'
    
    return e + '@' + dm