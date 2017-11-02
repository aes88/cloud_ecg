


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



