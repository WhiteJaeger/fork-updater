
function postData(event) {

    const url = $(event.data.row).attr('id')
    const strategy = event.data.strategy


    $.ajax({
        url: '/update',
        method: 'POST',
        data: JSON.stringify({'url': url, 'strategy': strategy}),
        mimeType: 'application/json',
        processData: false,
        success: function (data) {
            if (data['returnCode'] === '0') {
                alert('Fork updated!')
            } else {
                alert(`Error! Code: ${data['returnCode']}`)
            }
        }
    });
}


const forkRows = $('#fork-table').children('.fork-row');
forkRows.each(function () {
    const row = this
    $(row).find('#update').each(function () {
        $(this).click({row: row, strategy: 'getNew'}, postData)
    })

    $(row).find('#update-keep-fork').each(function () {
        $(this).click({row: row, strategy: 'keepFork'}, postData)
    })

    $(row).find('#update-keep-upstream').each(function () {
        $(this).click({row: row, strategy: 'keepUpstream'}, postData)
    })
});

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }
});

