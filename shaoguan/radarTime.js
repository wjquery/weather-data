"use strict";
var page = require('webpage').create();
var fs = require('fs');
page.open('http://www.sgqx.gov.cn/monitor/auto-monitor!toAutoMonitor.action', function(status) {
	console.log("Status :" + status);
	if(status == "success") {
		 
		 var input = page.evaluate(function(){
			return document.querySelector('input[id="radarTime"]').value;
		});
		console.log(input);
		fs.write('radarTime.dat', input, {mode: 'w',charset: 'UTF-8'});
		phantom.exit();
        
	}
});