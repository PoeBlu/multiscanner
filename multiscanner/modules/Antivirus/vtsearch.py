# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
import json
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import time

__author__ = "Drew Bonasera"
__license__ = "MPL 2.0"

TYPE = "Antivirus"
NAME = "VirusTotal"
REQUIRES = ["MD5"]
DEFAULTCONF = {
    'apikey': None,
    'ENABLED': True
}


def check(conf=DEFAULTCONF):
    if not conf['ENABLED']:
        return False
    return False if None in REQUIRES else bool(conf['apikey'])


def scan(filelist, conf=DEFAULTCONF):
    # Check for key rotation
    apikey = conf['apikey']
    rotkey = False
    if isinstance(conf['apikey'], list):
        rotkey = _repeatlist(conf['apikey'])
        apikey = rotkey.next()
    results = []
    md5s, junk = REQUIRES[0]
    requests = [[]]
    md5name = {}
    for fname, md5 in md5s:
        if len(requests[-1]) == 25:
            requests.append([])
        requests[-1].append(md5)
        md5name[md5] = fname
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    for md5list in requests:
        result = None
        while not result:
            param = {'resource': ', '.join(md5list), 'apikey': apikey}
            data = urlencode(param).encode('ascii')
            try:
                result = urlopen(url, data)
                result = result.read()
            except Exception as e:
                result = None
            if not result:
                time.sleep(30)
            if rotkey:
                apikey = rotkey.next()
        jdata = json.loads(result)
        if isinstance(jdata, list):
            for j in jdata:
                if ret := _vt_report(j, md5name):
                    results.append(ret)
        elif ret := _vt_report(jdata, md5name):
            results.append(ret)
    metadata = {"Name": NAME, "Type": TYPE, "Include": False}
    return (results, metadata)


def _vt_report(report, md5name):
    if report['response_code'] == 0:
        return None
    if report['response_code'] == 1:
        fname = md5name[report['md5']]
        del report['response_code']
        del report['verbose_msg']
        return (fname, report)


def _repeatlist(data):
    while True:
        yield from data
