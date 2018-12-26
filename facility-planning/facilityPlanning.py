import math
from gurobipy import *
import matplotlib.pyplot


# initialize data
noTime = 3
noFC = 10
noDP = 20

# years per time period
years = [6, 5, 9]

fcs = [0 for i in range (noFC)]
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


dps = [0 for i in range (noDP)]
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

# calculate distance (cost) for each FC-DP match
def distance(fc, dp): 
	return math.sqrt((fc[0] - dp[0]) ** 2 + (fc[1] - dp[1]) ** 2)

costs = [[distance(fc, dp) for dp in dps] for fc in fcs]

# create model
myModel = Model("hw11")

# create decision variables for serving DP from each FC at each time period
myVars = [ [ [0 for k in range ( noTime)] for i in range ( noDP )] for j in range (noFC) ]

for i in range( noFC ):
	for j in range ( noDP ):
		for k in range ( noTime ):
			curVar = myModel.addVar (vtype = GRB.BINARY, name = "y" + "FC" + str( i ) + "DP" + str( j ) + "Time" + str( k ))
			myVars[i][j][k] = curVar

myModel.update()

# create decision variables for which FC to open at each time
kfcVars = [ [ 0 for k in range( noTime )] for i in range (noFC)]

for i in range( noFC ):
	for k in range ( noTime ):
		curVar = myModel.addVar (vtype = GRB.BINARY, name = "x" + "FC" + str( i ) + "Time" + str( k ))
		kfcVars[i][k] = curVar

# create objective function
objExpr = LinExpr()
for i in range( noFC ):
	for j in range ( noDP ):
		for k in range ( noTime ):
			curVar = myVars[i][j][k]
			objExpr += years[k] * costs[i][j] * curVar

myModel.setObjective ( objExpr , GRB.MINIMIZE )
myModel.update()

#constraints

# one new open FC each time period
for k in range(noTime):
	constExpr = LinExpr()
	for i in range(noFC):
		curVar = kfcVars[i][k]
		constExpr += curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.LESS_EQUAL , rhs = 1 , name = "openFC" + str ( i ) + "Time" + str ( k ))


myModel.update()

#all DPs are served at each time period, with open FCs
#first time period
for j in range(noDP):
	constExpr = LinExpr()
	for i in range(noFC):
		curVar = myVars[i][j][0]
		constExpr += kfcVars[i][0] * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.GREATER_EQUAL , rhs = 1 , name = "serveDP" + str ( j ) + "Time0")

#second time period
for j in range(noDP):
	constExpr = LinExpr()
	for i in range(noFC):
		curVar = myVars[i][j][1]
		constExpr += kfcVars[i][0] * curVar
		constExpr += kfcVars[i][1] * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.GREATER_EQUAL , rhs = 1 , name = "serveDP" + str ( j ) + "Time1")

#second time period
for j in range(noDP):
	constExpr = LinExpr()
	for i in range(noFC):
		curVar = myVars[i][j][2]
		constExpr += kfcVars[i][0] * curVar
		constExpr += kfcVars[i][1] * curVar
		constExpr += kfcVars[i][2] * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.GREATER_EQUAL , rhs = 1 , name = "serveDP" + str ( j ) + "Time2")

myModel.update()
#write model to file
myModel.write(filename = "hw11.lp")

#optimize
myModel.optimize()

# print optimal objective and optimal solution
print("\nOptimal Objective: " + str( myModel.ObjVal))

print("\nOptimal Solution:" )
allVars = myModel.getVars()
for curVar in allVars:
	print(curVar.varName + " " + str( curVar.x))

"""
#FCs opened at each time period (from above optimization)
#k = 0, FC = 6
#k = 1, FC = 1
#k = 2, FC = 9

#assignments (from above optimization)
assgns0 = [0 for j in range (noDP)]
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

assgns1 = [0 for j in range (noDP)]
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

assgns2 = [0 for j in range (noDP)]
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

#plot locations of FCs and DPs
for fc in range( noFC ):
    matplotlib.pyplot.plot( fcs[ fc ][ 0 ]  , fcs[ fc ][ 1 ] , 'ro' , color = "green" , lw = 9 )

for dp in range( noDP ):
    matplotlib.pyplot.plot( dps[ dp ][ 0 ]  , dps[ dp ][ 1 ] , 'ro' , color = "red" , lw = 9 )
#plot connections for serviced DP from each servicing FC (can adjust assgns0 for appropraite time period)
for dp in range( nodps ):
    dpx = dps[ dp ][ 0 ]
    dpy = dps[ dp ][ 1 ]
    fcx = fcs[ assgns0[ dp ] ][ 0 ]
    fcy = fcs[ assgns0[ dp ] ][ 1 ]
    matplotlib.pyplot.plot( [ dpx , fcx ], [ dpy , fcy ]  , color = "black"  )
"""

