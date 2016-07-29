(function() {
  'use strict';

  angular
  .module('pointsboost')
  .controller('ChallengeController', ChallengeController);

  /** @ngInject */
  function ChallengeController($timeout, $q, toastr, pointsBoostAPI, moment, fitBitAuth, challengeType) {
    var vm = this;

    vm.currentUser = pointsBoostAPI.getCurrentUser();
    vm.viewLoading = true;
    vm.challenges = []
    vm.userActivity = {}
    vm.challengeType = challengeType.name
    activate();


    function activate() {
      var challenges = challengeType.fn().then(function(response) {
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

    vm.acceptChallenge = function(cid) {
      pointsBoostAPI.enrollInAChallenge(cid).then(function() {
        toastr.success('<md-icon class="material-icons">done_all</md-icon><p>Congrats! You have accepted this challenge.</p>', 'Challenge accepted!', {timeOut: 5000})
      })
    }

    vm.rejectChallenge = function(cid) {
      pointsBoostAPI.enrollInAChallenge(cid).then(function() {
        toastr.success('<md-icon class="material-icons">done_all</md-icon><p>Fail! You have rejected this challenge.</p>', 'Challenge refused!', {timeOut: 5000})
      })
    }
  }
})();