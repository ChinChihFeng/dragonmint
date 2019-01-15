from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()

class Overview(db.Model):
    __tablename__ = "overview"
    id = db.Column(db.Integer, primary_key=True)
    #ip = db.Column(db.String, unique=True, nullable=False)
    ip = db.Column(postgresql.INET, unique=True, nullable=False)
    macaddress = db.Column(db.String, unique=True, nullable=False)
    worker_num = db.Column(db.String, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    workers = db.relationship("Worker", backref='overview', lazy=True)
    
    def add_worker(self, dt1_status, dt1_temperture, dt2_status, dt2_temperture, dt3_status, dt3_temperture):
        p = Worker(host_id = self.id, dt1_status = dt1_status, dt1_temperture = dt1_temperture, dt2_status = dt2_status, dt2_temperture = dt2_temperture, dt3_status = dt3_status, dt3_temperture = dt3_temperture)
        db.session.add(p)
        db.session.commit()
    
    def __repr__(self):
        return "<Overview(id='%s', ip='%s', macaddress='%s', worker_num='%s', update_time='%s')>" % (self.id, self.ip, self.macaddress, self.worker_num, self.update_time)
    
    #def to_json(self):
    #    return {
    #        'id': self.id,
    #        'ip': self.ip,
    #        'macaddress': self.macaddress,
    #        'worker_num': self.worker_num,
    #        'update_time': self.update_time
    #    }
        
class Worker(db.Model):
    __tablename__ = "worker"
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer,db.ForeignKey("overview.id"), nullable=False)
    dt1_status = db.Column(db.String)
    dt1_temperture = db.Column(db.Integer)
    dt2_status = db.Column(db.String)
    dt2_temperture = db.Column(db.Integer)
    dt3_status = db.Column(db.String)
    dt3_temperture = db.Column(db.Integer)
    hosts = db.relationship("Overview", backref='worker', lazy=True)
    
    def __repr__(self):
        return "<Worker(id='%s', host_id='%s', dt1_status='%s', dt1_temperture='%s', dt2_status='%s', dt2_temperture='%s', dt3_status='%s', dt3_temperture='%s')>" % (self.id, self.host_id, self.dt1_status, self.dt1_temperture, self.dt2_status, self.dt2_temperture, self.dt3_status, self.dt3_temperture)
    
    #def to_json(self):
    #    return {
    #        'id': self.id,
    #        'host_id': self.host_id,
    #        'dt1_status': self.dt1_status,
    #        'd1_temperture': self.dt1_temperture,
    #        'dt2_status': self.dt2_status,
    #        'dt2_temperture': self.dt2_temperture,
    #        'dt3_status': self.dt1_status,
    #        'dt3_temperture': self.dt3_temperture
    #    }