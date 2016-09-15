(function($) {
    $('.djn-group-nested').find('b:first').text('Default settings').next().remove();
    $('.field-weekday:first').hide();

    $(document).on('formset:added', function(event, $row, formsetName) {

        $('.field-weekday').find('input[type=checkbox]').click(function () {
            ch_val = $(this).val()
            if (!$(this).is(":checked")){
                $(this).parents('.djn-group-nested').children().find('.field-weekday').find('input[type=checkbox][value=' + ch_val + ']').prop('disabled', false);
            }else{
                $(this).parents('.djn-group-nested').children().find('.field-weekday').find('input[type=checkbox][value=' + ch_val + ']').prop('disabled', true);
                $(this).prop('disabled', false)
            }

        });

    });

    $(document).on('formset:removed', function(event, $row, formsetName) {

    });
})(django.jQuery);