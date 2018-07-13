import datetime
import json
import random
import sys
import os
import numpy
import itertools
import os.path
from configparser import ConfigParser
import subprocess


class Utility:
    process = None
    variables = {}
    ibotm_flag = 0
    config = ConfigParser()
    config.read("csic/icm/monocle/app/properties/properties.ini")
    date_now = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    current_directory = os.getcwd()
    return_code = 1
    name = "name: "
    cloud = "cloud: "
    suntheta = "suntheta: "
    depth = "depth: "
    chl = "chl: "
    cdom = "cdom: "
    mineral = "mineral: "
    bottom = "bottom: "
    temp = "temp: "
    salinity = "salinity: "
    windspd = "windspeed: "

    @staticmethod
    def check_values(param):
        """
        Check values from line in configuration file. It comes in a list or in a range of values
        :param param: list of values or range of values
        :return: list of values
        """
        values = param.split("=")[1]

        # if is a list of values (1 or more values)
        if "[" and "]" in values:
            values_list = values.replace('[', '').replace(']', '').split()
            values_list = list(map(float, values_list))
        # if is an string value
        elif '"' in values:
            values_list = values.replace('"', '').split()
        # if is a range of values. We process min, max and interval values to not exceed max values
        elif len(values.split()) == 3:
            values_list = list(map(float, values.split()))
            min = values_list[0]
            max = values_list[1]
            step = values_list[2]
            if (max / step).is_integer():
                values_list = list(numpy.arange(min, max + step, step).
                                   round(2))
                last_value = values_list[len(values_list) - 1]
                last_position = len(values_list) - 1
                if last_value > max:
                    values_list.pop(last_position)
            else:
                values_list = list(numpy.arange(min, max, step).round(2))
        else:
            print("incorrect value in config.txt")
            values_list = []

        return values_list

    @staticmethod
    def qc_range_values(values, variable):
        """
        Quality control for every variable. If values are out of range print message
        :param values: values list
        :param variable: name of variable
        :return: true if it is within range, false if it is out of range
        """
        if variable == "iop":
            try:
                if values[0] < 0 or values[0] > 1:
                    print("iop index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("iop without values")
                return False

        if variable == "zetanom":
            try:
                if values[0] < 0:
                    print("zetanom index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("zetanom without values")
                return False

        if variable == "chl":
            try:
                if values[0] < 0:
                    print("chl index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("chl without values")
                return False

        if variable == "cdom":
            try:
                if values[0] < 0:
                    print("cdom index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("cdom without values")
                return False

        if variable == "mineral":
            try:
                if values[0] < 0:
                    print("mineral index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("mineral without values")
                return False

        if variable == "ibotm":
            try:
                if not values[0].is_integer() or values[0] < 0 or values[0] > 2:
                    print("ibotm index out of range")
                    return False
                else:
                    Utility.ibotm_flag = values[0]
                    return True
            except IndexError:
                print("ibotm without values")
                return False

        if variable == "rflbot":
            try:
                if values[0] < 0 or values[len(values) - 1] > 1:
                    print("rflbot index out of range")
                    return False
                else:
                    if Utility.ibotm_flag != 1.0:
                        return False
                    else:
                        return True
            except IndexError:
                print("rflbot without values")
                return False

        if variable == "RbottomFile":
            try:
                if values[0] == "*":
                    if Utility.ibotm_flag != 2.0:
                        return False
                    return True
                else:
                    bottom_list = Utility.config.get('BOTTOM', 'bottom_list')
                    bottoms = json.loads(bottom_list)
                    for word in bottoms:
                        if word in values:
                            if Utility.ibotm_flag != 2.0:
                                return False
                            return True
                    print("RbottomFile file not found")
                    return False
            except IndexError:
                print("RbottomFile without values")
                return False

        if variable == "windspd":
            try:
                if values[0] < 0:
                    print("windspd index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("windspd without values")
                return False

        if variable == "temp":
            try:
                if values[0] < 0 or values[len(values) - 1] > 40:
                    print("temp index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("temp without values")
                return False

        if variable == "salinity":
            try:
                if values[0] < 0 or values[len(values) - 1] > 100:
                    print("salinity index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("salinity without values")
                return False

        if variable == "cloud":
            try:
                if values[0] < 0 or values[len(values) - 1] > 1:
                    print("cloud index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("cloud without values")
                return False

        if variable == "suntheta":
            try:
                if values[0] < 0 or values[len(values) - 1] > 90:
                    print("suntheta index out of range")
                    return False
                else:
                    return True
            except IndexError:
                print("suntheta without values")
                return False

    @staticmethod
    def read_config_file():
        """
        Read configuration file
        Set model with config file values
        :return:
        """
        file_name = ""
        arguments = len(sys.argv) - 1

        if arguments:
            for i in range(len(sys.argv)):
                name = sys.argv[i]
                file_name = os.path.splitext(name)[0]
                if file_name == "chl":
                    # todo import chl file if we want heterogeneus concentration
                    print("chl")
                if file_name == "cdom":
                    # todo import cdom file if we want heterogeneus concentration
                    print("cdom")
                if file_name == "mineral":
                    # todo import mineral file if we want heterogeneus concentration
                    print("mineral")
            config_filename = sys.argv[1]

            if config_filename == "config.txt":
                with open(config_filename, 'r') as file:
                    for line in file:
                        if not line.startswith("#"):

                            if line.startswith("iop"):
                                iop = Utility.check_values(line)
                                if Utility.qc_range_values(iop, "iop"):
                                    Utility.variables["iop"] = iop
                                else:
                                    Utility.variables["iop"] = [0.0]

                            if line.startswith("zetanom"):
                                zetanom = Utility.check_values(line)
                                if len(zetanom) > 49:
                                    print("zetanom over 100 depth")
                                    Utility.variables["zetanom"] = [0.0]
                                # elif zetanom[0] != 0.0:
                                #     print("zetanom[0] not 0.0")
                                elif Utility.qc_range_values(zetanom, "zetanom"):
                                    Utility.variables["zetanom"] = zetanom
                                else:
                                    Utility.variables["zetanom"] = [0.0]

                            if line.startswith("chl"):
                                chl = Utility.check_values(line)
                                if Utility.qc_range_values(chl, "chl"):
                                    Utility.variables["chl"] = chl
                                else:
                                    Utility.variables["chl"] = [0.0]

                            if line.startswith("cdom"):
                                cdom = Utility.check_values(line)
                                if Utility.qc_range_values(cdom, "cdom"):
                                    Utility.variables["cdom"] = cdom
                                else:
                                    Utility.variables["cdom"] = [0.0]

                            if line.startswith("mineral"):
                                mineral = Utility.check_values(line)
                                if Utility.qc_range_values(mineral, "mineral"):
                                    Utility.variables["mineral"] = mineral
                                else:
                                    Utility.variables["mineral"] = [0.0]

                            if line.startswith("ibotm"):
                                ibotm = Utility.check_values(line)
                                if Utility.qc_range_values(ibotm, "ibotm"):
                                    Utility.variables["ibotm"] = ibotm
                                else:
                                    Utility.variables["ibotm"] = [0.0]

                            if line.startswith("rflbot"):
                                rflbot = Utility.check_values(line)
                                if Utility.qc_range_values(rflbot, "rflbot"):
                                    Utility.variables["rflbot"] = rflbot
                                else:
                                    Utility.variables["rflbot"] = [0.0]

                            if line.startswith("RbottomFile"):
                                rbottomFile = Utility.check_values(line)
                                if Utility.qc_range_values(rbottomFile, "RbottomFile"):
                                    #print("rbottomFile" + str(rbottomFile))
                                    Utility.variables["rbottomFile"] = rbottomFile
                                else:
                                    Utility.variables["rbottomFile"] = ["dummyR.bot"]

                            if line.startswith("windspd"):
                                windspd = Utility.check_values(line)
                                if Utility.qc_range_values(windspd, "windspd"):
                                    Utility.variables["windspd"] = windspd
                                else:
                                    Utility.variables["windspd"] = [0.0]

                            if line.startswith("temp"):
                                temp = Utility.check_values(line)
                                if Utility.qc_range_values(temp, "temp"):
                                    Utility.variables["temp"] = temp
                                else:
                                    Utility.variables["temp"] = [5.0]

                            if line.startswith("salinity"):
                                salinity = Utility.check_values(line)
                                if Utility.qc_range_values(salinity, "salinity"):
                                    Utility.variables["salinity"] = salinity
                                else:
                                    Utility.variables["salinity"] = [0.0]

                            if line.startswith("cloud"):
                                cloud = Utility.check_values(line)
                                if Utility.qc_range_values(cloud, "cloud"):
                                    Utility.variables["cloud"] = cloud
                                else:
                                    Utility.variables["cloud"] = [0.0]

                            if line.startswith("suntheta"):
                                suntheta = Utility.check_values(line)
                                if Utility.qc_range_values(suntheta, "suntheta"):
                                    Utility.variables["suntheta"] = suntheta
                                else:
                                    Utility.variables["suntheta"] = [0.0]
            else:
                print("config.txt not found")
        else:
            print("no configuration file")

    @staticmethod
    def iterate_variables(bottom, depth, chl, cdom, mineral, cloud, suntheta, windspeed, temp, salinity):
        """
        Iterate variables as a cartesian product
        Only iterate Depth from 1m to final
        Create file name list
        :return:
        """
        lakes = []
        depth_to_iterate = depth[51:]
        i = 0
        # 0 = bottom
        # 1 = depth
        # 2 = chl
        # 3 = cdom
        # 4 = mineral
        # 5 = cloud
        # 6 = suntheta
        # 7 = windspeed
        # 8 = temp
        # 9 = salinity
        for r in itertools.product(bottom, depth_to_iterate, chl, cdom, mineral, cloud, suntheta, windspeed, temp,
                                   salinity):
            i += 1
            path = os.path.join(Utility.date_now,
                                'bottom_' + str(r[0]),
                                'depth_' + str(r[1]),
                                'chl_' + str(r[2]),
                                'cdom_' + str(r[3]),
                                'mineral_' + str(r[4]),
                                'cloud_' + str(r[5]),
                                'suntheta_' + str(r[6]),
                                'windspeed_' + str(r[7]),
                                'temp_' + str(r[8]),
                                'salinity_' + str(r[9]))
            lake = [i, path, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]]
            lakes.append(lake)
        print(i)
        return lakes

    @staticmethod
    def iterate_variables_apply_random_to_variables(bottom, depth, chl, cdom, mineral, cloud, suntheta, windspeed, temp, salinity):
        """
        Iterate variables as a cartesian product
        Only iterate Depth from 1m to final
        Create file name list
        :return:
        """
        lakes = []
        depth_to_iterate = depth[51:]
        i = 0
        # 0 = bottom
        # 1 = depth
        # 2 = chl
        # 3 = cdom
        # 4 = mineral
        # 5 = cloud
        # 6 = suntheta
        # 7 = windspeed
        # 8 = temp
        # 9 = salinity
        for r in itertools.product(bottom, depth_to_iterate, chl, cdom, mineral, cloud, suntheta, windspeed, temp,
                                   salinity):
            chl = random.uniform((float(r[2]) * 0.90), (float(r[2]) * 1.10))
            cdom = random.uniform((float(r[3]) * 0.90), (float(r[3]) * 1.10))
            mineral = random.uniform((float(r[4]) * 0.90), (float(r[4]) * 1.10))

            i += 1
            path = os.path.join(Utility.date_now,
                                'bottom_' + str(r[0]),
                                'depth_' + str(r[1]),
                                'chl_' + str(chl),
                                'cdom_' + str(cdom),
                                'mineral_' + str(mineral),
                                'cloud_' + str(r[5]),
                                'suntheta_' + str(r[6]),
                                'windspeed_' + str(r[7]),
                                'temp_' + str(r[8]),
                                'salinity_' + str(r[9]))
            lake = [i, path, r[0], r[1], chl, cdom, mineral, r[5], r[6], r[7], r[8], r[9]]
            lakes.append(lake)
        print(i)
        return lakes

    @staticmethod
    def record1_default_parameters(file):
        # contains: icompile, Parmin, Parmax, PhiChl, Raman0, RamanXS, iDynZ, RamanExp
        file.write("0, 400, 700, 0.02, 488, 0.00026, 1, 5.3")
        file.write("\n")

    @staticmethod
    def record2_run_title(file, ititle):
        # contains: ititle
        file.write(ititle)
        file.write("\n")

    @staticmethod
    def record3_rootname(file, rootname):
        # contains: rootname
        file.write(rootname)
        file.write("\n")

    @staticmethod
    def record4a_output_options(file):
        # contains: iOptPrnt, iOptDigital, iOptExcelS, iOptExcelM, iOptRad, nwskip
        file.write("0,0,0,0,0,1")
        file.write("\n")

    @staticmethod
    def record4b_model_options(file):
        # contains: iIOPmodel, iSkyRadModel, iSkyIrradModel, iChl, iCDOM
        file.write("2,1,0,2,3")
        file.write("\n")

    @staticmethod
    def record5a_number_of_components(file):
        # contains: ncomp, nconc
        file.write("4,4")
        file.write("\n")

    @staticmethod
    def record5b_component_concentrations(file, chl, cdom, mineral):
        # contains: compconc(j), j = 1, nconc
        file.write("0, " + str(chl) + ", " + str(cdom) + ", " + str(mineral))
        file.write("\n")

    @staticmethod
    def record5c_specific_absortion_parameters(file):
        # contains: iastropt(i), astarRef(i), astar0(i), asgamma(i)
        file.write("0, 0, 440, 0.1, 0.014")
        file.write("\n")
        file.write("0, 0, 440, 0.1, 0.014")
        file.write("\n")
        file.write("0, 0, 440, 0.2, 0.014")
        file.write("\n")
        file.write("0, 0, 440, 0.1, 0.014")
        file.write("\n")

    @staticmethod
    def record5d_specific_absorption_data_file_names(file):
        # contains: astarfile(i)
        file.write(r"C:\HE52\data\H2OabDefaults_FRESHwater.txt")
        file.write("\n")
        file.write(r"C:\HE52\data\examples\astarchl.txt")
        file.write("\n")
        file.write(r"C:\HE52\data\examples\a_CDOMz.txt")
        file.write("\n")
        file.write(r"C:\HE52\data\defaults\astarmin_average.txt")
        file.write("\n")

    @staticmethod
    def record5e_specific_scattering_parameters(file):
        # contains: ibstropt(i), bstarRef(i), bstar0(i), coef1, coef2, coef3
        file.write("0, -999, -999, -999, -999, -999")
        file.write("\n")
        file.write("2, 550, 0.3, -0.001126, 1.62517, 0.62")
        file.write("\n")
        file.write("-1, -999, 0, -999, -999, -999")
        file.write("\n")
        file.write("0, -999, -999, -999, -999, -999")
        file.write("\n")

    @staticmethod
    def record5f_specific_scattering_data_file_names(file):
        # contains: bstarfile(i)
        file.write("bstarDummy.txt")
        file.write("\n")
        file.write("dummybstar.txt")
        file.write("\n")
        file.write("dummybstar.txt")
        file.write("\n")
        file.write(r"C:\HE52\data\defaults\bstarmin_average.txt")
        file.write("\n")

    @staticmethod
    def record5g_type_of_concentrations_and_phase_functions(file):
        # contains: itype(i), ibbopt(i), bbfrac(i), BfrefPL(i), Bf0PL(i), BfmPL(i)
        file.write("0, 0, 550, 0.01, 0")
        file.write("\n")
        file.write("1, 0, 0, 0, 0")
        file.write("\n")
        file.write("0, 0, 0, 0, 0")
        file.write("\n")
        file.write("3, 0, 550, 0.03, 0.5")
        file.write("\n")

    @staticmethod
    def record5h_phase_function_file_names(file):
        # contains: pfname(1) to pfname(ncomp)
        file.write("pureh2o.dpf")
        file.write("\n")
        file.write("isotrop.dpf")
        file.write("\n")
        file.write("isotrop.dpf")
        file.write("\n")
        file.write("isotrop.dpf")
        file.write("\n")

    @staticmethod
    def record6_wavelengths(file):
        # contains: nwave. if nwave = 0 -> wavel, areset, breset. if nwave >=1 -> waveb(1), waveb(2)... wabev(nwave+1)
        file.write("89")
        file.write("\n")
        file.write("350, 355, 360, 365, 370, 375, 380, 385, 390, 395,")
        file.write("\n")
        file.write("400, 405, 410, 415, 420, 425, 430, 435, 440, 445,")
        file.write("\n")
        file.write("450, 455, 460, 465, 470, 475, 480, 485, 490, 495,")
        file.write("\n")
        file.write("500, 505, 510, 515, 520, 525, 530, 535, 540, 545,")
        file.write("\n")
        file.write("550, 555, 560, 565, 570, 575, 580, 585, 590, 595,")
        file.write("\n")
        file.write("600, 605, 610, 615, 620, 625, 630, 635, 640, 645,")
        file.write("\n")
        file.write("650, 655, 660, 665, 670, 675, 680, 685, 690, 695,")
        file.write("\n")
        file.write("700, 705, 710, 715, 720, 725, 730, 735, 740, 745,")
        file.write("\n")
        file.write("750, 755, 760, 765, 770, 775, 780, 785, 790, 795,")
        file.write("\n")


    @staticmethod
    def record7_inelastic_scattering_and_internal_sources(file):
        # contains: ibiolum, ichlfl, icdomfl, iraman, icompchl
        file.write("0,1,1,1,2")
        file.write("\n")

    @staticmethod
    def record8a_sky_model_parameters(file, suntheta, cloud):
        # contains: iflagsky, nsky, skydata(1), skydata(2), ..., skydata(nsky)
        file.write("2, 3, " + str(suntheta) + ", 0, " + str(cloud))
        file.write("\n")

    @staticmethod
    def record8b_atmospheric_conditions(file):
        # contains: jday, rlat, rlon, pres, am, rh, wv, vi, wsm, ro3
        file.write("-1, 0, 0, 29.92, 1, 80, 2.5, 15, 3.99618, 300")
        file.write("\n")

    @staticmethod
    def record9_surface_information(file, windspd, temp, salinity):
        # contains: windspd, refr, temp, salinity
        file.write(str(windspd) + ", -1.34, " + str(temp) + ", " + str(salinity))
        file.write("\n")

    @staticmethod
    def record10_bottom_reflectance(file):
        # contains: ibotm, rflbot
        file.write("0, 0")
        file.write("\n")

    @staticmethod
    def record11_output_depths(file, iop, depth):
        # contains: iop, nznom, zetanom(1), zetanom(2), ..., zetanom(nznom)
        nznom = len(depth)
        depth_string = str(depth)
        format_depth_string = ""

        if iop == 0.0:
            iop = 0
        elif iop == 1.0:
            iop = 1

        if "[" and "]" in depth_string:
            format_depth_string = depth_string.replace('[', '').replace(']', '')

        file.write(str(iop) + ", " + str(nznom) + ", " + format_depth_string)
        file.write("\n")

    @staticmethod
    def record12_data_files(file, bottom):
        # contains: PureWaterDataFile, nac9Files, ac9DataFile, Ac9FilteredDataFile, HydroScatDataFile, ChlzDataFile,
        # CDOMDataFile, RbottomFile, TxtDataFile(i) for i = 1 to ncomp, IrradDataFile, S0biolumFile
        file.write(r"C:\HE52\data\H2OabDefaults_FRESHwater.txt")
        file.write("\n")
        file.write("1")
        file.write("\n")
        file.write("dummyac9.txt")
        file.write("\n")
        file.write("dummyFilteredAc9.txt")
        file.write("\n")
        file.write("dummyHscat.txt")
        file.write("\n")
        file.write("dummyComp.txt")
        file.write("\n")
        file.write("dummyComp.txt")
        file.write("\n")
        file.write(str(bottom))
        file.write("\n")
        file.write("dummydata.txt")
        file.write("\n")
        file.write("dummyCompChl.txt")
        file.write("\n")
        file.write("dummyCompCDOM.txt")
        file.write("\n")
        file.write("dummyCompMineral.txt")
        file.write("\n")
        file.write("DummyIrrad.txt")
        file.write("\n")
        file.write(r"..\data\MyBiolumData.txt")
        file.write("\n")

    @staticmethod
    def create_index(lake, path):
        """
        Create index.html with info from all the lakes we have created
        :return:
        """
        message = """
                <html>
                    <head>
                    </head>
                        <body>
                        <table border="1">
                            <th>name</th>
                            <th>Cloud</th>
                            <th>Suntheta</th>
                            <th>Depth</th>
                            <th>Chl</th>
                            <th>CDOM</th>
                            <th>Mineral</th>
                            <th>Bottom</th>
                            <th>Temp</th>
                            <th>Salinity</th>
                            <th>Windspeed</th>  
                        """
        name = str(lake.name)
        cloud = str(lake.cloud)
        suntheta = str(lake.suntheta)
        depth = str(lake.depth)
        chl = str(lake.chl)
        cdom = str(lake.cdom)
        mineral = str(lake.mineral)
        bottom = str(lake.bottom)
        temp = str(lake.temp)
        salinity = str(lake.salinity)
        windspd = str(lake.windspeed)

        # <td><a href=file:///""" + Utility.current_directory + """/""" + lake.pathname + """/""" + lake.name \
        #    + """>""" + name + """

        message += """
                <tr>

                <td><a href=file:///""" + Utility.current_directory + """/""" + lake.pathname + """/""" + \
                   lake.input_filename + """>""" + name + """
                </a></td>
                <td>""" + cloud + """
                </td>
                <td>""" + suntheta + """
                </td>
                <td>""" + depth + """
                </td>
                <td>""" + chl + """
                </td>
                <td>""" + cdom + """
                </td>
                <td>""" + mineral + """
                </td>
                <td>""" + bottom + """
                </td>
                <td>""" + temp + """
                </td>
                <td>""" + salinity + """
                </td>
                <td>""" + windspd + """
                </td>

                </tr>
                """
        message += """
                </table>
                </body>
        </html>"""

        with open(path + "/index.html", 'a') as file:
            file.write(message)

    @staticmethod
    def setup_readme(lake):
        """"
        Set up Utility variables with lake values: name, pathname, bottom, depth, chl, cdom, mineral, cloud, suntheta,
        windspeed, temp, salinity
        :param lake:
        :return:
        """
        # depth, chl, cdom, mineral, bottom, temp, salinity, windspd = ""
        message = ""
        Utility.name += str(lake.name) + ", "

        if not (str(lake.cloud) in Utility.cloud):
            Utility.cloud += str(lake.cloud) + ", "
        if not (str(lake.suntheta) in Utility.suntheta):
            Utility.suntheta += str(lake.suntheta) + ", "
        if not (str(lake.depth) in Utility.depth):
            Utility.depth += str(lake.depth) + ", "
        if not (str(lake.chl) in Utility.chl):
            Utility.chl += str(lake.chl) + ", "
        if not (str(lake.cdom) in Utility.cdom):
            Utility.cdom += str(lake.cdom) + ", "
        if not (str(lake.mineral) in Utility.mineral):
            Utility.mineral += str(lake.mineral) + ", "
        if not (str(lake.bottom) in Utility.bottom):
            Utility.bottom += str(lake.bottom) + ", "
        if not (str(lake.temp) in Utility.temp):
            Utility.temp += str(lake.temp) + ", "
        if not (str(lake.salinity) in Utility.salinity):
            Utility.salinity += str(lake.salinity) + ", "
        if not (str(lake.windspeed) in Utility.windspd):
            Utility.windspd += str(lake.windspeed) + ", "

    @staticmethod
    def create_readme(path, Lake):
        with open(path + "/readme.md", 'a') as file:
            file.write("Numero de llacs: " + str(len(Lake.values)) + "\n")
            file.write(Utility.name + "\n")
            file.write(Utility.cloud + "\n")
            file.write(Utility.suntheta + "\n")
            file.write(Utility.depth + "\n")
            file.write(Utility.chl + "\n")
            file.write(Utility.cdom + "\n")
            file.write(Utility.mineral + "\n")
            file.write(Utility.bottom + "\n")
            file.write(Utility.temp + "\n")
            file.write(Utility.salinity + "\n")
            file.write(Utility.windspd + "\n")

    @staticmethod
    def copy_input_file(input_file, input_file_hydrolight):
        with open(input_file, 'r') as file:
            content = file.read()
        os.chdir(r'C:\HE52\run\batch')
        with open(input_file_hydrolight, 'w') as file:
            file.write(content)
        # try:
        #     os.remove(input_file_hydrolight)
        # except OSError:
        #     pass
        os.chdir(Utility.current_directory)

    @staticmethod
    def run_process(process):
        """
        Run subprocess EcoEcli(Ecolight) with files in runlist.txt
        :return:
        """
        Utility.process = process
        os.chdir(r'C:\HE52\run')

        if process == "1":
            proc = subprocess.Popen([os.getcwd() + r'\runHL'])
            stdoutdata, stderrdata = proc.communicate()
            Utility.return_code = proc.returncode
            os.chdir(Utility.current_directory)
        if process == "2":
            proc = subprocess.Popen([os.getcwd() + r'\runEL'])
            stdoutdata, stderrdata = proc.communicate()
            Utility.return_code = proc.returncode
            os.chdir(Utility.current_directory)



    @staticmethod
    def get_output_file(output_file_name):
        content = ""
        try:
            os.chdir(r'C:\HE52\output\Ecolight\printout')
            # when process is finished, self.return_code = 0
            if not Utility.return_code:
                if os.path.isfile(output_file_name):
                    with open(output_file_name, 'r') as file:
                        content = file.read()

                else:
                    raise ValueError("%s isn't a file!" % output_file_name)
        except OSError:
            pass

        os.chdir(Utility.current_directory)

        return content

    @staticmethod
    def delete_files(input_file_hydrolight, output_file_hydrolight):
        os.chdir(r'C:\HE52\run\batch')
        try:
            os.remove(input_file_hydrolight)
        except OSError:
            pass
        os.chdir(r'C:\HE52\output\Ecolight\printout')
        try:
            os.remove(output_file_hydrolight)
        except OSError:
            pass
        os.chdir(Utility.current_directory)

    @staticmethod
    def get_json_lake(lake, input, output):
        post = {"name": lake.name,
                "input_filename": lake.input_filename,
                "output_filename": lake.output_filename,
                "pathname": lake.pathname,
                "root": lake.root,
                "abs_path": lake.abs_path,
                "bottom": lake.bottom,
                "depth": lake.depth,
                "chl": lake.chl,
                "cdom": lake.cdom,
                "mineral": lake.mineral,
                "cloud": lake.cloud,
                "suntheta": lake.suntheta,
                "windspeed": lake.windspeed,
                "temp": lake.temp,
                "salinity": lake.salinity,
                "iop": lake.iop,
                "input": input,
                "output": output,
                }

        return post




