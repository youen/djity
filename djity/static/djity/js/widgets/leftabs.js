

$.widget("ui.lefttabs", {
	/* This widget transforms a div containing a list of links into a left
	 * menu for djity
	 */
	options: {
		position: 'left'
	},
	_create: function() {
		// fetch elements to act upon
		this.current = $('#' + this.element.find('.active_tab').text());
		this.list = this.element.find('ol,ul').eq(0);
		this.lis = $('li:has(a[href])', this.list);

		// set default style classes
		this.element.addClass('ui-widget');
		this.list.addClass('ui-tabs-nav ui-helper-reset ui-helper-clearfix');
		this.lis.addClass('ui-state-default ui-corner-left');
		// make tabs large
		this.lis.each(function(i,li){
			li.style.height = '20px';
			li.style.marginBottom = '5px';
		});

		// add hover reaction on tabs
		$(this.lis).hover(
			function () {
				$(this).addClass("ui-state-hover");
			},
			function () {
				$(this).removeClass("ui-state-hover");
			}
		);

		// change display of current tab
		this.current.addClass("ui-tabs-selected");
		this.current.addClass("ui-state-active");
		this.current[0].style.width = '100%';
	},
});


