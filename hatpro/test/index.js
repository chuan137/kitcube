var $ = require('jquery');

require(["../js/hatpro.js"], function(hatpro) {

  console.log('hatpro ok');
  $("#HATPRO").load('content.html', hatpro);
});
