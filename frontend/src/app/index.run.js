(function() {
  'use strict';

  angular
    .module('pointsboost')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {

    $log.debug('runBlock end');
  }

})();
