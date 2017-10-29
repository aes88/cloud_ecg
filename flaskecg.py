from flask import Flask,request,jsonify
app = Flask(__name__)

class HrmVals:

    def __init__(self,time,voltage,start_min,end_min):
        self.time = time
        self.voltage = voltage
        self.start_min = start_min
        self.end_min = end_min
        self.instant_hr = []
        self.average_hr = None
        self.brady_limit = 60
        self.tachy_limit = 100
        self.tachy = []
        self.brady = []

    def hrm_data(self, peak_thresh = 0.9, base_thresh = 0.1):
        import statistics
        import numpy as np
        from hrmcalcs2oo import hrmcalcs
        from hrmtb import TachyBrady
        toggle_peak_status = False
        peak_times = []
        peak_vector = []
        baseline = statistics.median(self.voltage)
        pos_range = max(self.voltage) - baseline
        count = 0
        for i in self.voltage:
            if not toggle_peak_status:
                if i > (baseline + peak_thresh * pos_range):
                    peak_times.append(round(self.time[count], 2))
                    toggle_peak_status = True
                    count += 1
            if toggle_peak_status:
                if i < (baseline + base_thresh * pos_range):
                    toggle_peak_status = False
                    count += 1
            else:
                count += 1
            peak_vector = np.array(peak_times)
        timebeat = np.diff(peak_vector)

        calc_ecg = hrmcalcs(timebeat,peak_vector,self.start_min,self.end_min) # creating an object
        calc_ecg.hrm_instant() # runs the hrm_instant module
        self.instant_hr = calc_ecg.instant_hr
        calc_ecg.hrm_average()
        self.average_hr = calc_ecg.average_hr
        tb_ecg = TachyBrady(self.instant_hr,self.brady_limit,self.tachy_limit)
        tb_ecg.tb()
        self.tachy = tb_ecg.tachy
        self.brady = tb_ecg.brady

@app.route("/api/heart_rate/summary", methods = ['POST'])
def hrsummary ():
    data = request.get_json()
    t = data['t']
    v = data['v']
    start_min = data['start min']
    end_min = data['end min']
    time = np.array(t)
    voltage = np.array(v)
    ecgcalcs = HrmVals(time,voltage,start_min,end_min)
    ecgcalcs.hrm_data()
    instantHR = hrm_data.instant_hr
    tachycondition = hrm_data.tachy
    bradycondition = hrm_data.brady
    for row in list(zip(time,instantHR,tachycondition,bradycondition)):
        return("{},{},{},{}\n".format(np.round(row[0], 2),
                                       np.round(row[1], 2),
                                       np.round(row[2], 2),
                                       np.round(row[3], 2)))

@app.route("api/heart_rate/average", methods = ['POST'])
def hraverage ():

@app.route("api/requests",methods = ['GET'])
def requests ():
