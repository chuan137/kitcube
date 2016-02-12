 $(document).ready(function() {
    $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.WAT.VAP.CNT', 'water-vapor content', 'kg m-2').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L2A.ATM.LIQ.WAT.CNT', 'liquid-water content', 'g m-2').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP', 'brightness temperature', 'K').outerHTML);
    $('#HATPRO #timeseries ul').append(sensor('L1B.BRIGHT.TEMP.IR', 'brightness temperature IR', 'C').outerHTML);
    $('#HATPRO #timeseries ul li').first().addClass('highlight');

    $('#HATPRO #profile ul').append(sensor('L2C.AIR.POT.TEM.PRF', 'air potential temperature', 'm', 'K').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2C.REL.HUM.PRF', 'relative humidty profiling', 'm', '%').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2A.ATM.WAT.VAP.CNT.PRF', 'water-vapor content', 'azimuth angle', 'kg m-2').outerHTML);
    $('#HATPRO #profile ul').append(sensor('L2A.ATM.LIQ.WAT.CNT.PRF', 'liquid-water content', 'azimuth angle', 'g m-2').outerHTML);
    $('#HATPRO #profile ul li').first().addClass('highlight');

    setInterval(function update() {
        updateData('hatpro_time.cgi', 'L2A.ATM.WAT.VAP.CNT', '0d');
        updateData('hatpro_time.cgi', 'L2A.ATM.WAT.VAP.CNT', '1d');
        updateData('hatpro_time.cgi', 'L2A.ATM.WAT.VAP.CNT', '2d');
        updateData('hatpro_time.cgi', 'L2A.ATM.LIQ.WAT.CNT', '0d');
        updateData('hatpro_time.cgi', 'L2A.ATM.LIQ.WAT.CNT', '1d');
        updateData('hatpro_time.cgi', 'L2A.ATM.LIQ.WAT.CNT', '2d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP', '0d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP', '1d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP', '2d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP.IR', '0d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP.IR', '1d');
        updateData('hatpro_time.cgi', 'L1B.BRIGHT.TEMP.IR', '2d');
        updateData('hatpro_contour.cgi', 'L2C.AIR.POT.TEM.PRF', '0d');
        updateData('hatpro_contour.cgi', 'L2C.AIR.POT.TEM.PRF', '1d');
        updateData('hatpro_contour.cgi', 'L2C.AIR.POT.TEM.PRF', '2d');
        updateData('hatpro_contour.cgi', 'L2C.REL.HUM.PRF', '0d');
        updateData('hatpro_contour.cgi', 'L2C.REL.HUM.PRF', '1d');
        updateData('hatpro_contour.cgi', 'L2C.REL.HUM.PRF', '2d');
        updateData('hatpro_content.cgi', 'L2A.ATM.WAT.VAP.CNT', '0d');
        updateData('hatpro_content.cgi', 'L2A.ATM.WAT.VAP.CNT', '1d');
        updateData('hatpro_content.cgi', 'L2A.ATM.WAT.VAP.CNT', '2d');
        updateData('hatpro_content.cgi', 'L2A.ATM.LIQ.WAT.CNT', '0d');
        updateData('hatpro_content.cgi', 'L2A.ATM.LIQ.WAT.CNT', '1d');
        updateData('hatpro_content.cgi', 'L2A.ATM.LIQ.WAT.CNT', '2d');
 

        }, 300*1000);

    $( "#radiotime" ).buttonset();

    $(".navmenu#timeseries li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", {target: '#HATPRO_1D'}, makePlotD1);
      });

    $(".navmenu#profile li").each(function(index) {
        $(this).on("click", switchHighlight);
        $(this).on("click", makePlotD2);
      });

    $(".navmenu li a").each(function() {
       $(this).attr('title', $(this).parent().attr('id'));
      });

    $("#radiotime input").click(function(){ 
      var panelname = $(this).parents("div .ui-widget-content").attr('id');
      $(".highlight").click();
    }); 

    $(function() {
      $(".highlight").click();
    }); 

    $('.printbutton').button();
    $('.printbutton').click(function()  {
      var img1 = $(this).parents("div .ui-widget-content").data('img1');
      var img2 = $(this).parents("div .ui-widget-content").data('img2');
      var title1 = $(this).parents("div .ui-widget-content").data('title1');
      var title2 = $(this).parents("div .ui-widget-content").data('title2');

      w = window.open();
      w.document.write("<div style='text-align: center'><b>");
      w.document.write(title1);
      w.document.write("</b></div>");
      w.document.write("<img src='"+img1+"'/>");
      w.document.write("<br><br><div style='text-align: center'><b>");
      w.document.write(title2);
      w.document.write("</b></div>");
      w.document.write("<img src='"+img2+"'/>");
      w.print();
      w.close();
    });

  });

