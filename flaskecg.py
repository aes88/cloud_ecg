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

countave = 0
counts = 0

@app.route("/api/heart_rate/summary", methods=['POST'])
def hrsummary():
    import numpy as np
    global counts
    counts += 1
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
    try:
        time = np.array(t)
    except:
        return "Time is not an array of numeric values"
    try:
        voltage = np.array(v)
    except:
        return "Voltage is not an array of numeric values"
    if len(time) != len(voltage):
        return "Time and voltage not equal lengths"
    try:
        test_1 = t[0]
    except:
        return "Time and voltage are empty vectors"
    # errors to test: 1. non-numeric t or v
    # 2. unequal length
    # 3. empty vectors
    # 4. no heartbeats detected
    ecgcalcs = HrmVals(time, voltage)
    try:
        ecgcalcs.hrm_data()
    except:
        return "Error: no heartbeats detected"
    ecgcalcs.hrm_instant_data()
    instant_hr = ecgcalcs.instant_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    return_message = {"time":t, "instantaneous_heart_rate":instant_hr,
                      "tachycardia_annotations":tachycondition,
                      "bradycardia_annotations":bradycondition}
    return jsonify(return_message)


@app.route("/api/heart_rate/average", methods=['POST'])
def hrmaverage():
    import numpy as np
    global countave
    countave += 1
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
    try:
        time = np.array(t)
    except:
        return "Time is not an array"
    for i in time:
        try:
            test = float(i)
        except:
            return "Time is not entirely numeric"
    try:
        voltage = np.array(v)
    except:
        return "Voltage is not an array"
    for i in voltage:
        try:
            test = float(i)
        except:
            return "Time is not entirely numeric"

    try:
        average_window = float(average_window)
    except:
        return "Averaging window is not numeric"
    if len(time) != len(voltage):
        return "Time and voltage not equal lengths"
    try:
        test_1 = t[0]
    except:
        return "Time and voltage are empty vectors"
    ecgcalcs = HrmVals(time, voltage)
    try:
        ecgcalcs.hrm_data()
    except:
        return "Error: no heartbeats detected"
    ecgcalcs.hrm_average_data(average_window)
    average_hr = ecgcalcs.average_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    return_message = {"averaging_period":average_window, "time": t,
                      "average_heart_rate":average_hr,
                      "tachycardia_annotations": tachycondition,
                      "bradycardia_annotations": bradycondition}
    return jsonify(return_message)

@app.route("/api/requests",methods = ['GET'])
def requests ():
    totalhits = counts + countave
    a = jsonify(totalhits)
    return "The total number of hits at this API is %s." % a.get_data(as_text = True)