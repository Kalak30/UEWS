import tspi

class CalculationState:
    def __init__(self, store: tspi.TSPIStore, raw_rsdf: str, valid_data: dict, alarm_data: dict):
        self.store = store
        self.rsdf = raw_rsdf
        self.valid_data = valid_data
        self.alarm_data = alarm_data