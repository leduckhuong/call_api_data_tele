import re

def is_valid_mail_password(string):
    pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}:.+$'
    return bool(re.match(pattern, string))

def check_line_format(line):
    # url:user:pass
    # url:mail:pass
    if(line.count(":")==3 and ( line.startswith("http://") or line.startswith("https://") or line.startswith("apk://") or line.startswith("chrome://") )):
        return 1
    # url mail:pass
    elif(line.count(":")==2 and ( line.startswith("http://") or line.startswith("https://") or line.startswith("apk://") or line.startswith("chrome://") )):
        return 2
    # nimrarana4000@gmail.com:nimra11223      https://www.expressvpn.com/sign-in
    elif (line.count(":")==2 and ("http://" in line or "https://" in line or "apk://" in line)):
        return 3
    # Mail:pass date
    elif (is_valid_mail_password(line) and line.count(":")==1 and line.count(" ") == 1):
        return 4
    # user:pass
    elif (is_valid_mail_password(line) and line.count(":")==1):
        return 5
    return 6