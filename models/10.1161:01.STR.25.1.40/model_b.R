# model_b.R
# by Ted Morin
# 
# contains a function to predict 10-year Stroke Risk using point system from
# 10.1161/01.STR.25.1.40
# 1994 Stroke Risk Profile: Adjustment for Antihypertensive Medication
#
# (Tables 2 and 3)
#
# function expects parameters:
# "ismale"  "age"   "Systolic BP" "Hypertensive Medication Use" "Cardiovascular Disease" "Left Ventricular Hypertrophy" "Cigarettes" "Atrial Fibrillation" "Diabetic"
#           years        mg/dL        
#   bool   int/float    int/float             bool                      bool                        bool                     bool            bool            bool

# male data (Table 2)
age_brks = c(54, 57,60,63, 66, 69, 73, 76, 79, 82, 85);
age_vals = c( 0,  1, 2, 3,  4,  5,  6,  7,  8,  9, 10);
treated_brks   = c(97, 106, 113, 118, 124, 130, 136, 143, 151, 162, 177);
untreated_brks = c(97, 106, 116, 126, 136, 146, 156, 166, 176, 186, 196);
sbp_vals       = c( 0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10);
diab = 2;
cig = 3;
cvd  = 4;
af   = 4;
lvh  = 5;
risks = c(
  3, 3, 4, 4, 5,
  5, 6, 7, 8,10,
 11,13,15,17,20,
 22,26,29,33,37,
 42,47,52,57,63,
 68,74,79,84,88
);
risks = risks / 100.0;
male = list(
  age_brks = age_brks,
  age_vals = age_vals,
  treated_brks = treated_brks,
  untreated_brks = untreated_brks, 
  sbp_vals = sbp_vals,
  diab = diab,
  cig = cig,
  cvd = cvd,
  af = af,
  lvh = lvh,
  risks = risks
);

# female data (Table 3)
age_brks = c(54, 57,60,63, 65, 68, 71, 74, 77, 79, 82);
age_vals = c( 0,  1, 2, 3,  4,  5,  6,  7,  8,  9, 10);
treated_brks   = c( 0,  95, 107, 114, 120, 126, 132, 140, 149, 161, 205);
untreated_brks = c( 0,  95, 107, 119, 131, 144, 156, 168, 181, 193, 205);
sbp_vals       = c( 0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10);
diab = 3;
cig = 3;
cvd  = 2;
af   = 6;
lvh  = 4;
risks = c(
   1, 1, 2, 2, 2,
   3, 4, 4, 5, 6,
   8, 9,11,13,16,
  19,23,27,32,37,
  43,50,57,64,71,
  78,84
);
risks = risks / 100.0;
female = list(
  age_brks = age_brks,
  age_vals = age_vals,
  treated_brks = treated_brks,
  untreated_brks = untreated_brks, 
  sbp_vals = sbp_vals,
  diab = diab,
  cig = cig,
  cvd = cvd,
  af = af,
  lvh = lvh,
  risks = risks
);

save(list = c('female', 'male'), file = "model_b_table.Rdata");

# accepts a dataframe argument
model_df = function (patients) {
  # load table
  load("model_b_table.Rdata");
  
  # apply a lambda function to each row
  stroke_risk = apply(patients, 1, function(patient) {
    # set score to zero
    score = 0;
    
    # select gender
    if (patient['ismale']) { 
      tables = male;
    }
    else {
      tables = female;
    };
    
    # age
    score = score + tables$age_vals[max(which(patient['age'] > tables$age_brks))];
    
    # sbp
    if (patient['hrx']) {
      score = score + tables$sbp_vals[max(which(patient['sbp'] > tables$treated_brks))];
    }
    else {
      score = score + tables$sbp_vals[max(which(patient['sbp'] > tables$untreated_brks))];
    };
    
    # diabetes
    if (patient['diab']){ score = score + tables$diab; };
    
    # cigarette smoking
    if (patient['cig']){ score = score + tables$cig;};
    
    # cardiovascular disease
    if (patient['cvd']){ score = score + tables$cvd; };
    
    # Atrial Fibrillation
    if (patient['af']){ score = score + tables$af; };
    
    # Left Ventricular Hypertrophy
    if (patient['lvh']){ score = score + tables$lvh; };
    
    # assess risk
    return(tables$risks[score])
  });
  
  patients = cbind(patients, stroke_risk);
  
  # return the newly calculated risk column
  return(patients$stroke_risk)
}

save(model_df, file = "model_df_b.Rdata")

# accepts a VECTOR argument
model = function (patient) {
  load("model_df_b.Rdata");
  ismale = patient[1];
  age    = patient[2];
  sbp    = patient[3];
  hrx    = patient[4];
  cvd    = patient[5];
  lvh    = patient[6];
  cig    = patient[7];
  af     = patient[8];
  diab   = patient[9];
  # put the vectors into a dataframe
  patient.df = data.frame(age, sbp, hrx, cvd, lvh, cig, af, diab, ismale);
  # computes the risk
  risk = model_df(patient.df);
  return(risk[1])
}

save(model, file = "model_b.Rdata")

# the test patient from the paper, should have a risk of 19% using point system
testpat = c(0,70,135,1,1,0,1,0,0)
model(testpat)