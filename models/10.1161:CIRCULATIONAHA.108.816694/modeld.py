 # Ted Morin's comments
################################################################## NOT CHECKED
"""
model.py
by Ted Morin

contains a function to predict 30-year CVD risks using method from 
10.1161/CIRCULATIONAHA.108.816694
2009 Predicting the Thirty-year Risk of Cardiovascular Disease
The Framingham Heart Study

function expects parameters of
"isMale"  "Age"   "Systolic BP"     "antihypertensive medication use" "Smoker" "Diabetic"   "BMI"
          years     mm Hg   
  bool  int/float  int/float                     bool                   bool      bool    int/float  
  
model translated from javascript from Mayo Clinic Rochester, original comments below:
"""
 # original comments
"""
/*
 * Project - CVHCWeb, Mayo Clinic Rochester
 * Created on Mar 30, 2011
 * 
 * These calculations are based on the framingham 30 year risk study located at
 * http://circ.ahajournals.org/cgi/content/short/CIRCULATIONAHA.108.816694v1 Specifically, these calculations are a
 * reverse engineering of the spreadsheet located at
 * http://circ.ahajournals.org/content/vol0/issue2009/images/data/CIRCULATIONAHA.108.816694/DC1/CI816694.DSriskcalculator.xls
 * 
 * SPECIAL NOTE:  As of 4/8/2011 there is a bug on the spreadsheet listed above regarding the normal risk scores.  These risk 
 *                scores do not take into account the difference between male/female.  This code has been updated to address
 *                this issue, however the spreadsheet may not.
 */
/*
 * Authors: Michael J. Pencina PhD, Ralph B. D'Agostino Sr PhD, Martin G. Larson ScD, Joseph M. Massaro PhD, and
 * Ramachandran S. Vasan MD.
 */
/*
 * Excel spreadsheet calculations have been translated to Java by Aaron Vaneps (Vaneps.Michael@mayo.edu), and I make no
 * guarantee that there are no bugs in the translation. Use at your own risk.
 */
"""
"""
    /**
     * Calculates the hard CVD risk which is the risk of coronary death, myocardial infarction and fatal or non-fatal
     * stroke.
     * 
     * @param age
     *            age of the patient, in years.
     * @param isMale
     *            true if patient is male, false if female
     * @param systolicBp
     *            systolic blood pressure
     * @param smoker
     *            true if patient smokes, false if not
     * @param treatedBp
     *            true if patient is taking medications to treat high blood pressure, false if not
     * @param diabetic
     *            true if patient is diabetic, false if not
     * @param BMI
     *            The BMI of the patient
     * @return 
     *         A JSON object with the risk percentages in the form of:
     *                {"risk" : -1.0, "optimalRisk": -1.0, "normalRisk": -1.0}
     *         Note that -1 means something went wrong, otherwise it will be the percent risk.
     */
"""
    
# original function name: calculateHardRiskBmiInternal
def model(isMale,  age, systolicBp, treatedBp, smoker, diabetic, BMI):
    import numpy as np
    E = [ 0.999886631, 0.999886631, 0.999886631, 0.999773182, 0.999659708, 0.999659708, 0.999546127,
                0.999546127, 0.999546127, 0.999432393, 0.999432393, 0.999318617, 0.999318617, 0.999318617, 0.999204687,
                0.999090701, 0.998976654, 0.998862521, 0.998862521, 0.998862521, 0.998748247, 0.998748247, 0.998633852,
                0.998519451, 0.998519451, 0.998519451, 0.998404804, 0.998290128, 0.998175404, 0.998175404, 0.998060641,
                0.998060641, 0.997945825, 0.997945825, 0.997945825, 0.997945825, 0.997830584, 0.997715315, 0.997600014,
                0.997600014, 0.997484514, 0.99736865, 0.997252699, 0.997136706, 0.997020685, 0.996904572, 0.996788278,
                0.996671866, 0.996671866, 0.996671866, 0.996555198, 0.996438383, 0.996321272, 0.996321272, 0.996321272,
                0.996203964, 0.996086546, 0.995969071, 0.995851565, 0.995734062, 0.995616498, 0.995498817, 0.995380944,
                0.995263001, 0.995144774, 0.995026507, 0.994908252, 0.994789805, 0.994789805, 0.994671351, 0.994552878,
                0.994434352, 0.994315831, 0.994315831, 0.99419721, 0.99419721, 0.99407826, 0.99407826, 0.99407826,
                0.99407826, 0.99395904, 0.993839803, 0.993720551, 0.99360128, 0.99360128, 0.99360128, 0.993481808,
                0.993362157, 0.993242397, 0.993122593, 0.993002761, 0.993002761, 0.993002761, 0.993002761, 0.993002761,
                0.992882535, 0.992762246, 0.99264195, 0.992521648, 0.992401329, 0.992281005, 0.992281005, 0.992160589,
                0.992160589, 0.992160589, 0.99203974, 0.99203974, 0.991918857, 0.991797937, 0.991676993, 0.991676993,
                0.991555951, 0.991434843, 0.991313727, 0.991192515, 0.991071279, 0.990950039, 0.990828723, 0.990707375,
                0.990585982, 0.990464374, 0.990464374, 0.990342716, 0.990342716, 0.990220903, 0.990099048, 0.989977186,
                0.989977186, 0.989854921, 0.989732647, 0.989732647, 0.989610111, 0.989487473, 0.989487473, 0.989364779,
                0.98924208, 0.98924208, 0.989119144, 0.988996138, 0.988996138, 0.988873103, 0.988750049, 0.988750049,
                0.988626871, 0.988503637, 0.988380392, 0.988256951, 0.988133448, 0.988009944, 0.988009944, 0.987885869,
                0.987761636, 0.987761636, 0.987637299, 0.98751293, 0.98751293, 0.987388451, 0.987263964, 0.987139413,
                0.987139413, 0.98701484, 0.98701484, 0.98701484, 0.986890087, 0.986765303, 0.986640488, 0.986640488,
                0.986640488, 0.986515077, 0.986389511, 0.986389511, 0.986263795, 0.986263795, 0.986137965, 0.98601208,
                0.985886201, 0.98576019, 0.98576019, 0.985634017, 0.985634017, 0.985634017, 0.985507597, 0.985381063,
                0.985381063, 0.985254334, 0.985254334, 0.98512748, 0.985000515, 0.984873438, 0.984873438, 0.984745896,
                0.984618336, 0.984490687, 0.984490687, 0.984490687, 0.984362302, 0.984233899, 0.984233899, 0.984233899,
                0.984105093, 0.984105093, 0.984105093, 0.983976102, 0.983976102, 0.983847024, 0.983717927, 0.983588774,
                0.983459603, 0.983330385, 0.983330385, 0.983200981, 0.983200981, 0.983200981, 0.983071492, 0.983071492,
                0.983071492, 0.982941761, 0.982941761, 0.982811954, 0.982682146, 0.982552337, 0.982422463, 0.982292552,
                0.982162645, 0.982162645, 0.98203268, 0.981902698, 0.981772697, 0.981772697, 0.981642525, 0.981642525,
                0.9815123, 0.981381991, 0.981381991, 0.981381991, 0.98125149, 0.98125149, 0.981120919, 0.980990204,
                0.980859435, 0.980728596, 0.980597723, 0.980597723, 0.980466721, 0.980335694, 0.980335694, 0.980204585,
                0.980204585, 0.980204585, 0.980072912, 0.980072912, 0.979941063, 0.979941063, 0.979809125, 0.979809125,
                0.979677039, 0.979677039, 0.979677039, 0.979544518, 0.979544518, 0.979411754, 0.97927891, 0.979146068,
                0.979146068, 0.979146068, 0.979012937, 0.979012937, 0.978879628, 0.978746282, 0.978612884, 0.978612884,
                0.978479426, 0.978345938, 0.978345938, 0.978345938, 0.978345938, 0.978212218, 0.978212218, 0.978212218,
                0.978212218, 0.978078262, 0.977944261, 0.977810249, 0.977676191, 0.977541958, 0.977541958, 0.977407567,
                0.977407567, 0.97727305, 0.97727305, 0.977138407, 0.977003739, 0.977003739, 0.976868743, 0.976868743,
                0.976868743, 0.976733635, 0.976733635, 0.976733635, 0.976598298, 0.97646287, 0.97646287, 0.97646287,
                0.976327021, 0.976191177, 0.976055221, 0.975919226, 0.975783081, 0.975783081, 0.975783081, 0.975646849,
                0.975510468, 0.975510468, 0.975373687, 0.97523687, 0.97523687, 0.975099949, 0.975099949, 0.975099949,
                0.975099949, 0.974962505, 0.974824557, 0.974686407, 0.974548241, 0.974410042, 0.974410042, 0.974410042,
                0.97427171, 0.974133299, 0.973994778, 0.973994778, 0.973856178, 0.973856178, 0.973717398, 0.973717398,
                0.973578516, 0.973439648, 0.973439648, 0.973439648, 0.973300605, 0.973300605, 0.973161525, 0.973022434,
                0.972883257, 0.972883257, 0.972744011, 0.972604209, 0.972604209, 0.972464256, 0.972464256, 0.972324226,
                0.972184203, 0.972044111, 0.971903893, 0.97176363, 0.971623176, 0.971623176, 0.971482518, 0.971341745,
                0.971200968, 0.971060168, 0.971060168, 0.970919097, 0.970778008, 0.970636925, 0.970636925, 0.970495752,
                0.970354576, 0.970213345, 0.97007185, 0.969930191, 0.969930191, 0.969930191, 0.969930191, 0.969787849,
                0.969645485, 0.969645485, 0.969502565, 0.969502565, 0.969359524, 0.96921647, 0.96921647, 0.969073343,
                0.969073343, 0.96892995, 0.968786516, 0.968786516, 0.968786516, 0.968642928, 0.968499275, 0.968499275,
                0.96835547, 0.96835547, 0.968211532, 0.96806746, 0.96806746, 0.967923011, 0.967778484, 0.967633838,
                0.967489096, 0.967344295, 0.967344295, 0.967199305, 0.967054247, 0.967054247, 0.967054247, 0.967054247,
                0.966909023, 0.966763748, 0.966763748, 0.966618372, 0.96647293, 0.966327499, 0.966181853, 0.966181853,
                0.966181853, 0.966181853, 0.966181853, 0.966035946, 0.966035946, 0.966035946, 0.966035946, 0.966035946,
                0.965889721, 0.965889721, 0.965889721, 0.965743193, 0.965743193, 0.965596538, 0.965596538, 0.965596538,
                0.965449652, 0.965302661, 0.965155673, 0.965155673, 0.965155673, 0.965008348, 0.965008348, 0.964860987,
                0.96471357, 0.964566105, 0.964418255, 0.964418255, 0.964270229, 0.964270229, 0.964121776, 0.963973267,
                0.963973267, 0.963824708, 0.963676126, 0.963527338, 0.963527338, 0.963527338, 0.963527338, 0.963378317,
                0.963378317, 0.963378317, 0.963378317, 0.963378317, 0.963228013, 0.963228013, 0.963228013, 0.963228013,
                0.963228013, 0.963077194, 0.962926222, 0.962775245, 0.962775245, 0.962624134, 0.962472922, 0.962472922,
                0.962321576, 0.962170232, 0.962018905, 0.962018905, 0.961867483, 0.961715912, 0.961564113, 0.961412277,
                0.961260103, 0.961260103, 0.961107719, 0.960955306, 0.960802878, 0.960650324, 0.960650324, 0.960497272,
                0.960344201, 0.960344201, 0.96019082, 0.96019082, 0.960037357, 0.959883868, 0.959730376, 0.959576293,
                0.959422205, 0.959422205, 0.959422205, 0.959268013, 0.959268013, 0.959113818, 0.958959575, 0.958805307,
                0.958805307, 0.958805307, 0.958805307, 0.958805307, 0.958805307, 0.958805307, 0.958649936, 0.958494531,
                0.958338879, 0.958338879, 0.958338879, 0.958338879, 0.958338879, 0.958182476, 0.958026046, 0.958026046,
                0.958026046, 0.958026046, 0.958026046, 0.958026046, 0.958026046, 0.958026046, 0.957868818, 0.957868818,
                0.957710727, 0.957710727, 0.957552481, 0.957394232, 0.957235893, 0.957077569, 0.957077569, 0.957077569,
                0.957077569, 0.956919028, 0.956760399, 0.956760399, 0.956601719, 0.956601719, 0.956601719, 0.956601719,
                0.956601719, 0.956442722, 0.956442722, 0.956442722, 0.95628345, 0.956123917, 0.956123917, 0.956123917,
                0.956123917, 0.956123917, 0.955964065, 0.955964065, 0.955964065, 0.955804077, 0.955804077, 0.955804077,
                0.95564368, 0.95564368, 0.955483108, 0.955483108, 0.955483108, 0.955322359, 0.955322359, 0.955161582,
                0.955000798, 0.955000798, 0.955000798, 0.95483988, 0.954678744, 0.954678744, 0.954517577, 0.954356365,
                0.954195104, 0.954033679, 0.953872235, 0.953710721, 0.953548984, 0.953548984, 0.953387126, 0.953387126,
                0.953387126, 0.953387126, 0.953387126, 0.953387126, 0.953223896, 0.953060098, 0.952896185, 0.952896185,
                0.952896185, 0.952896185, 0.952732197, 0.952568124, 0.952568124, 0.952568124, 0.952568124, 0.952403967,
                0.952403967, 0.95223979, 0.95223979, 0.952075393, 0.952075393, 0.951910724, 0.95174604, 0.951581366,
                0.951581366, 0.951416534, 0.951416534, 0.951416534, 0.951251446, 0.951086341, 0.950921236, 0.950921236,
                0.950755882, 0.950590373, 0.950590373, 0.950590373, 0.950590373, 0.950424544, 0.9502587, 0.9502587,
                0.950092454, 0.950092454, 0.949926185, 0.949926185, 0.949759845, 0.949593459, 0.949427029, 0.949260571,
                0.949260571, 0.94909406, 0.948927457, 0.948760844, 0.948760844, 0.948760844, 0.9485937, 0.9485937,
                0.9485937, 0.948426195, 0.948258687, 0.948090148, 0.947921452, 0.947752748, 0.947752748, 0.947752748,
                0.947752748, 0.947583266, 0.947583266, 0.947583266, 0.947413642, 0.947244, 0.947074234, 0.947074234,
                0.946904383, 0.946904383, 0.946904383, 0.946734379, 0.946734379, 0.946734379, 0.946734379, 0.946564224,
                0.946564224, 0.946393328, 0.94622234, 0.94622234, 0.94622234, 0.946051104, 0.946051104, 0.946051104,
                0.945879648, 0.945708192, 0.945708192, 0.945536623, 0.945365058, 0.945365058, 0.945365058, 0.945193265,
                0.945021368, 0.944849408, 0.944849408, 0.944849408, 0.944677296, 0.944505151, 0.944332945, 0.944160749,
                0.944160749, 0.944160749, 0.943988322, 0.943815788, 0.943815788, 0.943643103, 0.943470374, 0.943297567,
                0.943124698, 0.943124698, 0.943124698, 0.942951442, 0.942951442, 0.942777851, 0.942777851, 0.942604052,
                0.942604052, 0.942430067, 0.942256058, 0.942256058, 0.942256058, 0.942256058, 0.942256058, 0.942256058,
                0.942081356, 0.941906396, 0.941906396, 0.941731247, 0.941731247, 0.941556068, 0.941380854, 0.941380854,
                0.941205472, 0.941205472, 0.941029944, 0.940854441, 0.940854441, 0.9406787, 0.9406787, 0.9406787,
                0.9406787, 0.940502645, 0.940502645, 0.940502645, 0.940326317, 0.940149937, 0.939973454, 0.939796956,
                0.939796956, 0.939620305, 0.939620305, 0.939443421, 0.939266539, 0.939089645, 0.938912767, 0.938912767,
                0.938735464, 0.938735464, 0.938557783, 0.938379855, 0.938379855, 0.938379855, 0.938379855, 0.938379855,
                0.938379855, 0.938201375, 0.938022886, 0.937844404, 0.937844404, 0.937665695, 0.937665695, 0.937665695,
                0.93748662, 0.937307441, 0.937307441, 0.937307441, 0.937307441, 0.937307441, 0.937307441, 0.937307441,
                0.937307441, 0.937127527, 0.937127527, 0.937127527, 0.936947454, 0.936947454, 0.93676735, 0.93676735,
                0.936587002, 0.936587002, 0.936587002, 0.936587002, 0.936406548, 0.936406548, 0.936406548, 0.93622576,
                0.936045, 0.936045, 0.935864151, 0.935683317, 0.935683317, 0.935683317, 0.935502063, 0.935320701,
                0.935320701, 0.935139161, 0.934957289, 0.934775351, 0.934775351, 0.934775351, 0.934593269, 0.934593269,
                0.934411105, 0.934228973, 0.934228973, 0.934228973, 0.934228973, 0.934228973, 0.934045692, 0.934045692,
                0.934045692, 0.933862299, 0.933862299, 0.933678218, 0.933678218, 0.933678218, 0.933678218, 0.933678218,
                0.933493513, 0.933493513, 0.933493513, 0.933308305, 0.933123069, 0.932937764, 0.932937764, 0.932937764,
                0.932937764, 0.932937764, 0.93275208, 0.93275208, 0.93275208, 0.93275208, 0.932565601, 0.932565601,
                0.932379032, 0.932379032, 0.932192416, 0.932192416, 0.932005714, 0.932005714, 0.931818998, 0.931818998,
                0.931818998, 0.931818998, 0.93163143, 0.93163143, 0.931443628, 0.931255751, 0.931255751, 0.931067544,
                0.931067544, 0.930879319, 0.93069079, 0.93069079, 0.930501609, 0.930312406, 0.930123171, 0.929933858,
                0.929933858, 0.929933858, 0.929933858, 0.929743733, 0.929553098, 0.929553098, 0.929362407, 0.929171651,
                0.928980882, 0.928789999, 0.928789999, 0.928789999, 0.928789999, 0.928789999, 0.928598604, 0.928407194,
                0.928407194, 0.928407194, 0.928215033, 0.928215033, 0.928215033, 0.928022402, 0.927829579, 0.927829579,
                0.927829579, 0.927829579, 0.927636214, 0.927442758, 0.927442758, 0.927442758, 0.927442758, 0.92724829,
                0.927053732, 0.927053732, 0.927053732, 0.926858748, 0.926858748, 0.926858748, 0.926858748, 0.926858748,
                0.926858748, 0.926661889, 0.926465052, 0.926465052, 0.926465052, 0.926268058, 0.926070643, 0.926070643,
                0.926070643, 0.926070643, 0.925872581, 0.925674548, 0.925674548, 0.925674548, 0.925674548, 0.925674548,
                0.925674548, 0.925674548, 0.925674548, 0.925674548, 0.925674548, 0.925674548, 0.925674548, 0.925474528,
                0.925474528, 0.925474528, 0.925474528, 0.925274197, 0.925274197, 0.925073608, 0.924872954, 0.924872954,
                0.924872954, 0.924872954, 0.924671334, 0.924671334, 0.924671334, 0.924671334, 0.924469211, 0.924265953,
                0.924062578, 0.924062578, 0.923859099, 0.923655556, 0.923655556, 0.923451995, 0.923451995, 0.923247945,
                0.923043841, 0.922839309, 0.922634734, 0.922430133, 0.922430133, 0.9222253, 0.922020201, 0.921815078,
                0.921609733, 0.921609733, 0.921609733, 0.921404112, 0.921404112, 0.921404112, 0.921404112, 0.921404112,
                0.921198024, 0.920991787, 0.920785378, 0.920785378, 0.920785378, 0.920785378, 0.92057815, 0.92057815,
                0.920370451, 0.920370451, 0.920370451, 0.920161653, 0.919952817, 0.919952817, 0.91974376, 0.91974376,
                0.91974376, 0.919533671, 0.919323591, 0.919323591, 0.919323591, 0.919112786, 0.919112786, 0.919112786,
                0.918901745, 0.918690678, 0.918479599, 0.918479599, 0.918479599, 0.918479599, 0.918268031, 0.918268031,
                0.918268031, 0.918056256, 0.917844425, 0.917632194, 0.917419978, 0.917419978, 0.917207312, 0.916994319,
                0.916781278, 0.916781278, 0.916568164, 0.916355077, 0.916355077, 0.916141835, 0.916141835, 0.915928369,
                0.91571478, 0.915500795, 0.915286373, 0.915286373, 0.915286373, 0.915071573, 0.915071573, 0.914856512,
                0.914856512, 0.914856512, 0.914856512, 0.914640701, 0.914640701, 0.914640701, 0.914640701, 0.91442426,
                0.91442426, 0.91442426, 0.914206903, 0.913988811, 0.913769894, 0.913769894, 0.913769894, 0.913769894,
                0.913549464, 0.913549464, 0.913549464, 0.913328395, 0.913107356, 0.913107356, 0.913107356, 0.913107356,
                0.912884334, 0.912884334, 0.912884334, 0.912884334, 0.912660192, 0.912660192, 0.912435468, 0.912435468,
                0.912209995, 0.912209995, 0.911984033, 0.911984033, 0.911984033, 0.911984033 ]
    J = [ 1, 0.999877382, 0.999754739, 0.999754739, 0.999754739, 0.999631956, 0.999631956, 0.999509067,
                0.99938608, 0.99938608, 0.999263007, 0.999263007, 0.999139889, 0.999016678, 0.999016678, 0.999016678,
                0.999016678, 0.999016678, 0.998892976, 0.998769284, 0.998769284, 0.998645434, 0.998645434, 0.998645434,
                0.998521446, 0.998397292, 0.998397292, 0.998397292, 0.998397292, 0.998272945, 0.998272945, 0.998148506,
                0.998148506, 0.998023965, 0.997899177, 0.997774398, 0.997774398, 0.997774398, 0.997774398, 0.99764933,
                0.99764933, 0.99764933, 0.99764933, 0.99764933, 0.99764933, 0.99764933, 0.99764933, 0.99764933,
                0.997523173, 0.997397002, 0.997397002, 0.997397002, 0.997397002, 0.997270314, 0.997143622, 0.997143622,
                0.997143622, 0.997143622, 0.997143622, 0.997143622, 0.997143622, 0.997143622, 0.997143622, 0.997143622,
                0.997143622, 0.997143622, 0.997143622, 0.997143622, 0.997015748, 0.997015748, 0.997015748, 0.997015748,
                0.997015748, 0.996887678, 0.996887678, 0.996759541, 0.996759541, 0.996631054, 0.996502453, 0.996373864,
                0.996373864, 0.996373864, 0.996373864, 0.996373864, 0.996245106, 0.996116316, 0.996116316, 0.996116316,
                0.996116316, 0.996116316, 0.996116316, 0.99598684, 0.995857361, 0.995727824, 0.995598176, 0.995598176,
                0.995598176, 0.995598176, 0.995598176, 0.995598176, 0.995598176, 0.995468184, 0.995468184, 0.9953379,
                0.995207583, 0.995207583, 0.99507714, 0.99507714, 0.99507714, 0.99507714, 0.994946543, 0.994946543,
                0.994946543, 0.994946543, 0.994946543, 0.994946543, 0.994946543, 0.994946543, 0.994946543, 0.994946543,
                0.994946543, 0.994815158, 0.994815158, 0.994683628, 0.994683628, 0.994683628, 0.994683628, 0.994551531,
                0.994551531, 0.994551531, 0.994419352, 0.994419352, 0.994419352, 0.994286789, 0.994286789, 0.994286789,
                0.99415392, 0.99415392, 0.99415392, 0.99402086, 0.99402086, 0.99402086, 0.993887623, 0.993887623,
                0.993887623, 0.993887623, 0.993887623, 0.993887623, 0.993887623, 0.993753886, 0.993753886, 0.993753886,
                0.993619609, 0.993619609, 0.993619609, 0.993485252, 0.993485252, 0.993485252, 0.993485252, 0.993350708,
                0.993350708, 0.993216101, 0.993081328, 0.993081328, 0.993081328, 0.993081328, 0.992946353, 0.992810951,
                0.992810951, 0.992810951, 0.992675218, 0.992675218, 0.99253922, 0.99253922, 0.99253922, 0.99253922,
                0.99253922, 0.992402998, 0.992402998, 0.992266653, 0.992130259, 0.992130259, 0.992130259, 0.991993578,
                0.991993578, 0.991856717, 0.991856717, 0.991856717, 0.991856717, 0.991719469, 0.991719469, 0.991719469,
                0.991719469, 0.991581685, 0.991443628, 0.991443628, 0.991443628, 0.99130538, 0.991167072, 0.991167072,
                0.991028617, 0.990890175, 0.990890175, 0.990751558, 0.990751558, 0.990751558, 0.990751558, 0.990751558,
                0.990751558, 0.990612634, 0.990612634, 0.990473621, 0.990334594, 0.990334594, 0.99019546, 0.990056335,
                0.990056335, 0.989917027, 0.989917027, 0.989917027, 0.989917027, 0.989917027, 0.989917027, 0.989917027,
                0.989777426, 0.989777426, 0.989777426, 0.989777426, 0.989637645, 0.989637645, 0.989497767, 0.989497767,
                0.989497767, 0.98935767, 0.989217478, 0.989217478, 0.989077219, 0.989077219, 0.989077219, 0.989077219,
                0.989077219, 0.989077219, 0.988936513, 0.988936513, 0.988936513, 0.988795593, 0.988795593, 0.988654524,
                0.988513437, 0.988513437, 0.988372073, 0.988372073, 0.988230595, 0.988230595, 0.988088949, 0.988088949,
                0.987946788, 0.987804572, 0.987804572, 0.987662108, 0.987662108, 0.987662108, 0.987662108, 0.987519331,
                0.987376548, 0.987376548, 0.98723357, 0.98723357, 0.98723357, 0.98723357, 0.987090265, 0.987090265,
                0.987090265, 0.986946733, 0.986803123, 0.986659486, 0.986659486, 0.986515672, 0.986371859, 0.986227962,
                0.986227962, 0.986227962, 0.986227962, 0.986227962, 0.986227962, 0.986083685, 0.986083685, 0.985939256,
                0.985939256, 0.985794627, 0.985794627, 0.985794627, 0.985649735, 0.985649735, 0.985504739, 0.985359714,
                0.985359714, 0.985214547, 0.985069356, 0.985069356, 0.985069356, 0.984923573, 0.984777568, 0.984777568,
                0.984777568, 0.984777568, 0.984777568, 0.984777568, 0.984631211, 0.984484816, 0.984484816, 0.984484816,
                0.984338114, 0.984338114, 0.984338114, 0.984191176, 0.984191176, 0.984044012, 0.983896794, 0.983749534,
                0.983749534, 0.983749534, 0.983749534, 0.983749534, 0.983749534, 0.983601556, 0.983453568, 0.983453568,
                0.983453568, 0.983453568, 0.983305154, 0.983305154, 0.983156628, 0.983156628, 0.983007969, 0.983007969,
                0.983007969, 0.9828592, 0.982710425, 0.982710425, 0.982561567, 0.982561567, 0.982561567, 0.982561567,
                0.982412558, 0.982412558, 0.982412558, 0.982263268, 0.982263268, 0.982113763, 0.982113763, 0.982113763,
                0.982113763, 0.982113763, 0.982113763, 0.982113763, 0.981963534, 0.981963534, 0.981963534, 0.981963534,
                0.981963534, 0.981812906, 0.981812906, 0.981812906, 0.981812906, 0.981661945, 0.981661945, 0.981661945,
                0.981661945, 0.981661945, 0.981661945, 0.981510211, 0.981358378, 0.981206513, 0.981206513, 0.981206513,
                0.981054375, 0.981054375, 0.980901912, 0.980901912, 0.980901912, 0.980749267, 0.980749267, 0.980596438,
                0.980596438, 0.980596438, 0.980443422, 0.980290408, 0.980290408, 0.980290408, 0.980137157, 0.980137157,
                0.979983794, 0.979983794, 0.979983794, 0.979830163, 0.979830163, 0.979830163, 0.979830163, 0.979830163,
                0.979830163, 0.979675974, 0.979675974, 0.979675974, 0.979521382, 0.979366801, 0.979212225, 0.979212225,
                0.979212225, 0.979057491, 0.979057491, 0.979057491, 0.979057491, 0.979057491, 0.978902557, 0.978747593,
                0.978592559, 0.978437479, 0.978437479, 0.978282209, 0.978126898, 0.977971592, 0.977816211, 0.977816211,
                0.977660465, 0.977504635, 0.977504635, 0.977348616, 0.977348616, 0.977192543, 0.977036362, 0.977036362,
                0.977036362, 0.977036362, 0.976880014, 0.976723667, 0.976723667, 0.976567075, 0.976567075, 0.976567075,
                0.976567075, 0.976567075, 0.976410029, 0.976410029, 0.97625267, 0.97625267, 0.97625267, 0.976095106,
                0.976095106, 0.976095106, 0.976095106, 0.975937294, 0.975779279, 0.975621258, 0.975621258, 0.975462583,
                0.975303689, 0.975144647, 0.97498534, 0.97498534, 0.974825835, 0.974666276, 0.974506489, 0.974346698,
                0.974346698, 0.974346698, 0.974346698, 0.974186335, 0.974186335, 0.974186335, 0.974025828, 0.974025828,
                0.974025828, 0.974025828, 0.973865137, 0.973865137, 0.973865137, 0.973865137, 0.973865137, 0.973865137,
                0.973703708, 0.973703708, 0.973703708, 0.973703708, 0.973703708, 0.973541461, 0.973541461, 0.973541461,
                0.973378704, 0.973378704, 0.973215827, 0.973215827, 0.973215827, 0.973215827, 0.973215827, 0.973215827,
                0.973052417, 0.972888992, 0.972888992, 0.972725547, 0.972725547, 0.972725547, 0.972725547, 0.972561904,
                0.972398144, 0.972234166, 0.972070187, 0.971906061, 0.971741794, 0.971741794, 0.971741794, 0.971741794,
                0.971576918, 0.971411807, 0.971246446, 0.971081015, 0.971081015, 0.971081015, 0.970915378, 0.970749651,
                0.970583889, 0.970418117, 0.970252289, 0.970086211, 0.969920146, 0.969920146, 0.969753575, 0.969753575,
                0.969586402, 0.969586402, 0.969586402, 0.969586402, 0.969586402, 0.969418925, 0.969251466, 0.96908398,
                0.96908398, 0.96908398, 0.968916318, 0.968916318, 0.968748598, 0.968580879, 0.968413051, 0.968245215,
                0.968245215, 0.968077237, 0.967909132, 0.967909132, 0.967909132, 0.967740501, 0.96757177, 0.967403013,
                0.96723424, 0.96723424, 0.967065309, 0.966896385, 0.966896385, 0.966727349, 0.966558318, 0.966558318,
                0.966389029, 0.966389029, 0.966219573, 0.966049999, 0.966049999, 0.96588038, 0.96588038, 0.96588038,
                0.965710661, 0.965540946, 0.965540946, 0.965540946, 0.965370754, 0.965370754, 0.965370754, 0.965370754,
                0.965370754, 0.965370754, 0.965370754, 0.965370754, 0.965199788, 0.965199788, 0.965028705, 0.964857288,
                0.964685837, 0.964514162, 0.964342507, 0.964342507, 0.964342507, 0.964342507, 0.964169532, 0.963996544,
                0.96382358, 0.96382358, 0.96382358, 0.963650469, 0.963477362, 0.963304235, 0.963304235, 0.963131096,
                0.963131096, 0.962957838, 0.962957838, 0.962784322, 0.962784322, 0.962784322, 0.962784322, 0.962610474,
                0.962610474, 0.96243628, 0.962262095, 0.962262095, 0.962262095, 0.962262095, 0.962087752, 0.962087752,
                0.962087752, 0.961912721, 0.961737614, 0.961562525, 0.961562525, 0.961562525, 0.961387132, 0.961387132,
                0.961211588, 0.961211588, 0.961035986, 0.961035986, 0.961035986, 0.961035986, 0.961035986, 0.960860048,
                0.960860048, 0.960860048, 0.960860048, 0.960683955, 0.960507609, 0.960507609, 0.960331134, 0.960154597,
                0.960154597, 0.960154597, 0.960154597, 0.960154597, 0.960154597, 0.959976939, 0.959798958, 0.95962098,
                0.95962098, 0.959442987, 0.959265012, 0.959265012, 0.959265012, 0.959265012, 0.95908663, 0.95908663,
                0.958908204, 0.958729788, 0.958729788, 0.958551221, 0.958372634, 0.958194074, 0.958194074, 0.958014995,
                0.958014995, 0.958014995, 0.957835556, 0.957656061, 0.957656061, 0.957476321, 0.957296561, 0.957296561,
                0.957296561, 0.957116684, 0.957116684, 0.957116684, 0.956936671, 0.956756454, 0.956756454, 0.956756454,
                0.956756454, 0.956575933, 0.956395352, 0.956395352, 0.956395352, 0.956395352, 0.956395352, 0.956214378,
                0.956033372, 0.956033372, 0.956033372, 0.955852143, 0.955852143, 0.955852143, 0.955852143, 0.955852143,
                0.955670521, 0.95548884, 0.95548884, 0.955306878, 0.955306878, 0.955124624, 0.955124624, 0.954942189,
                0.954942189, 0.954942189, 0.954759442, 0.954576498, 0.954393375, 0.954210241, 0.954027083, 0.954027083,
                0.954027083, 0.953843392, 0.953843392, 0.95365961, 0.95365961, 0.95365961, 0.953475582, 0.953475582,
                0.953291402, 0.953291402, 0.953291402, 0.953107108, 0.953107108, 0.952922627, 0.95273809, 0.952553257,
                0.952553257, 0.95236829, 0.952183133, 0.952183133, 0.952183133, 0.952183133, 0.952183133, 0.951997371,
                0.951997371, 0.95181148, 0.95181148, 0.95181148, 0.95181148, 0.95181148, 0.951625255, 0.951625255,
                0.951438479, 0.951438479, 0.951438479, 0.951251384, 0.951064294, 0.950877059, 0.950689809, 0.950502513,
                0.950502513, 0.950502513, 0.950502513, 0.950315017, 0.950315017, 0.95012732, 0.949939632, 0.949939632,
                0.949939632, 0.949751294, 0.949562853, 0.949374442, 0.949185944, 0.948997391, 0.948808754, 0.94862012,
                0.94862012, 0.948431419, 0.948242743, 0.948242743, 0.94805392, 0.94805392, 0.947864987, 0.947864987,
                0.947675913, 0.947486792, 0.947297683, 0.947297683, 0.94710855, 0.946919204, 0.946919204, 0.946919204,
                0.946729641, 0.946729641, 0.946729641, 0.946539953, 0.946350168, 0.946350168, 0.946350168, 0.946160021,
                0.946160021, 0.946160021, 0.946160021, 0.945969465, 0.945778759, 0.945778759, 0.945587939, 0.945587939,
                0.945587939, 0.945396871, 0.945205732, 0.945014497, 0.944823154, 0.944823154, 0.944631459, 0.944439698,
                0.944439698, 0.944247844, 0.944247844, 0.944055481, 0.943862999, 0.943670474, 0.943477804, 0.943477804,
                0.943284979, 0.943091861, 0.943091861, 0.943091861, 0.943091861, 0.942898217, 0.942704577, 0.942510846,
                0.942317027, 0.942317027, 0.942123019, 0.941928618, 0.941734111, 0.941734111, 0.941539389, 0.941539389,
                0.941344551, 0.941344551, 0.941149721, 0.941149721, 0.940954792, 0.940954792, 0.940759559, 0.940564088,
                0.940368394, 0.940368394, 0.940172666, 0.940172666, 0.940172666, 0.939976366, 0.939976366, 0.939779891,
                0.939779891, 0.939779891, 0.939582687, 0.939582687, 0.939582687, 0.939582687, 0.939582687, 0.939385094,
                0.93918724, 0.938989178, 0.938989178, 0.938989178, 0.938790267, 0.938790267, 0.938790267, 0.938790267,
                0.938790267, 0.938591055, 0.938391847, 0.938192381, 0.937992887, 0.937992887, 0.937992887, 0.937792671,
                0.937592469, 0.937592469, 0.937391872, 0.937190866, 0.937190866, 0.937190866, 0.936989394, 0.936787951,
                0.936586519, 0.936586519, 0.936586519, 0.936384794, 0.936183086, 0.935981283, 0.935981283, 0.935981283,
                0.935778797, 0.935576325, 0.935576325, 0.935373377, 0.935170257, 0.934966628, 0.934763006, 0.934559289,
                0.934559289, 0.934559289, 0.934355411, 0.9341515, 0.9341515, 0.9341515, 0.933946876, 0.933742151,
                0.933537132, 0.933537132, 0.933537132, 0.933332005, 0.933126886, 0.932921661, 0.932716458, 0.932510877,
                0.932305259, 0.932099345, 0.931893349, 0.93168738, 0.931481433, 0.931275275, 0.931275275, 0.931069075,
                0.93086282, 0.930656475, 0.930656475, 0.930449999, 0.930449999, 0.930449999, 0.930243312, 0.930036489,
                0.929829454, 0.929829454, 0.929622208, 0.929414947, 0.92920753, 0.92920753, 0.92920753, 0.92920753,
                0.928999257, 0.928999257, 0.928999257, 0.928790842, 0.928790842, 0.928582023, 0.928582023, 0.928582023,
                0.928582023, 0.928582023, 0.928582023, 0.928372046, 0.928372046, 0.928372046, 0.928372046, 0.928372046,
                0.928161369, 0.927950597, 0.927950597, 0.927739748, 0.927528894, 0.927317861, 0.927106619, 0.927106619,
                0.927106619, 0.927106619, 0.92689458, 0.92668228, 0.926469948, 0.926469948, 0.926257284, 0.926257284,
                0.926044011, 0.925830261, 0.925830261, 0.925830261, 0.925616177, 0.925616177, 0.925401464, 0.925186617,
                0.925186617, 0.925186617, 0.92497113, 0.924755558, 0.924755558, 0.924539611, 0.924323638, 0.924323638,
                0.924323638, 0.924323638, 0.924107424, 0.92389122, 0.923674944, 0.923674944, 0.923458501, 0.923241927,
                0.923241927, 0.923241927, 0.923241927, 0.923241927, 0.923024828, 0.923024828, 0.923024828, 0.923024828,
                0.922807067, 0.922807067, 0.922807067, 0.92258914, 0.92258914, 0.922370894, 0.922370894, 0.922370894,
                0.922370894, 0.922370894, 0.922151617, 0.921932103, 0.921932103, 0.921712341, 0.921712341, 0.921492116,
                0.921271713, 0.921051159, 0.921051159, 0.920830407, 0.920609706, 0.92038869, 0.92038869, 0.920167213,
                0.919945043, 0.919945043, 0.919945043, 0.919945043, 0.919720658, 0.919495992, 0.919271144, 0.919271144,
                0.919045503, 0.918819742, 0.918819742, 0.918819742, 0.918593651, 0.918367207, 0.918140177, 0.918140177,
                0.917912454, 0.917683706, 0.917454902, 0.917454902, 0.917225642, 0.917225642, 0.916995765, 0.916995765,
                0.916765558, 0.916765558, 0.91653476, 0.916303773, 0.916072612 ]
    F = []
    G = []
    K = []
    M = []
    Q2 = 0
    if (isMale) : Q2 = 1
    Q3 = np.log(age)
    Q4 = np.log(systolicBp)
    Q5 = 0
    if (smoker) : Q5 = 1
    Q6 = 0
    if (treatedBp) : Q6 = 1
    Q7 = np.log(BMI)
    Q8 = 0
    if diabetic: Q8 = 1
    R2 = 0.73413
    R3 = 3.07187
    R4 = 1.79939
    R5 = 0.79437
    R6 = 0.3926
    R7 = 1.1166
    R8 = 1.03634
    S2 = Q2 * R2
    S3 = Q3 * R3
    S4 = Q4 * R4
    S5 = Q5 * R5
    S6 = Q6 * R6
    S7 = Q7 * R7
    S8 = Q8 * R8
    S10 = S2 + S3 + S4 + S5 + S6 + S7 + S8
    T2 = 0.47275
    T3 = 3.55871
    T4 = 1.5204
    T5 = 0.96516
    T6 = 0.11331
    T7 = -0.27572
    T8 = 0.45868
    U2 = Q2 * T2
    U3 = Q3 * T3
    U4 = Q4 * T4
    U5 = Q5 * T5
    U6 = Q6 * T6
    U7 = Q7 * T7
    U8 = Q8 * T8
    U10 = U2 + U3 + U4 + U5 + U6 + U7 + U8
    W2 = 23.93525811
    X2 = 19.79731622
    W5 = np.exp(S10 - W2)
    X5 = np.exp(U10 - X2)
    # set F array
    for num in E:
        F.append( np.power(num, W5) )
    # set G
    for i in range(len(E) - 1):
        G.append( np.log(E[i]) - np.log(E[i + 1]) )
    # set K
    for num in J:
        K.append( np.power(num, X5) )
    # set M
    M.append( W5 * (-np.log(E[0])) )
    for i in range(min(len(F)-1,len(K)-1, len(G)-1)):
        M.append( F[i] * K[i] * W5 * G[i] )
    # now we can calculate the risk values
    hardRisk = 0.
    for num in M:
        hardRisk = hardRisk + num
    return hardRisk