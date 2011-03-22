
function initHeader(){
	/*
	 * encapsulate all header initialization function
	 */
	widgetify();
	init_right_tabs();
	if (dj_context.perm.manage){
		project_manage_buttons();
	}
	else {
		project_subscribe_button();
	}
	portal_parameters();
	parent_projects(); 
	children_projects();
	toolbar();
	paginator();
	init_tag();
   
	elRTE.prototype.options.lang = dj_context.LANGUAGE_CODE;
   //change elRTE save function	

	elRTE.prototype.save = function (){
		this.editor.prev().editable('close_editor');
	}	
   //after all send notification
	$(dj_context.django_messages).each(function(item,msg){
		$('#messages').notify('create',{text:msg});
		});
};

function parent_projects() {
	$('#parent_projects a').button({
		icons:{
		    primary:'ui-icon-carat-1-e'
			}
	})
	.addClass('dj-mini-button');
};

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
					'project_name':project_name,
					'module_name':module_name,
					'path':path,
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

function children_projects () {
	$('#children_projects a').button({
		icons : {
			primary : 'ui-icon-triangle-1-se'
			}
	});
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

function widgetify() {
	$("input:submit").button();
	
	$('#right_tabs_list li')
		.css("height","22px")
		.css("line-height","0.5");
	
	$('#right_tabs_list  li ul')
		.css("display","none");
	
	$("#right_tabs_list  li").hover(
		  function () {
				  $(this).addClass("ui-state-hover");
			},
		   function () {
				$(this).removeClass("ui-state-hover");
			}
	);

	$('#messages').notify();

	if(dj_context.perm.edit){
		$(".dj-editable").each(function(i,e){$(e).editable({save_function:eval(e.id +'_callback')});});
	}
}

function init_right_tabs() {
	/*
	 * Function called when document is loaded
	 * Create a scrolling menu for the right navigation tabs
	 *
	 */
		
	if (dj_context.perm.manage){
		$("#right_tabs_list").disableSelection();
		$('#right_tabs_list').sortable({

			placeholder: 'dj-sorting-tab ui-state-highlight dj-mini-button',
			update: function(event, ui) { 
				Dajaxice.djity.project.save_tab_order(
					'Dajax.process',{
						'project_name':dj_context.project_name,
						'array':$('#right_tabs_list').sortable('toArray')
				
					});	
			}
		});
	}

	/*
	 * Create delete tab dialog 
	 */

	$('#' + dj_context.module_name + '-delete')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					Dajaxice.djity.project.delete_tab(
						'Dajax.process',{
						'project_name':dj_context.project_name,
						'module_name':dj_context.module_name,
				
					});	
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind edit name dialog
	$('#' + dj_context.module_name + ' .ui-icon-close')
		.click(function(){
				$('#' + dj_context.module_name + '-delete').dialog('open');
				return false;
		});

	/*
	 * Create a edit name dialog 
	 */

	$('#' + dj_context.module_name + '-change-name')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			open: function(event,ui){ 
				$('#' + tab_name + '-title').val(
					$('#' + tab_name ).find('a')[0].textContent
					);
				
			},
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					$('#' + tab_name ).find('a')[0].textContent = $('#' + tab_name + '-title').val();
					Dajaxice.djity.project.save_tab_name(
						'Dajax.process',{
						'project_name':dj_context.project_name,
						'module_name':dj_context.module_name,
						'LANGUAGE_CODE':LANGUAGE_CODE,
						'label': $('#' + dj_context.tab_name + '-title').val(),
				
					});	
					
				},
				Cancel: function() {
					$(this).dialog('close');
				}
			}
		});

	//bind edit name dialog
	$('#' + dj_context.tab_name + ' .ui-icon-wrench')
		.click(function(){
				$('#' + dj_context.tab_name + '-change-name').dialog('open');
				return false;
		});


	
	/*
	 *  Bind add tab button
	 */
	$('#create_tab_button')
		.click(function(){
				$('#create_tab_dialog').dialog('open');
				return false;
		})
		.button({
			icons: {
				primary: 'ui-icon-circle-plus'
			},
			text : false,
		})
	
	$('#create_tab_dialog')
		.dialog({
			autoOpen:false,
			modal: true,
			resizable:false,
			show:'blind',
			open: function(event,ui){
				Dajaxice.djity.project.get_module(
					'Dajax.process',{
					'project_name' : dj_context.project_name,
					}
				
				);
				$("#module_list").change(function () {
						$('#new_tab_name')
							.val($("#module_list option:selected").text())
							.select();	
					});
			},
			
			buttons: {
				Ok : function() {
					$(this).dialog('close');
					Dajaxice.djity.project.add_module(
						'Dajax.process',{
							'project_name':dj_context.project_name,
							'tab_name':$('#new_tab_name').val(),
							'module_type':$("#module_list option:selected").val(),
						}
					);		
				},
				Cancel: function() {
					$(this).dialog('close');
					}
			}
			});
	$('#right_tabs').removeClass('ui-helper-hidden');
};

function initAmazonGroups() {
	 /*
	 * Function called by amazon publicity porlet
	 * Create an accordion style menu from the list of groups of products
	 *
	*/
	$(function() {
		$("#amazon_groups").accordion();
		$("#amazon_groups h3").each(function(i,head){
			$(head).addClass('dj-mini-button');
		});
	});
};

function toolbar() {
	$("#toolbar").buttonset();
	$("#toolbar a")
		.button()
		.addClass('dj-mini-button');
};

function paginator() {
	$('#paginator a')
		.button()
		.addClass('dj-mini-button');
	
	$('#paginator .off')
		.button('option','disabled','true');
	
	$('#paginator .active')
		.unbind()
		.addClass('ui-state-active');

	$('#paginator').removeClass('ui-helper-hidden');
	left = $('#paginator').width()/2 - ($('.page').width()/2 +$('.previous').width())  ;
	$('.pages').css('padding-left',left+'px');



}

function init_tag(){
	$('.tag').box({
			closeable:dj_context.perm.manage,
			icon: 'ui-icon-tag',
			state: 'ui-state-default',
			close: function (){
				eval(this.id+'_callback')(this.id);
			}
	});
	$(".new_tag")
		.autocomplete({
			source:["youen","lixia","alban"],
			select:function(event,ui){
			$('<span class="tag"><p><a>' + ui.item.value + '</a></p></span>')
				.box({
					closeable:dj_context.perm.manage,
					icon: 'ui-icon-tag',
					state: '',
					effect:'',
				})
				.insertBefore(this);
				
				$(this).val('new tag');
				this.select();
				// stop event ! http://stackoverflow.com/questions/2561903/clear-form-field-after-select-for-jquery-ui-autocomplete
				return false; 
			}
		})
		.focus(function(){
			// Select input field contents
			this.select();
		});
	
}

/* Define tools function  */

function message(msg) {
	$('#messages').notify('create',{text:msg});

}

function save_text_portlet(id,html) {
	/*
	 * save change for a text portlet 
	 *
	 */	
	Dajaxice.djity.portlet.save_text_portlet(
			'Dajax.process',{
			'project_name':dj_context.project_name,
			'LANGUAGE_CODE':dj_context.LANGUAGE_CODE,
			'div_id':id,
			'html':html,
			}
	);	
}

function project_title_callback(id,html){
		Dajaxice.djity.project.save_project_title(
				'Dajax.process',{
				'project_name':dj_context.project_name,
				'LANGUAGE_CODE':dj_context.LANGUAGE_CODE,
				'div_id':id,
				'html':html,
		}
																							);	
}

/* Define jquery-ui custom widgets for djity */

