import tspi

class CalculationState:
    def __init__(self, reset: bool, store: tspi.TSPIStore, raw_rsdf: str, valid_data: dict, alarm_data: dict, counters: dict):
        self.reset = reset
        self.store = store
        self.rsdf = raw_rsdf
        self.valid_data = valid_data
        self.alarm_data = alarm_data
        self.counters = counters