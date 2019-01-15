import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from models import *
from scan import *
from update import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
#from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost:5432/dragonmint"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def print_date_time():
    with app.app_context():
        update()

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetchminer", methods=["POST"])
def fetchminer():
    
    network = request.form.get("network")
    my_queue = queue.Queue()
    threads = []
    result = []
    #network = input('Enter which network you want to scan: ')
    ipset = []
    #print(network)
    #return "123"
    for addr in IPv4Network(network):
    #for addr in IPv4Network("192.1.3.0/24"):
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
        
    return jsonify(result)


@app.route("/dashboard")
def dashboard():
    """Trying to get all info I need from database."""
    """Make a query that it can be a joined query."""
    a = Overview.query.order_by(Overview.ip).all()
    info = []
    temperture = {}
    for i in a:
        #print(i.id)
        cond = 'Great' if i.worker_num == '3' else 'Failed'
        
        combine = {
            'ip': i.ip,
            'macaddress': i.macaddress,
            'worker_num': i.worker_num,
            'update_time': i.update_time.strftime("%X"),
            'cond': cond,
            'status': {
                'dt1_status': i.workers[0].dt1_status,
                'dt2_status': i.workers[0].dt2_status,
                'dt3_status': i.workers[0].dt3_status
            },
            'temperture': {
                'dt1_temperture': i.workers[0].dt1_temperture,
                'dt2_temperture': i.workers[0].dt2_temperture,
                'dt3_temperture': i.workers[0].dt3_temperture
            }
        }
        info.append(combine)

    return jsonify(info)