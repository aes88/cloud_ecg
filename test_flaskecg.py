import flaskecgmod
import unittest

class Validate(unittest.TestCase):
    def test_misspelling(self):
        self.assertRaises(ValueError, flaskecgmod.validate,
                          {"times": [1, 2, 3], "voltage": [1, 2, 3]})
        self.assertRaises(ValueError, flaskecgmod.validate,
                          {"time": [1, 2, 3], "voltageasdf": [1, 2, 3]})

    def test_different_lengths(self):
        self.assertRaises(ValueError, flaskecgmod.validate,
                          {"time": [1, 2, 3], "voltage": [1, 2, 3, 4]})

    def test_empty_inputs(self):
        self.assertRaises(ValueError, flaskecgmod.validate,
                          {"time": [], "voltage": []})

    def test_nonnumeric(self):
        self.assertRaises(ValueError, flaskecgmod.validate,
                          {"time":[1,2,3],"voltage":[1,2,"three"]})


class Validate_ave(unittest.TestCase):
    def test_misspelling(self):
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"times": [1, 2, 3], "voltage": [1, 2, 3],
                           "average_window": 20})
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [1, 2, 3], "voltageasdf": [1, 2, 3],
                           "average_window": 20})
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [1, 2, 3], "voltage": [1, 2, 3],
                           "average_window!!": 20})

    def test_different_lengths(self):
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [1, 2, 3], "voltage": [1, 2, 3, 4],
                           "average_window": 20})

    def test_empty_inputs(self):
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [], "voltage": [], "average_window": 20})

    def test_nonnumeric(self):
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time":[1,2,"three"],"voltage":[1,2,3],
                           "average_window": 20})
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [1, 2, 3], "voltage": [1, 2, "three"],
                           "average_window": 20})
        self.assertRaises(ValueError, flaskecgmod.validate_ave,
                          {"time": [1, 2, 3], "voltageasdf": [1, 2, 3],
                           "average_window": "twenty-four"})

def test_summary():
    assert flaskecgmod.hrmcalculate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                    [6, 4, 8, 4, 2, 45, 2, 4, 3, 48]) == \
           ([0,0,0,0,0,0,0,0,0,15],[False,False,False,False,False,False,False,False,False,False],
            [False, False, True, True, True, True, True, True, True, True])

def test_average():
    assert flaskecgmod.hrmcalculateave([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                    [6, 4, 8, 4, 2, 45, 2, 4, 3, 48], 2) == \
           ([0,0,0,0,0,0,0,0,0,15],[False, False, False, False, False, False, False, False, False, False],
            [False, False, True, True, True, True, True, True, True, True])

def test_respave():
    arr = flaskecgmod.generaterespave([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],[2],[0,0,0,0,0,0,0,0,0,15],
                                    [False,False,False,False,False,False,False,False,False,False],
                                    [False, False, True, True, True, True, True, True, True, True])
    assert arr["average_heart_rate"] == [0,0,0,0,0,0,0,0,0,15]
    assert arr['averaging_period'] == [2]
    assert arr['bradycardia_annotations'] == [False, False, True, True, True, True, True, True, True, True]
    assert arr['tachycardia_annotations'] == [False,False,False,False,False,False,False,False,False,False]


def test_respsummary():
    arr = flaskecgmod.generateresp([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0, 15],
                                      [False, False, False, False, False, False, False, False, False, False],
                                      [False, False, True, True, True, True, True, True, True, True])
    assert arr["instantaneous_heart_rate"] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 15]
    assert arr['bradycardia_annotations'] == [False, False, True, True, True, True, True, True, True, True]
    assert arr['tachycardia_annotations'] == [False, False, False, False, False, False, False, False, False, False]
