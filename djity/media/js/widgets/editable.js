

$.widget("ui.editable",{
		/* 
		 * HTML5 editable
		 */
	options : {
			show :'',
			autoOpen:false,
			save_function : function(){},
			effect:'clip',
	},
	_create: function() {
		var self=this,
			options = self.options,
			id = self.element.id,
			editorBox = (self.editorBox =  $('<div></div>'))
					 .appendTo(document.body)
					 .css('position','absolute')
			         .hide()
					 .addClass('ui-widget ui-widget-header dj-editor-box ui-corner-top'),

			
			_isOpen = false,
			doc = (self.doc = self.element)
				.blur(function(){
					//self.close();
				})
				.focus(function(){
					self.open();
				})

			
			doc.attr('contentEditable',true);
			
		    $('<button  title="save">save</button>')
				.button({
					icons:{
						'primary':''
					},
					text:false,
					label:'save',
								
				})
				.addClass('dj-mini-button')
				.click(	function (event){self.save();})
				.appendTo(editorBox);


			$('<button  title="Rich Edit">Riche Edit</button>')
				.button({
					icons:{
						'primary':''
					},
					text:false,
					label:'Rich Edit',
								
				})
				.addClass('dj-mini-button')
				.click(	function (event){self.editor();})
				.appendTo(editorBox);

			$('<button  title="Cancel">Cancel</button>')
				.button({
					icons:{
						'primary':''
					},
					text:false,
					label:'Cancel',
								
				})
				.addClass('dj-mini-button')
				.click(	function (event){self.cancel();})
				.appendTo(editorBox);

			editorBox.position({
						my:'left bottom',
						at:'left top',
						of:self.element,
					 });

					
    },

	_init: function() {
		    if ( this.options.autoOpen ) {
				this.open();
			}
	},
	close : function(){

		if (!this._isOpen) { return; }

			var self = this,
				options = self.options,
				editorBox = self.editorBox;

			editorBox.hide(options.effect);
			self.doc
				.removeClass('ui-state-highlight')
			self._isOpen = false;

			
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
					
			self.doc.addClass('ui-state-highlight')
			self._isOpen  = true;
			self.rollback=self.element.html();
			
			  
	},

	save : function(){
			var self = this,
				options = self.options,
				editorBox = self.editorBox;
			self.options.save_function(self.element.html(),self.element.attr('id'));
			self.close();	
	},

	editor : function(){
			var self = this,
				options = self.options,
				editorBox = self.editorBox;
			self.element.hide();

			self.element.elrte({lang:dj.LANGUAGES_CODE,toolbar:'maxi'});
			self.element.elrte('val',self.element.html());
			self.element.elrte('open');
			self.close();
	},

	close_editor : function() {
			var self = this;
			self.element.html(self.element.elrte('val'));
			self.element.elrte('close');
			self.element.show();
			self.save();
	},

	cancel : function(){
			var self = this;
			self.element.html(self.rollback);
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
