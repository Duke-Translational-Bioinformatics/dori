# example_d.R
# by Ted Morin
# 
# contains a function to predict 5-year Stroke or Death Risk for patients with new-onset AF using point system from
# 10.1001/jama.290.8.1093
# 2003 A Risk Score for Predicting Stroke or Death in Individuals With New-Onset Atrial Fibrillation in the Community
#
# Figure 2
#
# function expects parameters:
#  "age"   "Systolic BP" "Diabetes Mellitus" "History of CHF or MI" "Cigarette Smoking" "Significant Murmur" "Left Ventricular Hypertrophy"
#   years        mg/dL        
#  int/float    int/float         bool                bool                 bool                bool                        bool

# load the model
load('model_d.Rdata')


# testpatient1
testpat = c(70, 120, 0, 0, 0, 0, 0)
model(testpat)
# testpatient2
testpat = c(65, 130, 0, 0, 0, 0, 0)
model(testpat)
# testpatient3
testpat = c(65, 130, 0, 1, 0, 0, 0)
model(testpat)
# testpatient4
testpat = c(65, 130, 1, 1, 0, 0, 0)
model(testpat)
# testpatient5
testpat = c(65, 130, 0, 0, 0, 1, 1)
model(testpat)