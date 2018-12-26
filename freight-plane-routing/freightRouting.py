from gurobipy import *

# initialize  data
noDays = 5
noPorts = 3
noRoutes = noPorts ** 2
noAircraft = 1200
ports = ["A", "B", "C"]
week = ["Mon", "Tues", "Wed", "Thurs", "Fri"]


#cost for not moving cargo
stationaryCost = 10

#cost for moving empty aircraft
# format: cost = emptyCosts[starting aiport][ending airport]
# example: cost for A to B is emptyCosts[0][1]
emptyCosts =[[0,7,3],[7,0,6],[3,6,0]]


#initializing demand arrays
demand = [[[0 for k in range( noDays )] for j in range( noPorts )] for k in range( noPorts)]

demand[0][1] = [100,200,100,400,300]
demand[0][2] = [50,50,50,50,50]
demand[1][0] = [25,25,25,25,25]
demand[1][2] = [25,25,25,25,25]
demand[2][0] = [40,40,40,40,40]
demand[2][1] = [400,200,300,200,400]

# create model
myModel = Model()

# create decision variables

# number of loaded aircraft from i to j on day k
x = [[[0 for k in range( noDays )] for i in range( noPorts )] for j in range( noPorts )]
for i in range( noPorts ):
	for j in range( noPorts ):
		for k in range( noDays ):
			x[i][j][k] = myModel.addVar(vtype = GRB.CONTINUOUS, name = "x-" + week[k] + "-" + ports[i] + ports[j])
myModel.update()

#number of empty aircraft from i to j on day k
y = [[[0 for k in range( noDays )] for i in range( noPorts )] for j in range( noPorts )]
for i in range( noPorts ):
	for j in range( noPorts ):
		for k in range( noDays ):
			y[i][j][k] = myModel.addVar(vtype = GRB.CONTINUOUS, name = "y-" + week[k] + "-" + ports[i] + ports[j])
myModel.update()

# cargo remaining stationary at i, that is bound for j, on day k
z = [[[0 for k in range( noDays )] for i in range( noPorts )] for j in range( noPorts )]
for i in range( noPorts ):
	for j in range( noPorts ):
		for k in range( noDays ):
			z[i][j][k] = myModel.addVar(vtype = GRB.CONTINUOUS, name = "z-" + week[k] + "-" + ports[i] + ports[j])
myModel.update()

# create objective function
objExpr = LinExpr()
for i in range( noPorts ):
	for j in range ( noPorts ):
		for k in range ( noDays ):
			objExpr += ( 10 * z[i][j][k] ) + ( emptyCosts[i][j] * y[i][j][k] )
myModel.setObjective ( objExpr , GRB.MINIMIZE )
myModel.update()

# create constraints

# always have given number ( noAircraft ) of total aircraft on each day
for k in range( noDays ):
	constExpr = LinExpr()
	for i in range( noPorts ):
		for j in range( noPorts ):
			constExpr += x[i][j][k]
			constExpr += y[i][j][k]
	myModel.addConstr(lhs = constExpr , sense = GRB.EQUAL , rhs = noAircraft , name = "totalAircraft" + week[k])
myModel.update()

# flow balance for aircraft
# outgoing aircraft at time k (both x and y) have to equal arriving aircraft from time k-1
for k in range( noDays ):
	for i in range( noPorts ):
		constExpr = LinExpr()
		for j in range( noPorts ):
			constExpr += x[i][j][k] + y[i][j][k] - x[j][i][k-1] - y[j][i][k-1]
		myModel.addConstr(lhs = constExpr , sense = GRB.EQUAL , rhs = 0 , name = "aircraftFlow" + week[k] + ports[i])
myModel.update()

# flow balance for cargo
# stationary cargo on day k, bound for j from i, is equal to new demand from i to j on day k plus carryover demand from previous day minus shipped cargo that day
for k in range( noDays ):
	for i in range( noPorts ):
		for j in range( noPorts ):
			constExpr = LinExpr()
			constExpr += demand[i][j][k] + z[i][j][k-1] - x[i][j][k] - z[i][j][k]
			myModel.addConstr(lhs = constExpr , sense = GRB.EQUAL , rhs = 0 , name = "cargoFlow" + week[k] + ports[i] + ports[j])
myModel.update()

# write model to file
myModel.write(filename = "final.lp")

# optimize
myModel.optimize()

# print optimal objective value and optimal solution
print("\nOptimal Objective: " + str( myModel.ObjVal ))

"""
print("\nOptimal Solution:" )
allVars = myModel.getVars()
for curVar in allVars:
	print(curVar.varName + " " + str( curVar.x ))
"""