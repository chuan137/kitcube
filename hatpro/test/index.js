jQuery = $ = require('script!jquery');

require(["../js/hatpro.js",
         "script!flot/jquery.flot",
         "script!flot/jquery.flot.time",
        //  "script!vendor/jquery.flot.axislabels",
         "script!flot/jquery.flot.canvas"], function(hatpro) {

  $("#HATPRO").load('content.html', function() {
    // hatpro('DACCIWA', '2016-06-29 UTC');
    hatpro('HEADS', '2014-08-15 UTC');
    // hatpro('DACCIWA');
  });
});
