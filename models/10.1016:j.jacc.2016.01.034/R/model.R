#######################################################################################################################
# model.R
# by Ted Morin
# based on Score_new_data_in_R.R by Ben Neely
#
# calculates a single risk score risk scores based on trilogy_R_objects.Rdata

# computes risk scores from a database
model.df = function(newdatt) {
  # time at which risk is evaluated in output
  t = 900;
  load("trilogy_R_objects.Rdata");
  
  #Only 1 row of data - this is all we need for our APP!, reconsider linear algebra if >1
  same              <- intersect(names(newdatt),names(trilogy_R_objects$coef));
  same2             <- intersect(names(trilogy_R_objects$referencePoints),names(trilogy_R_objects$coef));
  
  # this calculation is done in accordance with the PMML Specification
  r                 <- as.matrix(newdatt[same])                %*% as.matrix(trilogy_R_objects$coef[same]);
  s                 <- t(as.matrix(trilogy_R_objects$referencePoints[same2]))  %*% as.matrix(trilogy_R_objects$coef[same2]);
  H_t               <- trilogy_R_objects$cumulativeHazard*exp(r-s);
  S_t               <- exp(-H_t);
  final_scored      <- data.frame("risk"=1-S_t,"time"=trilogy_R_objects$time);
  #At time 900:
  return(tail(final_scored[which(final_scored$time<=900),])$risk[1])
}

# converts a single input vector into a database for model.df
model = function (input) {
  #new data entered programatically 
  newdatt <- data.frame(cbind("CREATCN_IMP"=input[1],
                              "creatcn_imp85"=input[2], 
                              "N_PPIRD"=input[3],
                              "N_STATINRD"=input[4],
                              "NSTEMI"=input[5],
                              "KILLIP1_IMP"=input[6],
                              "AGEYR"=input[7],
                              "N_MHDIAB_IMP"=input[8],
                              "N_MHHYP_IMP"=input[9],
                              "N_MHCAD_IMP"=input[10],
                              "N_CANGIO_IMP"=input[11],
                              "SMOKE30_IMP"=input[12],
                              "N_MHHLP_IMP"=input[13],
                              "N_MHPAD_IMP"=input[14],                  
                              "N_MHPMI_IMP"=input[15],
                              "N_MHCHF_IMP"=input[16],
                              "N_MHPPCI_IMP"=input[17],
                              "N_MHPCABG_IMP"=input[18]
  ));
  return(model.df(newdatt));
}

# test (should give 0.5364669)
model(c(1.5, 0.65, 1, 1,1,1,85,1,1,0,0,1,1,0,1,0,1,0))