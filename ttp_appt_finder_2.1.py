import smtplib
import datetime
import time
import requests
from dateutil import parser

#Ports 465 and 587 are intended for email client to email server communication - sending email
server = smtplib.SMTP('smtp.gmail.com', 587)

#starttls() is a way to take an existing insecure connection and upgrade it to a secure connection using SSL/TLS.
server.starttls()

#Next, log in to the server
server.login("nbhalsema@gmail.com", "ytvy qcdi qwvb jbgs")

#Send the mail
def notify(message):
    print(message)
    msg = '\n' + message
    server.sendmail("nbhalsema@gmail.com", "9497420309@vtext.com", msg)
    print('message sent')

# The last appointment that we've notified about, to prevent duplicate notifications
prevstart = None

def check():
    # Check if it's 12pm - if yes, let me know you're still running
    now = datetime.datetime.now()
    if now.hour == 12 and now.minute == 00:
        print('still running')
        notify(f'Still Running xx')
    global prevstart

    # Check if any appointments are available, and if so, notify
    # Return True on error

    # TODO: COMPLETE Update the URL to match your location. (Use network monitor to find the URL in their appointment selector.) This URL points to Blaine's NEXUS center.
    #resp = requests.get('https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&minimum=1') #any
    #resp = requests.get('https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId=5500&minimum=1') #maine *(for testing)
    resp = requests.get('https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&locationId=5020&minimum=1') #bellingham
    if not resp.ok:
        notify(f'Failed with status code {resp.status_code}')
        return True
    appts = resp.json()
    if len(appts) > 0:
        appt = appts[0]
        start = appt.get('startTimestamp', '2099-01-01T00:00')
    
        # Prevent duplicates
        if start != prevstart:
            print(f'Found appt on {start}')
            prevstart = start
            date = parser.parse(start)
            if date.year == 2024:
                notify(f'Found appointment on {start}')
    print(f'Found 0 appts ',  datetime.datetime.now())
    return False

while True:
    if check():
        # Wait for 15 mins after error
        time.sleep(60*15)
    else:
        # Wait 1 min otherwise
        time.sleep(60)
