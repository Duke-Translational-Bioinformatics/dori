# model_d.R
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

# Tabular Data
age_brks = c(
   0,
  56,57,58,60,61,
  62,63,64,66,67,
  68,69,70,72,73,
  74,75,76,78,79,
  80,81,82,84,85,
  86,87,88,89,90,
  92,93,94
);
age_vals = 0:33;
sbp_brks = c(0, 120, 140, 160, 180);
sbp_vals = c(0,   1,   2,   3,   5);
risks = c(
   8,
   9,10,10,11,12,
  13,15,16,17,19,
  20,22,24,26,28,
  30,32,35,37,40,
  43,46,49,52,55,
  58,61,65,68,71,
  75,78,80
);
risks = risks / 100.0;
tabular = list(
  age_brks = age_brks,
  age_vals = age_vals,
  sbp_brks = sbp_brks,
  sbp_vals = sbp_vals,
  diab   = 4,
  smoker = 5,
  chf_mi = 6,
  murmur = 4,
  lvh    = 2,
  risks = risks
);

save(tabular, file = "model_table_d.Rdata");

# accepts a dataframe argument
model_df = function (patients) {
  load("model_table_d.Rdata");
  
  # apply a lambda function to each row
  stroke_risk = apply(patients, 1, function(patient) {
    # set score to zero (plus one to account for R language offset)
    score = 1;
    
    # age
    score = score + tabular$age_vals[max(which(patient['age'] >= tabular$age_brks))];
    
    # sbp
    score = score + tabular$sbp_vals[max(which(patient['sbp'] >= tabular$sbp_brks))];
    
    # other factors
    score  = score + tabular$diab   *   patient['diab'];
    score  = score + tabular$smoker * patient['smoker'];
    score  = score + tabular$chf_mi * patient['chf_mi'];
    score  = score + tabular$murmur * patient['murmur'];
    score  = score + tabular$lvh    *    patient['lvh'];
    
    # assess risk
    return(tabular$risks[score])
  });
  
  patients = cbind(patients, stroke_risk);
  
  # return the newly calculated risk column
  return(patients$stroke_risk)
}

save(model_df, file = "model_df_d.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_d.Rdata");
  age    = patient[1];
  sbp    = patient[2];
  diab   = patient[3];
  chf_mi = patient[4];
  smoker = patient[5];
  murmur = patient[6];
  lvh    = patient[7];
  
  # put the vectors into a dataframe
  patient.df = data.frame(age, sbp, diab, chf_mi, smoker, murmur, lvh);
  
  # computes the risk
  risk = model_df(patient.df);
  return(risk[1])
}

# store the vector model
save(model, file = "model_d.Rdata")

# the test patient from the paper, should have a risk of 19% using point system
testpat = c(75,150,0,0,0,0,0)
model(testpat)