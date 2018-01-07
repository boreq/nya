var errorDiv, uploadList, progressBar, spinner;


$(function() {
    var uploadButton = $('#upload-button'),
        uploadInput = $('#upload-input');
    errorDiv = $('#upload-error');
    uploadList = $('#upload-list');
    progressBar = $('progress');
    spinner = $('#spinner');

    uploadButton.on('click', function(e) {
        e.preventDefault();
        uploadInput.trigger('click');
    });

    uploadInput.on('change', fileSelectHandler);
});


function fileSelectHandler(e) {
    var formData = new FormData();

    for (var i = 0; f = this.files[i]; i++) {
        formData.append(this.getAttribute('name'), f);
    }
    formData.append('expires', 0);

    upload(formData);
}


function upload(formData) {
    $.ajax({
        url: extData.uploadUrl,
        type: 'POST',
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', uploadProgressHandler, false);
            }
            return myXhr;
        },
        data: formData,
        beforeSend: beforeSendHandler,
        success: uploadSuccessHandler,
        error: uploadErrorHandler,
        cache: false,
        contentType: false,
        processData: false
    });
}


function uploadProgressHandler(e) {
    if (e.lengthComputable) {
        progressBar.css('display', 'block');
        progressBar.attr({value:e.loaded, max:e.total});
    }
}


function uploadSuccessHandler(data, textStatus, jqXHR) {
    spinner.css('display', 'none');
    listUploadedFiles(data['files']);
}


function uploadErrorHandler(jqXHR, textStatus, errorThrown) {
    spinner.css('display', 'none');

    try {
        var data = $.parseJSON(jqXHR.responseText);
        listUploadedFiles(data['files']);
        errorDiv.text(data['message']);
    }

    catch (e) {
        errorDiv.text('Error.');
    }
}


function beforeSendHandler(qXHR, settings) {
    errorDiv.empty();
    uploadList.empty();
    spinner.css('display', 'block');
}


function listUploadedFiles(files) {
    if (!files)
        return;
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        uploadList.append('<li><span class="file-name">' + file.original_filename + '</span><a class="file-url" href="' + file.url + '">' + file.url + '</a></li>');
    }
}

