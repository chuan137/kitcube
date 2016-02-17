var Base64 = require('./base64');
var THREE = require('three');

function formatDate(date) {
    var dd = date.getDate()
    if ( dd < 10 ) dd = '0' + dd;
    var mm = date.getMonth()+1
    if ( mm < 10 ) mm = '0' + mm;
    var yy = date.getFullYear();
    if ( yy < 10 ) yy = '0' + yy;
    return dd+'.'+mm+'.'+yy;
}

function utc_start_of_day_timestamp(now) {
    if (typeof now === "undefined") {
	now = new Date;
        var ts = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
    }
    else {
        now = now.split("-");
        var year = parseInt(now[0]);
        var month = parseInt(now[1]) - 1;
        var day = parseInt(now[2]);
        var ts = Date.UTC(year, month, day);
    } 
    return ts/1000;
}

function plot_time(event) {
    var moduleName = $(this).parents('div .ui-widget-content').attr('id');
    var id = $(this).attr('id');
    var title = $(this).attr('title');
    var unit = $(this).attr('unit');

    var timestamp = utc_start_of_day_timestamp(event.data.date);
    var data_file = ['hatpro_time', event.data.campaign, id,  timestamp].join('_') + '.json';
    var plotDiv = event.data.div;
    var plotWidth = parseFloat($(plotDiv).css('width'));

    $(plotDiv).html('');

    $.ajax({
        url: 'cache/' + data_file,
        method: 'post',
        dataType: 'json'
    }).done(function (data) {

        var timestamp = data.timestamp;
        var values = data.data;

        var factor = Math.floor(timestamp.length/plotWidth/3 + 0.5);
        if (factor == 0) factor = 1;

        var dataset = [];
        var rows = values.length;
        for (var w = 0; w < rows; w++) {
          var temp = [];
          for (var i = 0; i < timestamp.length; i+=factor) {
              temp.push([timestamp[i]*1000, values[w][i]]);
          }
          dataset.push(temp);
        }

        var d0 = new Date(timestamp[0]*1000);
        var dmin = Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth(), d0.getUTCDate(), 0, 0, 0);
        var dmax = dmin + 86400000;
        var hour = 3600000; 
        var ticks = [];
        for (var i=0; i<=24; i+=3) ticks.push(dmin + i*hour);

        var options = {
            canvas: true,
            xaxis: { 
                mode: "time",
                ticks: ticks,
                min: dmin,
                max: dmax,
                timeformat: "%H:%M",
                axisLabelUseCanvas: true,
                axisLabelPadding: 16,
                axisLabelFontSizePixels: 16,
                axisLabelFontFamily: 'Arial',
                axisLabelColour: 'black',
                axisLabel: 'UTC Time   on   ' + formatDate(new Date(dmin)),
            },
            yaxis: {
                labelWidth: 40,
                axisLabelUseCanvas: true,
                axisLabelFontFamily: 'Arial',
                axisLabel: '[ ' + unit + ' ]'
            },
            series: {
                shadowSize: 0,
            },
        }

        var newplot = $.plot(plotDiv, dataset, options);

        var canvas = newplot.getCanvas();
        var img = canvas.toDataURL("img/png");
        $('div #'+moduleName).data('img1', img);
        $('div #'+moduleName).data('title1', title);
    });
}

function plot_contour(event) {
    var moduleName = $(this).parents("div .ui-widget-content").attr('id');
    var unit = $(this).attr('unit');
    var unit2 = $(this).attr('unit2');
    var title = $(this).attr('title');
    var id = $(this).attr('id');

    var timestamp = utc_start_of_day_timestamp(event.data.date);
    var data_file = ['hatpro_contour', event.data.campaign, id,  timestamp].join('_') + '.json';
    var plotDiv = event.data.div;
    var colorBarDiv = event.data.colorBarDiv;

    $(plotDiv).html('');
 
    $.ajax({
        url: 'cache/' + data_file,
        method: 'post',
        dataType: 'json'
    }).done(function (data) {

        var d0 = new Date(data["xmin"]*1000);
        var dmin = Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth(), d0.getUTCDate(), 0, 0, 0);
        var dmax = dmin + 86400000;
        var hour = 3600000; 
        var ticks = [];
        for (var i=0; i<=24; i+=3) ticks.push(dmin + i*hour);

        var options_left = {
            canvas: true,
          series: { 
              lines: {
                  lineWidth: 1
              }, 
              shadowSize: 0.5, 
          },
          xaxis: { 
              mode: 'time',
              min: dmin, 
              max: dmax, 
              ticks: ticks,
              timeformat: "%H:%M",
              axisLabelUseCanvas: true,
              axisLabelPadding: 16,
              axisLabelFontSizePixels: 16,
              axisLabelFontFamily: 'Arial',
              axisLabelColour: 'black',
              axisLabel: 'UTC Time   on   ' + formatDate(new Date(dmin)),
          },
          yaxis: { 
              min: data["ymin"], 
              max: data["ymax"],
              labelWidth: 40,
              axisLabelUseCanvas: true,
              axisLabelFontFamily: 'Arial',
              axisLabel: '[ ' + unit + ' ]'
          },
          grid: { 
              margin: {} 
          },
          hooks: { 
              drawSeries: [fillShape] 
          }
        }

    var dataset=[];
    
    for (var i = 0; i < data['data'].length; i++) {
        for (var j = 0; j < data['data'][i]["path"].length; j++) {
            if (data['data'][i]["path"][j] != null)
                data['data'][i]["path"][j][0] *= 1000;
        }
        dataset.push({
            data: data['data'][i]["path"], 
            color: data['data'][i]["color"]});
    }

    function fillShape(plot, ctx, series) {

		var plotOffset = plot.getPlotOffset();
		var offset_x = plotOffset.left;
		var offset_y = plotOffset.top;

		function coord_x(x) {
			return offset_x + series.xaxis.p2c(x)
		};
		function coord_y(y) {
			return offset_y + series.yaxis.p2c(y)
		};

		var data = series.data;
		var chk = 0;

		ctx.beginPath();
		for (var i = 0; i < data.length; i++) {
			if (data[i] == null) {
				chk = 0;
				continue;
			}
			if (chk == 0) {
				ctx.moveTo(coord_x(data[i][0]), coord_y(data[i][1]));
				chk = 1;
			} else {
				ctx.lineTo(coord_x(data[i][0]), coord_y(data[i][1]));
			}
		}
		ctx.fillStyle = series.color;
		ctx.fill();
		ctx.closePath();
    }

    var colorbar = [];
    var colorbar_val = [];
    var color = '';
    var value = -1000;
    for (var i=0; i<data['data'].length; i++) {
        var newcolor = data['data'][i]['color'];
        var newval = data['data'][i]['layer'];
        if (newval < value) {
            break;
        } else {
            value = newval;
        }
        if (newcolor !== color) {
            colorbar.push(newcolor);
            colorbar_val.push(newval);
            color = newcolor;
        }
    }

    var ymin = colorbar_val[0];
    var ymax = colorbar_val[colorbar_val.length-1];

    // console.log(colorbar, colorbar_val);

    var cntrArr = []; //last points
    var tempObj = {
        data: [],
        color: "",
    };
    
    var cntDataset = [];
    for (var i=0; i<data['data'].length; i++) {
        cntDataset.push({
            data: [[0,colorbar_val[i]],
                   [1,colorbar_val[i]],
                   [2,colorbar_val[i]]],
            color: colorbar[i]
        });
    }

        var options_right = {
            canvas: true,
          series: { 
              lines:{
                  fillColor: {colors: colorbar},
                  fill: true,
              }, 
              shadowSize: 0, 
          },
          xaxis: {
              axisLabel:  unit2,
              axisLabelPadding: 16,
              tickLength: 0,
              ticks: [0, 1],
              tickColor: 'transparent',
              tickFormatter: function(val, axis) {
                  return ""
              },
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 12,
              axisLabelFontFamily: 'Arial',
          },
          yaxis: { 
              min: ymin, 
              max: ymax,
              position: "right",
              axisLabelUseCanvas: true,
              ticks: 10
          },
          grid: { 
              margin: {left:0, right:0, bottom: 17} 
          },
          hooks: { 
          }
        }

        var plot1 = $.plot(plotDiv, dataset, options_left);
        var plot2 = $.plot(colroBarDiv, cntDataset, options_right); 

        var canvas1 = plot1.getCanvas();
        var canvas2 = plot2.getCanvas();

        var canvas3 = document.createElement('canvas');
        canvas3.width = 800;
        canvas3.height = 400;
        var ctx3 = canvas3.getContext('2d');

        ctx3.drawImage(canvas1, 0, 10);
        ctx3.drawImage(canvas2, 700, 10);

        var img = canvas3.toDataURL("img/png");
        $('div #'+moduleName).data('img2', img);
        $('div #'+moduleName).data('title2', title);
  });
}

exports.plot_time = plot_time;
exports.plot_contour = plot_contour;
