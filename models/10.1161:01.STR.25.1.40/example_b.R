# exapmle_b.R
# by Ted Morin
# 
# contains an example code for predicting 10-year Stroke Risk using point system from
# 10.1161/01.STR.25.1.40
# 1994 Stroke Risk Profile: Adjustment for Antihypertensive Medication

# load the function
load('model_b.Rdata')

# create a test patient (sample patient from the paper)
testpat = c(0,70,135,1,1,0,1,0,0)

# calculate single patient risk score
model(testpat)