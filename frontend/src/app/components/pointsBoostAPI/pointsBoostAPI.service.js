(function() {
  'use strict';

  angular
    .module('pointsboost')
    .factory('pointsBoostAPI', pointsBoostAPI);

  /** @ngInject */
  function pointsBoostAPI($log, $http) {
    var apiHost = 'http://127.0.0.1:5000';

    var service = {
      apiHost: apiHost,
      user: user
    };

    return service;

    function user(accessToken) {

      return $http.post(apiHost + '/user?accessToken=' + accessToken)
        .then(userComplete)
        .catch(userFailed);

      function userComplete(response) {
        return response.data;
      }

      function userFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }
  }
})();


