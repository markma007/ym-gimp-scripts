#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2023, Yunzhi Ma
# All rights reserved.

from gimpfu import *
import json, glob
import random

PLUGIN_PATH = r"C:\Users\yunzh\AppData\Roaming\GIMP\2.10\plug-ins"
PATH = r"C:\Users\yunzh\OneDrive\Documents\Blender\Textures"

def load_config():
    #gimp.message("00")
    f=open(PLUGIN_PATH+"\\config\\config_text_chuanghua.json", "r")
    #gimp.message("11")
    data = json.load(f)
    f.close()
    #gimp.message("22")
    return data

def nft_batch_chuanghua_text(img, lyer) :
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

def do_job(config, f, f2):

    pdb.gimp_context_set_foreground(black)
    pdb.gimp_context_set_background(white)

    image=pdb.gimp_image_new(1080, 1080, RGB)
    pdb.gimp_display_new(image)

    ##### BG Layer
    BgLayer = gimp.Layer(image, "BG", image.width, image.height, 0, 100, 28) ##
    nLayers, layer_ids = pdb.gimp_image_get_layers(image)
    image.add_layer(BgLayer, 0)
    pdb.gimp_edit_bucket_fill(BgLayer, 1, 28, 100, 255, False, 0, 0)

    ##### BG Layer
    fileName = config["BgTexture"]
    fileName = fileName%(random.randint(0,9))
    texturePath = PATH+fileName
    layer = pdb.gimp_file_load_layer(image, texturePath)
    pdb.gimp_image_insert_layer(image, layer, None, -1)

    ##### Load text - import svg to vectors
    num_vectors, vectors_ids = pdb.gimp_vectors_import_from_file(image, f, True, True)
    vectors = pdb.gimp_image_get_vectors_by_name(image, 'Imported Path')

    ##### Pressed-In Layer
    edgeLayer = gimp.Layer(image, "Pressed In", image.width, image.height, 0, 100, 28) ##
    image.add_layer(edgeLayer, 0)
    pdb.gimp_layer_add_alpha(edgeLayer)
    pdb.gimp_vectors_to_selection(vectors, 0, False, False, 0, 0)
    pdb.gimp_edit_bucket_fill(edgeLayer, 0, 28, 100, 255, False, 0, 0)
    pdb.gimp_selection_invert(image)
    pdb.gimp_drawable_edit_clear(edgeLayer)
    pdb.gimp_layer_scale(edgeLayer, image.width*0.4, image.height*0.4, True)

    ##### Clean up
    pdb.gimp_selection_none(image)

    ##### merge all layers to one and save
    layer = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)
    pdb.file_jpeg_save(image, layer, f2, f2, 0.9, 0, 0, 0, "Creating with GIMP", 0, 0, 0, 0)

    ##### close image here

register(
    "python_fu_hft_batch_text_chuanghua",
    "Chuang-hua text NFT (batch)",
    "Batch create NFT with chuang-hua text",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2023",
    "<Image>/Filters/NFT/Batch Text Chuang-hua",
    "*",
    [],
    [],
    nft_batch_chuanghua_text)

main()