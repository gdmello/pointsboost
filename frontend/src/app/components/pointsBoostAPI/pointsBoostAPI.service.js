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

    function user(fitbit_token) {

      return $http.post(apiHost + '/user?fitbit_token=' + fitbit_token)
        .then(userComplete)
        .catch(userFailed);

      function userComplete(response) {
        $log.info(angular.toJson(response.data));
      }

      function userFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }
  }
})();


