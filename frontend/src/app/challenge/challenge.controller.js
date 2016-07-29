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
    vm.challengeType = challengeType.name;
    vm.isAccepted = challengeType.name == "Accepted"
    activate();


    function activate() {
      var challenges = getChallenges()
      var promiseUserActivity = pointsBoostAPI.userActivity().then(function(response) {
        vm.userActivity = response;
      });

      $q.all([challenges, promiseUserActivity]).then(function() {
        vm.viewLoading = false;
      });
    }

    function getChallenges() {
      return challengeType.fn().then(function(response) {
        vm.challenges = response;
        var start = moment();
        vm.challenges.forEach(function (challenge) {
          var end   = moment(challenge.expiryTimestamp);
          challenge.friendlyTime = end.to(start, true);
        })
      })
    }

    vm.hasChallenges = function () {
      return vm.challenges.length > 0;
    }

    vm.acceptChallenge = function(cid) {
      pointsBoostAPI.enrollInAChallenge(cid).then(function() {
        toastr.success('<p>Congrats! You have accepted this challenge.</p>', 'Challenge accepted!', {timeOut: 5000})
        getChallenges();
      })
    }

    vm.rejectChallenge = function(cid) {
      pointsBoostAPI.rejectAChallenge(cid).then(function() {
        toastr.warning('<p>You have given up on this challenge.</p>', 'Challenge refused!', {timeOut: 5000})
        getChallenges();
      })
    }
  }
})();