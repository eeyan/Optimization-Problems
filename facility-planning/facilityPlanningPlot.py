import matplotlib.pyplot

# this array includes the coordinates of fulfillment centers
# there are 10 fulfillment center locations
# for each fulfillment center, we keep x and y coordinates
nofcs = 10
fcs = [ 0 for j in range ( nofcs ) ]
fcs[0] = [60 , 15]
fcs[1] = [26 , 36]
fcs[2] = [73 , 34]
fcs[3] = [57 , 54]
fcs[4] = [18 , 19]
fcs[5] = [11 , 1]
fcs[6] = [60 , 77]
fcs[7] = [68 , 44]
fcs[8] = [97 , 65]
fcs[9] = [4 , 79]

# this array includes the coordinates of demand points
# there are 10 demand points
# for each demand point, we keep x and y coordinates
# for this example, there are 20 demand points
nodps = 20
dps = [ 0 for j in range ( nodps ) ]
dps[0] = [25 , 75]
dps[1] = [49 , 7]
dps[2] = [17 , 8]
dps[3] = [12 , 84]
dps[4] = [3 , 83]
dps[5] = [57 , 5]
dps[6] = [46 , 39]
dps[7] = [83 , 89]
dps[8] = [78 , 96]
dps[9] = [27 , 44]
dps[10] = [64 , 16]
dps[11] = [52 , 86]
dps[12] = [57 , 72]
dps[13] = [33 , 55]
dps[14] = [66 , 47]
dps[15] = [25 , 28]
dps[16] = [9 , 97]
dps[17] = [85 , 87]
dps[18] = [98 , 3]
dps[19] = [19 , 97]

# this array includes which fulfillment center each demand point is connected to
# for this example, dem pnt 0 is connected to full cen 1, but dem pnt 8 is connected to full cen 6
assgns0 = [ 0 for j in range ( nodps ) ]
assgns0[0] = 6
assgns0[1] = 6
assgns0[2] = 6
assgns0[3] = 6
assgns0[4] = 6
assgns0[5] = 6
assgns0[6] = 6
assgns0[7] = 6
assgns0[8] = 6
assgns0[9] = 6
assgns0[10] = 6
assgns0[11] = 6
assgns0[12] = 6
assgns0[13] = 6
assgns0[14] = 6
assgns0[15] = 6
assgns0[16] = 6
assgns0[17] = 6
assgns0[18] = 6
assgns0[19] = 6

assgns1 = [0 for j in range (nodps)]
assgns1[0] = 6
assgns1[1] = 0
assgns1[2] = 0
assgns1[3] = 6
assgns1[4] = 6
assgns1[5] = 0
assgns1[6] = 0
assgns1[7] = 6
assgns1[8] = 6
assgns1[9] = 0
assgns1[10] = 0
assgns1[11] = 6
assgns1[12] = 6
assgns1[13] = 6
assgns1[14] = 6
assgns1[15] = 0
assgns1[16] = 6
assgns1[17] = 6
assgns1[18] = 0
assgns1[19] = 6

assgns2 = [0 for j in range (nodps)]
assgns2[0] = 9
assgns2[1] = 0
assgns2[2] = 0
assgns2[3] = 9
assgns2[4] = 9
assgns2[5] = 0
assgns2[6] = 0
assgns2[7] = 6
assgns2[8] = 6
assgns2[9] = 9
assgns2[10] = 0
assgns2[11] = 6
assgns2[12] = 6
assgns2[13] = 6
assgns2[14] = 6
assgns2[15] = 0
assgns2[16] = 9
assgns2[17] = 6
assgns2[18] = 0
assgns2[19] = 9

for fc in range( nofcs ):
    matplotlib.pyplot.plot( fcs[ fc ][ 0 ]  , fcs[ fc ][ 1 ] , 'ro' , color = "green" , lw = 9 )

for dp in range( nodps ):
    matplotlib.pyplot.plot( dps[ dp ][ 0 ]  , dps[ dp ][ 1 ] , 'ro' , color = "red" , lw = 9 )

for dp in range( nodps ):
    dpx = dps[ dp ][ 0 ]
    dpy = dps[ dp ][ 1 ]
    fcx = fcs[ assgns2[ dp ] ][ 0 ]
    fcy = fcs[ assgns2[ dp ] ][ 1 ]
    matplotlib.pyplot.plot( [ dpx , fcx ], [ dpy , fcy ]  , color = "black"  )

matplotlib.pyplot.show()