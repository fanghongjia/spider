# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64 
import random
import urllib2
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        proapi="http://dev.kuaidaili.com/api/getproxy/?orderid=985648137556545&num=20&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&quality=1&sep=4"
        pro_req = urllib2.Request(proapi) 
        pro_response = urllib2.urlopen(pro_req) 
        iplines = pro_response.read()
        proxy_ip_list = iplines.split('|')
        for i in range(len(proxy_ip_list)):
        	proxy_ip_list[i]="http://"+proxy_ip_list[i]

        proxy_ip = random.choice(proxy_ip_list)
        # Set the location of the proxy
        request.meta['proxy'] = proxy_ip
  
        # Use the following lines if your proxy requires authentication
        #proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #encoded_user_pass = base64.encodestring(proxy_user_pass)
        #request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass