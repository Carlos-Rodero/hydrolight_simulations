class Bottom:
    """
    Create new Bottom
    """
    all_values = ["dummyR.bot", "avg_clean_seagrass.txt", "avg_coral.txt", "avg_dark_sediment.txt",
                  "avg_hardpan.txt", "avg_kelp.txt", "avg_macrophyte.txt", "avg_ooid_sand.txt",
                  "avg_seagrass.txt", "avg_turf_algae.txt", "brown_algae.txt", "coral_sand.txt",
                  "green_algae.txt", "red_algae.txt"]

    values = []
    default = "dummyR.bot"

    def __init__(self, value):
        #print("value" + str(value))
        if type(value) is list:
            for val in value:
                if val == "*":
                    for v in self.all_values:
                        self.values.append(v)
                else:
                    #print("val" + str(val))
                    self.values.append(val)
        else:
            print("else value" + str(value))
            self.values.append(value)


class Cdom:
    """
    Create new Cdom
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Chl:
    """
    Create new Chl
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Cloud:
    """
    Create new Cloud
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Depth:
    """
    Create new Depth
    """
    # 51 values predefined
    values = [0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28,
              0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58,
              0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88,
              0.90, 0.92, 0.94, 0.96, 0.98, 1.00]

    default = 8.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                if not val in self.values:
                    self.values.append(val)
        else:
            if not value in self.values:
                self.values.append(value)


class Ibotm:
    """
    Create new Ibotm
    """
    values = []
    default = 2.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Iop:
    """
    Create new Iop
    """
    values = []
    default = 0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Mineral:
    """
    Create new Mineral
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Rflbot:
    """
    Create new Rflbot
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Salinity:
    """
    Create new Salinity
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Suntheta:
    """
    Create new Suntheta
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Temp:
    """
    Create new Temp
    """
    values = []
    default = 15.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)


class Windspeed:
    """
    Create new Windspeed
    """
    values = []
    default = 0.0

    def __init__(self, value):
        if type(value) is list:
            for val in value:
                self.values.append(val)
        else:
            self.values.append(value)

