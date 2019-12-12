$(function () {
    var $content_md = $('#div_id_content_md');
    var $content_ck = $('#div_id_content_ck');
    var $is_md = $('#id_is_md');
    var $witch_editor = function(is_md){
        if(is_md){
            $content_md.show();
            $content_ck.hide();
        }
        else{
            $content_md.hide();
            $content_ck.show();
        }
    };
    $is_md.on('click', function () {
        $witch_editor($(this).is(':checked'));
    });
    $witch_editor($is_md.is(':checked'));
});