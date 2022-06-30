from cgitb import reset
from dis import dis
import threading
import logging
from turtle import speed
from bounds_check import distance_to_edge
import configurator
from tspi import TSPIRecord
import bounds_check


logger = logging.getLogger(__name__)

class AlertProcessor:

    #get timers for differnt alarm types
    def get_no_data_timer(self, time):
        """timer for complete loss of data"""
        return threading.Timer(time, self.set_no_data_alarm)

    def get_no_sub_timer(self, time):
        """Timer for no code 11 sub track"""
        return threading.Timer(time, self.set_no_sub_alarm_enable)

    def get_between_timer(self, time):
        """Timer for monitoring the time in between messages"""
        return threading.Timer(time, self.between_ended)

    #function for get_between to call
    def between_ended(self):
        #reset valid counter because missed a message
        logger.debug("between timer ran out")
        self.consec_success = 0
         
    def calculate_no_track_time(self, last_record: TSPIRecord):
        #if there is no last record, set alarm
        if last_record == 0:
            return 0
        time_till_alarm = 0

        

        distance_edge = bounds_check.distance_to_edge(last_record.position)
        proj_distance_edge = bounds_check.distance_to_edge(last_record.proj_position)

        distance_factor = 5
        speed_factor = 12

        if distance_edge < 1500*3:
            distance_factor = 3
        if distance_edge < 750*3:
            distance_factor = 2

        #if projected to closer to edge then current, then heading towards boundary. Decrease distanc factor
        if proj_distance_edge < distance_edge:
            distance_factor -= 1

        #max alarm time with slow knots worse case is 7.8 seconds
        if last_record.knots > 15:
            speed_factor = 3 
        elif last_record.knots > 10:
            speed_factor = 5
        elif last_record.knots > 5:
            speed_factor = 8

        #formula taken from old uews software.
        time_till_alarm = distance_factor * speed_factor * .65

        return time_till_alarm



    #----start timers----
    def start_no_output_timer(self):
        """start timer for compleast loss of incomming data"""
        self.data_timer.start()
        logger.debug("Started no output timer")
        return

    def start_no_sub_data_timer(self, time):
        self.sub_timer = self.get_no_sub_timer(time)
        self.sub_timer.start()
        logger.debug(f"No sub timer started with {time} seconds")
        return


    #----reset timers----
    def reset_no_output_timer(self):
        """reset timer used for compleat loss of data incomming. Starts another timer to wait till next no output"""
        self.data_timer.cancel()
        self.data_timer = self.get_no_data_timer(self.no_output_alert_time)
        self.data_timer.start()
        logger.debug("Reset no output Timer")
        #this does not clear alarm, need 5 in a row to clear alarm
        return


    def reset_no_sub_data_timer(self): #resets after any code 11 recived
        """reset timer used for loss of code 11 sub track. It does not start another timer, but stops one if there is one active"""
        if self.sub_timer.is_alive():
            self.sub_timer.cancel()
            logger.debug("Ended no sub tack Timer")

        #clear alarm if it was on
        if(self.no_sub_alarm):
            self.clear_no_sub_alarm()
        return

    def reset_between_timer(self):
        """resets timer that is used for tracking time between messages"""
        if self.between_timer.is_alive():
            self.between_timer.cancel()
        self.between_timer = self.get_between_timer(self.between_time_max)
        self.between_timer.start()
        logger.debug("reset betwee timer")
        return
  
    #----reciving data functions----
    def recived_all_data(self):
        """function to handle a complete incomming message (has code 11).
         We do NOT know yet if it has valid data"""
        if self.no_output_alarm:
            self.check_between()

        #reset timers because we have all data
        self.reset_no_output_timer()
        self.reset_no_sub_data_timer()
        return

    def recived_noCode11_data(self, record : TSPIRecord):
        """Function to handle incommiong data that does NOT contain code 11 subtrack"""
        if self.no_output_alarm:
            self.check_between()
        
        #if timer has not started, start it
        if not self.sub_timer.is_alive():
            alarm_time = self.calculate_no_track_time(record)
            self.start_no_sub_data_timer(alarm_time)
        #reset no-output timer becuase we have some type of data comming in
        self.reset_no_output_timer()
        return


    def check_between(self):
        """checks if message came in the last 3 seconds. If this happens 5 times in a row, turn off no output alarm"""
        if self.between_timer.is_alive():
            self.consec_success += 1
            logger.debug(f"consecutive valid: {self.consec_success}")
        else:
            #if did not make it in time, reset counter to 1 becuase this is the first try for next 5 consec
            self.consec_success = 1

        if self.consec_success >= 5:
            self.clear_no_output_alarm()
            self.consec_success = 0
        else:
            self.reset_between_timer()
        return

    #----counting for position violations----
    #3 different count tpyes: invalid data, depth violation, porjected boundary violoation
    def invalid_data(self):
        """Handles an invaid data point"""
        self.invalid_data_count += 1
        logger.debug(f"got invaid data. count: {self.invalid_data_count}")
        if self.invalid_data_count >= self.id_max_count:
            self.set_invalid_alarm()
    
    def valid_data(self):
        """handles valid data point"""
        logger.debug("got valid data")


        #reset invaid data counter. Clear alarm if it is on
        self.invalid_data_count = 0
        self.total_valid_track += 1
        if self.valid_alarm:
            self.clear_invalid_alarm()
        return

    def depth_violation(self):
        """Handles a 220 foot depth violation. Adds to counter and alarm on if 5 consec."""
        self.depth_violation_count += 1
        if self.depth_violation_count >= self.depth_max_count:
            self.set_depth_alarm()

    def depth_ok(self):
        """Handles when 220 foot depth is ok. Resets counter and alarm"""
        self.depth_violation_count = 0
        if self.depth_alarm:
            self.clear_depth_alarm()
        return


    def bounds_violation(self):
        """Handles out of projected boundary. Adds to 2/5 counter"""
        self.bounds_violation_count.append(1)
        self.bounds_handle()

    def bounds_ok(self):
        """handles ok projected boundary. Resets alarm if on"""
        self.bounds_violation_count.append(0)
        self.bounds_handle()

    def bounds_handle(self):
        #pop oldest to keep track of only 5
        self.bounds_violation_count.pop(0)

        #enable alarm if at least 2 out of 5 projections are outside
        if sum(self.bounds_violation_count) >= self.bounds_max_count:
            self.set_boundary_alarm()
        
        #otherwise clear the alarm if it is on
        else:
            if self.boundary_alarm:
                self.clear_boundary_alarm()

        return

    #----Alarm setting-----
    #    5 types of alarms
    def set_no_data_alarm(self):
        """Turn on alarm for compleat loss of data"""
        self.total_alert += 1
        self.no_output_alarm = True
        self.between_timer = self.get_between_timer(3)
        self.between_timer.start()
        logger.info("no data alarm set")
        self.refresh_alarm()

    def set_no_sub_alarm_enable(self):
        """Turn on alarm for no code 11 sub track"""
        self.total_alert += 1
        self.total_no_sub += 1
        self.no_sub_alarm = True
        logger.info("no sub track alarm set")
        self.refresh_alarm()

    def set_boundary_alarm(self):
        """Trun on alarm for projected boundary"""
        self.total_alert += 1
        self.boundary_alarm = True
        logger.info("boundary alarm set")
        self.refresh_alarm()

    def set_invalid_alarm(self):
        """Turn on alarm for invalid data"""
        self.total_alert += 1
        self.valid_alarm = True
        logger.info("invaild alarm set")
        self.refresh_alarm()

    def set_depth_alarm(self):
        """Turn on alarm for under 220 foot depth"""
        self.total_alert += 1
        self.depth_alarm = True
        logger.info("depth alarm set")
        self.refresh_alarm()

    #----clearning alarms----
    #    5 tpyes of alarms
    def clear_no_output_alarm(self):
        """Turn off compleat loss of data alarm"""
        logger.info("No output alarm turned off")
        self.no_output_alarm = False
        self.refresh_alarm()
    
    def clear_no_sub_alarm(self):
        """Turn off no code 11 sub track alarm"""
        logger.info("No sub track alarm turned off")
        self.no_sub_alarm = False
        self.refresh_alarm()

    def clear_boundary_alarm(self):
        """Turn off projected boundary alarm"""
        logger.info("Boundary alarm turned off")
        self.boundary_alarm = False
        self.refresh_alarm()

    def clear_invalid_alarm(self):
        """Turn off invalid data alarm"""
        logger.info("invalid alarm turned off")
        self.valid_alarm = False
        self.refresh_alarm()

    def clear_depth_alarm(self):
        """Turn off depth under 220 feet alarm"""
        logger.info("depth alarm turned off")
        self.depth_alarm = False
        self.refresh_alarm()
    
    #----master alert----
    def clear_alert(self):
        """Turns on the Alarm_Enablew"""
        self.alarm_enable = False
        self.total_alert = 0
        logger.info("Alert Enable Now OFF")

    def set_alert(self):
        self.alarm_enable = True
        logger.info("Alert Enable Now ON")

    #refresh master alert
    def refresh_alarm(self):
        """checks all 5 types of alarms. Enables master alarm if any are set to True"""
        if self.no_output_alarm or self.no_sub_alarm or self.boundary_alarm or self.valid_alarm or self.depth_alarm:
            if not self.alarm_enable:
                self.set_alert()
                self.print_alarm()
        else:
            logger.debug("no alarms on")
            if self.alarm_enable:
                self.clear_alert()
        return

    #print which alarm set off alarm_enable, for debugging
    def print_alarm(self):
        """Debug function, tells which of the 5 alarms set off the master alarm"""
        if self.no_output_alarm:
            logger.debug(f"eanbled from no_output_alarm")
        if self.no_sub_alarm:
            logger.debug(f"eanbled from no_sub_alarm")
        if self.boundary_alarm:
            logger.debug(f"eanbled from boundary_alarm")
        if self.valid_alarm:
            logger.debug(f"eanbled from valid_alarm")
        if self.depth_alarm:
            logger.debug(f"eanbled from depth_alarm")
        else:
            logger.debug(f"no changes made")

    def get_alarm_state(self) -> dict:
        """Returns a dictionary containing the current state of the alert processor
        """
        return {"alarm_enable": self.alarm_enable, "no_output_alarm": self.no_output_alarm, "no_sub_alarm": self.no_sub_alarm,
                "valid_alarm": self.valid_alarm, "depth_alarm": self.depth_alarm, "boundary_alarm": self.boundary_alarm,
                "depth_violations": self.depth_violation_count, "consec_valid": self.consec_success, "bounds_violations": self.bounds_violation_count,
                "invalid_data": self.invalid_data_count, "total_valid_track": self.total_valid_track, "total_alert": self.total_alert,
                "total_no_sub": self.total_no_sub}

    def __new__(cls):
        """Function to force Alert Processor to only have 1 instance. 
        If an instance already exists, return that instance. Otherwise create a new one and return that. """

        if not hasattr(cls, 'instance'):
            logger.debug("created new instance")
            cls.instance =super(AlertProcessor, cls).__new__(cls)
            cls.instance.initialized = False
        return cls.instance
   
    def stop_all(self):
        logger.debug("timers stopped")
        self.sub_timer.cancel()
        self.data_timer.cancel()
        self.between_timer.cancel()
   
    def __init__(self):
        """init for Alert Processor. Creates all variables, also starts loss of data and no Code 11 timers."""
        #if not the first instance, don't rubn __init__
        if(self.initialized) : return

        #if first instance, set to turue
        self.initialized = True
        logger.debug("created alert_process")

        config_args = configurator.get_config()
        

        #master alarm (is set if any of below are true)
        self.alarm_enable = False

        #differnt types of alarms
        self.no_output_alarm = False
        self.no_sub_alarm = False
        
        self.valid_alarm = False
        self.depth_alarm = False
        self.boundary_alarm = False

        # Length in seconds of timer until an alert should be given if no sub track on PSK
        self.no_sub_alert_time = 39 #defulats to 39. #TODO add multiplier for speed up

        # Length in seconds of timer until an alert should be given if no output data received from RDMS
        self.no_output_alert_time = 10        #TODO add config for how long till alert if not data (config_args[""])

        self.between_time_max = 3   #TODO add config for how long till alert if not data (config_args[""])

        #count variable for num consecutive messages after loss of data
        self.consec_success = 0

        #count variables for number of violoations
        self.invalid_data_count = 0
        self.depth_violation_count = 0
        self.bounds_violation_count = [0,0,0,0,0]

        self.total_valid_track = 0
        self.total_no_sub = 0
        self.total_alert = 0

        #max number the violation counts can be before enable alarm
        self.id_max_count = config_args["invalid_data_max_count"]
        self.depth_max_count = config_args["depth_violation_max_count"]
        self.bounds_max_count = config_args["proj_pos_violation_max_count"]

        #create and start timer for no data
        self.data_timer = self.get_no_data_timer(self.no_output_alert_time)
        self.start_no_output_timer()

        #create and start timer for no sub track
        self.sub_timer = self.get_no_sub_timer(self.no_sub_alert_time)

        #in between data timer
        self.between_timer = self.get_between_timer(self.between_time_max)
        
