

$.widget("ui.editable",{
		/* 
		 * HTML5 editable
		 */
	options : {
			show :'',
			simple:false,
			autoOpen:false,
			save_function : function(){},
			effect:'clip',
			lang:'',
			get_function:undefined,
			//send the id of the div to the save and get function
			send_divid:false,

			toolbar:'maxi',
	},
	_create: function() {
		var self=this,
			options = self.options,
			id = self.element.id,
			editorBox = (self.editorBox =  $('<div></div>'))
					 .appendTo(document.body)
					 .css('position','absolute')
			         .hide()
					 .addClass('ui-widget ui-widget-content dj-editor-box ui-corner-top'),

			
			_isOpen = false,
			doc = (self.doc = self.element)
				.blur(function(){
					//self.close();
				})
				.focus(function(){
					self.open();
				})

			
			doc.attr('contentEditable',true);
				
			var toolbar = $('<span></span>')
				.appendTo(editorBox);

		    $('<button title="' + gettext('Save') + '">' + gettext('Save') + '</button>')
				.button({
					icons:{
						'primary':'ui-icon-disk'
					},
					text:false,
					label:gettext('Save'),
								
				})
				.click(	function (event){self.save(true);})
				.appendTo(toolbar);
			
			/*
			 * No rich editor for simple edition
			 */
			if(! self.options.simple)
			{

				self.editor_button = $('<button  title="'+gettext('Rich Edit')+'">'+gettext('Rich Edit')+'</button>')
					.button({
						icons:{
							'primary':'ui-icon-plusthick'
						},
						text:false,
						label:gettext('Rich Edit'),
									
					})
					.click(	function (event){self.editor();})
					.appendTo(toolbar);
			}

			$('<button  title="'+gettext('Cancel')+'">'+gettext('Cancel')+'</button>')
				.button({
					icons:{
						'primary':'ui-icon-cancel'
					},
					text:false,
					label:gettext('Cancel'),
								
				})
				.click(	function (event){self.cancel();})
				.appendTo(toolbar);

			toolbar.buttonset();

			if(self.options.lang != ''){
			self.langbar = $('<span></span>')
				.appendTo(editorBox);


			$.each(dj.context.LANGUAGES,function(i,lang)
			{
				$('<button class="'+lang[0] +'" title="'+gettext(lang[1])+'">'+gettext(lang[1])+'</button>')
				.button({
					icons:{
						'primary':'dj-icon-'+lang[0]
					},
					text:false,
					label:gettext(lang[1]),
				})
				.click(	function (event){self.activate_lang(lang[0]);})
				.appendTo(self.langbar);

								

			});
			
			self.langbar.find('.'+self.options.lang).addClass('ui-state-highlight');
			self.lang = self.options.lang;	
			self.langbar.buttonset();
			
			}

			editorBox.position({
						my:'left bottom',
						at:'left top',
						of:self.element,
					 });

    },

	_init: function() {

			this.element.addClass('dj-editable');
		    if ( this.options.autoOpen ) {
				this.open();
			}
		    if ( this.options.get_function != undefined ) {
				self.rollback=this.element.html();
				this.activate_lang(this.options.lang);
			}

	},
	close : function(){

		if (!this._isOpen) { return; }

			var self = this,
				options = self.options,
				editorBox = self.editorBox;

			editorBox.hide(options.effect);

			self._isOpen = false;
			if(self.is_editor){
				self.close_editor();
			}
			self.close();	
			
	},


	isOpen: function() {
				return this._isOpen;
	},

	

	open : function(){
		if (this._isOpen) { return; }

			var self = this,
				options = self.options,
				
				editorBox = self.editorBox;
			
			
			editorBox
				.show(options.effect);
				
			editorBox.position({
						my:'left bottom',
						at:'left top',
						of:self.element,
					 });	
	
			self._isOpen  = true;
			self.rollback=self.element.html();
			  
	},


	save : function(close){
			var self = this,
				options = self.options,
				editorBox = self.editorBox;

			if(self.is_editor){
				var html =  self.element.elrte('val');
			}
			else
			{
				var html =  self.element.html();

			}


			var args =	{
						js_target:self,
						html:html,
						lang:self.lang,
					};
			if (self.options.send_divid)
			{
				args['div_id'] = parseInt(self.element.attr('id'));
			}

			self.rollback=html;
			dj.remote(self.options.save_function,args)
			if(close)
			{
				self.close();
			}
	},


	activate_lang: function(lang)
	{

			var self = this,
				langbar = self.langbar;

			if(lang == self.lang){return}
			/*
			if(self.is_editor){
				var html =  self.element.elrte('val');
			}
			else
			{
				var html =  self.element.html();

			}
			if(self.rollback!= html ){
				alert(self.rollback + '|' + html)
				msg = $('<div id="dialog-message" title="' + gettext("Text not save") + '">'
					  +'<p>' + gettext("Save your change in the current language or cancel edition before changing language.") + '</p>'
					  +'<div>')
					.dialog({
						modal:true,
						buttons: {Ok: function() {$( this ).dialog( "close" );}}
					});
				return;
			}
			*/
			langbar.find('.'+self.lang).removeClass('ui-state-highlight');
			langbar.find('.'+lang).addClass('ui-state-highlight');
			self.lang = lang;
			dj.remote(self.options.get_function,
					{
						js_target:self,
						lang:lang,
					});

	},

	set_html:function(html)
	{
		var self = this,
			langbar = self.langbar;

		if(html == null)
		{
				msg = $('<div id="dialog-message" title="' + gettext("New version") + '">'
					  +'<p>' + gettext("This text haven't the required language version you are just starting a new version.") + '</p>'
					  +'<div>')
					.dialog({
						modal:true,
						buttons: {Ok: function() {$( this ).dialog( "close" );}}
					});
				return;
		}
		else
		{
			self.element.html(html);
			if(self.is_editor){
				self.element.elrte('val',self.element.html());
			}
			self.rollback=self.element.html();
		}
	},

	editor : function(){
			var self = this,
				options = self.options,
				editorBox = self.editorBox;

			if(self.is_editor)
			{
				self.close_editor();
				return;
			}
			self.element.hide();
			self.is_editor = true;
			self.editor_button.addClass('ui-state-highlight');
			self.element.elrte({lang:dj.LANGUAGES_CODE,toolbar:self.options.toolbar});
			self.element.elrte('val',self.element.html());
			self.rollback=self.element.elrte('val');
			self.element.elrte('open');
			//self.close();
	},

	close_editor : function(save) {
			var self = this;
			self.element.html(self.element.elrte('val'));
			self.element.elrte('close');
			self.element.show();
			self.is_editor = false;
			self.editor_button.removeClass('ui-state-highlight');

	},

	cancel : function(){
			var self = this;
			if(self.is_editor)
			{
				self.element.elrte('close');
				self.element.html(self.rollback);
				self.element.show();
				self.is_editor = false;
				self.editor_button.removeClass('ui-state-highlight');
			}
			self.close();
	},

	bold : function(){
			document.execCommand ('bold', false, null);
	},
	italic : function(){
			document.execCommand ('italic', false, null);
	},
	underline : function(){
			document.execCommand ('underline', false, null);
	},
	justifycenter : function(){
			document.execCommand ('justifycenter', false, null);
	},
	justifyleft : function(){
			document.execCommand ('justifyleft', false, null);
	},
	justifyright : function(){
			document.execCommand ('justifyright', false, null);
	},
	justifyfull : function(){
			document.execCommand ('justifyfull', false, null);
	},
	insertOrderedList : function(){
			document.execCommand ('insertOrderedList', false, null);
	},
	insertUnorderedList : function(){
			document.execCommand ('insertUnorderedList', false, null);
	},
	insertLineBreak : function(){
			document.execCommand ('insertLineBreak', false, null);
	},

});
