$(function() {
    let files;
    let fdata = new FormData();
$("inpit[type=file]").on("change", function (e) {
    files = this.files;

    $.each(files, function (i, file) {
        fdata.append("file" + i, file);
    });

    $.ajax({
        url: "/upload_photo",
        type: "post",
        data: fdata, 
        processData: false, 
        contentType: false, 
    });
});


});