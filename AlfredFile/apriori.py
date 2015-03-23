import httplib
import json
import os
import sys
from feedback import *
import datetime
'''
http://www.kuaidi100.com/autonumber/auto?num=880046513239379439

http://www.kuaidi100.com/query?type=yuantong&postid=880046513239379439&id=1&valicode=&temp=0.40347477863542736
'''
result =  Feedback();
if (len(sys.argv)>1):
    query = "880046513239379439"
    query = sys.argv[1];
    
    url = "http://www.kuaidi100.com/autonumber/auto?num="+query

    conn = httplib.HTTPConnection("www.kuaidi100.com")
    conn.request(method="GET",url=url) 

    response = conn.getresponse()
    res= response.read()
    company = json.loads(res)
    #print res
    count = 0
    for s in company:
        url = "http://www.kuaidi100.com/query?type="+s['comCode']+"&postid="+query
        newcon = httplib.HTTPConnection("www.kuaidi100.com")
        newcon.request(method="GET",url = url)
        gets = newcon.getresponse().read()
        ps = json.loads(gets)
        items = []
        if (ps['status'])=="200":
            for i in range(len(ps['data'])-1,-1,-1):
                t = ps['data'][i]
                items.append(t)
                #print t['ftime']
                #print datetime.datetime.strptime(t['ftime'],"%Y-%m-%d %H:%M:%S")
                count = count + 1
        items.sort(key=lambda x: x['ftime'],reverse = True)
        for t in items:
            t.setdefault('location',"");
            t.setdefault('context',"");
            t.setdefault('ftime',"");
            item = t['location']+" "+ t['context']
            result.add_item(item,subtitle="  "+t['ftime'])
        if (count>0):
            break;
                    
    

    if count==0:
        result.add_item("Can't find relate information")
    print result