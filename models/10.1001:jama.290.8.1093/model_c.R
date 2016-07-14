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

# Tabular Data
age_brks = c(55, 60, 63, 67, 72, 75, 78, 82, 86, 91, 94);
age_vals = c( 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10);
sbp_brks = c(0, 120, 140, 160, 180);
sbp_vals = c(0,   1,   2,   3,   4);
diab   = 5;
stroke = 6;
female = 6;
risks = c(
   5,
   5, 6, 6, 7, 8, 
   9, 9,11,12,13,
  14,16,18,19,21,
  24,26,28,31,34,
  37,41,44,48,51,
  55,59,63,67,71,
  75
);
risks = risks / 100.0;
tabular = list(
  age_brks = age_brks,
  age_vals = age_vals,
  sbp_brks = sbp_brks,
  sbp_vals = sbp_vals,
  diab   = diab,
  stroke = stroke,
  female = female,
  risks = risks
);

save(tabular, file = "model_table_c.Rdata");

# accepts a dataframe argument
model_df = function (patients) {
  load("model_table_c.Rdata");
  
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
    score  = score + tabular$stroke * patient['stroke'];
    score  = score + tabular$female * patient['female'];
    
    # assess risk
    return(tabular$risks[score])
  });
  
  patients = cbind(patients, stroke_risk);
  
  # return the newly calculated risk column
  return(patients$stroke_risk)
}

save(model_df, file = "model_df_c.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_c.Rdata");
  ismale = patient[1];
  age    = patient[2];
  sbp    = patient[3];
  diab   = patient[4];
  stroke = patient[5];
  
  # convert "ismale" to "female"
  female = as.numeric(!ismale);
  
  # put the vectors into a dataframe
  patient.df = data.frame(female, age, sbp, diab, stroke);
  
  # computes the risk
  risk = model_df(patient.df);
  return(risk[1])
}

# store the vector model
save(model, file = "model_c.Rdata")

# # the test patient from the paper, should have a risk of 19% using point system
# testpat = c(1,75,150,1,0)
# model(testpat)