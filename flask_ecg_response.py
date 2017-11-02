def generateresp(t,instant_hr,tachycondition,bradycondition):
    return_message = {"time":t, "instantaneous_heart_rate":instant_hr,
                    "tachycardia_annotations":tachycondition,
                    "bradycardia_annotations":bradycondition}
    return jsonify(return_message)