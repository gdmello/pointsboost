(function() {
  'use strict';

  angular
    .module('pointsboost')
    .config(config);

  /** @ngInject */
  function config($logProvider, $mdThemingProvider, toastrConfig) {

    
    $mdThemingProvider.theme('forest')
      .primaryPalette('brown')
      .accentPalette('green');
  
    // Enable log
    $logProvider.debugEnabled(true);

    // Set options third-party lib
    toastrConfig.allowHtml = true;
    toastrConfig.timeOut = 3000;
    toastrConfig.positionClass = 'toast-top-right';
    toastrConfig.preventDuplicates = true;
    toastrConfig.progressBar = true;
  }

})();