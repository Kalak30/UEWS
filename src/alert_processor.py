""" Handles the timers and various alert variables to be able to accuratly alert
    operators when a submarines should be alerted that they are about to make a mistake.
"""
from tkinter.tix import Tree
from dynaconf import settings

import threading
import logging
from tspi import TSPIRecord
import bounds_check



logger = logging.getLogger(__name__)

class AlertProcessor:
    """ Singleton class that creates threads for different timers for alerting submarines.
        Three timers are used, no_data, no_sub, and between. The between timer is counting the time
        between received messages, and if it expires, then it can be assumed that a message has been
        missed.
        If an alarm should be sent, alarm_enable is set to True, otherwise it is False.
    """
    #-----------get timers for differnt alarm types----------
    def __get_no_data_timer__(self, time):
        """timer for complete loss of data"""
        return threading.Timer(time, self.set_no_data_alarm)

    def __get_no_sub_timer__(self, time):
        """Timer for no code 11 sub track"""
        return threading.Timer(time, self.set_no_sub_alarm_enable)

    def __get_between_timer__(self, time):
        """Timer for monitoring the time in between messages"""
        return threading.Timer(time, self.__between_ended__)

    def __get_seconds_alarm_timer__(self, time):
        #TODO NEED TO PLAY ANOTHER ALERT SOUND WHILE THIS IS COUNTING DOWN
        return threading.Timer(time, self.set_alarm_ON_auto) 


    def play_computer_sound(self):
        #TODO play some alert sound from computer
        logger.info("COMPUTER SOUNDING")

    def play_water_sound(self):
        #TODO play wav file, probably do this somewhere else?
        logger.info("ALARM SOUNDING")
        return

    def stop_water_sound(self):
        #TODO stop the wav file, probabl do this somewhere else
        logger.info("ALARM STOPPED")

    def __between_ended__(self):
        """Function for get_between to call. Resets consec_successes"""
        logger.debug("between timer ran out")
        self.consec_success = 0

    def calculate_no_track_time(self, last_record: TSPIRecord):
        """ Calculates the time until alarm_enable should be set if the UEWS system were to loose
            track of the submarine.
            Currently uses a similar algorithm to that of the old UEWS system.
        """
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



    #-----------start timers--------------
    def __start_no_output_timer__(self):
        """ start timer for compleat loss of incomming data"""
        self.data_timer.start()
        logger.debug("Started no output timer")

    def __start_no_sub_data_timer__(self, time):
        """ Starts a timer for loss of submarine data.
        """
        self.sub_timer = self.__get_no_sub_timer__(time)
        self.sub_timer.start()
        logger.debug(f"No sub timer started with {time} seconds")

    def __start_seconds_till_alarm_timer__(self):
        logger.info("staring seconds till alarm timer")
        self.seconds_till_alarm = self.__get_seconds_alarm_timer__(10)
        self.seconds_till_alarm.start()


    #----------------reset timers---------------
    def __reset_no_output_timer__(self):
        """reset timer used for compleat loss of data incomming. Starts another timer to wait till next no output"""
        self.data_timer.cancel()
        self.data_timer = self.__get_no_data_timer__(self.no_output_alert_time)
        self.data_timer.start()
        logger.debug("Reset no output Timer")
        #this does not clear alarm, need 5 in a row to clear alarm


    def __reset_no_sub_data_timer__(self): #resets after any code 11 recived
        """ Reset timer used for loss of code 11 sub track. It does not start another timer,
            but stops one if there is one active
        """
        if self.sub_timer.is_alive():
            self.sub_timer.cancel()
            logger.debug("Ended no sub tack Timer")

        #clear alarm if it was on
        if self.no_sub_alarm:
            self.clear_no_sub_alarm()

    def __reset_between_timer__(self):
        """ Resets timer that is used for tracking time between messages"""
        if self.between_timer.is_alive():
            self.between_timer.cancel()
        self.between_timer = self.__get_between_timer__(self.between_time_max)
        self.between_timer.start()
        logger.debug("reset between timer")
  

    def __clear_seconds_till_alarm_timer(self):
        if self.seconds_till_alarm.is_alive():
            self.seconds_till_alarm.cancel()
            logger.debug("cleared seconds till alarm timer")
        return
    

    #----reciving data functions----
    def recived_all_data(self):
        """ Function to handle a complete incomming message (has code 11).
            We do NOT know yet if it has valid data
            """
        if self.no_output_alarm:
            self.__check_between__()

        #reset timers because we have all data
        self.__reset_no_output_timer__()
        self.__reset_no_sub_data_timer__()

    def recived_no_code11_data(self, record : TSPIRecord):
        """Function to handle incommiong data that does NOT contain code 11 subtrack"""
        if self.no_output_alarm:
            self.__check_between__()
       
        #if timer has not started, start it
        if not self.sub_timer.is_alive():
            alarm_time = self.calculate_no_track_time(record)
            self.__start_no_sub_data_timer__(alarm_time)
        #reset no-output timer becuase we have some type of data comming in
        self.__reset_no_output_timer__()



    def __check_between__(self):
        """ Checks if message came in the last 3 seconds. If this happens 5 times in a row,
            turn off no output alarm
        """
        if self.between_timer.is_alive():
            self.consec_success += 1
            logger.debug(f"consecutive valid: {self.consec_success}")
        else:
            # If did not make it in time, reset counter to 1 becuase this is the first try for 
            # next 5 consec
            self.consec_success = 1

        if self.consec_success >= 5:
            self.clear_no_output_alarm()
            self.consec_success = 0
        else:
            self.__reset_between_timer__()


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
        """ Counts the number of bounds violations in the last 5 cycles. Sets boundary alarm if
            there are 2 out of 5 bad boundary violations.
        """
        #pop oldest to keep track of only 5
        self.bounds_violation_count.pop(0)

        #enable alarm if at least 2 out of 5 projections are outside
        if sum(self.bounds_violation_count) >= self.bounds_max_count:
            self.set_boundary_alarm()

        #otherwise clear the alarm if it is on
        else:
            if self.boundary_alarm:
                self.clear_boundary_alarm()

    #----Alarm setting-----
    #    5 types of alarms
    def set_no_data_alarm(self):
        """Turn on alarm for compleat loss of data"""
        self.total_alert += 1
        self.no_output_alarm = True
        self.between_timer = self.__get_between_timer__(3)
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
        """Turns off the Alarm_Enable"""
        self.alarm_enable = False
        self.total_alert = 0
        logger.info("Alert Enable Now OFF")
        self.clear_alarm_ON_auto()


    def set_alert(self):
        self.alarm_enable = True
        logger.info("Alert Enable Now ON")
        if self.auto_toggle:
            self.__start_seconds_till_alarm_timer__()

    #-----ALARM ON-------
    def clear_alarm_ON_auto(self):
        #clear timer if it is on
        self.__clear_seconds_till_alarm_timer()
        if self.alarm_ON_auto:
            self.alarm_ON_auto = False
            logger.info("Turned off auto alarm")
            self.refresh_alarm_ON()
        


    def clear_alarm_ON_manual(self):
        if self.alarm_ON_manual:
            self.alarm_ON_manual = False
            logger.info("Turned off manual alarm")
            self.refresh_alarm_ON()

    def set_alarm_ON_auto(self):
        if not self.alarm_ON_auto:
            self.alarm_ON_auto = True
            self.refresh_alarm_ON()
            logger.info("Turned on alarm (from auto alarm)")

    def set_alarm_ON_manual(self):
        if not self.alarm_ON_manual:
            self.alarm_ON_manual = True
            self.refresh_alarm_ON()
            logger.info("Turned on alarm (from manual alarm)")

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

    def refresh_alarm_ON(self):
        """Checks the auto alarm and manual alarm. Sets master alarm_ON if either are True"""
        if self.alarm_ON_manual or self.alarm_ON_auto:
            if not self.alarm_ON:
                self.alarm_ON = True
                self.play_water_sound()
        else:
            self.alarm_ON = False
            self.stop_water_sound()

    #print which alarm set off alarm_enable, for debugging
    def print_alarm(self):
        """Debug function, tells which of the 5 alarms set off the master alarm"""
        if self.no_output_alarm:
            logger.debug("eanbled from no_output_alarm")
        if self.no_sub_alarm:
            logger.debug("eanbled from no_sub_alarm")
        if self.boundary_alarm:
            logger.debug("eanbled from boundary_alarm")
        if self.valid_alarm:
            logger.debug("eanbled from valid_alarm")
        if self.depth_alarm:
            logger.debug("eanbled from depth_alarm")
        else:
            logger.debug("no changes made")

    def get_alarm_state(self) -> dict:
        """Returns a dictionary containing the current state of the alert processor
        """
        return {
                "alarm_enable": self.alarm_enable,
                "no_output_alarm": self.no_output_alarm,
                "no_sub_alarm": self.no_sub_alarm,
                "valid_alarm": self.valid_alarm,
                "depth_alarm": self.depth_alarm,
                "boundary_alarm": self.boundary_alarm,
                "depth_violations": self.depth_violation_count,
                "consec_valid": self.consec_success,
                "bounds_violations": self.bounds_violation_count,
                "invalid_data": self.invalid_data_count,
                "total_valid_track": self.total_valid_track,
                "total_alert": self.total_alert,
                "total_no_sub": self.total_no_sub
                }

    def recived_auto_change(self, auto_status):
        """Function to call when the auto toggle button is hit.
        param: alarm: T/F what is the status of auto alarm (T = auto, F = manual)"""
        logger.debug(f"recived auto change. status: {auto_status}")
        self.auto_toggle = auto_status

        #manual mode has been switched to automatic
        if self.auto_toggle:
            if self.alarm_enable:
                self.__start_seconds_till_alarm_timer__()
            if self.alarm_ON_manual: #clear manual alarm if it is on
                self.clear_alarm_ON_manual()
            return
        #automatic mode has been switched to manuel. clear timer if nessisarty
        else:
            self.__clear_seconds_till_alarm_timer()
            self.clear_alarm_ON_auto() #clear alarm if it is on
            
        return
    def recived_inhibit(self):
        """Function to call when the inhibit button is hit.
        param: none"""
        logger.debug(f"recived inhibit")
        #make sure timer is active
        if self.seconds_till_alarm.is_alive():
            self.seconds_till_alarm.cancel()

            #start new timer at 2 minutes
            self.seconds_till_alarm = self.__get_seconds_alarm_timer__(30)
            self.seconds_till_alarm.start()
            print("inhibit pressed, reset timer to 2 minutes")

        #inhibit was pressed when either alarm_ON is already sounding, or when there is no coundown and everything is fine
        else:
            if self.alarm_ON:
                logger.debug("inhibit pressed but alarm is already sounding. No action taken")
            else:
                logger.debug("inhibit pressed but there is no coundown and no alarm. No action taken")
        return

    def recived_toggle_update(self, auto_input, manual_input):
        if auto_input != self.auto_toggle:
            self.recived_auto_change(auto_input)
        if manual_input != self.alarm_ON_manual:
            self.recived_manual_alarm(manual_input)

    def recived_manual_alarm(self, alarm):
        """Function to call when the manual button is hit.
        param: alarm: T/F if manual alarm is being enabled or disabled"""
        logger.debug(f"recived manual alarm change. status: {alarm}")
        
        if alarm:
            self.set_alarm_ON_manual()
        else:
            #if was previouly on, then turn off manual, but refresh in case alarm-on-auto is still on
            if self.alarm_ON_manual:
                self.clear_alarm_ON_manual()
        return
    def __new__(cls):
        """ Function to force Alert Processor to only have 1 instance. If an instance already
            exists, return that instance. Otherwise create a new one and return that.
        """

        if not hasattr(cls, 'instance'):
            logger.debug("created new instance")
            cls.instance =super(AlertProcessor, cls).__new__(cls)
            cls.instance.initialized = False
        return cls.instance

    def stop_all(self):
        """ Stops all timers the alert processor controls.
        """
        logger.debug("timers stopped")
        self.sub_timer.cancel()
        self.data_timer.cancel()
        self.between_timer.cancel()
        self.seconds_till_alarm.cancel()

    def clear_all_alarns(self):
        logger.debug("all alarms cleared")
        self.clear_boundary_alarm()
        self.clear_depth_alarm()
        self.clear_invalid_alarm()
        self.clear_no_output_alarm()
        self.clear_no_sub_alarm()
        self.refresh_alarm()

    def reset_AP(self):
        """Hard reset AP, use for when you switch rest files and such. Resets all timers and alarms"""
        self.stop_all()
        self.clear_all_alarns()

    def __init__(self):
        """ Init for Alert Processor. Creates all variables, also starts loss of data and
            no Code 11 timers."""
        #if not the first instance, don't rubn __init__
        if self.initialized :
            return

        #if first instance, set to turue
        self.initialized = True
        logger.debug("created alert_process")

        #actual alarm for sending sound
        self.alarm_ON = False
        self.alarm_ON_auto = False
        self.alarm_ON_manual = False

        #control input
        self.auto_toggle = True


        #master alarm (is set if any of below are true). Once this is enabled, 10 seconds until alarm_ON
        self.alarm_enable = False

        #differnt types of alarms
        self.no_output_alarm = False
        self.no_sub_alarm = False

        self.valid_alarm = False
        self.depth_alarm = False
        self.boundary_alarm = False

        # TODO: Add time dilationv for all timers
        # Length in seconds of timer until an alert should be given if no sub track on PSK
        self.no_sub_alert_time = settings.NO_SUB_ALERT_TIME #defulats to 39.

        # Length in seconds of timer until an alert should be given if no output data received from RDMS
        self.no_output_alert_time = settings.NO_OUTPUT_ALERT_TIME

        self.between_time_max = settings.BETWEEN_TIME_MAX

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
        self.id_max_count = settings.INVALID_DATA_MAX_COUNT
        self.depth_max_count = settings.DEPTH_VIOLATION_MAX_COUNT
        self.bounds_max_count = settings.PROJ_POS_VIOLATION_MAX_COUNT

        #create and start timer for no data
        self.data_timer = self.__get_no_data_timer__(self.no_output_alert_time)
        self.__start_no_output_timer__()

        #create timer for no sub track
        self.sub_timer = self.__get_no_sub_timer__(self.no_sub_alert_time)

        #create in between data timer
        self.between_timer = self.__get_between_timer__(self.between_time_max)

        #create timer for seconds till alarm on
        self.seconds_till_alarm = self.__get_seconds_alarm_timer__(10)
        
