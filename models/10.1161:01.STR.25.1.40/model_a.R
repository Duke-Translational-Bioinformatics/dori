# model_a.R
# by Ted Morin
# 
# contains a function to predict 10-year Stroke Risk using beta coefficients from
# 10.1161/01.STR.25.1.40
# 1994 Stroke Risk Profile: Adjustment for Antihypertensive Medication
#
# (Table 1)
#
# function expects parameters:
# "ismale"  "age"   "Systolic BP" "Hypertensive Medication Use" "Cardiovascular Disease" "Left Ventricular Hypertrophy" "Cigarettes" "Atrial Fibrillation" "Diabetic"
#           years        mg/dL        
#   bool   int/float    int/float             bool                      bool                        bool                     bool            bool            bool

# accepts a dataframe argument
model_df = function(patients) {
  
  # cox beta coefficients (Table 1)
  male_betas = c(
    0.0488,  # Age
    0.0152,  # SBP
    0.00019, # NEWHRXSBP
    0.5460,  # CVD
    0.7864,  # LVH
    0.5224,  # Cigs
    0.5998,  # AF
    0.3429   # Diabetes
  );
  female_betas = c(
    0.0699,   # Age
    0.0161,   # SBP
    0.00026,  # NEWHRXSBP
    0.4404,   # CVD
    0.8055,   # LVH
    0.5419,   # Cigs
    1.1173,   # AF
    0.5604    # Diabetes
  );
  
  # # S0 values, by sex and age range
  # male_S0 = c(
  #   0.059,
  #   0.078,
  #   0.110,
  #   0.137,
  #   0.180,
  #   0.223
  # );
  # female_S0 = c(
  #   0.030,
  #   0.047,
  #   0.072,
  #   0.109,
  #   0.155,
  #   0.239
  # );
  
  # S0 by sex only (Table 4 and unlabeled s(t) values from 10.1161:01.STR.22.3.312)
  male_s0   = 0.9044;
  female_s0 = 0.9353;
  
  # # average qualities for computing xbar(from 10.1161:01.STR.22.3.312, Table 2)
  # male_vals = c(
  #   65.4,  # Age
  #   139.3, # SBP
  #   0.161, # Antihypertensive Treatment
  #   0.222, # CVD
  #   0.035, # LVH
  #   0.338, # Cigs
  #   0.028, # AF
  #   0.106  # Diab
  # );
  # female_vals = c(
  #   66.1,  # Age
  #   142.8, # SBP
  #   0.250, # Antihypertensive Treatment
  #   0.142, # CVD
  #   0.029, # LVH
  #   0.264, # Cigs
  #   0.022, # AF
  #   0.079  # Diab
  # );
  
  # xbar
  # values COULD NOT BE DETERMINED because the paper 
  # does not record the average value of "NEWHRXSBP".
  # values derived from the average values in 
  # 10.1161:01.STR.22.3.312 are shown as comments, but 
  # disagree with the sample patient in the paper.
  # The female xbar was derived from the example patient in the
  # paper, but the program is not otherwise tested.
  male_xbar = 1;#5.74173362090000072299744715564884245395660400390625;
  female_xbar = 7.255348;#7.3392304999999993242454365827143192291259765625;
  
  
  # store gender separately
  ismale = as.logical(patients$ismale);
  patients$ismale = NULL;
  
  # turn the patients into a matrix
  patients = as.matrix(patients);
  
  # put NEWHRXSBP in the HRX column
  patients[which(110 < patients[,2] && patients[,2] < 200),3] = patients[,3]*(patients[,2] - 110)*(200 - patients[,2]);
  patients[which(!(110 < patients[,2] && patients[,2] < 200)),3] = 0;
  
  # produce the appropriate betas into a matrix
  l = length(ismale);
  male_betas = matrix(data=rep(male_betas,l),nrow=l,byrow=TRUE);
  betas      = matrix(data=rep(female_betas,l),nrow=l,byrow=TRUE);
  betas[which(ismale),] = male_betas[which(ismale),];
  
  # produce s0 and xbar vectors
  s0 = rep(female_s0,l);
  xbar = rep(female_xbar,l);
  s0[which(ismale)] = male_s0;
  xbar[which(ismale)] = male_xbar;
  
  # dot the betas 
  x = sum(betas*patients); #sum((betas*patients)[1:l,]);
  
  # return the risk vector
  risk = 1 - s0**exp(x-xbar);
  return(risk)
}

save(model_df, file="model_df_a.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_a.Rdata");
  ismale = patient[1];
  age    = patient[2];
  sbp    = patient[3];
  hrx    = patient[4];
  cvd    = patient[5];
  lvh    = patient[6];
  cigs   = patient[7];
  af     = patient[8];
  diab   = patient[9];
  # put the vectors into a dataframe
  patient.df = data.frame(age, sbp, hrx, cvd, lvh, cigs, af, diab, ismale);
  # computes the risk
  risk = model_df(patient.df);
  return(risk[1])
}

save(model, file = "model_a.Rdata")

# # for deriving xbar values
# sprintf('%.100f', model(c(1,male_vals)));
# sprintf('%.100f', model(c(0,female_vals)))

# the test patient from the paper
testpat = c(0,70,135,1,1,0,1,0,0)
model(testpat)
