#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2023, Yunzhi Ma
# All rights reserved.

from gimpfu import *
import json

PLUGIN_PATH = r"C:\Users\yunzh\AppData\Roaming\GIMP\2.10\plug-ins"
PATH = r"C:\Users\yunzh\OneDrive\Documents\Blender\Textures"

def load_config():
    #gimp.message("00")
    f=open(PLUGIN_PATH+r"\config_golden_text.json", "r")
    #gimp.message("11")
    data = json.load(f)
    f.close()
    #gimp.message("22")
    return data

def nft_golden_hanzi(img, lyer) :
    ''' Inverts the colors of the selected layer.
    
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    config = load_config()
    #gimp.message(json.dumps(config))
    
    # bg layer n set some color
    texturePath = PATH+config["BgTexture"]
    image = pdb.file_jpeg_load(texturePath,texturePath)
    display = pdb.gimp_display_new(image)

    layer = pdb.gimp_file_load_layer(image, PATH+config["FgTexture"])
    pdb.gimp_image_insert_layer(image, layer, None, -1)

    mask=pdb.gimp_layer_create_mask(layer, 0)
    pdb.gimp_layer_add_mask(layer, mask)


    num_vectors, vectors_ids = pdb.gimp_vectors_import_from_file(image, config["SvgFile"], True, 1)
    vectors = pdb.gimp_image_get_vectors_by_name(image, 'Imported Path')
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_context_set_foreground(gimpcolor.RGB(0,0,0))
    pdb.gimp_edit_bucket_fill(mask, 0, 28, 100, 255, False, 0, 0)
    pdb.gimp_selection_none(image)
    


    #m=pdb.file_png_load(r"C:\Users\yunzh\Downloads\Hanzi\3500\char-1-0.png","")
    #non_empty = pdb.gimp_edit_copy(m.active_layer)
    #floating_sel = pdb.gimp_edit_paste(mask, False)
    #pdb.gimp_drawable_invert(floating_sel, False)
    #floating_sel = pdb.gimp_item_transform_scale(floating_sel, 0, 0, 3200, 3200)
    #pdb.gimp_floating_sel_anchor(floating_sel)

register(
    "python_fu_hft_hanzi_golden",
    "Golden hanzi NFT",
    "Create NFT with golden Hanzi text",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2023",
    "<Image>/Filters/NFT/Golden Text",
    "*",
    [],
    [],
    nft_golden_hanzi)

main()