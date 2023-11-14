#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2023, Yunzhi Ma
# All rights reserved.

from gimpfu import *

def make_gold_foil_material(image, layer, width, height) :
    ''' Inverts the colors of the selected layer.
    
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    # bg layer n set some color
    image=pdb.gimp_image_new(width,height,RGB)
    layer = gimp.Layer(image, "BG", width, height, RGB_IMAGE, 100, NORMAL_MODE)
    image.add_layer(layer)
    pdb.gimp_edit_fill(layer, 0)

    # make a new layer
    drawable = gimp.Layer(image, layer.name + "# 1", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    pdb.gimp_image_insert_layer(image, drawable, None, -1)
    pdb.plug_in_solid_noise(image, drawable, False, False, 99, 15, 4, 4)
    pdb.plug_in_edge(image, drawable, 2, 2, 0)
    pdb.gimp_drawable_invert(drawable, False)
    pdb.gimp_layer_set_opacity(drawable, 60)

    # make a new layer
    drawable = gimp.Layer(image, layer.name + "# 2", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
    pdb.gimp_image_insert_layer(image, drawable, None, -1)
    pdb.plug_in_solid_noise(image, drawable, False, False, 99, 15, 4, 4)
    pdb.script_fu_difference_clouds(image, drawable)
    drawable=image.active_layer
    pdb.gimp_drawable_equalize(drawable, False)
    pdb.gimp_drawable_levels(drawable, 0, 0, 1, True, 5, 0, 1, True)
    pdb.gimp_layer_set_mode(drawable, 31)

register(
    "python_fu_material_gold_foil",
    "Gold foil Material",
    "Create a gold material",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2023",
    "<Image>/Filters/Material/Gold foil",
    "*",
    [
        (PF_INT, "width", "Image width", 1000, ""),
        (PF_INT, "height", "Image height" , 1000, "")
    ],
    [],
    make_gold_foil_material)

main()