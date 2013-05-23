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
import time
import urllib2
import HTMLParser
import webbrowser

statuses = ['reward', 'reward shipping', 'disabled reward',
           'disabled reward shipping', 'last reward shipping']

# Parse the pledge HTML page
#
# It looks like this:
#
# <li class="reward shipping" ...>
# <input alt="$75.00" ... title="$75.00" />
# ...
# </li>
#
# So we need to scan the HTML looking for <li> tags with the proper class,
# (the class is the status of that pledge level), and then remember that
# status as we parse inside the <li> block.  The <input> tag contains a title
# with the pledge amount.  We return a list of tuples that include the pledge
# level, its status, and the number of remaining slots
#
# The 'rewards' dictionary uses the reward value as a key, and
# (status, remaining) as the value.
class KickstarterHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_li_block = False    # True == we're inside an <li class='...'> block
        self.in_p_block = False     # True == we're inside a <p class='remaining'> block
        self.rewards = []
        self.remaining = None

    def process(self, url) :
        f = urllib2.urlopen(url)
        html = unicode(f.read(), 'utf-8')
        f.close()
        self.feed(html)   # feed() starts the HTMLParser parsing
        return self.rewards

    def handle_starttag(self, tag, attributes):
        global status

        attrs = dict(attributes)

        # It turns out that we only care about tags that have a 'class' attribute
        if not 'class' in attrs:
            return

        if self.in_li_block and tag == 'input':
            # Convert the value into a float
            self.value = float(attrs['title'][1:].replace(',', ''))

        if self.in_li_block and tag == 'p' and attrs['class'] == 'remaining':
            self.in_p_block = True
            self.remaining = None

        if tag == 'li' and attrs['class'] in statuses:
            self.in_li_block = True
            # Remember the status of this <li> block
            self.status = attrs['class']

    def handle_endtag(self, tag):
        if tag == 'li':
            if self.in_li_block:
                self.rewards.append((self.value, self.status, self.remaining))
                self.in_li_block = False
        if tag == 'p':
            self.in_p_block = False

    def handle_data(self, data):
        if self.in_p_block:
            self.remaining = data

    def result(self):
        return self.rewards

# Generate the URL
url = sys.argv[1].split('?', 1)[0]  # drop the stuff after the ?
url += '/pledge/new' # we want the pledge-editing page
pledge = float(sys.argv[2])

status = None
ks = KickstarterHTMLParser()

while True:
    rewards = ks.process(url)

    s = next(r for r in rewards if r[0] == pledge)
    status = status or s[1]     # Initialize 'status' once

    if status != s[1]:
        print 'Status changed!'
        webbrowser.open_new_tab(url)
        time.sleep(10)   # Give the web browser time to open
        break

    print s[2]

    time.sleep(60)
