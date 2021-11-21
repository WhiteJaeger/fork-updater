
function postData(event) {

    const url = $(event.data.row).attr('id')


    $.ajax({
        url: '/update',
        method: 'POST',
        data: JSON.stringify({'url': url}),
        mimeType: 'application/json',
        processData: false,
        success: function (data) {
            // JSON.parse(data);
            if (data['returnCode'] === '0') {
                alert('Fork updated!')
            } else {
                alert('Error!')
            }
        }
    });
}


const forkRows = $('#fork-table').children('.fork-row');
forkRows.each(function () {
    const row = this
    $(row).find('#update').each(function () {
        $(this).click({row: row}, postData)
    })
});

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }
});

