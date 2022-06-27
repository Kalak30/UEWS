import tspi

class CalculationState:
    def __init__(self, store: tspi.TSPIStore, raw_rsdf: str):
        self.store = store
        self.rsdf = raw_rsdf