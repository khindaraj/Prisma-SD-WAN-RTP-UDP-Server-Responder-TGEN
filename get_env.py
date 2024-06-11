#!/usr/bin/python

import os
import time
import random

random.seed()

n = random.uniform(0,6)
time.sleep(n)
print "Content-type: text/html\r\n\r\n";

print "Delayed response by "+ str(n) + " seconds"
print "<font size=+1>Environment</font><\br>";
for param in os.environ.keys():
   print "<b>%20s</b>: %s<\br>" % (param, os.environ[param])
