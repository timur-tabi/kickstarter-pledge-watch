#!/usr/bin/env python

# Copyright 2013, Timur Tabi
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# This software is provided by the copyright holders and contributors "as is"
# and any express or implied warranties, including, but not limited to, the
# implied warranties of merchantability and fitness for a particular purpose
# are disclaimed. In no event shall the copyright holder or contributors be
# liable for any direct, indirect, incidental, special, exemplary, or
# consequential damages (including, but not limited to, procurement of
# substitute goods or services; loss of use, data, or profits; or business
# interruption) however caused and on any theory of liability, whether in
# contract, strict liability, or tort (including negligence or otherwise)
# arising in any way out of the use of this software, even if advised of
# the possibility of such damage.

import sys
import os
import re
import tempfile
import subprocess
import time
import datetime
import smtplib
import getpass
import urllib2
import lxml.html
import webbrowser
from optparse import OptionParser, OptionGroup

# Command line options are global
options = None
args = None

# Get the command-line parameters
def command_line():
    global options, args

    parser = OptionParser(usage='usage: %prog <project-home-url> <pledge-amount>',
        description='')

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)

def find_reward(tree, reward):
    rewards = []

    for e in tree.findall('.//li[@class="reward"]'):
        rewards.append(e)
    for e in tree.findall('.//li[@class="reward shipping"]'):
        rewards.append(e)
    for e in tree.findall('.//li[@class="disabled reward"]'):
        rewards.append(e)
    for e in tree.findall('.//li[@class="disabled reward shipping"]'):
        rewards.append(e)

    for r in rewards:
        for e in r:
            if e.tag == 'input':
                if float(e.attrib['title'][1:].replace(',', '')) == reward:
                    return r

    print 'Pledge amount not found'
    print 'Valid levels:',
    for r in rewards:
        for e in r:
            if e.tag == 'input':
                print e.attrib['title'][1:].rstrip('0').rstrip('.'),
    print

    return None

def login():
    global options, args
    status = None

    # Generate the URL
    url = args[0].split('?', 1)[0]  # drop the stuff after the ?
    url += '/pledge/new' # we want the pledge-editing page

    while True:
        f = urllib2.urlopen(url)
        response = f.read()
        f.close()

        tree = lxml.html.fromstring(response)

        reward = find_reward(tree, float(args[1]))
        if reward is None:
            break
        s = reward.attrib['class']
        if not status:
            status = s
        if status != s:
            print 'Status changed!'
            webbrowser.open_new_tab(url)
            sleep(10)   # Give the web browser time to open
            break

        for e in reward.findall('.//p[@class="remaining"]'):
            print e.text

        time.sleep(60)

command_line()
login()
