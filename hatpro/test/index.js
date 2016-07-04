jQuery = $ = require('script!jquery');

require(["../js/hatpro.js",
         "script!flot/jquery.flot",
         "script!flot/jquery.flot.time"], function(hatpro) {

  $("#HATPRO").load('content.html', function() {
    hatpro('2016-06-29 UTC');
  });
});
