(function() {
  'use strict';

  angular
    .module('pointsboost')
    .factory('fitBitAuth', fitBitAuth);

  /** @ngInject */
  function fitBitAuth($log, $http, $window, $httpParamSerializer, $cookies, $interval, $location, $q, locationHash) {


    var TOKEN_COOKIE = 'FITBIT_TOKEN'

    // Implicit grant flow

    var clientId = '227QRF'
    var clientSecret = 'aacdb90aaaa175c50e0556e1a50f35ab'
    var authScopes = ["activity", "nutrition", "heartrate", "location", "nutrition", "profile", "settings", "sleep", "social", "weight"]
    var redirectUri = 'http://localhost:3000'
    var authorizeUri = 'https://www.fitbit.com/oauth2/authorize'

    var accessToken = "";
    var authCheckTimer = null;

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
        accessToken = $cookies.get(TOKEN_COOKIE, accessToken);
      }
      return accessToken;
    }

    function setToken(token) {
      accessToken = token
      $cookies.put(TOKEN_COOKIE, accessToken);
    }

    function authenticate() {
      if (locationHash != undefined && locationHash.indexOf("access_token") !== -1) {
        var parsed = locationHash.match(/^#.*access_token=([A-z0-9_\-.]+).*$/)
        if (parsed.length > 0) {
          var token = parsed[1];
          setToken(token)
          return true;
        }
      }
      return false;
    }

    function authorize() {

      var deferred  = $q.defer();

      var authorizeOpts = {
        'response_type': 'token',
        'client_id': clientId,
        'redirect_uri': redirectUri,
        'scope': authScopes.join(" "),
        'expires_in': '31536000',
        'state': 'login/'
      }
      var qs = $httpParamSerializer(authorizeOpts);
      var fullUrl = authorizeUri + "?" + qs;
      console.log("Opening auth: " + fullUrl)
      _openPopup(fullUrl);
      _kickOffAuthCheck(deferred);

      return deferred.promise;
    }

    function _kickOffAuthCheck(deferred) {
      if (authCheckTimer != null) {
        $interval.cancel(authCheckTimer);
      }
      authCheckTimer = $interval(function() {
        if (isAuthenticated()) {
          $interval.cancel(authCheckTimer);
          deferred.resolve(getToken());
        }
      }, 2000)
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