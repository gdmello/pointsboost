(function() {
    'use strict';

    angular
        .module('pointsboost')
        .controller('LoginController', LoginController);

    /** @ngInject */
    function LoginController($timeout, $rootScope, webDevTec, toastr, fitBitAuth) {

        var vm = this;

        vm.awesomeThings = [];
        vm.classAnimation = '';
        vm.creationDate = 1469725303069;



        activate();


        function activate() {
            $timeout(function() {
                vm.classAnimation = 'rubberBand';
            }, 4000);
        }

        this.authorizeFitBit = function() {
            fitBitAuth.authorize()
            showLoginMsg();
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