var errorDiv, uploadList, progressBar, spinner, uploadInput, uploadButton, dropZone;


/*
    A separate div called "#drop-zone" is needed because of the problems related
    to dropping the files on the text label instead of the parent button.

    While the click event is not stopped by the fact that the child element
    covers the parent element, the same situation is a problem when the drop
    event occurs.
*/


$(function() {
    uploadButton = $('#upload-button');
    uploadInput = $('#upload-input');
    errorDiv = $('#upload-error');
    uploadList = $('#upload-list');
    progressBar = $('progress');
    spinner = $('#spinner');
    dropZone = $('#drop-zone');

    // Clicking on the button.
    uploadButton.on('click', function(e) {
        e.preventDefault();
        uploadInput.trigger('click');
    });

    uploadInput.on('change', fileSelectHandler);

    // Dropping the files
    dropZone.on('dragover dragenter', function() {
        uploadButton.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function() {
        uploadButton.removeClass('is-dragover');
    })
    .on('dragover', function(e) {
        e.preventDefault();
    })
    .on('dragend', function(e) {
        // Remove all of the drag data
        var dt = e.dataTransfer;
        if (dt.items) {
            // Use DataTransferItemList interface to remove the drag data
            for (var i = 0; i < dt.items.length; i++) {
                dt.items.remove(i);
            }
        } else {
            // Use DataTransfer interface to remove the drag data
            e.dataTransfer.clearData();
        }
    });

    dropZone.on('drop', fileDropHandler);
});


function fileSelectHandler(e) {
    var formData = new FormData();
    for (var i = 0; f = this.files[i]; i++) {
        formData.append(uploadInput.attr('name'), f);
    }
    formData.append('expires', 0);
    upload(formData);
}


function fileDropHandler(e) {
    e.preventDefault();

    var formData = new FormData();
    $.each(e.originalEvent.dataTransfer.files, function(i, f) {
        formData.append(uploadInput.attr('name'), f);
    });
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

