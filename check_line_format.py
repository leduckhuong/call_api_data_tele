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
    elif (line.count(":")==1 and line.count(" ") == 1):
        return 4
    # {"id": "f67ca3bf-04c4-4e1f-bf56-f6951b2113bf", "name": "Илья", "phone": "+79998590783", "email": "ilya89999691659@gmail.com", "roles": "", "status": "ACTIVE", "organizations": [], "operationAreas": []}
    elif ("name" in line and "phone" in line and "email" in line):
        return 5
    # user:pass
    elif (line.count(":")==1):
        return 6
    return 7