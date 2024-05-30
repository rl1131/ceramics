## Ceramics Final Poject
Generate an "artful" randomized pattern that resembles a circuit board layout.
## Requirements
The following are required to reproduce this work.  The Python matrix generation program definitely runs on Windows, and may run on Linux, but has not been tested there.  Python 3.x is used to run the Python matrix generation program.  OpenSCAD is used to generate the 3D .stl model which can then be used for 3D printing.
 - Windows 10 or 11
 - Python 3.x
 - OpenSCAD - Language Based 3D Modeling 
## Other Software Used to Print
 Once you have a 3D .stl model, you will need other software to "slice" and print.  I used the following for this purpose:
 - Slicing:  PrusaSlicer
 - Raspberry Pi to run OctoPrint
 - Printing:  OctoPrint
 - Wanhao Duplicator 9 Printer
## Making it Real
Follow these basic steps:
 - Edit the file "elecmug.scad"
	 - Change any physical parameters in this file to size the "slab" to your liking.  The default settings produce an Espresso size Mug.
 - Load "elecmug.scad" into OpenSCAD
	 - You WILL GET AN ERROR.
	 - Note the following numbers (29 and 8):
		 - ECHO: col_count = 29
		 - ECHO: row_count = 8
	 - These are the number of columns and rows the matrix needs to fill in order to create your "slab" template.
 - Edit the Python script "matrix.py"
	 - Change the following two lines to equal the above col & row counts:
		 - col_count = 29
		 - row_count = 8
	 - At the command line run "python matrix.py"
		 - A window should appear with a crude representation of the matrix.
		 - Press "SPACE" to cycle to another rendering... continue to cycle until you find a rendering you like.  These are randomly generated.
		 - Press "ESC" to exit and print the last rendering as a matrix suitable for OpenSCAD.
	 - Edit the file "matrix.scad" and replace the variable "matrix" there with your newly created matrix.
	 - Run OpenSCAD again and load elecmug.scad.  You should now see your newly created "slab" template.
	 - From here, you will need to export the .stl file and continue with your normal 3D Printing workflow... or learn one on the interwebs.
