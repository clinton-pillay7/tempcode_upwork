import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets


def parse():
    drives = ["W", 'X', 'Y', 'Z', 'F']
    consolidated = {}
    for drive in drives:
        drvpath = f"{drive}:\\"
        if os.path.exists(drvpath):
            with open(f"{drive}:\\latest_config_measurements.json", 'r') as h:
                datas = json.load(h)
                for data in datas["measurements"]:
                    tempresult = drive,":",data
                    consolidated[drive] = {}
                    consolidated[drive].update(data)
        else:
            consolidated[drive] = {}
            nodriveobj = {'co2_ppm': '-', 
                            'humidity_RH': '-', 
                            'pm01_ugm3': '-', 
                            'pm10_ugm3': '-', 
                            'pm25_AQICN': '-', 
                            'pm25_AQIUS': '-', 
                            'pm25_ugm3': '-', 
                            'temperature_C': '-', 
                            'temperature_F': '-', 
                            'voc_ppb': '-'}
            consolidated[drive].update(nodriveobj)
    return consolidated    

def update_rooms(consolidated):
    # Keys you want to rename - works
    key_replacements = {
        "W": "Office",
        "X": "Bedroom",
        "Y": "Kitchen",
        "Z": "Outdoor"
    }  

    updatedresult = {
        key_replacements.get(k, k): v for k, v in result.items()
    }
    return updatedresult

def generate_html(updatedresult):
    # Create HTML table
    html_table = """
    <table border="1">
        <tr>
            <th>Location</th>
            <th>co2_ppm</th>
            <th>humidity_RH</th>
            <th>pm01_ugm3</th>
            <th>pm10_ugm3</th>
            <th>pm25_AQICN</th>
            <th>pm25_AQIUS</th>
            <th>pm25_ugm3</th>
            <th>temperature_C</th>
            <th>temperature_F</th>
            <th>voc_ppb</th>
        </tr>
    """

    for item in updatedresult:
        html_table += f"""
        <tr>
            <td>{item}</td>
            <td>{result[item]["co2_ppm"]}</td>
            <td>{result[item]["humidity_RH"]}</td>
            <td>{result[item]["pm01_ugm3"]}</td>
            <td>{result[item]["pm10_ugm3"]}</td>
            <td>{result[item]["pm25_AQICN"]}</td>
            <td>{result[item]["pm25_AQIUS"]}</td>
            <td>{result[item]["pm25_ugm3"]}</td>
            <td>{result[item]["temperature_C"]}</td>
            <td>{result[item]["temperature_F"]}</td>
            <td>{result[item]["voc_ppb"]}</td>
        </tr>
    """

    html_table += "</table>"

    return html_table

def mailto(htmltable):


    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = secrets.sender_email
    sender_password = secrets.sender_password
    receiver_email = secrets.receiver_email

    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = "Air quality"
    message['From'] = sender_email
    message['To'] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    This is a plain text version of the message.
    """
    headers = ("co2_ppm","humidity_RH","pm01_ugm3","pm10_ugm3","pm25_AQICN","pm25_AQIUS","pm25_ugm3","temperature_C","temperature_F","voc_ppb")
    html = "<table border='1' style='border-collapse: collapse;'>"
        
    # Table headers
    html += "<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Add both parts to MIMEMultipart (HTML last for email clients that prefer it)
    message.attach(part1)
    message.attach(part2)

    # Send the email via SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
