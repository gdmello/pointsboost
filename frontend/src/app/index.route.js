(function() {
  'use strict';
  angular
    .module('pointsboost')
    .config(routeConfig);

  function routeConfig($routeProvider, fitBitAuthProvider) {

    fitBitAuthProvider.setLocationHash(window.location.hash)


    $routeProvider
      .when('/login', {
        templateUrl: 'app/login/login.html',
        controller: 'LoginController',
        controllerAs: 'login',
      })
      .when('/', {
        templateUrl: 'app/main/main.html',
        controller: 'MainController',
        controllerAs: 'main',
        resolve: {
          factory: checkRouting
        }
      })
      .when('/accepted-challenges', {
        templateUrl: 'app/challenge/challenge.html',
        controller: 'ChallengeController',
        controllerAs: 'challenge',
        resolve: {
          factory: checkRouting,
          challengeType: function(pointsBoostAPI) {
            return { name: 'Accepted', fn: pointsBoostAPI.acceptedChallenges };
          }
        }
      })
      .when('/new-challenges', {
        templateUrl: 'app/challenge/challenge.html',
        controller: 'ChallengeController',
        controllerAs: 'challenge',
        resolve: {
          factory: checkRouting,
          challengeType: function(pointsBoostAPI) {
            return { name: 'New', fn: pointsBoostAPI.newChallenges };
          }
        }
      })
      .otherwise({
        redirectTo: '/'
      });
  }

  var checkRouting = function($q, $location, $window, fitBitAuth, pointsBoostAPI) {
    var deferred = $q.defer();

    // We're already authenticated.
    if (pointsBoostAPI.getCurrentUser()) {
      return true;
    } else if (fitBitAuth.authenticate()) {
        // Success!
        $window.close();  
    } else {
        // Couldn't log you in.
        deferred.reject();
        $location.path("/login")
    }
    return deferred.promise;
  };

})();