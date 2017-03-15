# encoding:utf-8

import re
import smtplib
import dns.resolver

# Address used for SMTP MAIL FROM command
fromAddress = 'for_cyn@163.com'


def match_regex(email_address):
    """
    :param email_address:
    :return:
    """
    # Simple Regex for syntax checking  国外和国内的邮箱注册规则不一样，所以正则表达式只能代表部分情况。
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    match = re.match(regex, email_address)
    if match is None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')


# Email address to verify
# inputAddress = input('Please enter the emailAddress to verify:')
inputAddress = "mrcheng@163.com"
email_address = str(inputAddress)

# Syntax check


def get_mx(email_address):

    # Get domain for DNS lookup
    splitAddress = email_address.split('@')
    domain = str(splitAddress[1])
    print('Domain:', domain)

    # MX record lookup
    records = dns.resolver.query(domain, 'MX')
    print type(records[0])
    for i in records:
        print i
    mxRecord = records[0].exchange
    print mxRecord
    mxRecord = str(mxRecord)

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
    server.mail(fromAddress)
    code, message = server.rcpt(str(email_address))
    server.quit()

    # print(code)
    # print(message)

    # Assume SMTP response 250 is success
    if code == 250:
        print('Success')
    else:
        print('Bad')
