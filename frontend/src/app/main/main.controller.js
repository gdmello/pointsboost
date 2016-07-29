(function() {
  'use strict';

  angular
    .module('pointsboost')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($timeout, $q, toastr, pointsBoostAPI, fitBitAuth) {
    var vm = this;

    vm.classAnimation = '';
    vm.creationDate = 1469725303069;
    vm.currentUser = pointsBoostAPI.getCurrentUser();
    vm.viewLoading = true;
    vm.activeChallenges = []
    vm.userActivity = {}
    activate();


    function activate() {
      var promiseActiveChallenges = pointsBoostAPI.acceptedChallenges().then(function(response) {
        vm.activeChallenges = response;
      })
      var promiseUserActivity = pointsBoostAPI.userActivity().then(function(response) {
        console.log(response)
        vm.userActivity = response;
      });

      $q.all([promiseActiveChallenges, promiseUserActivity]).then(function() {
        vm.viewLoading = false;
      });
    }


    vm.hasActiveChallenges = function () {
      return vm.activeChallenges.length > 0;
    }

  }
})();