$(document).ready(function () {
    $('#search-form').keyup(function (event) {
        event.preventDefault();
        var current_request = null;
        let query = $('#search-input').val();
        let url = $('#search-url').attr('data-url');

        current_request = $.ajax({
            url: url,
            type: 'GET',
            data: {'query': query},
            beforeSend: function () {
                if (current_request != null) {
                    current_request.abort();
                }
            },
            success: function (data) {
                $('#card').empty()
                $('#navbar').hide()
                let json_array = JSON.parse(data);
                console.log(json_array);
                let res_data = '';
                for (var i = 0; i < json_array.length; i++) {
                    let edit_project = $('#edit-url').attr('data-url');
                    let edit_url = edit_project.replace("1", json_array[i].pk);
                    let complete = '<p class="red">pending</p>';
                    if (json_array[i].fields.is_completed) {
                        complete = '<p class="green">Completed</p>';
                    } else {
                        complete = '<p class="red">Pending</p>';
                    }
                    let tags = json_array[i].fields.tags.slice(1, -1).split(',');
                    let tag_data = '';
                    for (let tag in tags) {
                        tag_data += '<ul><li>' + tags[tag] + '</li></ul>'
                    }
                    res_data += '<div class="card">\n' +
                        '                <header class="card-header">\n' +
                        '                    <h3>' + json_array[i].fields.name + '<a href=' + edit_url + '><i\n' +
                        '                            class="ph ph-pencil-simple"></i></a>\n' +
                        '                    </h3>\n' +
                        '                    <div class="dis-box">\n' +
                        '                        <p><b>' + json_array[i].fields.acronym + '</b></p>\n' + complete +
                        '                    </div>\n' +
                        '                </header>\n' +
                        '                <article class="card-content">\n' +
                        '                    <p>\n' +
                        '                    <ul>\n' +
                        '                        <li><b>Description:</b> <br>' + json_array[i].fields.description + '</li>\n' +
                        '                        <li><b>Tags:</b> <br>' + tag_data +
                        '                        </li>\n' +
                        '                        <li><b>Deadline:</b> <br> ' + json_array[i].fields.dead_line + '</li>\n' +
                        '                        <li><b>Created by:</b> <br> ' + json_array[i].fields.created_by + '</li>\n' +
                        '                        <li><b>Created at:</b> <br> ' + json_array[i].fields.created_at + '</li>\n' +
                        '                        <li><b>Updated by:</b> <br>  ' + json_array[i].fields.updated_by + '</li>\n' +
                        '                        <li><b>Updated at:</b> <br> ' + json_array[i].fields.updated_at + '</li>\n' +
                        '                </ul>\n' +
                        '                </article>\n' +
                        '                <footer class="card-footer">\n' +
                        '                    <a class="footer-link">View Tasks</a>\n' +
                        '                </footer>\n' +
                        '            </div>'
                }
                $('#card').html(res_data)
            },
            complete: function () {
                current_request = null;
            }
        });
    });
});