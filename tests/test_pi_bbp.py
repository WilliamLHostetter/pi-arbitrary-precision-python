from pi_bbp import piBBP
import pytest
import decimal
from decimal import Decimal
# First 1 million digits of π can be found at
# #https://www.piday.org/million/
# One hundred decimal places of π is given below
pi_str = "3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798"


decimal.getcontext().prec = 103
parameters_list =  [(10, round(Decimal(pi_str), 10)), 
                    (50, round(Decimal(pi_str), 50)), 
                    (100, round(Decimal(pi_str), 100)),]
@pytest.mark.parametrize("precision_num_digits, expected", parameters_list)
def test_piBBP(precision_num_digits, expected):
    '''
    Testing the Bailey-Borwein-Plouffe (BBP) formula by comparing to piday.org calculation of π 
    piBBP(precision_num_digits: int) -> Decimal
    '''
    assert piBBP(precision_num_digits) == expected