/**
 * main.js
 *
 * js classes and procedures for the main demo interface
 */



/**
 * whole_interface
 * 
 * class to write and maintain the main div of the doirisks interface
 **/

function whole_interface(own_div_id, init_riskfactors = []) {
    // the id of the div where the interface will be placed
    this.own_div_id = own_div_id;
    
    // all data stored on models and CUIs 
    this.all_models = {};
    this.all_CUIs = {};
    
    // list of visible models and CUIs
    this.vis_models = [];
    this.vis_CUIs = [];
    
    // the left side of the interface - models
    this.lefttable  =  new models_table(this);
    this.leftfinder = new models_finder(this);
    // the right side of the interface - risk factors
    this.righttable  =  new riskfactors_table(this);
    this.rightfinder = new riskfactors_finder(this);
    
    // the base text of the interface
    var text = '<table class="table-condensed" ><tr>\n'
    text    += '    <td style="vertical-align:Top;border:1px solid">\n';
    
    // left interface
    text    += '        <h4 >Models</h4>\n';
    text    += this.lefttable.base;
    text    += '        <br>\n';
    text    += this.leftfinder.base;
    
    text    += '    </td>\n';
    text    += '    <td style="vertical-align:Top;border:1px solid">\n';
    
    // right interface
    text    += '        <h4>Risk Factors</h4>\n';
    text    += '        <div>\n';
    text    += this.righttable.base;
    text    += '            <br>\n';
    text    += this.rightfinder.base;
    text    += '        </div>\n';
    
    text    += '    </td>\n';
    text    += '</tr></table>\n';
    this.base = text;
    
    // add a CUI
    this.fetchCUI = function (CUI, vis = true) {
        // try to fetch the CUI
        if (this.all_CUIs[CUI] == null){
            // fetch and handle data from server
            this.all_CUIs[CUI] = $.ajax({
                url : "api/cui/by_cui/", 
                data : {"CUIs": [CUI]},
                master : this, 
                headers: {"Content-Type": "application/json"},
                success: function(reply) {
                    // store the pertinent pointers
                    var master = this.master; 
                    
                    // parse the reply
                    var data = JSON.parse(reply);
                    var CUI = Object.keys(data)[0];
                    
                    // store the data in the all_CUIs array
                    master.all_CUIs[CUI] = data[CUI]; 
                    master.all_CUIs[CUI]["local_obj"] = new riskfactors_single(master, CUI); 
                    
                    // show the CUI
                    master.vis_CUIs.push(CUI); 
                    master.righttable.push(master.all_CUIs[CUI]["local_obj"]);
                }
            });
            // TODO add a memory variable to make sure that the CUIs are added in the right order
        } else if ( this.all_CUIs[CUI]['CUI'] == CUI ) {
            // browser already has CUI data, but it is hidden => unhide it!
            this.vis_CUIs.push(CUI);
            this.update();
        } else {
            // do nothing - CUI is either being gotten already or it is bad
        }
    }
    
    $('#'+own_div_id).html(this.base);
    $('#allriskfactors').after(this.righttable.buttons);
    $(this.righttable.buttons).after(this.righttable.names);
    $(this.righttable.names).after(this.righttable.values);
    $(this.righttable.values).after(this.righttable.unit_names);
    // iterate through given risk factors and add them
    for (CUI in init_riskfactors) {
        this.fetchCUI(CUI);
    }
}

/**
 * models_table
 * 
 * class to write and maintain the models table (active models)
 **/

function models_table(master) {
    this.master = master;
    var text = "        <div id = 'models'>\n";
    text    += '            <!-- available models are added here -->\n';
    text    += '        </div>\n';
    this.base = text;
}

/**
 * riskfactors_table
 * 
 * class to write and maintain the risk factors table (risk factors in use)
 **/

function riskfactors_table(master) {
    this.master = master;
    var text = "            <form id = 'riskfactors' style='width:400px'>\n";
    // TODO make cell formats into a css class
    text    += '                <span id="riskfactortitles" style="width:300px"> <span style="width:20px"></span> <span style="width:180px">Risk Factor</span> <span style="width:50px"><p>Value</p></span> <span style="width:50px">Units</span> </span>';
    text    += '                <div id="allriskfactors" class="wrapper"></div>\n';
    text    += '                <!-- risk factor inputs added by getrisk.js -->\n';
    text    += '            </form>\n';
    this.base = text;
    
    this.buttons = $("<div style='float:left; width:30px; display:block; overflow:hidden'></div>"); //document.createElement('span');
    this.names = $("<div style='float:left; width:150px; display:block; overflow:hidden'></div>"); //document.createElement('span');
    this.values = $("<div style='float:left; width:120px; display:block; overflow:hidden'></div>"); //document.createElement('span');
    this.unit_names = $("<div style='style='width:50px; display:block; overflow:hidden'></div>"); //document.createElement('span');
    
    // the most recent addition
    this.head = null;
    
    // makes a CUI visible in the table
    this.push = function (CUI_obj) {
        CUI_obj.show(this.head);
        this.head = CUI_obj;
    }
    
    // remove a CUI from the table
    this.pop = function (CUI_obj) {
        CUI_obj.remove();
    }
}

/**
 * models_finder
 * 
 * class to hold the search for new models
 **/
function models_finder(master) {
    this.id = "newmodel";
    this.master = master;
    var text = "        <form id = 'newmodel'> <!-- add a new risk factor -->\n";
    text    += '            <span class="searchform">\n';
    text    += '                <span><b>Search for Models</b></span>\n';
    text    += '                <div>\n';
    text    += '                    <span><button>Find</button></span>\n';
    text    += '                    <span><input type="text" name="search"  style="text-align:center;width:100px"></input></span>\n';
    text    += '                </div>\n';
    text    += '            </span>\n';
    text    += '        </form>\n';
    this.base = text;
}

/**
 * riskfactors_finder
 * 
 * class to hold the search for new models
 **/
function riskfactors_finder(master) {
    this.id = "newriskfactor";
    this.master = master;
    var text = "            <form id = 'newriskfactor'> <!-- add a new risk factor -->\n";
    text    += '                <span class="searchform">\n';
    text    += '                    <span><b>Search for Risk Factors</b></span>\n';
    text    += '                    <div>\n';
    text    += '                        <span><button>Add</button></span>\n';
    text    += '                        <span><input type="text" name="search"  style="text-align:center;width:100px"></input></span>\n';
    text    += '                    </div>\n';
    text    += '                </span>\n';
    text    += '            </form>\n';
    this.base = text;
}

/**
 * riskfactors_finder
 * 
 * class to hold the search for new models
 **/
 
function models_single(master, model) {
    var text = ""; //TODO
    this.text = text;
   
    // previous and next in the table
    this.prev = null;
    this.next = null;
    
    this.show = function (prev) {
        // adjust place in list
        this.prev = prev;
        if (prev != null && prev.next != null) {
            this.next = prev.next;
        }
        prev.next = this;
        
        // show in html
        $("#" + prev.id).after(this.content);
    }
}

/**
 * riskfactors_finder
 * 
 * class to hold the search for new models
 **/
 
function riskfactors_single(master,CUI) {
    this.master = master;
    this.CUI = CUI;
    this.id = CUI;
    //TODO this.datatype = master.;
    
    //TODO this.val = ;
    
    var text = '<div id="' + this.id + '">\n';
    // button - removal button
    var text = '<div style="text-align:center; height:30px;">';
    text +=    '    <button id = "remove' + CUI + '" onclick=the_interface.righttable.pop(master.all_CUIs["'+CUI+'"]["local_obj"]) >-</button>'; //TODO
    text +=    '</div>';
    this.button = $(text);
    
    // rf - name of risk factor CUI displayed w/link
    var text = '<div style= "text-align:center; height:30px; overflow:visible;">';
    var riskname = toTitleCase(master.all_CUIs[CUI]['name1']);
    text +=    '    <a href="CUIquery.php?CUI=' + CUI + '" >'+riskname+'</a>'; // TODO link destination
    text +=    '</div>';
    this.rf = $(text);
    
    // interpret the datatype and units
    var inputdata = "";
    var units = "";
    if (CUI == 'C28421') { // Sex
        inputdata = 'type="radio" value="male" checked> Male</input>  <input type="radio" name="'+CUI+'" value="female"> Female<p></p';
    } else if (master.all_CUIs[CUI]['datatype'].toLowerCase() == 'float') {
        inputdata = 'type="number" placeholder="Float" style="width:50px"';
        units += master.all_CUIs[CUI]['units'];
    } else if (master.all_CUIs[CUI]['datatype'].toLowerCase() == 'int' || master.all_CUIs[CUI]['datatype'].toLowerCase() == 'integer') {
        inputdata = 'type="number" placeholder="Integer" style="width:50px';
        units += master.all_CUIs[CUI]['units'];
    } else /*if (master.all_CUIs[CUI]['datatype'].toUpperCase() == 'BOOL')*/ {
        inputdata = 'type = "checkbox" ';
    } 
    
    // input
    var text = '<div style= "text-align:center; height:30px;">';
    text +=    '    <input name = "' + CUI + '" ' + inputdata + ' ></input> ';
    text +=    '</div>';
    this.input = $(text);
    
    // units
    var text = '<div style= "text-align:center; height:30px;">' + units + '</div>';
    this.units = $(text);
    
    // previous and next in the table
    this.prev = null;
    this.next = null;
   
    this.show = function (prev) {
        // adjust list pointers
        this.prev = prev;
        if (prev != null && prev.next != null) {
            this.next = prev.next;
        }
        if (prev != null) {
            prev.next = this;
        }
        
        // show content
        if (prev == null){
            // show button
            $(master.righttable.buttons).html(this.button);
            // show rf
            $(master.righttable.names).html(this.rf);
            // show input
            $(master.righttable.values).html(this.input);
            // show units
            $(master.righttable.unit_names).html(this.units);
        }
        else {
            // show button
            $(prev.button).after(this.button);
            // show rf
            $(prev.rf).after(this.rf);
            // show input
            $(prev.input).after(this.input);
            // show units
            $(prev.units).after(this.units);
        }
    }
    
    this.hide = function () {
        // adjust list pointers
        if (this.prev !== null) {
            this.prev.next = this.next;
        }
        if (this.next !== null) {
            this.next.prev = this.prev;
        }
        else {
            // change head of table if appropriate
            master.righttable.head = this.prev;
        }
        
        // remove html
        $("#" + this.id).remove();
    }
    
    this.getVal = function () {
        //TODO
    }
}

// document.ready
$(document).ready( function () {
    the_interface = new whole_interface("main", riskfactors);
});
