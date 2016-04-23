function initJournal() {
	var indicator = $('#ajax-progress-indicator'),
		error_indicator = $('#ajax-error-indicator'),
		ajax_info = $('#ajax-info');

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
	$('input#id_birthday').attr("placeholder", "День народження студента");

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


//Edit students
function initAdd_EditPage() {
	$('a.student-edit-form-link, a#addButton, a.group-edit-form-link,\
		a.exam-edit-form-link, a#contact').click(function(event){

		var link = $(this), url = link.attr('href'),
			loading = $('.cssload-container');

		$.ajax({
			'url': url,
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				loading.show();
				$('a').attr('onclick', 'return false');
			},

			'success': function(data, status, xhr){
				//save actions to browser history
				history.pushState({ path: url }, '', url);
				history.replaceState({ path: window.location.href }, '');
				

				$('a').removeAttr('onclick', 'return false');
				loading.hide();
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'), html = $(data),
					form = html.find('#content-column form');

				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);
				showPhotoAtForm();
			

				// init our edit form
				initAdd_EditForm(form, modal, url);
				// setup and show modal window finally
				modal.modal({
					'keyboard': false,
					'show': true
				});	

			},

			'error': function(){
				$('a').removeAttr('onclick', 'return false');
				//remove old alert
				$('.alert').remove();
				loading.hide();
	
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
				return false;
			}
		});

		return false;
	});
}

function initAdd_EditForm(form, modal, url) {
	var loading = $('.cssload-container');
	// attach datepicker
	initDateFields();

	// make form work in AJAX mode
	form.ajaxForm({
		'url': url,
		'dataType': 'html',

		'beforeSend': function(xhr, settings){
			loading.show();
			$('input, textarea, select').attr('disabled', '1');	
		},

		'success': function(data, status, xhr) {

			$('input, textarea, select').removeAttr('disabled');
			loading.hide();
			var html = $(data), newform = html.find('#content-column form');

			//remove old alert
			$('.alert').remove();

			// close modal window on Cancel button click
			form.find('input[name="cancel_button"]').click(function(event){
				modal.modal('hide');
				$('.alert').html(html.find('.alert'));
				return false;
			});

			// copy alert to modal window
			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').html(html.find('.alert'));
				modal.find('.modal-body').append(newform);
				// initialize form fields and buttons
				initAdd_EditForm(newform, modal, url);
			} else {
				//setTimeout(function(){modal.modal('hide');}, 1000);

				//hide modal window
				modal.modal('hide');
				//give info about successful or unsuccessful operation
				$('.alert').html(html.find('.alert'));
				//Up to date list of students

				$('#content-column').hide().html(html.find('#content-column')).fadeIn('slow');;
				$('#global-navigation').hide().html(html.find('#global-navigation')).fadeIn('slow');;

				initAdd_EditPage();
				globalNavigation();
				loadMore();
				return false;
			}
		},

		'error': function(){		
			//remove old alert
			$('.alert').remove();
			loading.hide();
			modal.modal('hide');

			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		}
	});
}


//Navigation at site
function globalNavigation() {
	$('a#students, a#visiting, a#groups, a#exams, a#month, a#pagination, a#ordering').click(function(){
		var link = $(this), url = link.attr('href'),
			loading = $('.cssload-container');

		$.ajax({
			'url': url,
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				loading.show();
				$('a').attr('onclick', 'return false');
			},

			'success': function(data, status, xhr){
				//save actions to browser history
				history.pushState({ path: url }, '', url);
				history.replaceState({ path: window.location.href }, '');

				$('a').removeAttr('onclick', 'return false');
				loading.hide();
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
				// update modal window with arrived content from the server
				var html = $(data);

				
				if (url === "/" || url === "/journal/" || url === "/groups/" || url === "/exams/"){

					$('#content-column').hide().html(html.find('#content-column')).fadeIn('slow');
					$('#global-navigation').html(html.find('#global-navigation'));

				} else {
					$('p#journal-nav').hide().html(html.find('p#journal-nav')).fadeIn('slow');
					$('table.table').hide().html(html.find('table.table')).fadeIn('slow');
					$('ul.pagination').hide().html(html.find('ul.pagination')).fadeIn('slow');
				}

				globalNavigation();
				initAdd_EditPage();
				initJournal();
				loadMore();
			},

			'error': function(){
				$('a').removeAttr('onclick', 'return false');
				//remove old alert
				$('.alert').remove();
				loading.hide();
	
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
				return false;
			}
		});

		return false;
		
	});
}

function historyBackButton() {

	$(window).bind('popstate', function(event) {
		// if the event has our history data on it, load the page fragment with AJAX
		var state = event.originalEvent.state, loading = $('.cssload-container'),
			url = location.pathname+location.search;


		//console.log(load(state.path));
		if (state) {
			//$('div.container').load(location.href);
		$.ajax({
			'url': url,
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				loading.show();
				$('a').attr('onclick', 'return false');
			},

			'success': function(data, status, xhr){
				//console.log(url);
				//save actions to browser history

				$('a').removeAttr('onclick', 'return false');
				loading.hide();
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
				// update modal window with arrived content from the server
				var html = $(data),  modal = html.find('#myModal');

				//modal.modal('hide');
				$('#myModal').modal('hide')
				$('#content-column').hide().html(html.find('#content-column')).fadeIn('slow');
				$('#global-navigation').html(html.find('#global-navigation'));

				globalNavigation();
				initAdd_EditPage();
				initJournal();
				loadMore();
			},

			'error': function(){
				$('a').removeAttr('onclick', 'return false');
				//remove old alert
				$('.alert').remove();
				loading.hide();
	
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
				return false;
			}
		});

		return false;
	}

});
}

function showPhotoAtForm(){

	//show current photo at edit form
	var src = $('#div_id_photo a').attr('href')
	$('#div_id_photo a').html("<img>");
	$('#div_id_photo img').attr("src", src)
		.attr("width", "30px").attr("height", "30px").attr('class', 'img-circle');

	//show new download photo at add and edut form
	$("input#id_photo").after('<img id="formImage">');

	$("input#id_photo").change(function(){

    if (this.files && this.files[0]) {

        var reader = new FileReader();

        reader.onload = function (event) {
        	$("img#formImage").html('<img id="formImage">')
        	
            $('#formImage').attr('src', event.target.result)
            	.attr("width", "30px").attr("height", "30px").attr('class', 'img-circle');
        };

        reader.readAsDataURL(this.files[0]);
    }

	});

}


$(document).ready(function(){
	
	initGroupSelector();
	initJournal();
	initDateFields();
	initAdd_EditPage();
	globalNavigation();
	historyBackButton();
	showPhotoAtForm();

});



/*
!!! Realised page with 'load more...' button !!!

function loadMore() {
	//$('a#loadMore').attr('href', '?page=1')
	var n = 1;
	
	$('a#loadMore').click(function(){
		n++;
		$('a#loadMore').attr('href', '/?page='+n);
		var link = $(this), url = link.attr('href'),
			loading = $('.cssload-container');

		$.ajax({
			'url': url,
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				loading.show();
				$('a').attr('onclick', 'return false');
			},

			'success': function(data, status, xhr){
				//save actions to browser history
				history.pushState({ path: url }, '', url);
				history.replaceState({ path: window.location.href }, '');

				$('a').removeAttr('onclick', 'return false');
				loading.hide();
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
				// update modal window with arrived content from the server
				var html = $(data);


					$('table.table').hide().html(html.find('table.table')).fadeIn('slow');

				

				globalNavigation();
				initAdd_EditPage();
				initJournal();
			},

			'error': function(){
				$('a').removeAttr('onclick', 'return false');
				//remove old alert
				$('.alert').remove();
				loading.hide();
	
				alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
				return false;
			}
		});


		return false;
		
	});
}
*/
