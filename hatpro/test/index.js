jQuery = $ = require('script!jquery');

require(["../js/hatpro.js",
         "script!flot/jquery.flot",
         "script!flot/jquery.flot.time",
        //  "script!vendor/jquery.flot.axislabels",
         "script!flot/jquery.flot.canvas"], function(hatpro) {

  $("#HATPRO").load('content.html', function() {
    hatpro('DACCIWA', '2016-06-29 UTC');
    // hatpro('DACCIWA');
  });
});
