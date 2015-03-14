#!/usr/bin/env python

"""
Copyright (c) 2014-2015 Miroslav Stampar (@stamparm)
See the file 'LICENSE' for copying permission
"""

import csv
import os
import subprocess
import urllib
import urllib2
import zipfile

from core.enums import TRAIL
from core.settings import NAME
from core.settings import TIMEOUT
from core.settings import TRAILS_FILE

def retrieve_content(url, data=None):
    """
    Retrieves page content from given URL
    """

    try:
        req = urllib2.Request("".join(url[i].replace(' ', "%20") if i > url.find('?') else url[i] for i in xrange(len(url))), data, {"User-agent": NAME})
        retval = urllib2.urlopen(req, timeout=TIMEOUT).read()
    except Exception, ex:
        retval = ex.read() if hasattr(ex, "read") else getattr(ex, "msg", str())
    return retval or ""

def check_sudo():
    """
    Checks for sudo/Administrator privileges
    """

    check = None

    if not subprocess.mswindows:
        if getattr(os, "geteuid"):
            check = os.geteuid() == 0
    else:
        import ctypes
        check = ctypes.windll.shell32.IsUserAnAdmin()

    return check

def extract_zip(filename, path=None):
    _ = zipfile.ZipFile(filename, 'r')
    _.extractall(path)

def addr_to_int(value):
    _ = value.split('.')
    return (long(_[0]) << 24) + (long(_[1]) << 16) + (long(_[2]) << 8) + long(_[3])

def int_to_addr(value):
    return '.'.join(str(value >> n & 0xFF) for n in (24, 16, 8, 0))

def make_mask(bits):
    return 0xffffffff ^ (1 << 32 - bits) - 1

def retrieve_file(url, filename=None):
    try:
        filename, _ = urllib.urlretrieve(url, filename)
    except:
        filename = None
    return filename

def load_trails(quiet=False):
    if not quiet:
        print "[i] loading trails file..."

    retval = dict((getattr(TRAIL, _), {}) for _ in dir(TRAIL) if _ == _.upper())

    try:
        with open(TRAILS_FILE, "rb") as f:
            reader = csv.reader(f, delimiter=',', quotechar='\"')
            reader.next()  # discard first (header) line
            for row in reader:
                type_, trail, info, reference = row
                retval[type_][trail] = (info, reference)

    except Exception, ex:
        exit("[x] something went wrong during trails file read '%s' ('%s')" % (TRAILS_FILE, ex))

    if not quiet:
        for type_ in retval:
            print "[i] %d %s trails loaded" % (len(retval[type_]), type_)

    return retval