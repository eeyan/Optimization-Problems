from gurobipy import *
import csv

# import cost data - CSV file with no header and costs replacing referees stated preferences
# costs were implemented as "yes" = 1, "maybe" = 2, "no" = 5, and "conflict" was set to have a cost of 1000 to ensure it wouldn't be a chosen decision in the optimal solution
with open('hw10_data.csv', 'rb') as csvfile:
    costs = [list(map(int,rec)) for rec in csv.reader(csvfile, delimiter=',')]

noPapers = len(costs)
noReferees = len(costs[0])

# create model
myModel = Model("hw10")

# create variables
myVars = [ [0 for i in range ( noPapers )] for j in range (noReferees) ]

for i in range( noReferees ):
	for j in range ( noPapers ):
		curVar = myModel.addVar (vtype = GRB.BINARY, name = "x" + str( i ) + "-" + str( j ))
		myVars[i][j] = curVar

myModel.update()

# objective function
objExpr = LinExpr()
for i in range( noReferees ):
	for j in range ( noPapers ):
		curVar = myVars[i][j]
		objExpr += costs[j][i] * curVar

myModel.setObjective ( objExpr , GRB.MINIMIZE )
myModel.update()

# constraints - each referee gets 10 or 11 papers
for i in range(noReferees):
	constExpr = LinExpr()
	for j in range(noPapers):
		curVar = myVars[i][j]
		constExpr += 1 * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.GREATER_EQUAL , rhs = 10 , name = "minPapers" + str ( i ))

for i in range(noReferees):
	constExpr = LinExpr()
	for j in range(noPapers):
		curVar = myVars[i][j]
		constExpr += 1 * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.LESS_EQUAL , rhs = 11 , name = "maxPapers" + str( i ))


# constraints - each paper gets at least 3 referees
for j in range(noPapers):
	constExpr = LinExpr()
	for i in range(noReferees):
		curVar = myVars[i][j]
		constExpr += 1 * curVar
	myModel.addConstr(lhs = constExpr , sense = GRB.GREATER_EQUAL , rhs = 3 , name = "minReferees" + str ( j ))


#write model to file
myModel.write(filename = "testOutput.lp")

#optimize
myModel.optimize()

# print optimal objective and optimal solution

print("\nOptimal Objective: " + str( myModel.ObjVal))
print("\nOptimal Solution:" )
allVars = myModel.getVars()
for curVar in allVars:
	print(curVar.varName + " " + str())