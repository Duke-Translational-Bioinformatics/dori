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
                    // store the pertinent pointer
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
    
    this.fetchmodels = function(vis = true) {
        var CUIs = this.getInputData();
        // request to check for new models
        $.ajax({
            url : "api/model/by_riskfactors/", 
            data : CUIs,
            master : this, 
            headers: {"Content-Type": "application/json"},
            success: function(reply) {
                // store the pertinent pointer
                var master = this.master; 
                
                // parse the reply
                var data = JSON.parse(reply);
                
                // identify new ids
                var new_ids = [];
                for (id in data) {
                    if (!(id in master.all_models)) {
                        new_ids.push(id);
                    }
                }
                
                // request to find data and add it to all_models
                $.ajax({
                    url : "api/model/by_id",
                    data : {"ids" : new_ids},
                    master: master,
                    headers: {"Content-Type": "application/json"},
                    success: function(reply) {
                        // store the pertinent pointer
                        var master = this.master; 
                        
                        // parse the reply
                        var data = JSON.parse(reply);
                        
                        // store data on all newly acquired models
                        // TODO find a way to prevent extraneous multi-requesting of the same models
                        // TODO maybe just make a variable whole_interface.requesting models that 
                        // TODO will stall requests...
                        for (id in data) {
                            if (!(id in master.all_models)) {
                                master.all_models[id] = data[id];
                                console.log(master.all_models[id]);
                            }
                        }
                    }
                    
                });
                
                // TODO make models visible as appropriate
                
            }
        });
    }
    
    this.getInputData = function() {
        var data = {};
        for (i in this.vis_CUIs) {
            var obj = this.all_CUIs[this.vis_CUIs[i]]["local_obj"];
            data[this.vis_CUIs[i]] = obj.getVal();
        }
        return(data);
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



// document.ready
$(document).ready( function () {
    the_interface = new whole_interface("main", riskfactors);
});
