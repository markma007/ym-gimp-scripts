#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2023, Yunzhi Ma
# All rights reserved.

from gimpfu import *
import json, glob

PLUGIN_PATH = r"C:\Users\yunzh\AppData\Roaming\GIMP\2.10\plug-ins"
PATH = r"C:\Users\yunzh\OneDrive\Documents\Blender\Textures"

def load_config():
    #gimp.message("00")
    f=open(PLUGIN_PATH+"\\config\\config_text_carved_in.json", "r")
    #gimp.message("11")
    data = json.load(f)
    f.close()
    #gimp.message("22")
    return data

def nft_batch_carved_in_text(img, lyer) :
    ''' Inverts the colors of the selected layer.
    
    img : image The current image.
    layer : layer The layer of the image that is selected.
    '''
    config = load_config()
    ff = glob.glob(config["SvgPath"]+"svg\\*.svg")
    for f in ff:
        fout = f.replace("\\svg", "\\out")
        fout = fout.replace(".svg", ".jpg")
        do_job(config, f, fout)


black = gimpcolor.RGB(0,0,0)
white = gimpcolor.RGB(255,255,255)
carvedColor = gimpcolor.RGB(33,21,15) ## <--#21150f

def do_job(config, f, f2):

    ##### BG Layer
    fileName = config["WoodTexture"]
    if config["use"]=="marble":
        fileName = config["MarbleTexture"]
    texturePath = PATH+fileName
    image = pdb.file_jpeg_load(texturePath,texturePath)
    display = pdb.gimp_display_new(image)

    pdb.gimp_context_set_foreground(carvedColor)
    pdb.gimp_context_set_background(white)

    ##### Load text - import svg to vectors
    num_vectors, vectors_ids = pdb.gimp_vectors_import_from_file(image, f, True, True)
    vectors = pdb.gimp_image_get_vectors_by_name(image, 'Imported Path')

    ##### Pressed-In Layer
    edgeLayer = gimp.Layer(image, "Pressed In", image.width, image.height, 0, 100, 45) ##
    image.add_layer(edgeLayer, 0)
    pdb.gimp_layer_add_alpha(edgeLayer)
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_selection_invert(image)
    pdb.gimp_drawable_edit_clear(edgeLayer)
    pdb.gimp_selection_none(image)

    ##### Drop Shadow Layer
    prepLayer = gimp.Layer(image, "Drop Shadow Prep", image.width, image.height, 0, 100, 28) ##
    image.add_layer(prepLayer, 0)
    pdb.gimp_layer_add_alpha(prepLayer)
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_drawable_edit_clear(prepLayer)
    ## Drop Shadow
    pdb.gimp_selection_none(image)
    pdb.script_fu_drop_shadow(image, prepLayer, 36, 36, 14, black, 100, False)
    pdb.gimp_item_set_visible(prepLayer, False)
    ## cut the drop shadow layer
    shadow = pdb.gimp_image_get_layer_by_name(image, "Drop Shadow")
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_selection_invert(image)
    pdb.gimp_drawable_edit_clear(shadow)
    pdb.gimp_selection_none(image)

    ##### Edge Layer
    edgeLayer = gimp.Layer(image, "Edge", image.width, image.height, 0, 40, 45) ##
    image.add_layer(edgeLayer, 0)
    pdb.gimp_layer_add_alpha(edgeLayer)
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_selection_grow(image, 18)
    pdb.gimp_edit_bucket_fill(edgeLayer, 1, 28, 100, 255, False, 0, 0)
    pdb.gimp_selection_shrink(image, 18)
    pdb.gimp_drawable_edit_clear(edgeLayer)

    # ##### Clean up
    pdb.gimp_selection_none(image)

    ##### merge all layers to one and save
    layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
    ##### gmic Frame
    ##pdb.plug_in_gmic_qt(image, layer, 5, 0, "command")
    pdb.file_jpeg_save(image, layer, f2, f2, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)

    ##### close image here

register(
    "python_fu_hft_batch_text_carved_in",
    "Carved-in text NFT (batch)",
    "Batch create NFT with carved-in text",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2023",
    "<Image>/Filters/NFT/Batch Text Carved-In",
    "*",
    [],
    [],
    nft_batch_carved_in_text)

main()