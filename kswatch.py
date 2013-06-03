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
        self.in_remaining_block = False # True == we're inside a <p class="remaining"> block
        self.in_desc_block = False # True == we're inside a <p class="description short"> block

    def process(self, url) :
        f = urllib2.urlopen(url)
        html = unicode(f.read(), 'utf-8')
        f.close()
        self.rewards = []
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
            self.ident = attrs['id']

        if self.in_li_block and tag == 'p':
            if attrs['class'] == 'remaining':
                self.in_remaining_block = True
            if attrs['class'] == 'description full':
                self.in_desc_block = True

        # We only care about certain kinds of reward levels -- those that
        # might be limited.
        if tag == 'li' and attrs['class'] in statuses:
            self.in_li_block = True
            # Remember the status of this <li> block
            self.status = attrs['class']
            self.remaining = ''
            self.description = ''

    def handle_endtag(self, tag):
        if tag == 'li':
            if self.in_li_block and self.remaining:
                self.rewards.append((self.value,
                    self.status,
                    self.remaining,
                    self.ident,
                    ' '.join(self.description.split())))
            self.in_li_block = False
        if tag == 'p':
            self.in_remaining_block = False
            self.in_desc_block = False

    def handle_data(self, data):
        if self.in_remaining_block:
            self.remaining += data
        if self.in_desc_block:
            self.description += self.unescape(data)

    def result(self):
        return self.rewards

def pledge_menu(rewards):
    import re

    count = len(rewards)

    if count == 1:
        return rewards[0]

    for i in xrange(count):
        print '%u. $%u %s' % (i + 1, rewards[i][0], rewards[i][4][:70])

    while True:
        try:
            ans = raw_input('\nSelect pledge levels: ')
            numbers = map(int, ans.split())
            return [rewards[i - 1] for i in numbers]
        except (IndexError, NameError, SyntaxError):
            continue

# Generate the URL
url = sys.argv[1].split('?', 1)[0]  # drop the stuff after the ?
url += '/pledge/new' # we want the pledge-editing page
pledges = None   # The pledge amounts on the command line
ids = None       # A list of IDs of the pledge levels
selected = None  # A list of selected pledge levels
rewards = None   # A list of valid reward levels
if len(sys.argv) > 2:
    pledges = map(float, sys.argv[2:])

stats = None   # A list of the initial statuses of the selected pledge level
ks = KickstarterHTMLParser()

while True:
    rewards = ks.process(url)

    if not rewards:
        print 'No limited rewards for this Kickstarter'
        sys.exit(0)

    if ids:
        selected = [r for r in rewards if r[3] in ids]
    else:
        if pledges:
            selected = [r for r in rewards if r[0] in pledges]
        else:
            # If a pledge amount was not specified on the command-line, then prompt
            # the user with a menu
            selected = pledge_menu(rewards)

        ids = [s[3] for s in selected]
        stats = [s[1] for s in selected]

    for stat, s, id in zip(stats, selected, ids):
        if stat != s[1]:
            print 'Status changed!'
            webbrowser.open_new_tab(url)
            ids = [x for x in ids if x != id]   # Remove the pledge we just found
            if not ids:     # If there are no more pledges to check, then exit
                time.sleep(10)   # Give the web browser time to open
                sys.exit(0)
            break   # Otherwise, keep going

    print [str(s[2]) for s in selected]

    time.sleep(60)
