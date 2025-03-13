from email.mime.text import MIMEText
from smtplib import SMTP as SMTP, SMTPConnectError, SMTPRecipientsRefused, SMTPHeloError


class MailUtils:

    def __init__(self, host):
        self.host = host

    def send_mail(self, subject, body, to_address, from_address="poststelle@blha.brandenburg.de") -> bool:
        try:
            body = '<font face="Arial Narrow">' + body + '</font>'
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = from_address
            msg['To'] = to_address
            # msg.set_content(body)
            # host: str = ApplicationParamModel.find_by_id(ApplicationParamModel.MAIL_SMTP_HOST).param_value

            with SMTP(self.host) as smtp:
                smtp.send_message(msg)
                return True
        except (SMTPConnectError, SMTPRecipientsRefused, SMTPHeloError):
            return False
