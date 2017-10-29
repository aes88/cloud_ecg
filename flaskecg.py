from flask import Flask,request,jsonify
app = Flask(__name__)

class Values:

    def __init__(self,time,voltage):
        self.time = time
        self.voltage = voltage
        import statistics
        import numpy as np
        from hrmcalcs2oo import hrmcalcs
        from hrmtb import TachyBrady
        from hrm_oo import extract_vals
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


@app.route("/api/heart_rate/summary", methods = ['POST'])
def hrsummary ():
    data = request.get_json()
    t = data['t']
    v = data['v']
    time = np.array(t)
    voltage = np.array(v)
    a = Values(time,voltage)
    a.instant_hr



@app.route("api/heart_rate/average", methods = ['POST'])
def hraverage ():

@app.route("api/requests",methods = ['GET'])
def requests ():
