import ujson
import base64
import urllib2
import socket
from ftplib import FTP, error_perm
import re
from StringIO import StringIO
import time

#creates a searalized json object for bill sources
def bill_source_to_json(url,source,date):
    jsonObj = {}
    jsonObj['url'] = url
    jsonObj['date'] = date
    jsonObj['source'] = base64.b64encode(source)

    return ujson.encode(jsonObj)


#wrapper for urllib2.urlopen that catches URLERROR and socket error
def fetch_url(url):

    #fetch ftp file
    if 'ftp://' in url:

        try:
            domain_pattern = re.compile("/[A-Za-z0-9\.]+")
            domain_name = domain_pattern.search(url).group(0)[1:]
            ftp = FTP(domain_name,timeout=10)
            ftp.login()
            file_name = "/".join(url.split("/")[3:])

            r = StringIO()
            ftp.retrbinary('RETR {0}'.format(file_name), r.write)
            document = r.getvalue()
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            document = None


        return document

    #fetch http file
    else:

        try:
            req  = urllib2.urlopen(url,timeout=10)
            document = req.read()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            document = None

        return document
