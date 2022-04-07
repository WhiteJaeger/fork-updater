function getActionButtonsFromRow(row) {
    return row.find('.fork-actions').children('.btn');
}

function disableActionButtons(buttons) {
    buttons.each(function () {
        $(this).prop('disabled', true);
    });
}

function enableActionButtons(buttons) {
    buttons.each(function () {
        $(this).prop('disabled', false);
    });
}


async function updateFork(event) {

    const url = $(event.data.row).attr('id');
    const strategy = event.data.strategy;

    $(event.data.row).find('.fork-actions').addClass('loading');
    $(event.data.row).find('.fork-update-status').addClass('loading');
    const actionButtons = getActionButtonsFromRow($(event.data.row));
    disableActionButtons(actionButtons);

    const response = await fetch('/update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json;charset=utf-8'},
        body: JSON.stringify({'url': url, 'strategy': strategy})
    });

    if (response.ok) {
        const result = await response.json();
        if (result['returnCode'] !== '0') {
            alert(`Error! Code: ${result['returnCode']}`);
            $(event.data.row).find('.fork-actions').removeClass('loading');
            $(event.data.row).find('.fork-update-status').removeClass('loading');
            return;
        }

        $(event.data.row).find('.update-status-value').text(result['updateStatus']);
        $(event.data.row).find('.update-status-time').text(result['lastUpdateTime']);

        $(event.data.row).find('.fork-actions').removeClass('loading');
        $(event.data.row).find('.fork-update-status').removeClass('loading');

        enableActionButtons(actionButtons);

        $(event.data.row).addClass('table-success');
        await new Promise(r => setTimeout(r, 500));
        $(event.data.row).removeClass('table-success');
    } else {
        alert('Error in server request!');
        $(event.data.row).find('.fork-actions').removeClass('loading');
        $(event.data.row).find('.fork-update-status').removeClass('loading');
    }
}

async function updateForkStatus(event) {

    const url = $(event.data.row).attr('id')

    $(event.data.row).find('.fork-upstream-status').addClass('loading');
    $(event.data.row).find('.fork-actions').addClass('loading');
    const actionButtons = getActionButtonsFromRow($(event.data.row));
    disableActionButtons(actionButtons);

    const response = await fetch('/update-fork-status', {
        method: 'POST',
        headers: {'Content-Type': 'application/json;charset=utf-8'},
        body: JSON.stringify({'url': url})
    });

    if (response.ok) {
        const result = await response.json();
        if (result['returnCode'] !== '0' && result['returnCode'] !== '1') {
            alert(`Error! Code: ${result['returnCode']}`);
            $(event.data.row).find('.fork-actions').removeClass('loading');
            $(event.data.row).find('.fork-upstream-status').removeClass('loading');
            return;
        }

        $(event.data.row).find('.sync-status-value').text(result['syncStatus']);
        $(event.data.row).find('.sync-status-time').text(result['lastSyncTime']);

        $(event.data.row).find('.fork-actions').removeClass('loading');
        $(event.data.row).find('.fork-upstream-status').removeClass('loading');
        enableActionButtons(actionButtons);

        $(event.data.row).addClass('table-success');
        await new Promise(r => setTimeout(r, 500));
        $(event.data.row).removeClass('table-success');
    } else {
        alert('Error!');
        $(event.data.row).find('.fork-actions').removeClass('loading');
        $(event.data.row).find('.fork-upstream-status').removeClass('loading');
    }
}

$body = $("body");

async function syncForksWithGithub() {
    $body.addClass('loading');
    const response = await fetch('/sync-forks-with-github');
    const result = await response.json();
    if (result['result'] !== 'ok') {
        alert('ERROR!')
    } else {
        $body.removeClass('loading');
        location.reload();
    }
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
