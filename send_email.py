import smtplib,email,ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import datetime




def generate_email(csvfile,recv):

    sender_email = "chetantayal.cs17@rvce.edu.in"
    reciever_email = recv
    password = "iamaboy3801"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = reciever_email
    message['Subject'] = 'CSV FILE'
    today = datetime.date.today()
    body = "DATED FOR " + str(today)

    
    
    message.attach(MIMEText(body,'plain'))
    
    filename = csvfile
    
    
    with open(filename,"rb") as attachment :
        part = MIMEBase("application","octet-stream")
        part.set_payload(attachment.read())
    
    
    encoders.encode_base64(part)
    part.add_header("Content-Disposition","attachment; filename="+filename,)
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,reciever_email,text)



    return True

            
