import unittest

# importing sys
import sys
  
# adding Folder_2 to the system path
sys.path.insert(0, '../src')
  
# importing the add and odd_even 
# function

from tspi import Vector
import bounds_check
import alert_processor
import time

class TestAP(unittest.TestCase):
    """
    continious = False

    def test_valid_data(self):
        #initialize AP
        if not self.continious:
            AP = alert_processor.AlertProcessor()
        
        AP.valid_data()
        self.assertEqual(AP.valid_alarm, 0)

        AP.valid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.total_valid_track,2)

        AP.invalid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.invalid_data_count,1)


        AP.valid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.invalid_data_count,0)

        #send 4 invalid data points (only the 5th one should enable alarm)
        AP.invalid_data()
        AP.invalid_data()
        AP.invalid_data()
        AP.invalid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.invalid_data_count,4)

        #test 1 point (reset conter)
        AP.valid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.invalid_data_count,0)

        #send 5 invalid data points (alarm should enable)
        AP.invalid_data()
        AP.invalid_data()
        AP.invalid_data()
        AP.invalid_data()
        AP.invalid_data()
        self.assertEqual(AP.valid_alarm, 1)
        self.assertEqual(AP.invalid_data_count,5)
        
        #send another, alarm should stay on
        AP.invalid_data()
        self.assertEqual(AP.valid_alarm, 1)
        self.assertEqual(AP.invalid_data_count,6)

        #send a valid, should turn alarm off
        AP.valid_data()
        self.assertEqual(AP.valid_alarm, 0)
        self.assertEqual(AP.invalid_data_count,0)

        #total valid should be 6
        self.assertEqual(AP.total_valid_track, 5)

        if not self.continious:
            del AP

    def test_depth(self):
        if not self.continious:
            AP = alert_processor.AlertProcessor()

        AP.depth_violation()  
        self.assertEqual(AP.depth_violation_count, 1)      
        AP.depth_ok()
        self.assertEqual(AP.depth_violation_count, 0)

        AP.depth_violation()  
        AP.depth_violation()  
        AP.depth_violation()  
        AP.depth_violation()  
        AP.depth_violation() 
        self.assertEqual(AP.depth_violation_count,5)
        self.assertEqual(AP.depth_alarm, 1) 

        #add more violations, alarm should stay on
        AP.depth_violation()  
        AP.depth_violation() 
        self.assertEqual(AP.depth_violation_count,7)
        self.assertEqual(AP.depth_alarm, 1) 

        #alarm should turn off, depth ok and doesn't reach 5 consec
        AP.depth_ok()
        self.assertEqual(AP.depth_alarm, 0) 
        AP.depth_violation()  
        self.assertEqual(AP.depth_alarm, 0)
        AP.depth_ok()
        AP.depth_violation()
        AP.depth_ok()
        AP.depth_violation()
        self.assertEqual(AP.depth_alarm, 0) 
        AP.depth_ok()
        self.assertEqual(AP.depth_alarm, 0) 
        AP.depth_violation()
        AP.depth_violation()
        AP.depth_violation()
        AP.depth_violation()
        self.assertEqual(AP.depth_violation_count,4)
        self.assertEqual(AP.depth_alarm, 0) 
        AP.depth_ok()
        self.assertEqual(AP.depth_alarm, 0) 

        if not self.continious:
            del AP

    
    def test_no_data(self):
        if not self.continious:
            AP = alert_processor.AlertProcessor()

        #recive 2 sets of data, then stop
        AP.recived_all_data()
        AP.recived_all_data()

        #stop for 5 seconds. This is NOT enough time to start alarm
        time.sleep(5)
        self.assertEqual(AP.no_output_alarm, 0)

        AP.recived_all_data()
        self.assertEqual(AP.no_output_alarm, 0)

        #stop for 9 seconds. This is NOT enough time to start alarm
        time.sleep(9)
        self.assertEqual(AP.no_output_alarm, 0)

        AP.recived_all_data()
        self.assertEqual(AP.no_output_alarm, 0)

        #stop for 10 seconds. This is  enough time to start alarm
        time.sleep(12)
        self.assertEqual(AP.no_output_alarm, 1)

        #alarm should stay on even though recived data. need 5 valid to turn off
        AP.recived_no_code11_data()
        self.assertEqual(AP.no_output_alarm, 1)
        self.assertEqual(AP.consec_success, 1)

        #wait to simulate 1 missed message
        time.sleep(4)
        self.assertEqual(AP.consec_success, 0)

        #five messages of either full or no code 11 should turn off alarm. 2 seconds between each one to simulate real data
        AP.recived_noCode11_data()
        self.assertEqual(AP.consec_success, 1)
        time.sleep(2)
        
        AP.recived_all_data()
        time.sleep(2)
        AP.recived_noCode11_data()
        time.sleep(2)
        AP.recived_all_data()
        time.sleep(2)

        self.assertEqual(AP.consec_success,4)

        #after the 5th it should reset
        self.assertEqual(AP.no_output_alarm, 1)
        AP.recived_all_data()
        self.assertEqual(AP.no_output_alarm, 0)


        if not self.continious:
            del AP

    #TODO (need R value calculations to test functionality)
    def test_no_sub_tack(self):
        if not self.continious:
            AP = alert_processor.AlertProcessor()

        
        if not self.continious:
            AP.stop_all()
            del AP

        return
    
    def test_boundary(self):
        if not self.continious:
            AP = alert_processor.AlertProcessor()


            AP.bounds_violation()
            AP.bounds_ok()
            AP.bounds_ok()
            AP.bounds_ok()
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 0)
            AP.bounds_violation()
            AP.bounds_violation()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            AP.bounds_ok()
            AP.bounds_ok()
            AP.bounds_violation()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 0)

            AP.bounds_violation()
            AP.bounds_violation()
            AP.bounds_violation()
            AP.bounds_violation()
            AP.bounds_violation()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 1)
            AP.bounds_ok()
            self.assertEqual(AP.boundary_alarm, 0)


        if not self.continious:
            AP.stop_all()
            del AP

        return

    def test_alarm(self):
        if not self.continious:
            AP = alert_processor.AlertProcessor()

        AP.set_boundary_alarm()
        AP.set_depth_alarm()

        self.assertEqual(AP.alarm_enable, 1)

        AP.clear_boundary_alarm()
        self.assertEqual(AP.alarm_enable, 1)

        AP.clear_depth_alarm()
        self.assertEqual(AP.alarm_enable, 0)

        AP.set_invalid_alarm()
        AP.set_no_sub_alarm_enable()
        AP.set_no_data_alarm()
        self.assertEqual(AP.alarm_enable, 1)

        AP.clear_no_sub_alarm()
        AP.clear_no_output_alarm()
        self.assertEqual(AP.alarm_enable, 1)

        AP.clear_invalid_alarm()
        self.assertEqual(AP.alarm_enable, 0)


        return
"""
    def test_alart_ON(self):
        AP = alert_processor.AlertProcessor()
        
        AP.set_alert()

        AP.recived_toggle_update(0,0)
        AP.recived_toggle_update(1,0)
        AP.recived_toggle_update(1,1)

        """
        #check if timer started
        self.assertTrue(AP.seconds_till_alarm.is_alive())

        #wait 9 seconds and wait to make sure alarm is not on
        time.sleep(9)
        self.assertFalse(AP.alarm_ON)

        #after 1 more second it should be on
        #it should also be on from auto, not manual
        time.sleep(1.1)
        self.assertTrue(AP.alarm_ON)
        self.assertTrue(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)

        #change auto to manual control, should turn off alarm
        AP.recived_auto_change(0)

        self.assertFalse(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)

        #turn back to automatic, alarm counter should start again becuase aler_enable is still one
        AP.recived_auto_change(1)
        self.assertTrue(AP.seconds_till_alarm.is_alive())
        time.sleep(10.1)
        self.assertTrue(AP.alarm_ON)
        self.assertTrue(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)

        #turn alert off, should turn alarm_on off
        AP.clear_alert()
        self.assertFalse(AP.alarm_ON)


        #start alart and inhibit it. Should take 2 minutes to enable
        AP.set_alert()
        time.sleep(9)
        AP.recived_inhibit()
        time.sleep(1.1)
        self.assertFalse(AP.alarm_ON)
        self.assertTrue(AP.seconds_till_alarm.is_alive())
        time.sleep(120)
        self.assertFalse(AP.seconds_till_alarm.is_alive())
        self.assertTrue(AP.alarm_ON)
        self.assertTrue(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)


        #change to manual mode while alert is on. This will turn alarm off
        AP.recived_auto_change(0)
        self.assertFalse(AP.alarm_ON)

        #set alarm on manualy. This should enable alarm again, but from manual 
        AP.recived_manual_alarm(1)
        self.assertTrue(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertTrue(AP.alarm_ON_manual)

        #turn off manual alarm
        AP.recived_manual_alarm(0)
        self.assertFalse(AP.alarm_ON_manual)


        #turn BACK to automatic. 
        #alarm should turn off and automatic counter should start again
        AP.recived_auto_change(1)
        self.assertFalse(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)
        self.assertTrue(AP.seconds_till_alarm.is_alive())

        #alarm should enable again after 10 seconds
        time.sleep(10.1)
        self.assertTrue(AP.alarm_ON)
        self.assertTrue(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)

        #turn off alert and then back on. wait halfway though timer, then switch to manual
        AP.clear_alert()
        AP.set_alert()
        self.assertTrue(AP.seconds_till_alarm.is_alive())
        time.sleep(5)
        AP.recived_auto_change(0)

        #now in manual mode everything should be off., even after waiting 
        self.assertFalse(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)
        time.sleep(6)
        self.assertFalse(AP.alarm_ON)

        # Enable the alarm, then switch back to auto before disabling.
        AP.recived_manual_alarm(1)
        AP.recived_auto_change(1)

        #manual alarm should turn off, and automatic should start again
        self.assertFalse(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)
        self.assertTrue(AP.seconds_till_alarm.is_alive())

        #cancel alert 5 seconds in. Should stop the timer and alarm_on
        time.sleep(5)
        AP.clear_alert()
        AP.seconds_till_alarm.cancel()
        #self.assertFalse(AP.seconds_till_alarm.is_alive()) #cannot assert false after canceling, race condition
        time.sleep(10.1)
        self.assertFalse(AP.alarm_ON)
        self.assertFalse(AP.alarm_ON_auto)
        self.assertFalse(AP.alarm_ON_manual)
        self.assertFalse(AP.seconds_till_alarm.is_alive())
        """

    def test_clear_all(self):
        AP = alert_processor.AlertProcessor()
        AP.alarm_enable()
        AP.reset_AP()
        self.assertEqual(AP.no_output_alarm, 0)

if __name__ == '__main__':
    unittest.main()