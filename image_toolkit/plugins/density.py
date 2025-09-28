# DensityAdjustmentPluginダミー実装
class DensityAdjustmentPlugin:
    def __init__(self):
        self.parameter_change_callback = None
        self.histogram_callback = None
        self.threshold_callback = None

    def set_parameter_change_callback(self, func):
        self.parameter_change_callback = func

    def set_histogram_callback(self, func):
        self.histogram_callback = func

    def set_threshold_callback(self, func):
        self.threshold_callback = func
