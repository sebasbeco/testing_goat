window.SuperLists = {};
window.SuperLists.initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        console.log('in keypress handler');
        $('.has-error').hide();
    });
};
