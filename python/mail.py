import config
import smtplib
import email.message

class Mail:
    def __init__(self):
        self.sendInfo = {
            "From": config.MAIL_AUTHOR,
            "To": config.MAIL_SEND,
            "Subject": config.MAIL_SUBJECT
        }
        self.smtpInfo = {
            "Server": config.SMTP_SERVER,
            "Port": config.SMTP_PORT
        }
        self.logInfo = {
            "login": config.EMAIL_LOGIN,
            "password": config.EMAIL_PASSWORD
        }

    def change_content(self, change, chTo):
        cont = self.html_content
        cont.replace(change, chTo)
        self.html_content = cont

    def set_content(self, act_link):
        self.email_dir = config.MAIL_CONTENT
        f = open(self.email_dir, "r")
        self.html_content = f.read()
        f.close()
        #self.change_content(config.CHANGE_MAIL, config.AUTH_LINK)
        self.msg = email.message.Message()
        self.msg['Subject'] = self.sendInfo["Subject"]
        self.msg['From'] = self.sendInfo["From"]
        self.msg['To'] = self.sendInfo["From"]
        self.msg.add_header('Content-Type', 'text/html')
        self.msg.set_payload(config.EMAIL_CONTENT.replace("https://QWERTY_DHHAERYDJRfffgfg.com", act_link))

        print(self.msg.as_string())


    def set_emails(self, array = None, string = None):
        if array != None:
            res = ""
            for i in array:
                res += (i + " ")
        elif string != None:
            res = string

        if res[-1] == " ": res = res[:-1]

        num = res.count(" ")+1
        print(f"Для рассылки загружен {num} почтовых адресов")

        self.sendInfo["To"] = res

    def sendEmail(self):
        self.server = smtplib.SMTP(self.smtpInfo['Server'], str(self.smtpInfo['Port']))
        self.server.starttls()
        print("Подключено")
        self.server.login(self.logInfo['login'], self.logInfo['password'])
        self.server.sendmail(self.sendInfo["From"], self.sendInfo["To"], self.msg.as_string())
        self.server.close()