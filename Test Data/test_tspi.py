from datetime import datetime
from turtle import pos
import unittest

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, '../src')
  
# importing the add and odd_even 
# function

import tspi
from tspi import TSPIRecord, Vector
import bounds_check
import alert_processor
import time
import datetime

#test data
t1 = datetime.datetime(1,1,1,1,1,1)
t2 = datetime.datetime(1,1,1,1,1,2)
t3 = datetime.datetime(1,1,1,1,1,3)
t4 = datetime.datetime(1,1,1,1,1,4)
t5 = datetime.datetime(1,1,1,1,1,5)
t6 = datetime.datetime(1,1,1,1,1,6)
t21  = datetime.datetime(1,1,1,1,2,1)
t31 = datetime.datetime(2,1,1,1,1,1)

p1 = Vector(0,0,0)
p2 = Vector(2,0,0)
p3 = Vector(2,2,0)
p4 = Vector(0,0,0)
p5 = Vector(-4,-4,0)
p6 = Vector(-4,-4,-10)



class TestTsip(unittest.TestCase):
    r1 = tspi.TSPIRecord(p1, Vector(0, 0, 0), time=t1, heading=0, knots=1.18497)
    r2 = tspi.TSPIRecord(p2, Vector(2, 0, 0), time=t2, heading=0, knots=1.18497)
    r3 = tspi.TSPIRecord(p3, Vector(0, 2, 0), time=t3, heading=90, knots=1.18497)
    r4 = tspi.TSPIRecord(p4, Vector(-2, -2, 0), time=t4, heading=225, knots=1.67580064501)
    r5 = tspi.TSPIRecord(p5, Vector(8.43905, 0, 0), time=t5, heading=225, knots=3.35160)
    r6 = tspi.TSPIRecord(p6, Vector(8.43905, 0, 0), time=t6, heading=0, knots=0)
    
    def test_record(self):
        ttl = 4
        #test values entered
        self.assertEqual(self.r1.position, Vector(0,0,0))
        self.assertEqual(self.r1.heading, 0)
        self.assertFalse(self.r1.is_old(ttl, t2))
        self.assertFalse(self.r1.is_old(ttl, t3))
        self.assertFalse(self.r1.is_old(ttl, t4))
        self.assertFalse(self.r1.is_old(ttl, t5))
        self.assertTrue(self.r1.is_old(ttl, t6))
        self.assertTrue(self.r1.is_old(ttl, t21))
        self.assertTrue(self.r1.is_old(ttl, t31))


    def test_store(self):
        store = tspi.TSPIStore(ttl=4)
        store.add_record(self.r1)
        self.assertEqual(store.records[0].deltas, Vector(0,0,0))
        store.add_record(self.r2)
        self.assertEqual(store.records[0].deltas, Vector(2,0,0))
        self.assertEqual(len(store.records), 2)
        store.add_record(self.r3)
        self.assertEqual(store.records[0].deltas, Vector(0,2,0))
        self.assertEqual(store.total_speeds, Vector(2,2,0))

        #it has been 2 seconds since last record
        store.add_record(self.r5)
        print("added r5")
        self.assertEqual(store.records[0].deltas, Vector(-3,-3,0))
        self.assertEqual(store.total_speeds,  Vector(-1,-1,0))
        self.assertEqual(len(store.records), 4)

        #has been over 4 seconds since first record, need to remove
        store.add_record(self.r6)
        self.assertEqual(store.records[0].deltas, Vector(0,0,-10))
        self.assertEqual(len(store.records), 4)
        #total speed from r2 to r6 with 4 seconds having past
        print(store.records[-1].position)
        print(store.records[0].position)
        print(store.records[-1].time)
        print(store.records[0].time)
        self.assertEqual(store.records[-1].position, p2)
        self.assertEqual(store.records[0].position, p6)
        #self.assertEqual(store.total_speeds,  Vector(-1.5, -4, -10))
        self.assertEqual(store.get_average_speeds(),  Vector(-1.5,-1,-2.5))
        
    
    #def test_speed(self):




if __name__ == '__main__':
    unittest.main()