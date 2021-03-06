import requests,urllib,socket,random,time,re,threading,sys,whois,json,os
import bs4
from bs4 import BeautifulSoup
from bane.payloads import *
if os.path.isdir('/data/data/com.termux/')==False:
    import dns.resolver
def info(u,timeout=10,proxy=None):
 '''
   this function fetchs all informations about the given ip or domain using check-host.net and returns them to the use as string
   with this format:
   'requested information: result'
    
   it takes 2 arguments:
   
   u: ip or domain
   timeout: (set by default to: 10) timeout flag for the request
   usage:
   >>>import bane
   >>>domain='www.google.com'
   >>>bane.info(domain)
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 try:
  h=''
  u='https://check-host.net/ip-info?host='+u
  c=requests.get(u, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout).text
  soup = BeautifulSoup(c,"html.parser")
  d=soup.find_all("tr")
  for a in d:
   try:
    b=str(a)
    if "IP address" not in b:
     a=b.split('<td>')[1].split('!')[0]
     a=a.split('</td>')[0].split('!')[0]
     c=b.split('<td>')[2].split('!')[0]
     c=c.split('</td>')[0].split('!')[0]
     if "strong" in c:
      for n in ['</strong>','<strong>']:
       c=c.replace(n,"")
     if "<a" in c:
      c=c.split('<a')[0].split('!')[0]
      c=c.split('</a>')[0].split('!')[0]
     if "<img" in c:
      c=c.split('<img')[1].split('!')[0]
      c=c.split('/>')[1].split('!')[0]
     n=a.strip()+': '+c.strip()
     h+=n+'\n'
   except Exception as e:
    pass
 except Exception as e:
  pass
 return h
def nortonrate(u,logs=True,returning=False,timeout=15,proxy=None):
 '''
   this function takes any giving and gives a security report from: safeweb.norton.com, if it is a: spam domain, contains a malware...
   it takes 3 arguments:
   u: the link to check
   logs: (set by default to: True) showing the process and the report, you can turn it off by setting it to:False
   returning: (set by default to: False) returning the report as a string format if it is set to: True.
   usage:
   >>>import bane
   >>>url='http://www.example.com'
   >>>bane.nortonrate(domain)
'''
 if proxy:
  proxy={'http':'http://'+proxy}
 s=""
 try:
  if logs==True:
   print('[*]Testing link with safeweb.norton.com')
  ur=urllib.quote(u, safe='')
  ul='https://safeweb.norton.com/report/show?url='+ur
  c=requests.get(ul, headers = {'User-Agent': random.choice(ua)},proxies=proxy,timeout=timeout).text 
  soup = BeautifulSoup(c, "html.parser").text
  s=soup.split("Summary")[1].split('=')[0]
  s=s.split("The Norton rating")[0].split('=')[0]
  if logs==True:
   print('[+]Report:\n',s.strip())
 except:
  pass
 if returning==True:
  return s.strip()
def myip(proxy=None,proxy_type=None,timeout=15):
 '''
   this function is for getting your ip using: ipinfo.io
   usage:
   >>>import bane
   >>>bane.myip()
   xxx.xx.xxx.xxx
'''
 proxies={}
 if proxy:
  if proxy_type.lower()=="http":
   proxies = {
     "http": "http://"+proxy,
     }
  if proxy_type.lower()=="socks4":
   proxies = {
     "http": "socks4://"+proxy,
      }
  if proxy_type.lower()=="socks5":
   proxies = {
     "http": "socks5://"+proxy,
      } 
 try:
   return requests.get("http://ipinfo.io/ip",headers = {'User-Agent': random.choice(ua)},  proxies=proxies ,timeout=timeout).text.strip()
 except:
  pass
 return ''
'''
   functions below are using: api.hackertarget.com services to gather up any kind of informations about any given ip or domain
   they take 3 arguments:
   u: ip or domain
   logs: (set by default to: True) showing the process and the report, you can turn it off by setting it to:False
   returning: (set by default to: False) returning the report as a string format if it is set to: True
   general usage:
   >>>import bane
   >>>ip='50.63.33.34'
   >>>bane.dnslookup(ip)
   >>>bane.traceroute(ip)
   etc...
'''
def who_is(u):
 import whois
 u=u.replace('www.','')
 try:
  return whois.whois(u)
 except:
  pass
 return {}
def geoip(u,timeout=15):
 '''
   this function is for getting: geoip informations
 '''
 try:
   r=requests.get('https://geoip-db.com/jsonp/'+u,timeout=timeout).text
   return json.loads(r.split('(')[1].split(')')[0])
 except:
  pass
 return {}
def headers(u,timeout=10,logs=True,returning=False,proxy=None):
 try:
   s=requests.session()
   a=s.get(u,headers = {'User-Agent': random.choice(ua)} ,proxies=proxy,timeout=timeout).headers
 except Exception as ex:
   return None
 if logs==True:
  for x in a:
   print("{} : {}".format(x,a[x]))
 if returning==True:
  return a
def reverse_ip_lookup(u,timeout=10,logs=True,returning=False,proxy=None):
 '''
   this function is for: reverse ip look up
   if you've used it 100 times in 24 hours, your IP will be banned by "api.hackertarget.com" so i highly recommand you to use the "proxy" option by adding a http(s) proxy:

   bane.reverse_ip_lookup('XXX.XXX.XXX.XXX',proxy='IP:PORT')

 '''
 if proxy:
  proxy={'http':'http://'+proxy}
 try:
   r=requests.get("https://api.hackertarget.com/reverseiplookup/?q="+u,headers = {'User-Agent': random.choice(ua)} ,proxies=proxy,timeout=timeout).text
   return r.split('\n')
 except Exception as ex:
   pass
 return []
'''
   end of the information gathering functions using: api.hackertarget.com
'''
def resolve(u,server='8.8.8.8',timeout=1,lifetime=1):
 o=[]
 r = dns.resolver.Resolver()
 r.timeout = 1
 r.lifetime = 1
 r.nameservers = ['8.8.8.8']
 a = r.query(u)
 for x in a:
  o.append(str(x))
 return o
"""
this slass is used to scan a target for open ports

usage:

a=bane.ports_scan("8.8.8.8",ports=[21,22,23,80,443,3306],timeout=5)
print(a.result)

this should give you a dict like this:

{'443': 'Open', '22': 'Closed', '21': 'Closed', '23': 'Closed', '80': 'Closed', '3306': 'Closed'}

"""
class ports_scan:
 def scan (self):
        p=self.por[self.flag2]
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        r = s.connect_ex((self.target, int(p)))
        if r == 0:
         self.result.update({str(p):"Open"})
        else:
         self.result.update({str(p):"Closed"})
        s.close()
 def __init__(self,u,ports=[21,22,23,25,43,53,80,443,2082,3306],timeout=5):
  try:
   thr=[]
   self.result={}
   self.timeout=timeout
   self.por=ports
   self.target=u
   for x in range(len(self.por)):
    self.flag2=x
    thr.append(threading.Thread(target=self.scan).start())
    time.sleep(.001)
   while(len(self.result)!=len(ports)):
    time.sleep(.1)
  except:
      pass
  for x in thr:
    try:
      x.join(1)
    except:
      pass
    del x
def subdomains_finder(u,process_check_interval=5,logs=True,returning=False,requests_timeout=15,https=False):
 https_flag=0
 if (https==True) or('https://' in u):
     https_flag=1
 if "://" in u:
  host=u.split('://')[1].split('/')[0]
 else:
  host=u
 sd=[]
 while True:
  try:
   s=requests.session()
   r=s.post('https://scan.penteston.com/scan_system.php',data={"scan_method":"S201","test_protocol":https_flag,"test_host":host},timeout=requests_timeout).text
   if '"isFinished":"no"' not in r:
    if logs==True:
     print("[+]Scan results:")
    c=r.split('strong><br\/>')[1].replace('"}','')
    for x in (c.split('<br\/>')):
     if x.strip():
      if logs==True:
       print(x)
      sd.append(x)
    if returning==True:
     return sd
    break
   else:
    if logs==True:
     print("[*]Scan in progress...")
  except KeyboardInterrupt:
      break
  except:
    pass
  try:
   time.sleep(process_check_interval)
  except KeyboardInterrupt:
      break
  except:
    pass
 if returning==True:
  return []
