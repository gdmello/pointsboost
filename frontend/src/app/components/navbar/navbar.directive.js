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
    function NavbarController(moment, $mdSidenav, pointsBoostAPI) {
      var vm = this;
      
      vm.user = pointsBoostAPI.getCurrentUser();
      if (vm.user) {
        
        vm.userName = vm.user.name;
        vm.userSummary = "You have collected " + vm.user.points_balance + " points so far!";

        vm.loginButtonText = "Logout"
      } else {
        vm.loginButtonText = "Login"
      }
      
      vm.openSideNav = function() {
       $mdSidenav('left').open()
        .then(function () {
          $log.debug("close LEFT is done");
        }); 
      }

      vm.closeSideNav = function() {
       $mdSidenav('left').close()
        .then(function () {
          $log.debug("close LEFT is done");
        }); 
      }
      
    }
  }

})();