(function() {
  'use strict';

  angular
    .module('pointsboost')
    .controller('MainController', MainController);

  /** @ngInject */
  function MainController($timeout, toastr, pointsBoostAPI, fitBitAuth) {
    var vm = this;

    vm.classAnimation = '';
    vm.creationDate = 1469725303069;
    vm.currentUser = pointsBoostAPI.getCurrentUser();

    activate();


    function activate() {
      $timeout(function() {
        vm.classAnimation = 'rubberBand';
      }, 4000);
    }

  }
})();