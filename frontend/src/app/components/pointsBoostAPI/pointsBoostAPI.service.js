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
      user: user,
      newChallenges: newChallenges,
      acceptedChallenges: acceptedChallenges,
      enrollInAChallenge: enrollInAChallenge
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

    function newChallenges(user_id) {

      return $http.get(apiHost + '/user/' + user_id + '/challenges/_new')
        .then(newChallengeList)
        .catch(newChallengeGetFailed);

      function newChallengeList(response) {
        $log.info(angular.toJson(response.data));
      }

      function newChallengeGetFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

    function acceptedChallenges(user_id) {

      return $http.get(apiHost + '/user/' + user_id + '/challenges/_accepted')
        .then(acceptedChallengeList)
        .catch(acceptedChallengeGetFailed);

      function acceptedChallengeList(response) {
        $log.info(angular.toJson(response.data));
      }

      function acceptedChallengeGetFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

    function enrollInAChallenge(user_id, challenge_id) {

      return $http.post(apiHost + '/challenges/' + challenge_id + '/user/' + user_id)
        .then(enrolledChallenge)
        .catch(challengeEnrollmentFailed);

      function enrolledChallenge(response) {
        $log.info(angular.toJson(response.data));
      }

      function challengeEnrollmentFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

  }
})();