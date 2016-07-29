(function() {
  'use strict';

  angular
    .module('pointsboost')
    .controller('LoginController', LoginController);

  /** @ngInject */
  function LoginController($timeout, $location, toastr, fitBitAuth, pointsBoostAPI) {

    var vm = this;

    vm.awesomeThings = [];
    vm.classAnimation = '';
    vm.creationDate = 1469725303069;



    activate();


    function activate() {
      
      // We log out the user on this page load.
      pointsBoostAPI.logOut();

      $timeout(function() {
        vm.classAnimation = 'rubberBand';
      }, 4000);
    }

    this.logIn = function() {
      fitBitAuth.authorize().then(function (token_user) {
        showLoggedInMsg();
        token_user = token_user.split("|");
        pointsBoostAPI.user(token_user[0], token_user[1]).then(function () {
          $location.path("/");
        })
      })
      showLoginMsg();
    }


    function showLoggedInMsg() {
      toastr.info('Retrieving your data.');
    }
    function showLoginMsg() {
      toastr.info('Logging you in. Follow the instructions on the open window.');
      vm.classAnimation = '';
    }

    // function getWebDevTec() {
    //   vm.awesomeThings = webDevTec.getTec();

    //   angular.forEach(vm.awesomeThings, function(awesomeThing) {
    //     awesomeThing.rank = Math.random();
    //   });
    // }
  }
})();