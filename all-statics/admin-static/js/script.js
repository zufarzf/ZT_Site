$("#select_all").click(function () {
    $(':checkbox').prop('checked', this.checked);
});

$('#delete-btn').on('click', function (e) {
    e.preventDefault();
    // selecting all checkboxes
    // of group language using querySelectorAll()
    var checkboxes = document.querySelectorAll('input[name="check"]');
    var values = [];
    // looping through all checkboxes
    // if checked property is true then push
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == true) {
            values.push(checkboxes[i].value);
        }
    }
    // alert(values)
    $('#input_for_submit_cheked_checkboxs').val(values);
    $("input#submit_cheked_checkboxs").click();
});



// Search in teble
$(document).ready(function () {
    $("#search_in_list").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



