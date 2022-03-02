
class Weather:

    def __init__(self, state, wind_speed, visibility_impairment, temperature, humidity):
        self.state = state
        self.wind_speed = wind_speed
        # float value:  1 < value < 2
        if visibility_impairment < 1 or visibility_impairment > 2:
            self.visibility_impairment = 1
        else:
            self.visibility_impairment = visibility_impairment
        self.temperature = temperature
        self.humidity = humidity
