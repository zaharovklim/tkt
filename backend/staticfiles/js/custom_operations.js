(function($) {
    $('.djn-group-nested').find('b:first').text('Default settings').next().remove();
    function check_weekday(){
        $('.items').find('.items').each(function(){
            var checked = []
            $(this).find('.field-weekday').find('input[type=checkbox]').each(function () {
                ch_val = $(this).val()
                if (checked.indexOf(ch_val) == -1){
                    if (!$(this).is(":checked")){
                        $(this).parents('.djn-items').first().children().find('.field-weekday').find('input[type=checkbox][value=' + ch_val + ']').prop('disabled', false);
                    }else{
                        $(this).parents('.djn-items').first().children().find('.field-weekday').find('input[type=checkbox][value=' + ch_val + ']').prop('disabled', true);
                        $(this).prop('disabled', false);
                        checked.push(ch_val);
                    }
                }

            });
        });
    }

    $(document).ready(function() {
        check_weekday();
        $('.field-weekday').find('input[type=checkbox]').click(function () {
            check_weekday();
            });
        $('.items h2').click(function(){
            var items_group = $(this).parents('.inline-group').first().find('.items')
            var add_row = $(this).parents('.inline-group').first().find('.add-row')
            if (items_group.is(":visible")){
                items_group.slideUp();
                add_row.slideUp();
            }else{
                items_group.slideDown();
                add_row.slideDown();
            }
        });
    });


})(django.jQuery);