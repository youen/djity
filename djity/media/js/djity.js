
/*
 * Define empty Djity base datastructure in a 'dj' dictionary when this file is loaded
 */
dj = {}
dj.functions = {}
dj.widgets = {}

dj.remote = function(func,params){
	/*
	 * this function defines a standard way for all dj.context functions and widgets
	 * to interact with the remote server.
	 * 
	 * Today only ajax calls through the dajax framework are supported.
	 *
	 * dj.context must have been set before calling this function
	 */

	/* add standard dj.context context parameters */
	params.project_name = this.context.project_name;
	params.module_name = this.context.module_name;
	params.LANGUAGE_CODE = this.context.LANGUAGE_CODE;

	/* call the function using dajax */
	eval("Dajaxice."+func+"('Dajax.process',params);");	
};

dj.init = function(){
	/*
	 * encapsulate all Djity initialization functions and widgets
	 *
	 * dj.context must have been set before calling this function
	 */
	init_right_tabs();
	if (dj.context.perm.manage){
		project_manage_buttons();
	}
	else {
		project_subscribe_button();
	}
	widgetify();
	dj.functions.portal_parameters();
	parent_projects(); 
	children_projects();
	toolbar();
	paginator();
	init_tag();
   
	elRTE.prototype.options.lang = dj.context.LANGUAGE_CODE;
   //change elRTE save function	

	elRTE.prototype.save = function (){
		this.editor.prev().editable('close_editor');
	}	
   //after all send notification
	$(dj.context.django_messages).each(function(item,msg){
		$('#messages').notify('create',{text:msg});
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

	if(dj.context.perm.edit){
		$(".dj-editable").each(function(i,e){$(e).editable({save_function:eval(e.id +'_callback')});});
	}
}

/*
 * ###########################################################################
 * WARNING:
 * All functions below should be taken out of this file and into
 * separate widgets.
 * ###########################################################################
 */

function toolbar() {
	$("#toolbar").buttonset();
	$("#toolbar a")
		.button()
		.addClass('dj.context.mini-button');
};

function paginator() {
	$('#paginator a')
		.button()
		.addClass('dj.context.mini-button');
	
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
			closeable:dj.context.perm.manage,
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
					closeable:dj.context.perm.manage,
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
};

function save_text_portlet(id,html) {
	/*
	 * save change for a text portlet 
	 *
	 */
	dj.remote('djity.portlet.save_text_portlet',{
			'div_id':id,
			'html':html,
			}
	);
};

function project_title_callback(id,html){
	dj.remote('djity.portlet.save_project_title',{
			'div_id':id,
			'html':html,
		}
	);
};


