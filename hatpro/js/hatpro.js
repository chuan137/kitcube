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
        
module.exports = function() {

    $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.WAT.VAP.CNT', 'atmosphere_water_vapor_content', 'kg m-2').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.LIQ.WAT.CNT', 'atmosphere_liquid_water_content', 'g m-2').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP', 'brightness_temperature', 'K').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP.IR', 'brightness_temperature_IR', 'C').outerHTML);
    $('#HATPRO #timeseries ul li').first().addClass('highlight');

    $('#HATPRO #profile ul').append(sensor('L2C.AIR.POT.TEM.PRF', 'air_potential_temperature_profile', 'm', 'K').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2C.REL.HUM.PRF', 'relative_humidty_profile', 'm', '%').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2A.ATM.WAT.VAP.CNT.PRF', 'atmosphere_water_vapor_content', 'azimuth angle', 'kg m-2').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2A.ATM.LIQ.WAT.CNT.PRF', 'atmosphere_liquid_water_content', 'azimuth angle', 'g m-2').outerHTML);
    $('#HATPRO #profile ul li').first().addClass('highlight');

    $(".navmenu#timeseries li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {div: '#HATPRO_1D', campaign: 'HEADS', date: '2014-12-7'}, plotData.plot_time);
      });

    $(".navmenu#profile li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {div: '#HATPRO_2D', colorBarDiv: '#HATPRO_2D_ColorBar', campaign: 'HEADS', date: '2014-12-7'}, plotData.plot_contour);
      });

    $(".navmenu li a").each(function() {
       $(this).attr('title', $(this).parent().attr('id'));
      });

    $("#radiotime input").click(function(){ 
      var panelname = $(this).parents("div .ui-widget-content").attr('id');
      $(".highlight").click();
    }); 

    // $(function() {
    //   $(".highlight").click();
    // }); 
};

