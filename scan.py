from requests.auth import HTTPBasicAuth
from ipaddress import IPv4Network
import os, requests, json, threading, queue

class myThread (threading.Thread):
    def __init__(self, ip, queue):
        threading.Thread.__init__(self)
        self.ip = ip
        self.queue = queue 
    def run(self):
        auth = HTTPBasicAuth('admin','dragonadmin')
        overviewurl = 'http://' + self.ip + '/api/overview'
        summaryurl = 'http://' + self.ip + '/api/summary'
        try:
            r1 = requests.post(overviewurl, timeout=1, auth = auth).json()
            r2 = requests.post(summaryurl, timeout=1, auth = auth).json()
            
            if r1['success'] is True:
                ipaddr = r1['network']['ipaddress']
                macaddress = r1['version']['ethaddr']
                worker = 0
                temperture = {}
                status = {}
                for i in range(len(r2['DEVS'])):
                    status.update({ 'D' + str(i + 1): r2['DEVS'][i]['Status'] })
                    if r2['DEVS'][i]['Status'] == 'Alive':
                        worker += 1
                        temperture.update({ 'D' + str(i + 1): r2['DEVS'][i]['Temperature'] })
                info = {'IP': ipaddr, 'MAC': macaddress, 'Workers': worker, 'Status': status, 'Temperture': temperture}
                self.queue.put(info)
        except:
            pass
        #else:
        #    if r1['success'] is True:
        #        ipaddr = r1['network']['ipaddress']
        #        macaddress = r1['version']['ethaddr']
        #        worker = 0
        #        temperture = {}
        #        status = {}
        #        for i in range(len(r2['DEVS'])):
        #            status.update({ 'D' + str(i + 1): r2['DEVS'][i]['Status'] })
        #            if r2['DEVS'][i]['Status'] == 'Alive':
        #                worker += 1
        #                temperture.update({ 'D' + str(i + 1): r2['DEVS'][i]['Temperature'] })
        #        info = {'IP': ipaddr, 'MAC': macaddress, 'Workers': worker, 'Status': status, 'Temperture': temperture}
        #        self.queue.put(info)
        
#if __name__ == '__main__':
    
    #my_queue = queue.Queue()
    #threads = []
    #result = []
    #network = input('Enter which network you want to scan: ')
    #ipset = []
    
    #for addr in IPv4Network(network):
    #for addr in IPv4Network("192.1.3.0/24"):
    #    ip = str(addr)
    #    ipset.append("".join(ip))
    
    #for i in ipset:
    #    thread = myThread(i, my_queue)
    #    thread.start()
    #    threads.append(thread)

    #for i in threads:
    #    i.join()
    
    #while not my_queue.empty():
    #    a = my_queue.get()
    #    result.append(a)
    #print(result)