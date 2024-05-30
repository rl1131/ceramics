/* NOTES:
   All dimensions are in milimeters (mm)
   
*/

/* Place the Python Generated Matrix In This File: */

include <matrix.scad>
mtx_row_count = len(matrix);     // Number of rows in matrix
mtx_col_count = len(matrix[0]);  // Number of cells in each row

/* Base Plate Dimensions:
   A rectangular template to cut out the slab.
   hieght -> Slab 'x' dimension is the circumference of the mug / cylinder.
   circumference   -> Slab 'y' dimension is the height of the mug / cylinder.
*/

height    = 49;  // The desired height of the finished mug
mug_width = 59;  // The desired diameter of the finished mug
circumference      = mug_width * 3.14159;

/* Shrinkage "factor":
   The xy,z factors of expected clay body shrinkage after firing 
*/

xy_factor  = 1.15;  // 15 % more in size to accomodate for shrinkage
z_factor   = 1.12;  // 12 % more in size to accomodate for shrinkage

/* Handle allowance (mm)
   This is area on the x/y ends of the slab to leave blank. (1/2 on each end).
   This area is used to attach a handle, and to attach the 
   x/y ends to each other to form the cylinder.
   Once the x/y ends of the cylinder are attached, this will 
   be doubled since it is applied at the x AND y ends.
*/

handle_allowance_factor = 0.16;  // 16 % of width / circumference is allocated for the handle
// handle_allowance_factor = 0.02;  // 15 % of width / circumference is allocated for the handle

/* Base Plate Thickness (mm):
   bpz is the thickeness of the baseplate.
   This dimension is not part of the clay project, it determines
   how sturdy the template's baseplate is (thicker is more sturdy).
   Too thick and it's bulky and takes more time to print.
   I've found 3mm to be nearly ideal.
*/

bpz = 3;

/* Top and Bottom Margins (mm)
   Blank area on top and bottom of the mug / slab (area without the circuit matrix).
*/

top_margin_factor = 0.03;  // Factor of height is blank at top    // 0.10 is 10%
bot_margin_factor = 0.03;  // Factor of height is blank at bottom // 0.10 is 10%

/* Circuit generation factors: */

trace_depth = 0.80;
trace_width = 1.00;
via_depth   = 0.45;
via_diam    = 2.75;
via_width   = 0.80;
pad_depth   = 0.55;
pad_diam    = 3.80;
pad_width   = 1.00;



/************* Function to Generate the baseplate *************/

adj_height = round(height * z_factor);
adj_circ   = round(circumference * xy_factor);

module baseplate(){
    translate([0, 0, 0])
        cube( size = [adj_circ, adj_height, bpz], center = false);
}
echo(adj_height=adj_height);
echo(adj_circ=adj_circ);

/************* Baseplate done. *************/



/************* Build the Circuit now...  *************/

desn_width  = adj_circ - (adj_circ * handle_allowance_factor);
desn_height = adj_height - (adj_height * top_margin_factor) - (adj_height * bot_margin_factor);


/* Calculate the Cell Size (mm):
   HOWEVER, it shouldn't be too large or small... so adjust the number of columns and rows of the matrix to fit.
*/

cell_size = 6.0;

// ideal_cell_size      = 6.0;
// cell_x_size = desn_width / mtx_col_count;
// cell_y_size = desn_height / mtx_row_count;
// cell_size = min(cell_x_size, cell_y_size);


/* Build it... */

col_count = floor(desn_width / cell_size);
row_count = floor(desn_height / cell_size);

echo(matrix_col_count=len(matrix[0]));
echo(matrix_row_count=len(matrix));
echo(col_count=col_count);
echo(row_count=row_count);
echo("IF YOU GET AN ERROR HERE... REGENERATE THE PYTHON MATRIX WITH THE ABOVE COLOUMN AND ROW COUNTS");
assert(mtx_col_count == col_count, "MATRIX COLUMN COUNT NOT EQUAL");
assert(mtx_row_count == row_count, "MATRIX ROW COUNT NOT EQUAL");

/* Adjust the desn_width and desn_height to be integral with the col/row counts: */

adj_desn_width  = col_count * cell_size;
adj_desn_height = row_count * cell_size;

design_offset_x = (adj_circ - adj_desn_width) / 2;
design_offset_y = (adj_height - adj_desn_height) / 2;

echo(adj_desn_width=adj_desn_width);
echo(adj_desn_height=adj_desn_height);

col_base = floor((adj_circ - (adj_desn_width / 2)));
row_base = floor(adj_height - adj_desn_height);

echo(col_base=col_base);
echo(row_base=row_base);

csdiv2 = cell_size / 2;

ccpad = csdiv2;
ccircp0 = [csdiv2, csdiv2];
ccircp1 = [pad_diam, pad_diam];



function get_cell_x(col) = cell_size * col;
function get_cell_y(row) = cell_size * row;

// Gridlines:
module gridlines(){
    translate([0,0-cell_size,-0.1])
        cube( size = [15, 0.05, 0.1]);
    translate([0,0-(cell_size / 2),-0.1])
        cube( size = [15, 0.05, 0.1]);
    translate([cell_size/2,(-15) + (cell_size / 2),-0.1])
        rotate([0,0,90])
        cube( size = [15, 0.05, 0.1]);
    translate([cell_size,(-15) + (cell_size / 2),-0.1])
        rotate([0,0,90])
        cube( size = [15, 0.05, 0.1]);
}        


module do459(){
    // Verticle 4-5
    translate([(csdiv2 / 2), 0-csdiv2, (trace_depth / 2)])
        cube( size = [csdiv2, trace_width, trace_depth], center = true);
    // Diagonal 5-9
    translate([csdiv2 + (csdiv2 / 2), 0-(csdiv2 + (csdiv2 / 2)), (trace_depth / 2)])
       rotate([0,0,-45])
           cube( size = [sqrt(2*(csdiv2^2)), trace_width, trace_depth], center = true);
    // Fill the gap
    translate([csdiv2, 0-csdiv2, (trace_depth / 2)])
      cylinder(h = trace_depth, r = (trace_width / 2), $fn=96, center = true);
}

module bender(cx, cy, tx45, ty45, my45, rz45){
    translate([cx * cell_size, (-cy) * cell_size, 0]){
        translate([tx45,ty45,0])
          mirror([0,my45,0])
            rotate(a=[0,0,rz45])
              do459();
    }
}
 
module line19(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, (trace_depth / 2)])
           rotate([0,0,-45])
               cube( size = [sqrt(2*(cell_size^2)), trace_width, trace_depth], center = true);
    }
}    

module line37(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, (trace_depth / 2)])
           rotate([0,0,45])
               cube( size = [sqrt(2*(cell_size^2)), trace_width, trace_depth], center = true);
    }
}    

module line46(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, (trace_depth / 2)])
           cube( size = [cell_size, trace_width, trace_depth], center = true);
    }
}    

module line28(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, (trace_depth / 2)])
           cube( size = [trace_width, cell_size, trace_depth], center = true);
    }
}


module ring(diaO, diaI, depth){
    difference(){
        cylinder(h = depth, r = (diaO / 2), $fn=96);
        translate([0, 0, ((depth+0.004) / 2) - 0.002])
          cylinder(h = depth+0.001, r = (diaI / 2), $fn=96, center=true);
    }
}


module via(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, 0])
            ring(via_diam, via_diam-(via_width * 2), via_depth);
    }
}

module pad(cx, cy){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([csdiv2, -csdiv2, 0])
            ring(pad_diam, pad_diam-(pad_width * 2), pad_depth);
    }
}

module term1(){
    translate([-(cell_size / 2),cell_size / 2, 0]){
        dlen = sqrt(2*(cell_size^2));
        pad_rad = (pad_diam / 2);
        ring_midpoint = (pad_rad - pad_width) + (pad_width / 1.33);  // Distance from center of cell to middle of the ring
        ll = (dlen/2) - ring_midpoint;
        xyofs = sqrt(((ll/2)^2)/2);
        translate([xyofs, -xyofs, (trace_depth / 2)])
           rotate([0,0,-45])
               cube( size = [ll, trace_width, trace_depth], center = true);
        translate([csdiv2, -csdiv2, 0])
            ring(pad_diam, pad_diam-(pad_width * 2), pad_depth);
    }
}

module term_diag(cx, cy, rot){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([cell_size / 2, -(cell_size / 2), 0])
            rotate([0,0,rot])
                term1();
    }
}    
    

module term2(){
        pad_rad = (pad_diam / 2);
        ring_midpoint = (pad_rad - pad_width) + (pad_width / 1.33);  // Distance from center of cell to middle of the ring
        ll = (cell_size/2) - ring_midpoint;
        ypos = (cell_size/2)-(ll/2);
        translate([0, ypos, trace_depth / 2])
           cube( size = [trace_width, ll, trace_depth], center=true );
        translate([0, 0, 0])
            ring(pad_diam, pad_diam-(pad_width * 2), pad_depth);
}


module term90(cx,cy,rot){
    translate([cx * cell_size, (-cy) * cell_size, 0])
    {
        translate([cell_size / 2, -(cell_size / 2), 0])
            rotate([0,0,rot])
                term2();
    }
}    



/* The shape dictionary */
gls = [
    ["A", ["B",         0,          0,   0,   0] ],
    ["B", ["B",         0,          0,   1,  90] ],
    ["C", ["B", cell_size, -cell_size,   1, 270] ],
    ["D", ["B",         0, -cell_size,   0,  90] ],
    ["E", ["B", cell_size,          0,   0, 270] ],
    ["F", ["B", cell_size,          0,   1, 180] ],
    ["G", ["B", cell_size, -cell_size,   0, 180] ],
    ["H", ["B",         0, -cell_size,   1,   0] ],

    ["L", ["1"] ],
    ["/", ["2"] ],
    ["|", ["3"] ],
    ["-", ["4"] ],
    
    ["o", ["V"] ],

    ["1", ["D",   0] ],
    ["3", ["D", -90] ],
    ["6", ["D",  90] ],
    ["8", ["D", 180] ],

    ["2", ["P",   0] ],
    ["4", ["P",  90] ],
    ["5", ["P", -90] ],
    ["7", ["P", 180] ],
];


module place(cx, cy, command){
    letter = command[0];
    if (letter == "B") {
        tx45 = command[1];
        ty45 = command[2];
        my45 = command[3];
        rz45 = command[4];
        bender(cx,cy,tx45,ty45,my45,rz45);
    } else if (letter == "1") {
        line19(cx,cy);
    } else if (letter == "2") {
        line37(cx,cy);
    } else if (letter == "3") {
        line28(cx,cy);
    } else if (letter == "4") {
        line46(cx,cy);
    } else if (letter == "V") {
        via(cx,cy);
    } else if (letter == "D") {
        rz45 = command[1];
        term_diag(cx,cy,rz45);
    } else if (letter == "P") {
        rz45 = command[1];
        term90(cx,cy,rz45);
    }
}


module circuit() {
    for (y = [ 0 : len(matrix) - 1 ]){
        for (x = [ 0 : len(matrix[y]) - 1]){
            if (matrix[y][x] != "0"){
                idxs = search(matrix[y][x], gls);
                command = gls[idxs[0]][1];
                place(x, y, command);
            }
        }
    }
}


baseplate();

translate([design_offset_x, design_offset_y, bpz])
  mirror([0,1,0])
    circuit();


// linear_extrude(0.5)
// text("Robert Lee", font="Ariel", size=4, $fn=100);


