class AlertProcessor:
    def __init__(self, invalid_data_max_count, depth_violation_max_count, proj_pos_violation_max_count):
        self.alarm_enable = False

        # Length in seconds of timer until an alert should be given if no sub track on PSK
        self.no_sub_alert_time = 0

        # Length in seconds of timer until an alert should be given if no output data received from RDMS
        self.no_output_alert_time = 0

        self.invalid_data_count = 0
        self.depth_violation_count = 0
        self.bounds_violation = 0

        self.id_max_count = invalid_data_max_count
        self.depth_max_count = depth_violation_max_count
        self.bounds_max_count = proj_pos_violation_max_count

    def start_no_output_timer(self):
        # TODO: Start a timer that can be interrupted with PP or code11 data. Start/don't stop no_sub data timer
        return

    def reset_no_output_timer(self):
        # TODO: Interrupt no_output timer. Start/don't stop no_sub data timer
        return

    def reset_no_sub_data_timer(self):
        # TODO: Interrupt no_sub data timer
        return

    def invalid_data(self):
        self.invalid_data_count += 1

        if self.invalid_data_count >= self.id_max_count:
            self.alarm_enable = True

    def depth_violation(self):
        self.depth_violation_count += 1
        if self.depth_violation_count >= self.depth_max_count:
            self.alarm_enable = True

    def bounds_violation_alert(self):
        self.bounds_violation += 1
        if self.bounds_violation >= self.bounds_max_count:
            self.alarm_enable = True

    def clear_alert(self):
        self.alarm_enable = False
