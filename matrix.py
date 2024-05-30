from random import *
import sys

DEBUG_ENABLED=False

# Column and Row Counts

col_count = 29
row_count = 8

# ------------------------------------------
# Random Weigting For Generation of Matrix
# ------------------------------------------

# Arbitrary change in direction chance
chance_of_dir_change = 1/10  

# Target trace length weighting
wlen = [0,0,1,2,2,2,2,3,3,3,3,4,4,4,5,5,6,7,8]


# ------------------------------------------
# Helper functions and top level initializations
# ------------------------------------------

# For debug... prints a message and line number.
# Uncomment the code to enable debug messages
def LINE(s=None):
    if DEBUG_ENABLED:
        l = sys._getframe(1).f_lineno
        if s is None:
            print(sys._getframe(1).f_lineno)
        else:
            print(sys._getframe(1).f_lineno, ' ', s)

# Represents 'o' termination for each of the directions.  That is:
# 1   2   3  4-5
#  \  |  /
#   3 7 6
#
# 1,2,3,
# 4,  5,
# 6,7,8,
#
# 'o' is reserved for Vias (no trace)

dir1 = (-1,-1)
dir2 = ( 0,-1)
dir3 = ( 1,-1)
dir4 = (-1, 0)
dir5 = ( 1, 0)
dir6 = (-1, 1)
dir7 = ( 0, 1)
dir8 = ( 1, 1)


sel_dxn = [dir1, dir2, dir3,
           dir4,       dir5,
           dir6, dir7, dir8]

sel_dxn_weight = [ 12,  2,  2, 
                   4,       4, 
                   2,  1,  10 ]

o_dxn_from_to = {}
o_dxn_from_to[(dir1, dir4)] = 'A'  # 
o_dxn_from_to[(dir5, dir8)] = 'A'  # 
o_dxn_from_to[(dir1, dir2)] = 'B'  # 
o_dxn_from_to[(dir7, dir8)] = 'B'  # 
o_dxn_from_to[(dir2, dir1)] = 'C'  # 
o_dxn_from_to[(dir8, dir7)] = 'C'  # 
o_dxn_from_to[(dir2, dir3)] = 'D'  # 
o_dxn_from_to[(dir6, dir7)] = 'D'  # 
o_dxn_from_to[(dir3, dir2)] = 'E'  # 
o_dxn_from_to[(dir7, dir6)] = 'E'  # 
o_dxn_from_to[(dir3, dir5)] = 'F'  # 
o_dxn_from_to[(dir4, dir6)] = 'F'  # 
o_dxn_from_to[(dir4, dir1)] = 'G'  # 
o_dxn_from_to[(dir8, dir5)] = 'G'  # 
o_dxn_from_to[(dir5, dir3)] = 'H'  # 
o_dxn_from_to[(dir6, dir4)] = 'H'  # 

o_dxn_from_to[(dir1, dir1)] = '\\'
o_dxn_from_to[(dir2, dir2)] = '|'
o_dxn_from_to[(dir3, dir3)] = '/'
o_dxn_from_to[(dir4, dir4)] = '-'
o_dxn_from_to[(dir5, dir5)] = '-'
o_dxn_from_to[(dir6, dir6)] = '/'
o_dxn_from_to[(dir7, dir7)] = '|'
o_dxn_from_to[(dir8, dir8)] = '\\'

nxt_dxn = {}
nxt_dxn[dir1] = [dir4, dir2]
nxt_dxn[dir2] = [dir1, dir3]
nxt_dxn[dir3] = [dir2, dir5]
nxt_dxn[dir4] = [dir6, dir1]
nxt_dxn[dir5] = [dir3, dir8]
nxt_dxn[dir6] = [dir7, dir4]
nxt_dxn[dir7] = [dir8, dir6]
nxt_dxn[dir8] = [dir5, dir7]

o_end_code = {}
o_end_code[dir1] = '8'
o_end_code[dir2] = '7'
o_end_code[dir3] = '6'
o_end_code[dir4] = '5'
o_end_code[dir5] = '4'
o_end_code[dir6] = '3'
o_end_code[dir7] = '2'
o_end_code[dir8] = '1'

o_start_code = {}
o_start_code[dir1] = '1'
o_start_code[dir2] = '2'
o_start_code[dir3] = '3'
o_start_code[dir4] = '4'
o_start_code[dir5] = '5'
o_start_code[dir6] = '6'
o_start_code[dir7] = '7'
o_start_code[dir8] = '8'


# ------------------------------------------
# The circuit class (an x,y matrix of symbols)
# ------------------------------------------

class Circart(list):
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
    
        super().__init__()

        for i in range(rows):
            self.append([0] * cols)

        tcnt = 0
        vcnt = 0

        for z in range(100):
            try:
                (x,y) = self.getspoint()
            except Exception as e:
                print(e)
                break
            l = choice(wlen)
            dxn = None

            if l > 0:
                # Select initial direction:
                dxn_choices = sample(sel_dxn, counts=sel_dxn_weight, k=30)

                while dxn_choices:
                    ndxn = dxn_choices.pop(0)
                    nx = x + ndxn[0]
                    ny = y + ndxn[1]
                    if self.checknext(x, y, nx, ny):
                        dxn = ndxn
                        break

            if dxn is not None:
                # We have a direction and length and a next(x,y)
                self[y][x] = o_start_code[dxn]
                LINE("x,y,c: {},{},{} ".format(x,y,self[y][x]) + str(dxn))
                while l > 0:
                    x += dxn[0]
                    y += dxn[1]
                    prev_dxn = dxn
                    try:
                        dxn = self.newdxn(dxn, x, y)
                    except Exception as e:
                        print(e)
                        break
                    self[y][x] = o_dxn_from_to[(prev_dxn, dxn)]
                    LINE("x,y,c: {},{},{} ".format(x,y,self[y][x]) + str(dxn))
                    l = l - 1

                self[y][x] = o_end_code[prev_dxn]
                LINE("x,y,c: {},{},{} ".format(x,y,self[y][x]) + str(prev_dxn))
                tcnt += 1
            else:
                self[y][x] = 'o'
                LINE("x,y,c: {},{},{} ".format(x,y,self[y][x]))
                vcnt += 1

        #print("T/V count: ", tcnt, vcnt)

    def getspoint(self):
        LINE()
        max = 50
        while max:
            max -= 1
            x = randint(0, self.cols - 1)
            y = randint(0, self.rows - 1)
            if self[y][x] == 0:
                return (x,y)
        raise Exception

    def getdxnchoices(self, dxn):
        dxc = []
        if random() < chance_of_dir_change:
            # First two choices are random change of direction
            dxc.extend(sample(nxt_dxn[dxn], k=len(nxt_dxn[dxn])))
            dxc.append(dxn)
        else:
            # First choice is to go strait
            dxc.append(dxn)
            dxc.extend(sample(nxt_dxn[dxn], k=len(nxt_dxn[dxn])))
        return dxc

    def checknext(self, x, y, nx, ny):
        # Does this change go out of bounds?
        if (nx < 0) or (nx >= self.cols) or (ny < 0) or (ny >= self.rows):
            return False
        # Is the change diagonal?
        # if ndxn[0] != 0 and ndxn[1] != 0:    
        if x != nx and y != ny:
            # It is diagonal, need to check if we are busting through another trace:
            # If both the cells on either side of the line are taken, then we are trying 
            # to bust through a trace.
            # Are both adjacent cells taken?
            if self[ny][x] != 0 and self[y][nx] != 0:
                return False
            # Is the target cell taken?
        if self[ny][nx] != 0:
            return False
        # All tests pass... go for it.
        return True

    def newdxn(self, dxn, x, y):
        dxc = self.getdxnchoices(dxn)
        while dxc:
            ndxn = dxc.pop(0)
            nx = x + ndxn[0]
            ny = y + ndxn[1]
            if self.checknext(x, y, nx, ny):
                return ndxn
        # We ran out of choices... quit while we are ahead
        raise Exception

    def __str__(self):
        ostr = ''
        for ys in mtx:
            for xs in ys:
                if xs:
                    ostr += xs
                else:
                    ostr += '∙'
            ostr += '\n'
        return ostr


# ------------------------------------------
# Visualization of the matrix (crude, but it works).
# ------------------------------------------

from tkinter import Tk, Canvas

cell_width = 30
cell_height = 30
cell_min = min(cell_width, cell_height)

ccp = {}
ccp['x'] = int(cell_width / 2)
ccp['y'] = int(cell_height / 2)

vwidth  = cell_width * col_count
vheight = cell_height * row_count

def get_cell_xy(col, row):
    return (col * cell_width, row * cell_height)


# Position like phone keypad
cpos1 = (0, 0)
cpos2 = (ccp['x'], 0)
cpos3 = (cell_width - 1, 0)
cpos4 = (0, ccp['y'])
cpos5 = (ccp['x'], ccp['y'])
cpos6 = (cell_width - 1, ccp['y'])
cpos7 = (0, cell_height - 1)
cpos8 = (ccp['x'], cell_height - 1)
cpos9 = (cell_width - 1, cell_height - 1)

ccpad = int(cell_min / 6)
ccircp0 = (ccpad, ccpad)
ccircp1 = (cell_width - ccpad, cell_height - ccpad)

gls = {}
gls['A']  = [('L', cpos4, cpos5),('L', cpos5, cpos9)]
gls['B']  = [('L', cpos2, cpos5),('L', cpos5, cpos9)]
gls['C']  = [('L', cpos1, cpos5),('L', cpos5, cpos8)]
gls['D']  = [('L', cpos3, cpos5),('L', cpos5, cpos8)]
gls['E']  = [('L', cpos7, cpos5),('L', cpos5, cpos2)]
gls['F']  = [('L', cpos7, cpos5),('L', cpos5, cpos6)]
gls['G']  = [('L', cpos1, cpos5),('L', cpos5, cpos6)]
gls['H']  = [('L', cpos4, cpos5),('L', cpos5, cpos3)]
gls['\\'] = [('L', cpos1, cpos9)]
gls['/']  = [('L', cpos7, cpos3)]
gls['|']  = [('L', cpos2, cpos8)]
gls['-']  = [('L', cpos4, cpos6)]
gls['o']  = [('C', ccircp0, ccircp1)]
gls['1']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos1)]
gls['2']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos2)]
gls['3']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos3)]
gls['4']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos4)]
gls['5']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos6)]
gls['6']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos7)]
gls['7']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos8)]
gls['8']  = [('C', ccircp0, ccircp1),('L', cpos5, cpos9)]


class MVis:
    def __init__(self, win):
        self.win = win
        self.canvas = None
        self.matrix = None

    def glyph(self, col, row, ch):
        gx, gy = get_cell_xy(col,row)
        for el in gls[ch]:
            if el[0] == 'L':
                x1,y1 = el[1]
                x2,y2 = el[2]
                self.canvas.create_line(gx + x1, gy + y1, gx + x2, gy + y2, width=6)
            elif el[0] == 'C':
                x1,y1 = el[1]
                x2,y2 = el[2]
                self.canvas.create_oval(gx + x1, gy + y1, gx + x2, gy + y2, width=4, outline="#BB0")

    def show_matrix(self, x=0):
        if self.canvas:
            self.canvas.destroy()
        self.canvas=Canvas(self.win, width=vwidth, height=vheight)
        self.canvas.pack()
        self.matrix = Circart(col_count, row_count)
        for y in range(row_count):
            for x in range(col_count):
                if self.matrix[y][x]:
                    self.glyph(x,y, self.matrix[y][x])


# Start the TK window for display
win = Tk()
win.geometry("{}x{}".format(vwidth, vheight))
visual = MVis(win)
visual.show_matrix()
win.after(1, lambda: win.focus_force())
win.bind("<Escape>", lambda x: win.destroy())
win.bind("<space>", visual.show_matrix)
win.mainloop()
# When we exit the mainloop, it will be because of the escape key being pressed.


# ------------------------------------------
# Print the final matrix for inclusion in 
# the OpenSCAD Project
# ------------------------------------------

def pscad(mtx):
    print("matrix = [")
    rfirst = True
    for row in mtx:
        print("        [", end='')
        cfirst = True
        for pc in row:
            col = pc
            if col == "\\":
                col = "L"
            if cfirst:
                print('"{}"'.format(col), end='')
            else:
                print(",", '"{}"'.format(col), end='')
            cfirst = False
        if row is mtx[-1]:
            print("]")
        else:
            print("],")
    print("];")

pscad(visual.matrix)
