# model_a.R
# by Ted Morin
# 
# contains a function to predict 5-year Stroke Risk for patients with new-onset AF using beta coefficients from
# 10.1001/jama.290.8.1093
# 2003 A Risk Score for Predicting Stroke or Death in Individuals With New-Onset Atrial Fibrillation in the Community
#
# Warfarin censored (Table 2, mid-left)
#
# function expects parameters:
# "ismale"  "age"   "Systolic BP" "Diabetes Mellitus" "Previous History of Stroke"
#           years        mg/dL        
#   bool   int/float    int/float         bool                bool

# accepts a dataframe argument
model_df = function(patients) {
  
  # produce stroke risks for each patient via lambda function
  stroke_risk = apply(patients, 1, function(patient) {
    
    # cox beta coefficients and s0 (from spreadsheet on FHS website)
    betas = data.frame(
      female = c(0.650715),
      age    = c(0.029065),
      sbp    = c(0.006130),
      diab   = c(0.589268),
      stroke = c(0.631572)
    );
    betas = as.matrix(betas);
    s0 = 0.857100; 
    
    # dot the betas and the patient data 
    same = intersect(names(patient),   names(betas));
    x = betas * patient;
    x    = sum(x);

    # # for initial calculation of xbar
    # # values used to compute xbar value
    # xbar_vals = c(
    #   0.4765957,
    #   74.9205674,
    #   145.9106383,
    #   0.1531915,
    #   0.1446809
    # );
    # xbar = betas[1,] * xbar_vals;
    # xbar = sum(xbar);
    
    # xbar value
    xbar = 3.5637737293822997486358872265554964542388916015625;
    
    # return the risk vector
    risk = 1 - s0**exp(x-xbar);
    return(risk)
    
  });
  patients = cbind(patients, stroke_risk);
  return(patients$stroke_risk)
}

# store the df model
save(model_df, file="model_df_a.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_a.Rdata");
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
save(model, file = "model_a.Rdata")

# # test code
# testpat = c(0,70,120,0,0)
# model(testpat)