$(document).ready(function () {
    $('div.baseNav span').hover(
        function () {
            //show its submenu
            $('ul', this).css('left',$('a.baseNavMain', this).position()['left']);
            $('ul', this).css('top',$('a.baseNavMain', this).position()['top'] + 39);
            $('ul', this).show();

        },
        function () {
            //hide its submenu
            $('ul', this).hide();
        }
    );
});
