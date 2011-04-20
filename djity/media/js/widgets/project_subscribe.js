function project_subscribe_button(){
	$("#project_subscribe_dialog").dialog({
		autoOpen:false,
		modal:true,
		show:'blind',
		buttons:{
			Ok:function(){
			},
			Cancel:function(){
				$(this).dialog('close');
				return false;
			}
		}

	})

	switch(dj.context.role == 0){
		case 'awaiting':
			button_label = "Cancel subscription";
			break;
		case 0:
			button_label = "Subscribe";
			break;
		default:
			button_label = "Unsubscribe";
	}
		
	$("#project_subscribe_button")
		.button({
			disabled:(dj.role=='awaiting'),
			icons: {
				primary:'ui-icon-person'
			},
			text:false,
			label:button_label,
		});
	
	if(dj.context.user == "anonymous"){
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
					dj.remote('djity.project.project_subscribe',{});
			});
	}
	$('#project_buttons').removeClass('ui-helper-hidden');
};


