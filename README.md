kickstarter-pledge-watch
========================

This Python program notifies you when a locked Kickstarter pledge level
becomes available.

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
