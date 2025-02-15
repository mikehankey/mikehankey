var cur_json_data;
var cur_state; 
var cur_county;

// Change state
function change_state() { 
   cur_json_data = "";
   cur_state = "";
   cur_county = "";
   $("#county_select").html("");
   $('#calc_mortality').val(""); 
   load_data();
}

function change_county() {  
   //show_loader();
   $('#calc_mortality').val(""); 
   setTimeout(function() {load_data();},150);
}


// Load data based on urlInfo or selected values on the state & county select
function load_data(urlInfo, reload) {
   
   var state  = (urlInfo&&urlInfo.state)?urlInfo.state:($('#state_selector').val()?$('#state_selector').val():"0");
   var county = (urlInfo&&urlInfo.county)?urlInfo.county:($('#county_selector').val()?$('#county_selector').val():undefined);
    
   
   if($.trim(state)!=='0') {
      // Update Soc Sharing with Full State Name
      if(county!=='' && typeof county !== "undefined") {
         setShareLinks({state:county+", "+ state, state_code:state,county:county});
      } else {
         setShareLinks({state:$("#state_selector option[value='"+state+"']").text(), state_code:state});
      } 
      cur_county = county;
      if(cur_json_data=="") { 
         getJSONData("../json/" + state + ".json",$.trim(state),$.trim(county));
      } else { 
         //displayData(cur_json_data,cur_state,county); 
         new_display_data(cur_json_data,state,county);
      }
     
   } 
}




/**
 * Load JSON DATA
 * @param {*} url 
 * @param {*} state 
 * @param {*} county 
 * @param {*} reload 
 */
function getJSONData(url,state,county,reload) {
   
   if(typeof reload == 'undefined') {
      show_loader();	
   }
  
   $.ajax({
      type: "get",
      url:  url,
      dataType: "json",

      success: function (result, status, xhr) {
       
         // Create Select County
         countySelect(getAllCounties(result) , state); 
         $('#county_selector').unbind("change").change(function(e) {
            change_county();
            return false;
         })
 
         cur_json_data = result;
         cur_county     = county;   
         cur_state      = state;
         new_display_data(result,state,county)  
         hide_loader();	 
         $('#recalculate').html($('#recalculate').attr('data-htmlx'));
         $('#recalculate').removeAttr('data-htmlx');
         
 
      },
      error: function (xhr, status, error) {
         alert("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText)
         hide_loader();	
      }
   });
}


/**
 * Setup action on selects
 */
function setupActions() {
   // Create action on state select 
   $('#state_selector').change(function() { change_state(); });

   // Creation action on recalculate button
   $('#recalculate').click(function() { 
      $(this).attr('data-htmlx',$(this).html()).html('Computing...');
      $('body').addClass('wait');
      setTimeout(function() {
         displayData(cur_json_data,cur_state,cur_county);
      },850);
   });

      
   $('#reset').click(function() {
      reset();
      $('#recalculate').trigger('click');
   })
 
}

// Do we have parameters we can work with 
// We want 
// coronafiles.us/?MD+Baltimore
// or 
// coronafiles.us/?MD
function getInfoFromUrl(cururl) {
   var selState;
   var toReturn = {state:"",county:""}, possibleStates=[];

   // Remove Dash from url
   if (cururl.indexOf('#') > 0) {
      cururl = cururl.substring(0,cururl.indexOf('#'));
   } 

   // Do we have a state? a county? both?
   if(cururl.indexOf('?')>0) {
      selState = cururl.substring(cururl.indexOf('?')+1, cururl.length);

      if(selState.indexOf('+')>0) {
         init_select_county = selState.substring(selState.indexOf('+')+1, selState.length);
         selState = selState.substring(0,selState.indexOf('+')).toUpperCase();
         toReturn.county = init_select_county;
      } else {
         selState = selState.toUpperCase();
      }

      // Get all the possible state value
      $('#state_selector option').each(function(i,v){
         possibleStates.push(v.value);
      })
      
      if(possibleStates.indexOf(selState)>0) {
         toReturn.state = selState; 
         // Update Soc Sharing with Full State Name
         setShareLinks({state:$("#state_selector option[value='"+selState+"']").text(), state_code:selState});
      }

      possibleStates = null; // gc
   } 

   return toReturn;

}

 


$(function() {
    

   // Once the page is loaded we enable the state select
   $('#state_selector').removeAttr('disabled');
   $('body').removeClass('wait');

   setupActions();
  
   // ... 
   hide_loader(false);

   // Do we have parameters we can work with 
   // We want 
   // coronafiles.us/?MD+Baltimore
   // or 
   // coronafiles.us/?MD
   urlInfo = getInfoFromUrl(decodeURIComponent(window.location.href));
   load_init_data(urlInfo);
   
   setShareLinks();

   // Scroll Top even with hidden elements
   window.scrollTo(0,0);

})