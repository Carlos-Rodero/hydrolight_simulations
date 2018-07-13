# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:00:00 2018

@author: Carlos Rodero García

Multi-spectral Case 2 water simulation.

"""
import os
from pathlib import Path

from csic.icm.monocle.app.model.lake import Lake
from csic.icm.monocle.app.model.variable import Bottom, Cdom, Chl, Cloud, Depth, Ibotm, Iop, Mineral, Rflbot, Salinity, \
    Suntheta, Temp, Windspeed
from csic.icm.monocle.app.utility import Utility
from pymongo import MongoClient


def init_variables_classes():
    """
    Create Variables Class with values from configuration file
    If there are not data values, they come from a default class attribute
    :return:
    """
    try:
        Iop(Utility.variables["iop"])
    except KeyError:
        Iop(Iop.default)

    try:
        Depth(Utility.variables["zetanom"])
    except KeyError:
        Depth(Depth.default)

    try:
        Chl(Utility.variables["chl"])
    except KeyError:
        Chl(Chl.default)

    try:
        Cdom(Utility.variables["cdom"])
    except KeyError:
        Cdom(Cdom.default)

    try:
        Mineral(Utility.variables["mineral"])
    except KeyError:
        Mineral(Mineral.default)

    try:
        Ibotm(Utility.variables["ibotm"])
    except KeyError:
        Ibotm(Ibotm.default)

    try:
        Rflbot(Utility.variables["rflbot"])
    except KeyError:
        Rflbot(Rflbot.default)

    try:
        Bottom(Utility.variables["rbottomFile"])
    except KeyError:
        Bottom(Bottom.default)

    try:
        Windspeed(Utility.variables["windspd"])
    except KeyError:
        Windspeed(Windspeed.default)

    try:
        Temp(Utility.variables["temp"])
    except KeyError:
        Temp(Temp.default)

    try:
        Salinity(Utility.variables["salinity"])
    except KeyError:
        Salinity(Salinity.default)

    try:
        Cloud(Utility.variables["cloud"])
    except KeyError:
        Cloud(Cloud.default)

    try:
        Suntheta(Utility.variables["suntheta"])
    except KeyError:
        Suntheta(Suntheta.default)


def print_values():
    """
    Print model classes values
    :param values:
    :return:
    """
    print(Iop.values)
    print(Depth.values)
    print(Chl.values)
    print(Cdom.values)
    print(Mineral.values)
    print(Ibotm.values)
    print(Rflbot.values)
    print(Bottom.values)
    print(Windspeed.values)
    print(Temp.values)
    print(Salinity.values)
    print(Cloud.values)
    print(Suntheta.values)


def create_lake(lakes):
    """
    Create every lake object
    Previously we have to obtain default depth and add the last depth we have iterated
    :param lakes:
    :return:
    """
    for lake in lakes:
        index = Depth.values.index(lake[3])
        lake[3] = Depth.values[:index + 1]

    for lake in lakes:
        Lake.values.append(Lake(str(lake[0]), lake[1], lake[2], lake[3], lake[4], lake[5], lake[6], lake[7], lake[8],
                                lake[9], lake[10], lake[11]))


def reset_index_readme_file():
    """
    Reset index file
    :return:
    """
    for lake in Lake.values:
        if not os.path.exists(lake.pathname):
            os.makedirs(lake.pathname)
        path = os.path.join(lake.pathname, lake.name)
        path_list = path.split("\\")
        date = path_list[0]
        with open(str(date) + "/index.html", 'w') as file:
            file.write("")
        with open(str(date) + "/readme.md", 'w') as file:
            file.write("")


def create_input_files():
    """
    Start creating input files
    Create file '{{filename}}.txt' in 'HE52\run\batch' with input file content
    :return:
    """
    p = ""
    for lake in Lake.values:
        if not os.path.exists(lake.pathname):
            os.makedirs(lake.pathname)
        path = os.path.join(lake.pathname, lake.input_filename)
        with open(path, 'w') as file:
            file.write("")

        with open(path, 'a') as file:
            Utility.record1_default_parameters(file)
            Utility.record2_run_title(file, lake.name)
            Utility.record3_rootname(file, lake.name)
            Utility.record4a_output_options(file)
            Utility.record4b_model_options(file)
            Utility.record5a_number_of_components(file)
            Utility.record5b_component_concentrations(file, lake.chl, lake.cdom, lake.mineral)
            Utility.record5c_specific_absortion_parameters(file)
            Utility.record5d_specific_absorption_data_file_names(file)
            Utility.record5e_specific_scattering_parameters(file)
            Utility.record5f_specific_scattering_data_file_names(file)
            Utility.record5g_type_of_concentrations_and_phase_functions(file)
            Utility.record5h_phase_function_file_names(file)
            Utility.record6_wavelengths(file)
            Utility.record7_inelastic_scattering_and_internal_sources(file)
            Utility.record8a_sky_model_parameters(file, lake.suntheta, lake.cloud)
            Utility.record8b_atmospheric_conditions(file)
            Utility.record9_surface_information(file, lake.windspeed, lake.temp, lake.salinity)
            Utility.record10_bottom_reflectance(file)
            Utility.record11_output_depths(file, lake.iop, lake.depth)
            Utility.record12_data_files(file, lake.bottom)

            # start creating index.html for every lake
            p = Path(path)
            Utility.create_index(lake, p.parts[0])
            Utility.setup_readme(lake)

        Utility.copy_input_file(p, lake.input_filename)
    Utility.create_readme(p.parts[0], Lake)


def setup_runlist():
    """
    Set up runlist.txt in 'HE52\run' with name of input files
    :param path: path from last lake created
    :return:
    """
    os.chdir(r'C:\HE52\run')
    with open("runlist.txt", 'w') as f:
        f.write("")
    for lake in Lake.values:
        with open("runlist.txt", 'a') as f:
            f.write(lake.input_filename + "\n")
    os.chdir(Utility.current_directory)


def delete_files():
    for lake in Lake.values:
        Utility.delete_files(lake.input_filename, lake.output_filename)


def output_file():
    """
    Wait Hydrolight process to finish and read output file content
    :return:
    """
    for lake in Lake.values:
        content = Utility.get_output_file(lake.output_filename)

        output_path = os.path.join(lake.pathname, lake.output_filename)
        with open(output_path, 'w') as file:
            file.write(content)


def connect_mongodb(name_collection):
    """
    Add data to Mongo Database
    :return:
    """
    client = MongoClient('localhost', 27017)
    # client.drop_database('hydrolight')
    db = client['hydrolight']
    for lake in Lake.values:

        input_path = os.path.join(lake.pathname, lake.input_filename)
        with open(input_path, 'r') as file:
            input = file.read()

        output_path = os.path.join(lake.pathname, lake.output_filename)
        with open(output_path, 'r') as file:
            output = file.read()

        post = Utility.get_json_lake(lake, input, output)
        collection = db[name_collection]

        collection.insert_one(post)


if __name__ == "__main__":

    Utility.read_config_file()
    init_variables_classes()
    #print_values()
    #lakes = Utility.iterate_variables(Bottom.values, Depth.values, Chl.values, Cdom.values, Mineral.values,
    #                                  Cloud.values, Suntheta.values, Windspeed.values, Temp.values, Salinity.values)

    lakes = Utility.iterate_variables_apply_random_to_variables(Bottom.values, Depth.values, Chl.values, Cdom.values, Mineral.values,
                                      Cloud.values, Suntheta.values, Windspeed.values, Temp.values, Salinity.values)

    user_input = input("Continue Simulation? Yes or No\n")
    if (user_input == "Yes")or(user_input == "yes")or(user_input == "y")or (user_input == "Y"):
        while True:
            name_lake_input = input("Write name of collection in Database: \n")
            if (name_lake_input.strip() != ""):
                break
        while True:
            process_input = input("Run Hydrolight(1) or Ecolight(2)? \n")
            if (process_input == "1")or(process_input == "2"):
                break
        print("continue")

        create_lake(lakes)
        reset_index_readme_file()
        create_input_files()
        setup_runlist()

        Utility.run_process(process_input)

        output_file()
        delete_files()

        connect_mongodb(name_lake_input)

    else:
        print("exit")






