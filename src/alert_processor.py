from cgitb import reset
import threading
import logging
import configurator


logger = logging.getLogger(__name__)

class AlertProcessor:

    #get timers for differnt alarm types
    def get_no_data_timer(self, time):
        return threading.Timer(time, self.set_no_data_alarm)

    def get_no_sub_timer(self, time):
        return threading.Timer(time, self.set_no_sub_alarm_enable)

    def get_between_timer(self, time):
        return threading.Timer(time, self.print_between)

    #function for get_between to call
    def print_between(self):
        logger.debug("between timer ran out")
         
    def set_no_sub_alert_time():
        #TODO calculate "r", the no subtack time, using info from tspi

        return

    #start timers
    def start_no_output_timer(self):
        self.data_timer.start()
        logging.debug("Started no output timer")
        return

    def start_no_sub_data_timer(self):
        self.sub_timer.start()
        logging.debug("Started no subtrack timer")
        return

    #reset timers
    def reset_no_output_timer(self):
        self.data_timer.cancel()
        self.data_timer = self.get_no_data_timer(self.no_output_alert_time)
        self.data_timer.start()
        logging.debug("Reset no output Timer")
        #this does not clear alarm, need 5 in a row to clear alarm
        return

    def reset_no_sub_data_timer(self): #resets after any code 11 recived
        self.sub_timer.cancel()
        self.sub_timer = self.get_no_sub_timer(self.no_sub_alert_time)
        self.sub_timer.start()
        logging.debug("Reset no sub tack Timer") #TODO doulbe check 1 instance clears alarm
        if(self.no_sub_alarm):
            self.clear_no_sub_alarm()
        return

    def reset_between_timer(self):
        if self.between_timer.is_alive():
            self.between_timer.cancel()
        self.between_timer = self.get_between_timer(self.between_time_max)
        self.between_timer.start()
        logging.debug("reset betwee timer")
        return
  

    #logic for getting data (NOTE: WE DO NOT KNOW IT IS VALID YET)
    def recived_all_data(self):

        
        #reset timers because we have all data
        self.reset_no_output_timer()
        self.reset_no_sub_data_timer()
        return

    #logic for getting data that is missing code 11
    def recived_noCode11_data(self):
        if self.no_output_alarm:
            self.check_between()

        #reset no-output timer becuase we have some type of data comming in
        self.reset_no_output_timer()
        return

    #checks if message came in the last 3 seconds. If this happens 5 times in a row, turn off alarm
    def check_between(self):
        if self.between_timer.is_alive():
            self.consec_valid += 1
        else:
            self.consec_valid = 0

        if self.consec_valid > 5:
            self.clear_no_output_alarm()
            self.consec_valid = 0
        else:
            self.reset_between_timer()
        return

    #counting for data/boundary violation
    def invalid_data(self):
        logger.debug("got invaid data")
        self.invalid_data_count += 1
        if self.invalid_data_count >= self.id_max_count:
            self.valid_alarm = True
    
    def valid_data(self):
        logger.debug("got valid data")

        #check if no ouput alarm is on, and turn it off if 5th consecutive valid data
        if self.no_output_alarm:
            self.check_between()

        self.invalid_data_count = 0
        self.valid_alarm = False
        return

    def depth_violation(self):
        self.depth_violation_count += 1
        if self.depth_violation_count >= self.depth_max_count:
            self.depth_alarm = True

    def depth_ok(self):
        self.depth_violation_count = 0
        self.depth_alarm = False
        return

    def bounds_violation_alert(self):
        self.bounds_violation += 1
        if self.bounds_violation >= self.bounds_max_count:
            self.boundary_alarm = True

    #alrm setting (each time one is set, refresh master)
    def set_no_data_alarm(self):
        self.no_output_alarm = True
        self.between_timer = self.get_between_timer(3)
        self.between_timer.start()
        logger.info("no data alarm set")
        self.refresh_alarm()

    def set_no_sub_alarm_enable(self):
        self.no_sub_alarm = True
        logger.info("no sub track alarm set")
        self.refresh_alarm()

    #clearning alarms. Each time an alarm is clearned, master alert is refreshed
    def clear_no_output_alarm(self):
        logging.info("No output alarm turned off")
        self.no_output_alarm = False
        self.refresh_alarm()
    
    def clear_no_sub_alarm(self):
        logging.info("No sub track alarm turned off")
        self.no_sub_alarm = False
        self.refresh_alarm()

    def clear_boundary_alarm(self):
        logging.info("Boundary alarm turned off")
        self.boundary_alarm = False
        self.refresh_alarm()
    
    # master alert
    def clear_alert(self):
        self.alarm_enable = False
        logging.info("Alert Enable Now OFF")

    def set_alert(self):
        self.alarm_enable = True
        logging.info("Alert Enable Now ON")

    #refresh master alert
    def refresh_alarm(self):
        if self.no_output_alarm or self.no_sub_alarm or self.boundary_alarm or self.valid_alarm or self.depth_alarm:
            if not self.alarm_enable:
                self.set_alert()
        else:
            logging.debug("no alarms on")
            if self.alarm_enable:
                self.clear_alert()
        return

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            logging.debug("created new instance")
            cls.instance =super(AlertProcessor, cls).__new__(cls)
            cls.instance.initialized = False
        return cls.instance
   
   
    def __init__(self):
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
        self.no_sub_alert_time = 5

        # Length in seconds of timer until an alert should be given if no output data received from RDMS
        self.no_output_alert_time = 10        #TODO add config for how long till alert if not data (config_args[""])

        self.between_time_max = 3   #TODO add config for how long till alert if not data (config_args[""])

        #count variable for num consecutive messages after loss of data
        self.consec_valid = 0

        #count variables for number of violoations
        self.invalid_data_count = 0
        self.depth_violation_count = 0
        self.bounds_violation = 0

        #max number the violation counts can be before enable alarm
        self.id_max_count = config_args["invalid_data_max_count"]
        self.depth_max_count = config_args["depth_violation_max_count"]
        self.bounds_max_count = config_args["proj_pos_violation_max_count"]

        #create and start timer for no data
        self.data_timer = self.get_no_data_timer(self.no_output_alert_time)
        self.start_no_output_timer()

        #create and start timer for no sub track
        self.sub_timer = self.get_no_sub_timer(self.no_sub_alert_time)
        self.start_no_sub_data_timer()

        #in between data timer
        self.between_timer = self.get_between_timer(self.between_time_max)
        
