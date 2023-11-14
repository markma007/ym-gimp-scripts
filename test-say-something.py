#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2013, Jose F. Maldonado
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#    - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation and/or 
#    other materials provided with the distribution.
#    - Neither the name of the author nor the names of its contributors may be used 
#    to endorse or promote products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.
#
# -------------------------------------------------------------------------------------
#
# This file is a basic example of a Python plug-in for GIMP.
#
# It can be executed by selecting the menu option: 'Filters/Test/Say something'
# or by writing the following lines in the Python console (that can be opened with the
# menu option 'Filters/Python-Fu/Console'):
# >>> image = gimp.image_list()[0]
# >>> layer = image.layers[0]
# >>> message = "This is a message"
# >>> gimp.pdb.python_fu_test_say_something(image, layer, message)

from gimpfu import *

def say_something(img, layer, message) :
    ''' Display a message, defined by the user, in the bottom of GIMP.
    
    Parameters:
    img : image The current image.
    layer : layer The layer of the image that is selected.
	message : string A message
    '''
    gimp.message(message)

register(
    "python_fu_test_say_something",
    "Say something",
    "Display a message defined by the user.",
    "JFM",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Filters/Test/Say something",
    "*",
    [
        (PF_STRING, "message", "Message to display", "hello")
	],
    [],
    say_something)

main()