'''
Complete email related tasks.
'''
from smtplib import SMTP_SSL


class GmailClient:
    ''' Gmail client handles tasks related to gmail '''
    username = None
    password = None

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def send_gmail(self, to: str, body: str,
                   subject: str) -> None:
        ''' Send gmail from username -> to '''
        message = """ \
        From: {}
        To: {}
        Subject: {}

        {}
        """.format(self.username, to, subject, body)
        with SMTP_SSL("smtp.gmail.com", 465) as server_ssl:
            server_ssl.login(self.username, self.password)
            server_ssl.sendmail(self.username, to, message)
