buttons_options = {};

buttons_options[gettext('Cancel')] = function(){
	$(this).dialog('close');
};

buttons_options[gettext('Create an account')] =	function(){
					$(this).dialog('close');
					dj.widgets.register.open()
};

buttons_options[gettext('Sign in')] =	function(){
					$(this).dialog('close');
					dj.widgets.login.open()
};

dj.functions.project_subscribe_button = function (){
	$("#project_subscribe_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
		width: 460 ,
		buttons: buttons_options

	})
	var icon = "";
	switch(dj.context.role){
		// Awaiting
		case 1:
			button_label = gettext("Cancel subscription");
			icon = 'ui-icon-clock';
			break;
		// Anonymous
		case 0:
			button_label = gettext("Subscribe");
			icon = 'ui-icon-locked';
			break;
		default:
			button_label = gettext("Unsubscribe");
			icon = 'ui-icon-unlocked';
	}
		
	$("#project_subscribe_button")
		.button({
			disabled:(dj.role=='awaiting'),
			icons: {
				primary:icon
			},
			text:false,
			label:button_label,
		});
	
	if(dj.context.user == "AnonymousUser"){
		$("#project_subscribe_button")
			.click(function(){
					$('#project_subscribe_dialog').dialog('open');
					return false;
			});
	}
	else{
		$("#project_subscribe_button")
			.click(function()
			{
					dj.remote('djity.project.project_subscribe',{js_target:Document});
			});
	}
	$('#project_buttons').removeClass('ui-helper-hidden');
};


