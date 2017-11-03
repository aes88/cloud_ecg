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

#def test_summary():
#    assert flaskecgmod.hrmcalculate() ==
    

#def test_average():



#def genresp():
