var responses = pbjs.getBidResponses();
var output = [];
for (var adunit in responses) {
	if (responses.hasOwnProperty(adunit)) {
		var bids = responses[adunit].bids;
		for (var i = 0; i < bids.length; i++) {
			var b = bids[i];
			output.push({
				'adunit': adunit,
				'adId': b.adId,
				'bidder': b.bidder,
				'time': b.timeToRespond,
				'cpm': b.cpm,
				'msg': b.statusMessage,
				'size': b.width + 'x' + b.height
			});
		}
	}
}
if (output.length) {
	if (console.table) {
		console.table(output);
	} else {
		for (var j = 0; j < output.length; j++) {
			console.log(output[j]);
		}
	}
} else {
	console.warn('NO prebid responses');
}
