// Need these for work to return a simulated bid response from various demand end-points when visiting a site served over HTTPS.

// Secure JPT Requests
if(oSession.HostnameIs("secure.adnxs.com") && oSession.isHTTPS){
    oSession.oRequest.headers.UriScheme = "http";
    oSession.hostname="demo.arrepiblik.com";
    oSession.port="3001";
}

// Any Prebid AST Request
if(oSession.HostnameIs("ib.adnxs.com") && oSession.isHTTPS){
    oSession.oRequest.headers.UriScheme = "http";
    oSession.hostname="demo.arrepiblik.com";
    oSession.PathAndQuery = oSession.PathAndQuery.Replace("ut/v3/prebid", "ast");
    oSession.port="3001";
}

// DMX Requests
if(oSession.HostnameIs("rtb.districtm.io") && oSession.isHTTPS){
    oSession.oRequest.headers.UriScheme = "http";
    oSession.hostname="demo.arrepiblik.com";
    oSession.PathAndQuery = oSession.PathAndQuery.Replace("bid?", "dmx?");
    oSession.port="3001";
}
