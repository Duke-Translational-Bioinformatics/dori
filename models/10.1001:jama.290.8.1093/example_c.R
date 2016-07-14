# model_c.R
# by Ted Morin
# 
# contains a function to predict 5-year Stroke Risk for patients with new-onset AF using point system from
# 10.1001/jama.290.8.1093
# 2003 A Risk Score for Predicting Stroke or Death in Individuals With New-Onset Atrial Fibrillation in the Community
#
# Figure 1
#
# function expects parameters:
# "ismale"  "age"   "Systolic BP" "Diabetes Mellitus" "Previous History of Stroke"
#           years        mg/dL        
#   bool   int/float    int/float         bool                bool


# load the model
load('model_c.Rdata')


# testpatient1
testpat = c(0,70,120,0,0) # 70-year-old woman with 120 mmHg sbp
model(testpat)
# testpatient2
testpat = c(0,70,130,0,0) # 70-year-old woman with 130 mmHg sbp
model(testpat)
# testpatient3
testpat = c(1,90,140,1,0) # 90-year-old man with 140 mmHg sbp and diabetes!
model(testpat)
# testpatient4
testpat = c(0,55,140,0,1) # 55-year-old woman with 140 mmHg sbp and History of Stroke
model(testpat)
# testpatient5
testpat = c(1,65,140,0,0) # 65-year-old man with 140 mmHg sbp
model(testpat)