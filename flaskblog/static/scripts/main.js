$(function() {

    let files;
    let fdata = new FormData();
    $("input[type=file]").on("change", function (e) {
        files = this.files;

        $.each(files, function (i, file) {
            fdata.append("file" + i, file);
        });

        $.ajax({
            url: "/upload_photo",
            type: "POST",
            data: fdata, 
            processData: false, 
            contentType: false, 
        });
    });

    $('.bottom_addphoto').click(() => {
        $('input[type=file]').click();
    });


    $('button.bottom_music').click(() => {
        if (!$('.panels').is(':visible') & (!$('button.bottom_text').hasClass('btn_selected'))) {
            $('button.bottom_music').toggleClass('btn_selected');
            $('.panels').slideToggle();
            $('.main').toggleClass('shadow');
            $('.panels_musik').show();
        } else if ($('.panels').is(':visible') & ($('button.bottom_text').hasClass('btn_selected'))) {
            $('button.bottom_music').toggleClass('btn_selected');
            $('button.bottom_text').toggleClass('btn_selected');
            $('.panels_text').hide();
            $('.panels_musik').show();
        } else if ($('.panels').is(':visible') & (!$('button.bottom_text').hasClass('btn_selected'))){
            $('button.bottom_music').toggleClass('btn_selected');
            $('.panels').slideToggle();
            $('.main').toggleClass('shadow');
            $('.panels_musik').hide();
        }
    });

    $('button.bottom_text').click(() => {
        if (!$('.panels').is(':visible') & (!$('button.bottom_music').hasClass('btn_selected'))) {
            $('button.bottom_text').toggleClass('btn_selected');
            $('.panels').slideToggle();
            $('.main').toggleClass('shadow');
            $('.panels_text').show();
        } else if ($('.panels').is(':visible') & ($('button.bottom_music').hasClass('btn_selected'))) {
            $('button.bottom_text').toggleClass('btn_selected');
            $('button.bottom_music').toggleClass('btn_selected');
            $('.panels_musik').hide();
            $('.panels_text').show();
        } else if ($('.panels').is(':visible') & (!$('button.bottom_music').hasClass('btn_selected'))){
            $('button.bottom_text').toggleClass('btn_selected');
            $('.panels').slideToggle();
            $('.main').toggleClass('shadow');
            $('.panels_text').hide();
        }
    });

    function radio() {
        for (let i = 0; i < a.length; i++) {
            $(a[i]).removeClass('checked');           
        }
    }



    let a = $('span.radio_btn').toArray();
    $(a[0]).click(() => {
        radio();
        $(a[0]).toggleClass('checked');
    });
    $(a[1]).click(() => {
        radio();
        $(a[1]).toggleClass('checked');
    });
    $(a[2]).click(() => {
        radio();
        $(a[2]).toggleClass('checked');
    });
    $(a[3]).click(() => {
        radio();
        $(a[3]).toggleClass('checked');
    });

});