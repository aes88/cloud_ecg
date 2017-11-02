
def hrmcalculate(time,voltage):
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
    return_message = {"time":t, "instantaneous_heart_rate":instant_hr,
                    "tachycardia_annotations":tachycondition,
                    "bradycardia_annotations":bradycondition}
    return jsonify(return_message)

def hrmcalculateave(time, voltage, average_window):
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
    return_message = {"averaging_period": average_window, "time": t,
                      "average_heart_rate": average_hr,
                      "tachycardia_annotations": tachycondition,
                      "bradycardia_annotations": bradycondition}
    return jsonify(return_message)


@app.route("/api/heart_rate/summary", methods=['POST'])
def hrsummary():
    import numpy as np
    global counts
    counts += 1
    try:
        validate(data)
    except ValidationError as inst:
        return send_error(inst), 400 # need to import send error
    try:
        hrmcalculate(time,voltage)
    except ValueError:
        print("No heartbeats detected")
    try:
        generateresp(t,instant_hr,tachycondition,bradycondition)
    except ValidationError
        print("Response not correct ")


@app.route("/api/heart_rate/average", methods=['POST'])
def hraverage():
    import numpy as np
    global countave
    countave += 1
    try:
        validateave(data)
    except ValidationError as inst:
        return send_error(inst), 400
    try:
        hrmcalculateave(time,voltage,average_window)
    except ValueError:
        print("No heartbeats detected")
    try:
        generaterespave(t,average_window, average_hr, tachycondition, bradycondition)
    except ValidationError:
        print("Response not correct ")


