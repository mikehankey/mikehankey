 // Fill Row
 function fillPredictedOutComeRow(title,total,cur,trend1,trend2) {
   return '<tr><th>'+title+'</th>\
   <td>' + usFormat(cur) + '</td><td>' +   (cur*100/total).toFixed(2) + '%</td>\
   <td>' + usFormat(trend1) + '</td><td>' +    (trend1*100/total).toFixed(2) + '%</td>\
   <td >' + usFormat(trend2) + '</td><td>' +   (trend2*100/total).toFixed(2) + '%</td></tr>';
}

// Fill Entire Table
function fillPredictedOutcome(data,cur,trend7,trend14) {
   var tbody;
 

   tbody =  fillPredictedOutComeRow("Deaths",data.pop, cur.deaths, trend14.deaths, trend7.deaths);
   tbody += fillPredictedOutComeRow("Confirmed Cases",data.pop, cur.conf_case,  trend14.conf_case, trend7.conf_case);
   tbody += fillPredictedOutComeRow("Non-Tracked Infected",data.pop, cur.total_non_tracked_infected, trend14.total_non_tracked_infected, trend7.total_non_tracked_infected);
   tbody += fillPredictedOutComeRow("Not Infected",data.pop, cur.not_infected,  trend14.not_infected, trend7.not_infected); 
   $('#new_trends tbody').html(tbody);
} 

// Fill Top Table & Pie Chars
function fill_top_table(data,phantom) {
   
   var herd_7 = data.trend_7.reach==-1?true:false; // It means herd immunity
   var herd_14 = data.trend_14.reach==-1?true:false; 
 
   
   var cur_table_data =  {  deaths: 0, conf_case: 0,  non_tracked_case: 0, not_infected: 0,  total_infected: 0  };
   var trend7_table_data =  {  deaths: 0, conf_case: 0,  non_tracked_case: 0, not_infected: 0,  total_infected: 0  };
   var trend14_table_data =  {  deaths: 0, conf_case: 0,  non_tracked_case: 0, not_infected: 0,  total_infected: 0  };

   // Herd or 0
   if(!herd_7) {
      $('#7_day_date').text(data.trend_7.reach);
   } else {
     $('#7_day_date').text(dateFormatMITFromDate(data.trend_7.herd_reach_date));
   }
   
   // We prepare the data
   trend7_table_data.conf_case               = parseInt(data.trend_7.total_at_end);
   trend7_table_data.deaths                  = parseInt(data.trend_7.total_at_end*data.last_mortality_rate/100);
   trend7_table_data.total_non_tracked_infected          = parseInt( trend7_table_data.conf_case / phantom ) ;
   trend7_table_data.not_infected            = data.pop -  trend7_table_data.total_non_tracked_infected -  trend7_table_data.deaths;
   
   // Herd or 0
   if(!herd_14) {
      $('#14_day_date').text(data.trend_14.reach);
   } else {
      $('#14_day_date').text(dateFormatMITFromDate(data.trend_14.herd_reach_date));
   } 
   
   // We prepare the data
   trend14_table_data.conf_case               = parseInt(data.trend_14.total_at_end);
   trend14_table_data.deaths                  = parseInt(data.trend_14.total_at_end*data.last_mortality_rate/100);
   trend14_table_data.total_non_tracked_infected          = parseInt( trend14_table_data.conf_case / phantom ) ;
   trend14_table_data.not_infected            = data.pop -  trend14_table_data.total_non_tracked_infected -  trend14_table_data.deaths;
 
 
   // Cur Data 
   cur_table_data.conf_case               = parseInt(data.total_case);
   cur_table_data.deaths                  = parseInt(data.total_death);
   cur_table_data.total_non_tracked_infected          = parseInt( data.total_case / phantom )  ;
   cur_table_data.not_infected            = data.pop -   cur_table_data.total_non_tracked_infected  -  cur_table_data.deaths;

 
   fillPredictedOutcome(data,cur_table_data, trend7_table_data,trend14_table_data );
  
   // Build the pies
   // Create Pies Pies
   var pie_lb = [ 'Not Infected', 'Infected', 'Confirmed Cases', 'Deaths'];
   plot_pie([trend14_table_data.not_infected, trend14_table_data.total_non_tracked_infected, trend14_table_data.conf_case,  trend14_table_data.deaths],pie_lb,"14-Day Trend","new_cases_pie_14");
   plot_pie([trend7_table_data.not_infected, trend7_table_data.total_non_tracked_infected, trend7_table_data.conf_case,  trend7_table_data.deaths],pie_lb,"7-Day Trend","new_cases_pie_7");
 
}
 


// Create Main Top Sentence, compute herd immunity if necessary and fill the top of the page
function create_top_page(data, phantom, herd_tresh) {
   var top_sentence = "";  
     
   if(data.trend_7['reach']!=-1 && data.trend_14['reach']!=-1) {
       // We reach 0 cases at one point 
      top_sentence = "Based on current data trends,<br><span class='good_t'>" +  data.name;

      if (data.trend_7['reach_raw_d'] == data.trend_14['reach_raw_d']) {
         // They will reach 0 on the same day
         if( data.trend_14['reach_raw_d'] < new Date()) {
            top_sentence += " has reached zero cases per day or is very close to doing so.";
         } else {
            top_sentence += " could have zero cases <span class='wn'>on " + data.trend_14['reach']  + "</span>.";
         } 

      } else {
         // Both will reach 0, but not on the same day
         top_sentence += " could have zero cases "; 
         if( data.trend_14.reach_raw_d < data.trend_7.reach_raw_d ) { 
            top_sentence +=  "somewhere between <span class='wn'>" +  data.trend_14['reach'] + " and " + data.trend_7['reach'] + "</span>.";
         } else if(  data.trend_14.reach_raw_d > data.trend_7.reach_raw_d) {
            top_sentence +=  "somewhere between <span class='wn'>" +  data.trend_7['reach'] + " and " + data.trend_14['reach'] + "</span>.";
         } else { 
            top_sentence +=  "<span class='wn'>around "  + data.trend_7['reach']  + " </span>";
         }
      } 

   } else {

 
      if(data.trend_7['reach']==-1 && data.trend_14['reach']!=-1  ) { 
         
         // We need to compute the Herd Immunity for 7 day trend only
         top_sentence = "Based on the 7-day trend,<br>" +  data.name;
         top_sentence += " could reach <span class='ugly_t'>herd immunity on <span class='wn'>" + dateFormatMITFromDate(data.trend_7['herd_reach_date']) + "</span></span>";
         top_sentence += "<br>but based on the 14-day trend,<br>";
         top_sentence += " it could have <span class='good_t'>zero cases by <span class='wn'>" + data.trend_14['reach']  + "</span>.";

      } else if(data.trend_7['reach']!=-1 && data.trend_14['reach']==-1) {

        
         // We need to compute the Herd Immunity for 14 day trend only 
         top_sentence = "Based on the 14-day trend,<br>" +  data.name;
         top_sentence += " could reach <span class='ugly_t'>herd immunity on <span class='wn'>" + dateFormatMITFromDate(data.trend_14['herd_reach_date']) + "</span></span>";
         top_sentence += "<br>but based on the 7-day trend,<br>";
         top_sentence += " it could have <span class='good_t'>zero cases by <span class='wn'>" + data.trend_7['reach']  + "</span>.";
       

      } else { 

         // Both are HERD
 
         
         if(data.trend_7['herd_reach_date'] == data.trend_14['herd_reach_date']) {
            top_sentence = "Based on the latest trends,<br>" +  data.name;
            top_sentence += " could reach <span class='ugly_t'>herd immunity around"
            top_sentence += " <span class='wn'>" +  dateFormatMITFromDate(data.trend_14['herd_reach_date']) + "</span></span>.";
         } else if( data.trend_7['herd_reach_date'] < data.trend_14['herd_reach_date'] ) {
            top_sentence = "Based on the latest trends,<br>" +  data.name;
            top_sentence += " could reach <span class='ugly_t'>herd immunity between"
            top_sentence += " <span class='wn'>" + dateFormatMITFromDate(data.trend_7['herd_reach_date']) + "</span> and ";
            top_sentence += " <span class='wn'>" + dateFormatMITFromDate(data.trend_14['herd_reach_date']) + "</span>";
            top_sentence += "</span>.";
         } else {
            top_sentence = "Based on the latest trends,<br>" +  data.name;
            top_sentence += " could reach <span class='ugly_t'>herd immunity between"
            top_sentence += " <span class='wn'>" + dateFormatMITFromDate(data.trend_14['herd_reach_date']) + "</span> and ";
            top_sentence += " <span class='wn'>" + dateFormatMITFromDate(data.trend_7['herd_reach_date'])  + "</span>";
            top_sentence += "</span>.";
          } 
 

      } 
   }

   // Fill Top Table & Pies
   fill_top_table(data, phantom, herd_tresh);

   // Create top Sentence
   $('#top_summary').html("<div id='sum_main'>"+top_sentence+"</div>"); 
 
} 

function createSummary(data, phantom, herd_tresh) { 
  create_top_page(data, phantom, herd_tresh);
}