import unittest

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, '../src')
  
# importing the add and odd_even 
# function

from tspi import Vector
import bounds_check

p1 = (15559*3,1499*3, -164)
p2 = (15559*3,1499*3, -164)
p3 = (15560*3,1500*3, -164)
p4 = (15561*3,1500*3, -164)
p5 = (15560*3,1501*3, -164)
p6 = (15560*3,1500*3, -164)
p4 = (15560*3,1501*3, -216)
p4 = (15560*3,1500*3, -165)


class TestBounds(unittest.TestCase):
    def check_bounds(self):
        return


if __name__ == '__main__':
    unittest.main()