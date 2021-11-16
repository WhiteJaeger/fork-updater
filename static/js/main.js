
function postData(event) {

    const url = $(event.data.row).attr('id')


    $.ajax({
        url: '/update',
        method: 'POST',
        data: JSON.stringify({'url': url}),
        mimeType: 'application/json',
        processData: false,
        success: function (data) {
            JSON.parse(data);
        }
    });
}


const forkRows = $('#fork-table').children('.fork-row');
forkRows.each(function () {
    const row = this
    $(row).find('#update').each(function () {
        $(this).click({row: row}, postData)
    })
})
