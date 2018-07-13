import os
from pathlib import Path

from csic.icm.monocle.app.model.variable import Iop


class Lake:
    """
    Create new Lake
    """
    values = []
    name = ""
    input_filename = ""
    output_filename = ""
    pathname = ""
    root = ""
    abs_path = ""
    bottom = ""
    depth = ""
    chl = ""
    cdom = ""
    mineral = ""
    cloud = ""
    suntheta = ""
    windspeed = ""
    temp = ""
    salinity = ""
    iop = ""
    current_directory = os.getcwd()

    def __init__(self, name, pathname, bottom, depth, chl, cdom, mineral, cloud, suntheta, windspeed, temp,
                 salinity):
        self.name = name
        self.input_filename = "I" + name + ".txt"
        self.output_filename = "P" + name + ".txt"
        self.pathname = pathname
        p = Path(self.pathname)
        self.root = (p.parts[0])
        self.abs_path = os.path.join(self.current_directory, self.pathname)
        self.bottom = bottom
        self.depth = depth
        self.chl = chl
        self.cdom = cdom
        self.mineral = mineral
        self.cloud = cloud
        self.suntheta = suntheta
        self.windspeed = windspeed
        self.temp = temp
        self.salinity = salinity
        self.iop = Iop.values[0]
