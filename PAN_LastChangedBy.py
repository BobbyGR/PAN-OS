#Small Script that uses the PALO ALTO API to get the name of the last person who made a configuration
#Change.
import re
import pycurl
import urllib3
from StringIO import StringIO

deviceip = ""  #This is your PA ip address
pa_key = "" #This is your PA API key

#Get the last JOBID
buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, "https://"+deviceip+"/api/?type=log&log-type=config&key="+pa_key)
c.setopt(c.WRITEDATA, buffer)
c.setopt(c.SSL_VERIFYPEER, 0)
c.perform()
c.close()
jobid = buffer.getvalue()
re1 = '.*?'
re2 = '\\d+'
re3 = '.*?'
re4 = '\\d+'
re5 = '.*?'
re6 = '(\\d+)'
rg = re.compile(re1+re2+re3+re4+re5+re6, re.IGNORECASE|re.DOTALL)
m = rg.search(jobid)
if m:
   jobid = m.group(1)
else:
   print "Unable to find the Job ID!"
   jobid = "0000"
#Get the last username to make a change based on the last job-id
if jobid != "0000":
  buffer = StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, "https://"+deviceip+"/api/?type=log&log-type=config&action=get&job-id="+jobid+"&key="+pa_key)
  c.setopt(c.WRITEDATA, buffer)
  c.setopt(c.SSL_VERIFYPEER, 0)
  c.perform()
  c.close()
  pa_config = buffer.getvalue()
  configLOC = os.path.dirname(os.path.realpath(__file__)) + "/PA.XML"
  target = open(configLOC, 'w')
  target.truncate()
  target.write(pa_config)
  #print pa_config
  f = open(configLOC, 'r')
  lines = f.readlines()
  userwhochanged = "Unknown"
  x = 0
  for line in lines:
      if x == 0:
        if re.match("(.*)admin(.*)", line):
            x = 1
            userwhochanged = str(line)
            userwhochanged = userwhochanged.replace("<admin>", "")
            userwhochanged = userwhochanged.replace("</admin>", "")
            userwhochanged = "".join(userwhochanged.split())
            print userwhochanged
