import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(user, message):
    """
    :param user:
    :param message:
    :return: 邮件发送
    """
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr(["监控", 'txzqmonitor@126.com'])
    msg['To'] = formataddr(["同信监控", 'txzqmonitor@126.com'])
    msg['Subject'] = "短信下发接口监控"

    try:
        server = smtplib.SMTP("smtp.126.com", 25, timeout=5)
        server.set_debuglevel(1)
        server.login("txzqmonitor@126.com", "txzq126")  # 126邮箱需要开启SMTP功能，使用授权码
        server.sendmail('txzqmonitor@126.com', ['txzqmonitor@126.com',], msg.as_string())
        server.quit()
    except Exception as err:
        print(err)
