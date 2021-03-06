(function() {
  'use strict';

  angular
  .module('pointsboost')
  .factory('pointsBoostAPI', pointsBoostAPI);

  /** @ngInject */
  function pointsBoostAPI($log, $http, $location, $cookies) {

    var USER_COOKIE = 'POINTSBOOST_USER';
    var apiHost = '';  
    if ($location.host().indexOf('local') < 0 && $location.host().indexOf('127.') < 0) {
      apiHost = '';
    } else {
      apiHost = 'http://127.0.0.1:5000'
    }
    
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
      rejectAChallenge: rejectAChallenge,
      userActivity: userActivity,
      refreshUser: refreshUser
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

    function refreshUser() {
      return user('', getCurrentUser().fitbitId)
    }

    function user(fitbit_token, user_id) {

     return $http.post(apiHost + '/user?access_token=' + fitbit_token + "&user_id=" + user_id)
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

    function enrollInAChallenge(challenge_id, user_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

      return $http.post(apiHost + '/users/' + user_id +  '/challenges/' + challenge_id)
      .then(enrolledChallenge)
      .catch(challengeEnrollmentFailed);

      function enrolledChallenge(response) {
        $log.info(angular.toJson(response.data));
      }

      function challengeEnrollmentFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

    function rejectAChallenge(challenge_id, user_id) {
      if (!user_id) {
        user_id = getCurrentUser().userId;
      }

      return $http.post(apiHost + '/users/' + user_id +  '/challenges/' + challenge_id + "?action=reject")
      .then(rejectedChallenge)
      .catch(challengeRejectionFailed);

      function rejectedChallenge(response) {
        $log.info(angular.toJson(response.data));
      }

      function challengeRejectionFailed(error) {
        $log.error('XHR Failed for user.\n' + angular.toJson(error.data, true));
      }
    }

  }
})();