var plotData = require('./plotdata');

function sensor(id, name, unit, unit2) {
    var e = document.createElement('li');
    var link = document.createElement('a');
    e.setAttribute('id', id);
    e.setAttribute('unit', unit);
    e.setAttribute('title', name);
    if (unit2 !== undefined)
        e.setAttribute('unit2', unit2);
    link.setAttribute('href', '#');
    link.innerHTML = name;
    e.appendChild(link);
    return e;
}

function updateData(script, id ,date) {
    $.ajax({
        url: 'browserify/python/hatpro/'+script + '?id='+id + '&date='+date,
        method: 'post',
    });
}

function switchHighlight() {
        $(this).siblings().each(function() {
                $(this).removeClass("highlight");
        });
        $(this).addClass("highlight");
}

function getUTCDateText(day) {
    return day.getUTCFullYear() + "-" + (day.getUTCMonth() + 1) + "-" + day.getUTCDate();
}

module.exports = function(campaignName, date) {
    // valid date format: '2015-01-31 UTC', '2015/01/31 GMT'
    campaignName = campaignName || 'DACCIWA';

    if (typeof date === 'string') {
      var today = new Date(date);
    } else {
      var today = new Date();
    }
    var displayDay = today;

    $('#HATPRO #today').html(getUTCDateText(today));
    $('#HATPRO #day-minus').click( function() {
        displayDay = new Date(displayDay.getTime() - 86400*1000);
        $('#HATPRO #today').html(getUTCDateText(displayDay));
        $('#HATPRO .highlight').click()
    });
    $('#HATPRO #day-plus').on("click", function() {
        displayDay = new Date(displayDay.getTime() + 86400*1000);
        $('#HATPRO #today').html(getUTCDateText(displayDay));
        $('#HATPRO .highlight').click()
    });
    $('#HATPRO #day-last').on("click", function() {
        displayDay = today;
        $('#HATPRO #today').html(getUTCDateText(today));
        $('#HATPRO .highlight').click()
    });

    if (campaignName === 'DACCIWA') {
      $('#HATPRO #timeseries ul').append(sensor('L2PRW.ATM.WAT.VAP.CNT', 'atmosphere_water_vapor_content', 'kg m-2').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L2CLWVI.ATM.LIQ.WAT.CNT', 'atmosphere_liquid_water_content', 'g m-2').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L1TB.BRIGHT.TEMP', 'brightness_temperature', 'K').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L1TB.BRIGHT.TEMP.IR', 'brightness_temperature_IR', 'K').outerHTML);
      $('#HATPRO #timeseries ul li').first().addClass('highlight');

      $('#HATPRO #profile ul').append(sensor('L2TABL.TEM.PRF', 'air_temperature_profile', 'm', 'K').outerHTML);
      $('#HATPRO #profile ul').append(sensor('L2HUA.ABS.HUM.PRF', 'absolute_humidty_profile', 'm', '%').outerHTML);
      $('#HATPRO #profile ul li').first().addClass('highlight');
    } else {
      $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.WAT.VAP.CNT', 'atmosphere_water_vapor_content', 'kg m-2').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.LIQ.WAT.CNT', 'atmosphere_liquid_water_content', 'g m-2').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP', 'brightness_temperature', 'K').outerHTML);
      $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP.IR', 'brightness_temperature_IR', 'C').outerHTML);
      $('#HATPRO #timeseries ul li').first().addClass('highlight');

      $('#HATPRO #profile ul').append(sensor('L2C.AIR.POT.TEM.PRF', 'air_potential_temperature_profile', 'm', 'K').outerHTML);
      $('#HATPRO #profile ul').append(sensor('L2C.REL.HUM.PRF', 'relative_humidty_profile', 'm', '%').outerHTML);
      $('#HATPRO #profile ul li').first().addClass('highlight');
    }


    $(".navmenu#timeseries li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {div: '#HATPRO_1D', campaign: campaignName, dateDiv: '#HATPRO #today'}, plotData.plot_time);
      });

    $(".navmenu#profile li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {div: '#HATPRO_2D', colorBarDiv: '#HATPRO_2D_ColorBar', campaign: campaignName, dateDiv: '#HATPRO #today'}, plotData.plot_contour);
      });

    $(".navmenu li a").each(function() {
       $(this).attr('title', $(this).parent().attr('id'));
      });

    $(function() {
      $("#HATPRO .highlight").click();
    });

    $('#HATPRO #print-button').on("click", function()  {
      var img1 = $('div #HATPRO').data('img1');
      var img2 = $('div #HATPRO').data('img2');
      var title1 = $('div #HATPRO').data('title1');
      var title2 = $('div #HATPRO').data('title2');

      w = window.open();
      w.document.write("<div style='width: 800px'>");
      w.document.write("<div style='text-align: center; margin: 20px auto'>");
      w.document.write("<b>"+title1+"</b></div>");
      w.document.write("<img src='"+img1+"'/>");
      w.document.write("<br/><br/>");
      w.document.write("<div style='text-align: center; margin: 20px auto'>");
      w.document.write("<b>"+title2+"</b></div>");
      w.document.write("<img src='"+img2+"'/>");
      w.document.write("</div>");

      // chrome bug; wait then print
      var is_chrome = Boolean(w.chrome);

      if (is_chrome) {
        setTimeout(function() {
          w.document.close();
          w.focus();
          w.print();
          w.close();
        }, 250);
      } else {
          w.document.close();
          w.focus();
          w.print();
          w.close();
      }
  });
};
