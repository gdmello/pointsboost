(function() {
  'use strict';

  angular
    .module('pointsboost')
    .factory('fitBitAuth', fitBitAuth);

  /** @ngInject */
  function fitBitAuth($log, $http, $window, $httpParamSerializer, $cookies, $interval, $location, $q, locationHash) {
    var FITBIT_ACCESS_TOKEN_COOKIE = 'FITBIT_ACCESS_TOKEN_COOKIE_V2'
    var clientId = '227QRF'
    var clientSecret = 'aacdb90aaaa175c50e0556e1a50f35ab'
    var authScopes = ["activity", "nutrition", "heartrate", "location", "nutrition", "profile", "settings", "sleep", "social", "weight"]
    var redirectUri = ""
    if ($location.host().indexOf('local') < 0 && $location.host().indexOf('127.') < 0) {
      redirectUri = window.location.protocol + "//" + window.location.host + "/dist";
    } else {
      redirectUri = 'http://localhost:3000/';
    }
    
    var authorizeUri = 'https://www.fitbit.com/oauth2/authorize'
    console.log($location.path())
    var accessToken = "";
    var _authCheckTimer = null;

    var service = {
      authorize: authorize,
      locationHash: locationHash,
      isAuthenticated: isAuthenticated,
      getToken: getToken,
      setToken: setToken,
      authenticate: authenticate,
    };

    return service;

    function isAuthenticated() {
      if (getToken()) {
        return true;
      } else {
        return false;
      }
    }

    function getToken() {
      if (!accessToken) {
        accessToken = $cookies.get(FITBIT_ACCESS_TOKEN_COOKIE);
      }
      return accessToken;
    }

    function setToken(token) {
      accessToken = token;
      $cookies.put(FITBIT_ACCESS_TOKEN_COOKIE, token);
    }

    function authenticate() {
      if (locationHash != undefined && locationHash.indexOf("access_token") !== -1) {
        var tokenParsed = locationHash.match(/^#.*access_token=([A-z0-9_\-.]+).*$/)
        var userIdParsed = locationHash.match(/^#.*user_id=([A-z0-9_\-.]+).*$/)
        if (tokenParsed.length > 0 && userIdParsed.length > 0) {
          var token = tokenParsed[1] + "|" + userIdParsed[1];
          setToken(token)

          return true;
        }
      }
      return false;
    }

    function authorize() {
      // Clear out existing tokens.
      var deferred  = $q.defer();

      setToken("");
      var authorizeOpts = {
        'response_type': 'token',
        'client_id': clientId,
        'redirect_uri': redirectUri,
        'scope': authScopes.join(" "),
        'expires_in': '31536000',
        'state': 'login/'
      }
      $log.info("REDIRECT URI : " + redirectUri);
      var qs = $httpParamSerializer(authorizeOpts);
      var fullUrl = authorizeUri + "?" + qs;
      console.log("Opening auth: " + fullUrl)
      _openPopup(fullUrl);
      _kickOffAuthCheck(deferred);

      return deferred.promise;
    }

    function _kickOffAuthCheck(deferred) {
      if (_authCheckTimer != null) {
        $interval.cancel(_authCheckTimer);
      }
      _authCheckTimer = $interval(function() {
        if (isAuthenticated()) {
          $interval.cancel(_authCheckTimer);
          deferred.resolve(getToken());
        } else {
          $log.info("Not authenticated yet :(")
        }
      }, 500)
    }

    function _openPopup(url) {
      var left = screen.width / 2 - 200,
        top = screen.height / 2 - 250,
        popup = $window.open(url, '', "top=" + top + ",left=" + left + ",width=400,height=500"),
        interval = 1000;
    }


  }

  angular
    .module('pointsboost')
    .provider('fitBitAuth', fitBitAuthProvider);

  /** @ngInject */
  function fitBitAuthProvider() {

    var locationHash = "";

    this.setLocationHash = function(value) {
      locationHash = value;
    };

    this.$get = function($log, $http, $window, $cookies, $httpParamSerializer, $location, $interval, $q) {
      return new fitBitAuth($log, $http, $window, $httpParamSerializer, $cookies, $interval, $location, $q, locationHash)
    }
  }
})();