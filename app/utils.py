"""
utils.py

@Author:    Maro Okegbero
@Date:      July 26, 2020
@Time:      7:57 AM

This module contains a number of utility functions useful throughout our application.
No references are made to specific models or views. As a result, they are useful with or
without the application context.
"""

from datetime import datetime
import random
import string


def generate_reference_number():
    """
    generates a unique reference number
    """

    year = datetime.now().year.__str__()
    month = datetime.now().month.__str__()
    x = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(9))
    return "-".join(["CB"] + [year] + [month] + ["".join([x])])


def populate_obj(obj, data):
    """
    Populates an object with the data passed to it

    param obj: Object to be populated
    param data: The data to populate it with (dict)

    returns: obj populated with data


    """
    for name, value in data.items():
        if hasattr(obj, name):
            # print(name, value)
            setattr(obj, name, value)

    return obj
