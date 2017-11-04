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
        """
        This method determines the range of what is considered as a heartbeat,
        then determines the time values at which a heartbeat occurs.

        :param peak_thresh: Ratio of ranges used to detect peaks. Default is
        0.8 V.

        :param base_thresh: Base threshold value to reset between peaks.
        Default is 0.2 V.

        :return: This method appends the resulting time values associated with
        heart beats onto an array called peak_vector. Additionally, an array called timebeat,
        which is the time between heart beats, is also returned.

        """
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
        """
        This uses imported modules from hrmcalcs and TachyBrady to deliver the instantaneous heart rate,
        tachycardia indications, and bradycardia indications.

        :return: The array instant_hr is the instantaneous heart rate of the data, while
        tachy and brady are the tachycardia and bradycardia indications, respectively.
        """
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
        """
        This method provides an array of average heart rate and bradycardia/tachycardia annotations
        over a specified time interval averaging window.

        :param averaging_window: This parameter is the period over which the average and brady/tachy
        annotations are calculated. It is in seconds.
        :return: The instantaneous heart rate and average over the specified window are returned, along
        with the tachy/bradycardia indications.
        """
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
countsum = 0

def validate(data):
    """
    This function takes the JSON input time and voltage data and verifies that both
    time and voltage data are entered and not empty vectors, not misspelled, numeric,
    in array form, and are equal lengths.
    :param data: This is a JSON input consisting of time data and voltage data.
    :return: The method returns parsed JSONs in t and v, and converts those into numpy
    arrays time and voltage.
    """
    import numpy as np
    t_check_1 = True
    t_check_2 = True
    v_check_1 = True
    v_check_2 = True
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
            raise ValueError("Error: Time not entered/misspelled")
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
            raise ValueError("Error: Voltage not entered/misspelled")
    try:
        time = np.array(t)
    except:
        raise ValueError("Time is not an array")
    for i in time:
        try:
            test = float(i)
        except:
            raise ValueError("Time is not entirely numeric")
    try:
        voltage = np.array(v)
    except:
        raise ValueError("Voltage is not an array")
    for i in voltage:
        try:
            test = float(i)
        except:
            raise ValueError("Voltage is not entirely numeric")
    if len(time) != len(voltage):
        raise ValueError("Time and voltage not equal lengths")
    try:
        test_1 = t[0]
    except:
        raise ValueError("Time and voltage are empty vectors")
    return t, v, time, voltage


def validate_ave(data):
    """
    This function takes the JSON input time and voltage data and verifies that both
    time and voltage data are entered and not empty vectors, not misspelled, numeric,
    in array form, and are equal lengths.  Additionally, it checks for the entering
    and proper spelling of an average period.

    :param data: This is a JSON input consisting of time data and voltage data.

    :return: The method returns parsed JSONs in t and v, and converts those into numpy
    arrays time and voltage. In addition, a user-inputted average_window is outputted
    as well.
    """
    import numpy as np
    t_check_1 = True
    t_check_2 = True
    v_check_1 = True
    v_check_2 = True
    avg_check_1 = True
    avg_check_2 = True
    avg_check_3 = True
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
            raise ValueError("Error: Time not entered/misspelled")
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
            raise ValueError("Error: Voltage not entered/misspelled")
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
            raise ValueError("Error: Average window not entered/misspelled")
    try:
        time = np.array(t)
    except:
        raise ValueError("Time is not an array")
    for i in time:
        try:
            test = float(i)
        except:
            raise ValueError("Time is not entirely numeric")
    try:
        voltage = np.array(v)
    except:
        raise ValueError("Voltage is not an array")
    for i in voltage:
        try:
            test = float(i)
        except:
            raise ValueError("Voltage is not entirely numeric")
    try:
        average_window = float(average_window)
    except:
        raise ValueError("Averaging window is not numeric")
    if len(time) != len(voltage):
        raise ValueError("Time and voltage not equal lengths")
    try:
        test_1 = t[0]
    except:
        raise ValueError("Time and voltage are empty vectors")
    return t, v, time, voltage, average_window


def hrmcalculate(time,voltage):
    """
    This method takes time and voltage data parsed from the validate stage and calculates
    instantaneous heart rates and tachy/bradycardia indications. If there are no heartbeats
    detected, an error is displayed.
    :param time: Taken from the validate method, this array is in seconds and
    provides the time data for calculations.
    :param voltage: Taken from the validate method, this array is in millivolts and
    provides the voltage data for calculations.
    :return: The arrays instant_hr, tachycondition, and bradycondition provide instantaneous
    heart rate data, tachycardia indications, and bradycardia indications, respectively.
    """
    ecgcalcs = HrmVals(time,voltage)
    try:
        ecgcalcs.hrm_data()
    except ValueError:
        print("No heartbeats detected")
    ecgcalcs.hrm_instant_data()
    instant_hr = ecgcalcs.instant_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    return instant_hr, tachycondition, bradycondition


def generateresp(t,instant_hr,tachycondition,bradycondition):
    """
    This method takes time, instantaneous heart rate, tachycardia condition, and
    bradycardia condition inputs and structures them into a JSON output.
    :param t: Time array in seconds
    :param instant_hr: Instantaneous heart rate in beats per minute
    :param tachycondition: Tachycardia indications (displayed as true or false)
    :param bradycondition: Bradycardia indications (displayed as true or false)
    :return: The method returns a JSON output consisting of time, instantaneous heart rate,
    tachycardia condition, and bradycardia condition.
    """
    return_message = {"time":t, "instantaneous_heart_rate":instant_hr,
                    "tachycardia_annotations":tachycondition,
                    "bradycardia_annotations":bradycondition}
    return return_message


def hrmcalculateave(time, voltage, average_window):
    """
    This method calculates the average heart rate over a specified time interval, along with
    the tachy/bradycardia indications.
    :param time: Taken from the validate method, this array is in seconds and
    provides the time data for calculations.
    :param voltage: Taken from the validate method, this array is in millivolts and
    provides the voltage data for calculations.
    :param average_window: User-specified time interval for calculating average, in seconds.
    :return: The average heart rate over the average window time interval, tachycardia indications,
    and bradycardia conditions are returned.
    """
    ecgcalcs = HrmVals(time,voltage)
    try:
        ecgcalcs.hrm_data()
    except ValueError:
        print("No heartbeats detected")
    ecgcalcs.hrm_average_data(average_window)
    average_hr = ecgcalcs.average_hr
    tachycondition = ecgcalcs.tachy
    bradycondition = ecgcalcs.brady
    return average_hr,tachycondition, bradycondition


def generaterespave(t,average_window,average_hr,tachycondition, bradycondition):
    """
    This method takes time, average window, average heart rate, tachycardia condition, and
    bradycardia condition inputs and structures them into a JSON output.
    :param t: Time array in seconds
    :param average_window: User-specified interval for average calculations, in seconds.
    :param average_hr: Average heart rate data in beats per minute.
    :param tachycondition: Tachycardia indications (displayed as true or false)
    :param bradycondition: Bradycardia indications (displayed as true or false)
    :return: The method returns a JSON output consisting of averaging period,
    time, average heart rate, tachycardia condition, and bradycardia condition.
    """
    return_message = {"averaging_period": average_window, "time": t,
                      "average_heart_rate": average_hr,
                      "tachycardia_annotations": tachycondition,
                      "bradycardia_annotations": bradycondition}
    return return_message


@app.route("/api/heart_rate/summary", methods=['POST'])
def hrsummary():
    """
    This method creates a web service that takes a JSON input of time and voltage values and
    delivers a JSON output of time, instantaneous heart rate, tachycardia annotations, and
    bradycardia annotations to a specified RESTful API route (endpoint: /api/heart_rate/summary)
    using the Flask application.
    :return: A JSON output consisting of time, instantaneous heart rate, tachycardia, and bradycardia
    data.
    """
    import numpy as np
    data = request.get_json()
    global countsum
    countsum += 1
    try:
        t, v, time, voltage = validate(data)
    except Exception as inst:
        return_string = str(inst) + ", 400"
        return return_string
    try:
        instant_hr, tachycondition, bradycondition = hrmcalculate(time,voltage)
    except ValueError:
        print("No heartbeats detected")
    try:
        arr = generateresp(t,instant_hr,tachycondition,bradycondition)
        return jsonify(arr)
        return arr
    except ValueError:
        print("Response not correct")

@app.route("/api/heart_rate/average", methods=['POST'])
def hraverage():
    """
    This method creates a web service that takes a JSON input of averaging period, time and voltage values
    and delivers a JSON output of averaging period, time, average heart rate, tachycardia annotations,
    and bradycardia annotations to a specified RESTful API route (endpoint: /api/heart_rate/average) using
    the Flask application.
    :return: A JSON output consisting of time, instantaneous heart rate, tachycardia, and bradycardia
    data.
    """
    import numpy as np
    global countave
    countave += 1
    data = request.get_json()
    try:
        t, v, time, voltage, average_window = validate_ave(data)
    except Exception as inst:
        return_string = str(inst) + ", 400"
        return return_string
    try:
        average_hr, tachycondition, bradycondition = hrmcalculateave(time,voltage,average_window)
    except ValueError:
        print("No heartbeats detected")
    try:
        return_message = generaterespave(t,average_window, average_hr, tachycondition, bradycondition)
        return jsonify(return_message)
    except ValueError:
        print("Response not correct")

@app.route("/api/requests",methods = ['GET'])
def requests ():
    """
    This method creates a GET request that provides the number of total requests this web service has
    served since its most recent reboot at the endpoint /api/requests.
    :return: A number of total requests for heart rate summary and heart rate average in a text string.
    """
    totalcount = countsum + countave
    return_str = "The total number of requests is %d" % (totalcount)
    return jsonify(return_str)

