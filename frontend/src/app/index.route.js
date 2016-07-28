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
            .otherwise({
                redirectTo: '/'
            });
    }

    var checkRouting = function($q, $location, $window, fitBitAuth) {
        var deferred = $q.defer();

        // We're already authenticated.
        if (fitBitAuth.isAuthenticated()) {
            return true;

            // We're authenticating (this page was loaded as a result of fitbit redirect_uri)
        } else if (fitBitAuth.authenticate()) {
            $window.close();

            // We're not logged in
        } else {
            deferred.reject();
            $location.path("/login")
        }
        return deferred.promise;
    };

})();