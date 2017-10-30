from flask import Flask, request, jsonify
app = Flask(__name__)


class HrmVals:

    def __init__(self, time, voltage):
        self.time = time
        self.voltage = voltage
        self.instant_hr = []
        self.average_hr = None
        self.brady_limit = 60
        self.tachy_limit = 100
        self.tachy = []
        self.brady = []
        self.peak_vector = []
        self.timebeat = []

    def hrm_data(self, peak_thresh=0.8, base_thresh=0.2):
        import statistics
        import numpy as np
        from bme590hrm.hrmcalcs2oo import hrmcalcs
        from bme590hrm.hrmtb import TachyBrady
        # from hrmcalcs2oo import hrmcalcs
        # from hrmtb import TachyBrady
        toggle_peak_status = False
        peak_times = []
        self.peak_vector = []
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
            self.peak_vector = np.array(peak_times)
        self.timebeat = np.diff(self.peak_vector)

    def hrm_instant_data(self):
        import statistics
        import numpy as np
        from bme590hrm.hrmcalcs2oo import hrmcalcs
        from bme590hrm.hrmtb import TachyBrady
        # from hrmcalcs2oo import hrmcalcs
        # from hrmtb import TachyBrady
        calc_ecg = hrmcalcs(self.time, self.timebeat, self.peak_vector, 20)  # creating an object
        # calc_ecg.hrm_instant() # runs the hrm_instant module
        self.instant_hr = calc_ecg.instant_hr
        tb_ecg = TachyBrady(self.instant_hr, self.brady_limit, self.tachy_limit)
        tb_ecg.tb()
        self.tachy = tb_ecg.tachy
        self.brady = tb_ecg.brady

    def hrm_average_data(self, averaging_window):
        import statistics
        import numpy as np
        from hrmcalcs2oo import hrmcalcs
        from hrmtb import TachyBrady
        # calc_ecg.hrm_average()
        calc_ecg = hrmcalcs(self.time, self.timebeat, self.peak_vector, averaging_window)
        self.instant_hr = calc_ecg.instant_hr
        self.average_hr = calc_ecg.average_hr
        tb_ecg = TachyBrady(self.instant_hr, self.brady_limit, self.tachy_limit)
        tb_ecg.tb()
        self.tachy = tb_ecg.tachy
        self.brady = tb_ecg.brady

countsum = [0]
countave = [0]

@app.route("/api/heart_rate/summary", methods=['POST'])
def hrsummary():
    import numpy as np
    data = request.get_json()
    t = data['time']
    v = data['voltage']
    time = np.array(t)
    voltage = np.array(v)
    ecgcalcs = HrmVals(time, voltage)
    ecgcalcs.hrm_data()
    ecgcalcs.hrm_instant_data()
    instant_hr = ecgcalcs.instant_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    countsum[0] += 1
    #for row in list(zip(time, instant_hr, tachycondition, bradycondition)):
    #    return("{},{},{},{}\n".format(np.round(row[0], 2),
    #                                  np.round(row[1], 2),
    #                                  np.round(row[2], 2),
    #                                  np.round(row[3], 2)))
    #count = 0
    #return_string = "["
    #for i in peak_vector:
    #    if count == 0:
    #        return_string += "{:}".format(peak_vector[count])
    #    else:
    #        return_string += ", {:}".format(peak_vector[count])
    #    count += 1
    #return_string += "]"
    #return "{:}".format(return_string)
    return_message = {"time":t, "instantaneous_heart_rate":instant_hr,
                      "tachycardia_annotations":tachycondition,
                      "bradycardia_annotations":bradycondition}
    return jsonify(return_message)


@app.route("/api/heart_rate/average", methods=['POST'])
def hrmaverage():
    import numpy as np
    data = request.get_json()
    t = data['time']
    v = data['voltage']
    average_window = data['averaging_period']
    time = np.array(t)
    voltage = np.array(v)
    ecgcalcs = HrmVals(time, voltage)
    ecgcalcs.hrm_data()
    ecgcalcs.hrm_average_data(average_window)
    average_hr = ecgcalcs.instant_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    countave[0] += 1
    for row in list(zip(time, average_hr, tachycondition, bradycondition)):
        return ("{},{},{},{}\n".format(np.round(row[0], 2),
                                       np.round(row[1], 2),
                                       np.round(row[2], 2),
                                       np.round(row[3], 2)))

@app.route("/api/requests",methods = ['GET'])
def requests ():
   totalhits = countsum[0] + countave[0]
   return totalhits