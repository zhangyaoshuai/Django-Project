$(function () {
    //click on input field to clear it:
    $("input").focus(function () {
		$(this).val('');
	});
});