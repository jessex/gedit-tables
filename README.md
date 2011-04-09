# Table Maker: a Gedit plugin for automatic table creation

## Description

Gedit is a severely underrated plain text editor, in my humble opinion. It is 
very simple and offers no frills, yes, but sometimes that's really all that 
is needed. Then again, Gedit does have a solid plugin system which allows some 
layer of extendability. Users can add all sorts of goodies to the editor to 
transform little minimalistic Gedit into a robust editing environment.

Table Maker is a Gedit plugin which affords pseudo-Word Document style table 
creation. A simple dialog is opened up and the user picks some parameters, such 
as the amount of rows and columns, and a table is inserted into the document. 
Done. Simple and easy.

A comprehensive list of Gedit plugins can be found <a href="http://live.gnome.org/Gedit/Plugins">right here</a>.

## Installation

1. Get Gedit (of course)

2. Get the gedittables.py and gedittables.gedit-plugin files

3. Copy the files into the plugin directory of Gedit
    
    If you are in a Linux environment, simply copy the files into the user-plugin 
    directory, `~/.gnome2/gedit/plugins/`, or into the system-wide plugin directory, 
    `/usr/lib/gedit-2/plugins/` (I suggest the latter)
    
    If you are in OS X, you move these files into the same directory, but the path 
    to getting there is a tad different. Because the `/usr/lib/gedit-2/plugins/` 
    directory is a hidden one, you can either use `cp` or `mv` in bash to send 
    the files to the directory or, if you're more comfortable this way, you can 
    set OS X to show all hidden files and folders then simply drag-and-drop 
    (there is plenty of literature on how to do this)
    
4. Sip your favorite beverage because you're finished

## Usage

1. Fire up Gedit and open the Preferences menu and then the list of available 
plugins. The Table Maker plugin entry will be inserted after installation. Enable 
the plugin by clicking the check mark to the ON position

2. When you wish to insert a blank table, open the Tools menu and click "Create 
Table" to bring up the dialog. Tune your table settings and click "Insert"

3. If you wish to auto-build a table around some data, open the dialog as in 
the previous step and check "Build around highlighted data". Then, highlight some 
data in your document, separated by a specified delimiter, and click "Insert". The 
highlighted data will be inserted into a freshly created table

## Screenshots

Please view the sample .png files in this directory
                   
## License

Copyright (c) 2011 Joshua Essex

     Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

