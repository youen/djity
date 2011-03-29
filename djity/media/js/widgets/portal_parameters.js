function portal_parameters() {
	$('#logout_button').click(
		function(){
			Dajaxice.djity.portal.logout('Dajax.process',{});	
		});

	$('#login_dialog').dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
		buttons:{
			'Login': function() {
				Dajaxice.djity.portal.login(
				'Dajax.process',{
					'project_name':dj_context.project_name,
					'module_name':dj_context.module_name,
					'path':dj_context.path,
					'username':$('#login_username').val(),
					'password':$('#login_password').val(),
				});
			}
		}
	})
	$('#login_button').click(function(){
		$('#login_dialog').dialog('open');
	});

	register_dialog();
	profile_dialog();
	
	$('#portal_parameters a,button')
		.addClass('dj-mini-button');

	choose_language_button();
	$('#portal_parameters').buttonset();
	$('#portal_parameters').removeClass('ui-helper-hidden');
};

function login_dialog_close(){
	$('#login_dialog').dialog('close');
};

function login_dialog_error(message) {
	$('#login_dialog_error')
	.text(message)
	.addClass('ui-state-error');
};

function register_dialog(){
	/*
	 * Create users management dialog
	 */
	$('#register_dialog').dialog({
		autoOpen:false,
		modal: true,
		show:'blind',
		buttons : {
			OK : function(){

				Dajaxice.djity.portal.register(
					'Dajax.process',{
						'username': $('#id_username').val(),
						'email': $('#id_email').val(),
						'password1': $('#id_password1').val(),
						'password2': $('#id_password2').val(),
						
					});

			},
			Cancel : function(){
				$(this).dialog('close');
			}
		},
		open: function(event,ui){
			Dajaxice.djity.portal.register(
				'Dajax.process',{
					'username': '',
					'email': '',
					'password1': '',
					'password2': '',
				});
		},
	});

	$('#signup_button').click(function(){
			$('#register_dialog').dialog('open');
			return false;
		});

};

function register_dialog_post_assign(){
	$('#register_dialog')
		.dialog("option","width","auto")
		.dialog("option","height","auto")
		.dialog("option","position","center");
}


function profile_dialog(){
	/*
	 * Profile Dialog
	 */
	$('#profile_dialog').dialog({
		autoOpen:false,
		modal: true,
		show:'blind',
		buttons : {
			OK : function(){

				Dajaxice.djity.project.profile(
					'Dajax.process',{
						'project_name':dj_context.project_name,
						'password1': $('#id_password1').val(),
						'password2': $('#id_password2').val(),
						
					});

			},
			Cancel : function(){
				$(this).dialog('close');
			}
		},
		open: function(event,ui){
			Dajaxice.djity.portal.profile(
				'Dajax.process',{
					'project_name':dj_context.project_name,
					'password1': '',
					'password2': '',
				});
		},
	});

	$('#profile_button').click(function(){
			$('#profile_dialog').dialog('open');
			return false;
		});

};

function profile_dialog_post_assign(){
	$('#profile_dialog')
		.dialog("option","width","auto")
		.dialog("option","height","auto")
		.dialog("option","position","center");
}

function choose_language_button(){
	$("#choose_language_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
	});

	$("#choose_language_dialog a")
	.each(function(i,head){
			$(head).button({
				icons:{
					primary:'dj-icon-' + $(head).attr('id').substring (5,7)
				}
				
			});
	});
		
	$("#choose_language_button")
		.button({
			icons: {
				primary: 'dj-icon-'+dj_context.LANGUAGE_CODE
			},
			text: false
		})
		.click(function(){
			$('#choose_language_dialog').dialog('open');
			return false;
		});
};
