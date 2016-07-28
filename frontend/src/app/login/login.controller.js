(function() {
  'use strict';

  angular
    .module('pointsboost')
    .controller('LoginController', LoginController);

  /** @ngInject */
  function LoginController($timeout, $rootScope, $location, toastr, fitBitAuth, pointsBoostAPI) {

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
      fitBitAuth.authorize().then(function (token) {
        showLoggedInMsg();
        pointsBoostAPI.user(token).then(function () {
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