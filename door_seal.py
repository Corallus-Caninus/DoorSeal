from solid import *
from solid.utils import *
from math import asin, atan, pi, cos, sin, sqrt, tan, acos
import toml
import os

eps = 1  # epsilon for hollow cone artifacts

"""a nozzle on either end of a hollow cylinder to couple two hoses of different diameter"""


#OBJECT PARAMETERS#
wall_thickness = 2
def DoorSeal(
    number_fins,
    module_length,
    door_height,
    door_overlap_height,
    door_width,
    fin_thickness,
    wall_thickness,
):
    # create cube of wall thickness and door_heightxmodule_length
    outer_overlap = cube(
        [module_length, wall_thickness, door_overlap_height],center=True)
    inner_overlap = cube(
        [module_length, wall_thickness, door_overlap_height],center=True)
    #move the inner and outer away by door_width/2
    outer_overlap = translate([0,door_width/2+wall_thickness/2,0])(outer_overlap)
    inner_overlap = translate([0,-door_width/2-wall_thickness/2,0])(inner_overlap)
    # move them up to the xy plane
    outer_overlap = translate([0,0,door_overlap_height/2])(outer_overlap)
    inner_overlap = translate([0,0,door_overlap_height/2])(inner_overlap)
    # join the two cubes by a cube of module_lengthxdoor_widthxwall_thickness
    overlap = cube(
        [module_length, door_width+wall_thickness, wall_thickness],center=True)
    overlap = translate([0,0,wall_thickness/2])(overlap)

    # create a small cube inside to allow modules to be connected
    coupler = cube(
        [module_length, wall_thickness,door_overlap_height],center=True)
    # move the coupler to the xy plane
    coupler = translate([0,0,door_overlap_height/2])(coupler)
    # move coupler module_length/4 along x axis
    coupler = translate([module_length/2,0,0])(coupler)
    # set one on either end
    outer_coupler = translate([0,door_width/2 + 1.5*wall_thickness,0])(coupler)
    inner_coupler = translate([0,-door_width/2 - 1.5*wall_thickness,0])(coupler)


    # create the fins
    fin = cube(
        [module_length, fin_thickness, door_height],center=True)
        # move fin to under the xy plane
    fin = translate([0,0,-door_height/2])(fin)
    # move fins back by door_width/2
    fin = translate([0,-door_width/2,0])(fin)
    fins = []
    # we are going to place the fins evenly along the y axis which is door_width/number_fins
    fin_spacing = door_width / number_fins
    # center fin given the fin_spacing
    fin = translate([0,fin_spacing/2,0])(fin)
    for i in range(number_fins):
        cur_fin = translate([0,i*fin_spacing,0])(fin)
        fins.append(cur_fin)

    door_seal = outer_overlap + inner_overlap + overlap + outer_coupler + inner_coupler
    for fin in fins:
        door_seal += fin
    # also create door_seal_end without coupler
    door_seal_end = outer_overlap + inner_overlap + overlap
    for fin in fins:
        door_seal_end += fin


    return door_seal, door_seal_end


def render_object(render_object, filename):
    """
    creates a .stl and .scad solution for the given solidpython OpenSCAD object
    PARAMETERS:
        render_object: the OpenSCAD object
        filename: a string for the file to be saved
    """
    scad_render_to_file(render_object, filename + ".scad", file_header="$fn=200;")
    # render with OpenSCAD
    print("Openscad is now rendering the solution..")
    os.system("openscad -o " + filename + ".stl " + filename + ".scad &")


if __name__ == "__main__":
    config = toml.load("configuration.toml")
    door_seal, door_seal_end = DoorSeal(**config)
    render_object(door_seal, "door_seal")
    render_object(door_seal_end, "door_seal_end")
