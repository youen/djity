$.widget("ui.box", {

	options : {
		icon: 'ui-icon-info',
		state: 'ui-state-highlight',
		closeable: false,
		effect: '',
		delay: false,
		
	},

	_create: function() {
		var self = this,
			options = self.options,
			uiBox = (self.uiBox = self.element)
					  .addClass('dj-box ui-corner-all ' + self.options.state),



			uiInner = (self.uiInner = self.element.find('p'))
				.prepend($('<span  class="ui-icon ' + self.options.icon +'"></span>'))

			if( options.closeable){
				closeIcon = $('<span  class="ui-icon ui-icon-circlesmall-close"></span>')
						.click(function() {
							self.close();
						});
				uiInner.append(closeIcon);
			}
				
			uiBox
				.show(options.effect)
				.fadeOut(options.delay,function(){self.close();});

			
		

	},

	close : function(event){
		var self = this;
		self._trigger('close',event,{id:self.uiBox.id});

	}
});

