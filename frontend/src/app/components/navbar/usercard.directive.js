(function() {
  'use strict';

  angular
    .module('pointsboost')
    .directive('userCard', userCard);

  /** @ngInject */
  function userCard() {
    var directive = {
      restrict: 'E',
      templateUrl: 'app/components/navbar/usercard.html',
      scope: {
        name: '@',
        description: '@'
      },
      controller: UsercardController,
    };

    return directive;

    /** @ngInject */
    function UsercardController() {
      
    }
      
    
  }

})();