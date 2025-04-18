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

def update_locations(consolidated):
    # Keys you want to rename - works
    key_replacements = {
        "W": "Office",
        "X": "Bedroom",
        "Y": "Kitchen",
        "Z": "Outdoor"
    }  

    updatedresult = {
        key_replacements.get(k, k): v for k, v in consolidated.items()
    }
    return updatedresult

def generate_html(result):
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

    for item in result:
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


    text = """\
    Hi,
    This is latest data collected.
    """

# Turn these into plain/html MIMEText objects
    
    part1 = MIMEText(htmltable, 'html')

# Add both parts to MIMEMultipart (HTML last for email clients that prefer it)
    
    message.attach(part1)

    # Send the email via SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        return "Email sent successfully!"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None
    finally:
        server.quit()

def main():
    parseoutput = parse()
    locations = update_locations(parseoutput)
    htmlcode = generate_html(locations)
    mailto(htmlcode)
    return "data collected and sent"

if __name__ == "__main__":
    result = main()
    print(result)
