(function() {
  'use strict';

  angular
  .module('pointsboost')
  .factory('pointsBoostAPI', pointsBoostAPI);

  /** @ngInject */
  function pointsBoostAPI($log, $http, $cookies) {

    var USER_COOKIE = 'POINTSBOOST_USER';

    var apiHost = 'http://127.0.0.1:5000';
    var currentUser = null;

    var service = {
      apiHost: apiHost,
      user: user,
      getCurrentUser: getCurrentUser,
      setCurrentUser: setCurrentUser,
      logOut: logOut,
      newChallenges: newChallenges,
      acceptedChallenges: acceptedChallenges,
      enrollInAChallenge: enrollInAChallenge,
      userActivity: userActivity
    };

    return service;

    function getCurrentUser() {
      if (!currentUser) {
        currentUser = $cookies.getObject(USER_COOKIE)
      }

      return currentUser;
    }

    function setCurrentUser(user) {
      $log.info("Setting current user", user)
      currentUser = user;
      $cookies.putObject(USER_COOKIE, user);
    }
    

    function logOut() {
      $log.info("Logging out.")
      setCurrentUser(null)
    }

    function user(fitbit_token) {

      return $http.post(apiHost + '/user?fitbit_token=' + fitbit_token)
      .then(userComplete)
      .catch(userFailed);

      function userComplete(response) {
        var respJson = response.data;
        setCurrentUser(respJson);
        return true;
      }

      function userFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true))
      }
    }

    function userActivity(user_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

      return $http.get(apiHost + '/user/' + user_id + '/activity').then(function (response) {
        return response.data;
      });
    }

    function newChallenges(user_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

      return $http.get(apiHost + '/user/' + user_id + '/challenges/_new')
      .then(newChallengeList)
      .catch(newChallengeGetFailed);

      function newChallengeList(response) {
        return response.data;
      }

      function newChallengeGetFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

    function acceptedChallenges(user_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

      return $http.get(apiHost + '/user/' + user_id + '/challenges/_accepted')
      .then(acceptedChallengeList)
      .catch(acceptedChallengeGetFailed);

      function acceptedChallengeList(response) {
        return response.data;
      }

      function acceptedChallengeGetFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

    function enrollInAChallenge(user_id, challenge_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

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