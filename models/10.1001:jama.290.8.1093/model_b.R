# model_b.R
# by Ted Morin
# 
# contains a function to predict 5-year Stroke or Death Risk for patients with new-onset AF using beta coefficients from
# 10.1001/jama.290.8.1093
# 2003 A Risk Score for Predicting Stroke or Death in Individuals With New-Onset Atrial Fibrillation in the Community
#
# Warfarin censored (Table 2, far-right)
#
# function expects parameters:
#  "age"   "Systolic BP" "Diabetes Mellitus" "History of CHF or MI" "Cigarette Smoking" "Significant Murmur" "Left Ventricular Hypertrophy"
#   years        mg/dL        
#  int/float    int/float         bool                bool                 bool                bool                        bool

# accepts a dataframe argument
model_df = function(patients) {
  
  # produce stroke risks for each patient via lambda function
  stroke_risk = apply(patients, 1, function(patient) {
    
    # cox beta coefficients and s0 (from spreadsheet on FHS website)
    betas = data.frame(
      age    = c(0.075673),
      sbp    = c(0.006062),
      diab   = c(0.333309),
      chf_mi = c(0.503179),
      cig    = c(0.492189),
      vhd    = c(0.355479),
      lvh    = c(0.167387)
    );
    betas = as.matrix(betas);
    s0 = 0.522500; 
    
    # dot the betas and the patient data 
    same = intersect(names(patient),   names(betas));
    x = betas * patient;
    x    = sum(x);
    
    # xbar value (from spreadsheet)
    xbar = 6.9394616667;
    
    # return the risk vector
    risk = 1 - s0**exp(x-xbar);
    return(risk)
    
  });
  patients = cbind(patients, stroke_risk);
  return(patients$stroke_risk)
}

# store the df model
save(model_df, file="model_df_b.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_b.Rdata");
  age    = patient[1];
  sbp    = patient[2];
  diab   = patient[3];
  chf_mi = patient[4];
  cig    = patient[5];
  vhd    = patient[6];
  lvh    = patient[7];
  
  # put the vectors into a dataframe
  patient.df = data.frame(age, sbp, diab, chf_mi, cig, vhd, lvh);
  
  # computes the risk
  risk = model_df(patient.df);
  return(risk[1])
}

# store the vector model
save(model, file = "model_b.Rdata")

# # test code
# testpat = c(70,120,0,0,0,0,0)
# model(testpat)