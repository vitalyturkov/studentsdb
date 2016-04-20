function initJournal() {
	var indicator = $('#ajax-progress-indicator');
	var error_indicator = $('#ajax-error-indicator');
	var ajax_info = $('#ajax-info');

	$('.day-box input[type="checkbox"]').click(function(event){
		var box = $(this);
		$.ajax(box.data('url'), {
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data': {
				'pk': box.data('student-id'),
				'date': box.data('date'),
				'present': box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr, settings){
				indicator.show();
			},
			'error': function(xhr, status, error){
				ajax_info.hide();
				error_indicator.show();
			},
			'success': function(data, status, xhr){
				error_indicator.hide();
				ajax_info.show();
				indicator.hide();
			}
		});
	});
}

function initGroupSelector() {
	// look up select element with groups and attach our even handler
	// on field "change" event
	$('#group-selector select').change(function(event){
		// get value of currently selected group option
		var group = $(this).val();

		if (group) {
			// set cookie with expiration date 1 year since now;
			// cookie creation function takes period in days
			$.cookie('current_group', group, {'path': '/', 'expires': 365});
		} else {
			// otherwise we delete the cookie
			$.removeCookie('current_group', {'path': '/'});
		}
		// and reload a page
		location.reload(true);
		return true;
	});
}

function initDateFields() {
	//placeholder to "birthday" field
	$('input#id_birthday').attr("placeholder", "Ваш день народження");

	$('input.dateinput').datetimepicker({
	locale: 'ru',
	format: 'YYYY-MM-DD'

	}).on('dp.hide', function(event){
		$(this).blur();
	});

	//click to calendar icon
	$('#calend').click(function(){
		$('#id_birthday').focus();
	});

	//click to calendar icon at exam forms
	$("#examcalend").click(function(){
		$("#examtime").focus();
	});
}



function initEditStudentPage() {
	$('a.student-edit-form-link').click(function(event){
		var link = $(this);
		var url = link.attr('href');
		$.ajax({
			'url': url,
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'), html = $(data),
					form = html.find('#content-column form');
					console.log(html.text());
				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);
				// init our edit form
				initEditStudentForm(form, modal, url);
				// setup and show modal window finally
				modal.modal({
					'keyboard': false,
					'show': true
				});
			},
			'error': function(){
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
				return false;
			}
		});

		return false;
	});
}

function initEditStudentForm(form, modal, url) {
	// attach datepicker
	initDateFields();

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'url': url,
		'dataType': 'html',
		'error': function(){
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		},
		'success': function(data, status, xhr) {

			var html = $(data), newform = html.find('#content-column form');
			console.log(html.text());

			// copy alert to modal window
			modal.find('.modal-body').html(html.find('.alert'));
			// copy form to modal if we found it in server response

			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);
				// initialize form fields and buttons
				initEditStudentForm(newform, modal, url);
			} else {
				// if no form, it means success and we need to reload page
				// to get updated students list;
				// reload after 1 seconds, so that user can read
				// success message
				console.log(html);
				//show();
				setTimeout(function(){modal.modal('hide');}, 1000);
				

			}
		}
	});
}

$(document).ready(function(){
	
	initGroupSelector();
	initJournal();
	initDateFields();
	initEditStudentPage();
});