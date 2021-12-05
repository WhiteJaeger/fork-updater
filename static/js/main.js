
function updateFork(event) {

    const url = $(event.data.row).attr('id')
    const strategy = event.data.strategy

    $(event.data.row).find('.fork-actions').addClass('loading');
    $(event.data.row).find('.fork-update-status').addClass('loading');
    const actionButtons = $(event.data.row).find('.fork-actions').children('.btn');
    actionButtons.each(function () {
        $(this).prop('disabled', true);
    });


    $.ajax({
        url: '/update',
        method: 'POST',
        data: JSON.stringify({'url': url, 'strategy': strategy}),
        mimeType: 'application/json',
        processData: false,
        success: async function (data) {
            if (data['returnCode'] !== '0') {
                alert(`Error! Code: ${data['returnCode']}`)
                $(event.data.row).find('.fork-actions').removeClass('loading');
                $(event.data.row).find('.fork-update-status').removeClass('loading');
            } else {
                $(event.data.row).find('.update-status-value').text(data['updateStatus']);
                $(event.data.row).find('.update-status-time').text(data['lastUpdateTime']);
                $(event.data.row).find('.fork-actions').removeClass('loading');
                $(event.data.row).find('.fork-update-status').removeClass('loading');
                actionButtons.each(function () {
                    $(this).prop('disabled', false);
                });
                $(event.data.row).addClass('table-success');
                await new Promise(r => setTimeout(r, 500));
                $(event.data.row).removeClass('table-success');
            }
        }
    });
}

function updateForkStatus(event) {

    const url = $(event.data.row).attr('id')

    $(event.data.row).find('.fork-upstream-status').addClass('loading');
    $(event.data.row).find('.fork-actions').addClass('loading');
    const actionButtons = $(event.data.row).find('.fork-actions').children('.btn');
    actionButtons.each(function () {
        $(this).prop('disabled', true);
    });


    $.ajax({
        url: '/update-fork-status',
        method: 'POST',
        data: JSON.stringify({'url': url}),
        mimeType: 'application/json',
        processData: false,
        success: async function (data) {
            if (data['returnCode'] !== '0' && data['returnCode'] !== '1') {
                alert(`Error! Code: ${data['returnCode']}`)
                $(event.data.row).find('.fork-actions').removeClass('loading');
                $(event.data.row).find('.fork-upstream-status').removeClass('loading');
            } else {
                $(event.data.row).find('.sync-status-value').text(data['syncStatus']);
                $(event.data.row).find('.sync-status-time').text(data['lastSyncTime']);
                $(event.data.row).find('.fork-actions').removeClass('loading');
                $(event.data.row).find('.fork-upstream-status').removeClass('loading');
                actionButtons.each(function () {
                    $(this).prop('disabled', false);
                });
                $(event.data.row).addClass('table-success');
                await new Promise(r => setTimeout(r, 500));
                $(event.data.row).removeClass('table-success');
            }
        }
    });
}

$body = $("body");

function syncForksWithGithub() {
    $body.addClass("loading");
    $.ajax({
        url: '/sync-forks-with-github',
        method: 'POST',
        mimeType: 'application/json',
        success: function (data) {
            if (data['result'] !== 'ok') {
                alert('ERROR!')
            } else {
                $body.removeClass("loading");
                location.reload();
            }
        }
    });
}


$(document).ready(function () {
    const forkRows = $('#fork-table').children('.fork-row');
    forkRows.each(function () {
        const row = this

        $(row).find('#update').each(function () {
            $(this).click({row: row, strategy: 'getNew'}, updateFork)
        })

        $(row).find('#update-keep-fork').each(function () {
            $(this).click({row: row, strategy: 'keepFork'}, updateFork)
        })

        $(row).find('#update-keep-upstream').each(function () {
            $(this).click({row: row, strategy: 'keepUpstream'}, updateFork)
        })

        $(row).find('#sync-fork-upstream-status').each(function () {
            $(this).click({row: row}, updateForkStatus)
        })
    });

    $('#sync-forks').click(syncForksWithGithub);
})
