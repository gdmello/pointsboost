(function() {
  'use strict';

  angular
    .module('pointsboost')
    .directive('acmeNavbar', acmeNavbar);

  /** @ngInject */
  function acmeNavbar() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navbar/navbar.html',
      scope: {
        creationDate: '=',
      },
      controller: NavbarController,
      controllerAs: 'vm',
      bindToController: true
    };

    return directive;

    /** @ngInject */
    function NavbarController(moment, pointsBoostAPI) {
      var vm = this;

      if (pointsBoostAPI.getCurrentUser()) {
        vm.loginButtonText = "Logout"
      } else {
        vm.loginButtonText = "Login"
      }
      // "vm.creationDate" is available by directive option "bindToController: true"
      vm.relativeDate = moment(vm.creationDate)
        .fromNow();
    }
  }

})();