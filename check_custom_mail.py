

mail_extensions = ['@agribank.com.vn', '@gov.vn', '@edu.vn']

def check_custom_mail(mail):
    return any(mail.endswith(suffix) for suffix in mail_extensions)
