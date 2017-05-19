
import commands
import json
import os
import re
print '''===========start============='''
getstr = commands.getstatusoutput('sudo docker ps |grep my-nginx')
if getstr[1] == '' :
    print 'error  the nginx is not running;'
    exit()
confdir = '/root/nginxconf/'
print 'you will create conf at '+confdir


container_name = raw_input("give me the container  name: ")

www_name =  raw_input("give me the web name: ")
port = raw_input("listen the port: [80] ")
if port != '':
    port = ':'+port
filename = confdir+www_name+'.conf'
if os.path.exists(filename): 
    print 'sorry the file is exists'
    exit()

getstr = commands.getstatusoutput('sudo docker inspect '+container_name)

getstr = json.loads(getstr[1])
try:
    ip =  getstr[0]['NetworkSettings']['IPAddress']
except Exception, e:
    print e
    exit()

try:
    fp = open(filename,'w')
except Exception, e:
    print e
else:
    fp.write('upstream '+www_name+'_server{\n')
    fp.write('server '+ip+port+';\n')
    fp.write('}\n')
    fp.write('server {\n')
    fp.write('listen       80;\n')
    fp.write('server_name  '+www_name+'.aitboy.cn;\n')
    fp.write('location / {\n')
    fp.write('proxy_redirect off;\n')
    fp.write('proxy_set_header Host $host;\n')
    fp.write('proxy_set_header X-Forwarded-Host $host;\n')
    fp.write('proxy_set_header X-Forwarded-Server $host;\n')
    fp.write('proxy_set_header X-Real-IP $remote_addr;\n')
    fp.write('proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n')
    fp.write('proxy_buffering on;\n')
    fp.write('proxy_pass http://'+www_name+'_server;\n')
    fp.write('}')
    fp.write('error_page   500 502 503 504  /50x.html;\n')
    fp.write('location = /50x.html {\n')
    fp.write('root   html;\n')
    fp.write('}\n')
    fp.write('}\n')
    fp.close()

nginx_test =  commands.getstatusoutput('sudo docker exec my-nginx nginx -t')
m = re.search(r'(failed)', nginx_test[1])
if m:
    print nginx_test
    print 'plese see error and vim the file , then restart the nginx'
    exit()
else:
    print commands.getstatusoutput('sudo docker exec my-nginx nginx -s reload')

print '''===========end============='''