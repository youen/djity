

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
	if(!( 'LANGUAGE_CODE' in params)) 	params.LANGUAGE_CODE = this.context.LANGUAGE_CODE;


	/* check if js_target is present and register object (if not already registered) */
	if(params.js_target != undefined && typeof params.js_target != 'string' )
	{
		params.js_target = dj.namespace.register(params.js_target);
	}
	/* call the function using dajax */
	eval("Dajaxice."+func+"(Dajax.process,params);");
	//dj.ws.send("dajax",{func:func,params:params})	
};

dj.namespace = 
/*
 * DEVELOPER NOTE
 * --------------
 *
 * this implementation use a list instead of a JS object because JS object doesn't compute the hash of 
 * an object (JS call silentlty the 'toString' propertie). JS hastable implementation exist [1] but is another
 * 1.4 KB script to add in the core of djity... The set and get method's complexity is O(n).
 * 
 * [1] http://code.google.com/p/jshashtable/downloads/detail?name=jshashset.js
 *
 */
{
	init : function ()
	{
		this.object2name = [];
		this.objects = {};
		this.abc = "abcdefghijklmnopqrstuvwxyz";
	},



	get_name : function(object)
	{
		$.each(this.object2name,function(i,o_n)
		{
			if(o_n[0] === object)
			{
				return o_n[1];
			}
		});
		return undefined;
	},


	generate_name : function(seed)
	{
		var name = '';
		if(seed === undefined)
		{
			seed = this.object2name.length;
			name = 'dj.namespace.objects.';
		}
		name += this.abc[seed % 26 ];
		rest = parseInt(seed/26);
		if(rest != 0)
		{
			name += this.generate_name(rest);
		}
		return name;
	},

	register : function(object, object_name)
	/* 
	 * Save the name of the object in an index. 
	 * If the name is not given, a generated name is saved except if the object is already registered.
	 * If the object is already registered and a new object_name is given, the new_name is saved.
	 * return the given or generated obect_name.
	 */
	{

		if( object_name === undefined)
		{
			object_name = this.get_name(object);
			if(object_name != undefined)
			{
				return object_name;
			}
			object_name = this.generate_name();
			eval( object_name + ' = object;'); 
		}
		else
		{
			eval( object_name + ' = object;'); 
		}
		this.object2name.push([object,object_name]);
		return object_name;
	}
}

/* Define tools function  */

dj.message = function(msg) {
	dj.messages_box.notify('create',{text:msg});
};

dj.init = function(){
	/*
	 * encapsulate all Djity initialization functions and widgets
	 *
	 * dj.context must have been set before calling this function
	 */
	dj.messages_box = $('#messages')
	// Try to open a websocket
		dj.ws = $.websocket(dj.context.ws_url,{
		events: {
         		notify: function(e) {
                        	dj.message(e.data); // 'baa'
                	},
         		dajax: function(e) {
                        	Dajax.process(e.data); // 'baa'
                	}
        	
        	}
		});
	dj.namespace.init();

	init_right_tabs();
	if (dj.context.perm.manage){
		project_manage_buttons();
	}
	else {
		dj.functions.project_subscribe_button();
	}
	widgetify();
	dj.functions.portal_parameters();
	parent_projects(); 
	children_projects();
	toolbar();
	paginator();
   
	elRTE.prototype.options.lang = dj.context.LANGUAGE_CODE;
   //change elRTE save function	

	elRTE.prototype.save = function (){
		this.editor.prev().editable('save');
	}	
   //after all send notification
	$(dj.context.messages).each(function(item,msg){
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
	
	$('#search_query').keypress(function(e) {
        if(e.which == 13) {
            $("#search_button").click();
        }});
	
	$('#search_button')
	    .addClass("dj-mini-button")
	    .button({
            icons: {
                primary: "ui-icon-search"
            },
            text:false,
            })
        .click(function(){
                query = $("#search_query").val();
                project_url = $("#search_button .ui-button-text").text();
                window.location.replace(project_url+"/search/?q="+query);
            });

	$('#messages').notify();

	
	if(dj.context.perm.manage){
		$("#project_title").editable({simple:true,save_function:'djity.project.save_project_title'});
	}

	if(dj.context.perm.edit){
		$(".dj-text-portlet").each(function(i,e){$(e).editable({
			save_function:'djity.portlet.save_text_portlet',
			send_divid:true,
		    toolbar:'compact',
			}
			);});
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



