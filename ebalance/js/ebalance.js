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


function switchHighlight() {
        $(this).siblings().each(function() {
                $(this).removeClass("highlight");
        });
        $(this).addClass("highlight");
}
        
module.exports = function() {

    $('#EBALANCE #timeseries ul').append(sensor('PYG_T_BOT_AVG', 'some sensor', 'some unit').outerHTML);
    $('#EBALANCE #timeseries ul').append(sensor('INK_G_INKW_AVG', 'some sensor', 'some unit').outerHTML);

    $(".navmenu#timeseries li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {div: '#EBALANCE_1D', campaign: 'HEADS', date: '2014-12-7'}, plotData.plot_time);
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

