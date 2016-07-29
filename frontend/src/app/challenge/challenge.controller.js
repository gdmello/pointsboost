(function() {
  'use strict';

  angular
    .module('pointsboost')
    .controller('ChallengeController', ChallengeController);

  /** @ngInject */
  function ChallengeController($timeout, $q, toastr, pointsBoostAPI, moment, fitBitAuth, challengeFn) {
    var vm = this;

    vm.currentUser = pointsBoostAPI.getCurrentUser();
    vm.viewLoading = true;
    vm.challenges = []
    vm.userActivity = {}
    activate();


    function activate() {
      var challenges = challengeFn().then(function(response) {
        vm.challenges = response;
        var start = moment();
        vm.challenges.forEach(function (challenge) {
          var end   = moment(challenge.expiryTimestamp);
          challenge.friendlyTime = end.to(start, true);
        })
        console.log(vm.challenges);
      })
      var promiseUserActivity = pointsBoostAPI.userActivity().then(function(response) {
        vm.userActivity = response;
      });

      $q.all([challenges, promiseUserActivity]).then(function() {
        vm.viewLoading = false;
      });
    }


    vm.hasChallenges = function () {
      return vm.challenges.length > 0;
    }

  }
})();