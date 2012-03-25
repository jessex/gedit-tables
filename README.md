# Table Maker: a Gedit plugin for automatic table creation

## Description

Gedit is a dead simple, highly effective text editor. Few frills, nothing 
extraneous, only what's needed. However, it also features a rich plugin system
to allow us to extend its functionality.

Table Maker is a Gedit plugin which affords pseudo-Word Document style table 
creation. A simple dialog is opened up and the user picks some parameters, such 
as the amount of rows and columns, and a table is inserted into the document. 
Done. Simple and easy.

A comprehensive list of Gedit plugins can be found <a href="http://live.gnome.org/Gedit/Plugins">right here</a>.

## Installation

1. Get <a href="http://projects.gnome.org/gedit/">Gedit</a>

2. Get the `gedittables.py` and `gedittables.plugin` files

    Note that since Gedit 3 broke compatibility with plugins for Gedit 2, there 
    are different downloads of the plugin available based on your editor version.

3. Copy the files into the plugin directory of Gedit. Specifically:
    
    Copy the files into the user-plugin directory: `~/.local/share/gedit/plugins/`, or, 
    into the system-wide plugin directory: `/usr/lib/gedit/plugins/`.
    
4. Fire up Gedit and open the Preferences menu and then the list of available 
plugins. The Table Maker plugin entry will be inserted after installation. Enable 
the plugin by clicking the check mark to the ON position
    
5. Sip your favorite beverage because you're finished

## Usage

1. When you wish to insert an empty table, open the Tools menu and click "Create 
Table" to bring up the dialog. Tune your table settings and click "Insert"

2. If you wish to auto-build a table around some data, open the dialog as in 
the previous step and check "Build around highlighted data". Then, highlight some 
data in your document, separated by a specified delimiter, and click "Insert". 
The highlighted data will be inserted into a freshly created table

## Screenshots

![Without Data](https://github.com/jessex/gedit-tables/raw/master/with_data.png)

![With Data](https://github.com/jessex/gedit-tables/raw/master/without_data.png)
                   
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

