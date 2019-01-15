from flask import Flask, render_template, request
from datetime import datetime
from models import *
from scan import *

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost:5432/dragonmint"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db.init_app(app)

def update():
    #db.create_all()
    my_queue = queue.Queue()
    threads = []
    ipset = []
    existip = []
    result = []
    #network = input('Enter which network you want to scan: ')
    network = '172.16.0.0/23'
    for addr in IPv4Network(network):
        ip = str(addr)
        ipset.append("".join(ip))
    
    for i in ipset:
        thread = myThread(i, my_queue)
        thread.start()
        threads.append(thread)

    for i in threads:
        i.join()
     
    while not my_queue.empty():
        a = my_queue.get()
        result.append(a)
    
    """update overview data."""
    for i in range(len(result)):
        try: 
            filter_ip = Overview.query.filter_by(ip = result[i]['IP']).first()
            existip.append(result[i]['IP'])
            
            """update overview list if there are exist."""
            if filter_ip.ip is not None:
                filter_ip.update_time = datetime.now()
                filter_ip.macaddress = result[i]['MAC']
                filter_ip.worker_num = result[i]['Workers']
        except:
            """create overview list if there are not in the list."""
            a = Overview(ip = result[i]['IP'], macaddress = result[i]['MAC'], worker_num = result[i]['Workers'], update_time = datetime.now())
            db.session.add(a)
        finally:
            db.session.commit()
            
    """remove non-existent ip."""       
    query = Overview.query.all()
    queryip = []
    for i in range(len(query)):
        queryip.append(query[i].ip)
    nonexistip = set(queryip) ^ set(existip)
    for j in nonexistip:
        iphost = Overview.query.filter_by(ip = j).first()
        workerid = Worker.query.filter_by(host_id = iphost.id).first()
        db.session.delete(workerid)
        db.session.commit()
        db.session.delete(iphost)
        db.session.commit()
    
    """update worker information."""
    for i in range(len(result)):
        try: 
            filter_ip = Overview.query.filter_by(ip = result[i]['IP']).first()
            filter_worker = Worker.query.filter_by(host_id = filter_ip.id).first()
            #print(filter_ip)
            #print(filter_worker)
            """create workers information if there are not exist."""
            if filter_worker is None:
                if filter_ip.worker_num == '3':
                    filter_ip.add_worker(dt1_status = result[i]['Status']['D'+ str(1)], dt1_temperture = result[i]['Temperture']['D'+ str(1)], dt2_status = result[i]['Status']['D'+ str(2)], dt2_temperture = result[i]['Temperture']['D'+ str(2)], dt3_status = result[i]['Status']['D'+ str(3)], dt3_temperture = result[i]['Temperture']['D'+ str(3)])
                elif filter_ip.worker_num == '2':
                    filter_ip.add_worker(dt1_status = result[i]['Status']['D'+ str(1)], dt1_temperture = result[i]['Temperture']['D'+ str(1)], dt2_status = result[i]['Status']['D'+ str(2)], dt2_temperture = result[i]['Temperture']['D'+ str(2)], dt3_status = 'Missing', dt3_temperture = 0)
                elif filter_ip.worker_num == '1':
                    filter_ip.add_worker(dt1_status = result[i]['Status']['D'+ str(1)], dt1_temperture = result[i]['Temperture']['D'+ str(1)], dt2_status = 'Missing', dt2_temperture = 0, dt3_status = 'Missing', dt3_temperture = 0)
            else:
                """update workers information if there are exist."""
                if filter_ip.worker_num == '3':
                    filter_worker.dt1_status = result[i]['Status']['D'+ str(1)]
                    filter_worker.dt1_temperture = result[i]['Temperture']['D'+ str(1)]
                    filter_worker.dt2_status = result[i]['Status']['D'+ str(2)]
                    filter_worker.dt2_temperture = result[i]['Temperture']['D'+ str(2)]
                    filter_worker.dt3_status = result[i]['Status']['D'+ str(3)]
                    filter_worker.dt3_temperture = result[i]['Temperture']['D'+ str(3)]
                elif filter_ip.worker_num == '2':
                    filter_worker.dt1_status = result[i]['Status']['D'+ str(1)]
                    filter_worker.dt1_temperture = result[i]['Temperture']['D'+ str(1)]
                    filter_worker.dt2_status = result[i]['Status']['D'+ str(2)]
                    filter_worker.dt2_temperture = result[i]['Temperture']['D'+ str(2)]
                    filter_worker.dt3_status = 'Missing'
                    filter_worker.dt3_temperture = 0
                elif filter_ip.worker_num == '1':
                    filter_worker.dt1_status = result[i]['Status']['D'+ str(1)]
                    filter_worker.dt1_temperture = result[i]['Temperture']['D'+ str(1)]
                    filter_worker.dt2_status = 'Missing'
                    filter_worker.dt2_temperture = 0
                    filter_worker.dt3_status = 'Missing'
                    filter_worker.dt3_temperture = 0
        except:
            pass
        finally:
            db.session.commit()
#if __name__ == '__main__':
#    with app.app_context():
#        update()
