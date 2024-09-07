import re
import urllib.request
import time
import dns.resolver


def domain_exists(email):
    domain = email.split('@')[-1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False

def extractEmailsFromUrlText(urlText, emailFile):
    emailRegex = re.compile(r'''
    (
    ([a-zA-Z0-9_.+-]+
    @
    [a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)
    )
    ''', re.VERBOSE)
    extractedEmail = emailRegex.findall(urlText)
    allemails = []
    for email in extractedEmail:
        allemails.append(email[0])

    print(f"\tNumber of Emails Found: {len(allemails)}")

    seen = set()
    for email in allemails:
        if email not in seen and domain_exists(email):
            seen.add(email)
            emailFile.write(email + "\n")

def htmlPageRead(url, i, emailFile):
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0'}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        urlHtmlPageRead = response.read()
        urlText = urlHtmlPageRead.decode()
        print(f"{i}.{url}\tFetched in : {time.time() - start:.2f} seconds")
        extractEmailsFromUrlText(urlText, emailFile)
    except Exception as e:
        print(f"Error reading {url}: {e}")

def emailsLeechFunc(url, i, emailFile):
    try:
        htmlPageRead(url, i, emailFile)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            try:
                url = 'http://webcache.googleusercontent.com/search?q=cache:' + url
                htmlPageRead(url, i)
            except Exception as e:
                print(f"Error with cached version of {url}: {e}")
        else:
            print(f"HTTP error {err.code} on {url}")

def scrap(name):
    start = time.time()

    urlFile = open("urls.txt", 'r')
    emailFile = open(f"{name}.txt", 'w')
    i = 0

    for urlLink in urlFile.readlines():
        urlLink = urlLink.strip('\'"')
        i += 1
        emailsLeechFunc(urlLink, i, emailFile)

    urlFile.close()
    emailFile.close()

    print(f"Elapsed Time: {time.time() - start:.2f} seconds")

if __name__=='__main__':
    scrap("thangamayil.com-backlinks")