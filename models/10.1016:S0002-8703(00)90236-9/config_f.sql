INSERT INTO models (DOI, papertitle, modeltitle, yearofpub, authors, must, mustnot, mustCUI, mustnotCUI, inpname, inpdesc, inpCUI, inpunits, inpdatatype, upper, lower, output, outcome, outcometime, outputCUI, outcomeCUI, filename, filepointer, datumname, datum, language, uncompiled, compiled, dependList, example, model_category, type, metric, value, lcl, ucl, numofinputs) VALUES ('10.1016/S0002-8703(00)90236-9', 'Primary and subsequent coronary risk appraisal: New results from The Framingham Study', 'Subsequent CHD, point system', '2000', '["D''Agostino, R.B.", "Russell, M.W."]', '["Coronary Heart Disease"]', '[""]', '["C0018802"]', '[""]', '["sex", "age", "total cholesterol", "hdl cholesterol", "systolic BP", "diabetes", "Cigarette Smoking"]', '["sex", "age", "total cholesterol", "hdl cholesterol", "systolic BP", "diabetes", "Cigarette Smoking"]', '["C0086582", "C0804405", "C0364708", "C0364221", "C0488055", "C1315719", "C3173717"]', '["male=T", "years", "mg/dL", "mg/dL", "mmHg", "", ""]', '["bool", "float", "float", "float", "float", "bool", "bool"]', '["", "74", "", "", "", "", ""]', '["", "35", "", "", "", "", ""]', '', 'Coronary Heart Disease', '2', '', 'C0018802', '[""]', '[""]', '["Sample Size"]', '["1176"]', 'python', '["model_f.py"]', '[""]', 'requirements.txt', '["example_f.py"]', '["prognostic"]', '[]', '[]', '[]', '[]', '[]', '7')