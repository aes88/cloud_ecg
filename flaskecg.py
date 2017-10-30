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
        from bme590hrm.hrmcalcs2oo import hrmcalcs
        from bme590hrm.hrmtb import TachyBrady
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
    t_check_1 = True
    t_check_2 = True
    v_check_1 = True
    v_check_2 = True
    data = request.get_json()
    try:
        t = data['time']
    except:
        t_check_1 = False
    if not t_check_1:
        try:
            t = data['Time']
        except:
            t_check_2 = False
    if not t_check_2:
        try:
            t = data['TIME']
        except:
            return "Error: Time not entered/misspelled"
    try:
        v = data['voltage']
    except:
        v_check_1 = False
    if not v_check_1:
        try:
            v = data['Voltage']
        except:
            v_check_2 = False
    if not v_check_2:
        try:
            v = data['VOLTAGE']
        except:
            return "Error: Voltage not entered/misspelled"
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
    t_check_1 = True
    t_check_2 = True
    v_check_1 = True
    v_check_2 = True
    avg_check_1 = True
    avg_check_2 = True
    avg_check_3 = True
    data = request.get_json()
    try:
        t = data['time']
    except:
        t_check_1 = False
    if not t_check_1:
        try:
            t = data['Time']
        except:
            t_check_2 = False
    if not t_check_2:
        try:
            t = data['TIME']
        except:
            return "Error: Time not entered/misspelled"
    try:
        v = data['voltage']
    except:
        v_check_1 = False
    if not v_check_1:
        try:
            v = data['Voltage']
        except:
            v_check_2 = False
    if not v_check_2:
        try:
            v = data['VOLTAGE']
        except:
            return "Error: Voltage not entered/misspelled"
    try:
        average_window = data['averaging_period']
    except:
        avg_check_1 = False
    if not avg_check_1:
        try:
            average_window = data['Averaging_period']
        except:
            avg_check_2 = False
    if not avg_check_2:
        try:
            average_window = data['Averaging_period']
        except:
            avg_check_3 = False
    if not avg_check_3:
        try:
            average_window = data['AVERAGING_PERIOD']
        except:
            return "Error: Average window not entered/misspelled"
    time = np.array(t)
    voltage = np.array(v)
    ecgcalcs = HrmVals(time, voltage)
    ecgcalcs.hrm_data()
    ecgcalcs.hrm_average_data(average_window)
    average_hr = ecgcalcs.average_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    countave[0] += 1
    return_message = {"averaging_period":average_window, "time": t,
                      "tachycardia_annotations": tachycondition,
                      "bradycardia_annotations": bradycondition}
    return jsonify(return_message)

@app.route("/api/requests",methods = ['GET'])
def requests ():
   totalhits = countsum[0] + countave[0]
   return totalhits