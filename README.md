kickstarter-pledge-watch
========================

This Python program notifies you when a locked Kickstarter pledge level
becomes available.  When the pledge is available, the program opens a
web browser window to the pledge, allowing you to enter the pledge
amount and select the new pledge.

kswatch.py must be run from the command line.  Since this is a Python
program, you must have Python installed.

Usage: kswatch.py project-url [cost-of-pledge]

Where project-url is the URL of the Kickstarter project, and cost-of-pledge
is the cost of the target pledge. If cost-of-pledge is not specified, then
a menu of pledges is shown.  Specify cost-of-pledge only if that amount
is unique among pledges.  Only restricted pledges are supported.

Example:

$ ./kswatch.py https://www.kickstarter.com/projects/1300298569/under-the-dog
1. $20 RECRUIT ============================== [Early Backer $25] HD Digital D
2. $30 SENIOR ATTENDANT ============================== [Early Backer $35] Dig
3. $40 SENIOR ANALYST ============================== [Early Backer $45] Digit
4. $50 SENIOR OPERATIVE ============================== [Early Backer $55] Dig

Select pledge levels:


I believe that this script does not violate the Kickstarter terms of service
(TOS):

   Additionally, you shall not: (i) take any action that imposes or may
   impose (as determined by the Company in its sole discretion) an
   unreasonable or disproportionately large load on the Company's or its
   third-party providers' infrastructure; (ii) interfere or attempt to
   interfere with the proper working of the Service or any activities
   conducted on the Service; (iii) bypass any measures the Company may use to
   prevent or restrict access to the Service (or other accounts, computer
   systems, or networks connected to the Service); (iv) run Maillist,
   Listserv, or any form of auto-responder or "spam" on the Service; or (v)
   use manual or automated software, devices, or other processes to "crawl"
   or "spider" any page of the Site.

As long as this script is run no more frequently than once a minute, it will
not "impose ... an unreasonable or disproportionately large load on the
Company's or its third-party providers' infrastructure".  Secondly, this tool
does not "crawl" or "spider" the Kickstarter web site or any page.  Wikipedia
defines crawling as "an Internet bot that systematically browses the World
Wide Web, typically for the purpose of Web indexing."  The script does not
index any pages, it just scrapes a single page.
