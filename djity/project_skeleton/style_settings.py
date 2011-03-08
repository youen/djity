# Default style values
DEFAULT_STYLE = [
        ["background_color","#FFF"],
        ["content_background_color","#FFF"],
		["corner_radius","4px"],

        ["font_family","Verdana,Arial,sans-serif"],
        ["font_size","1.1em"],

        ["header_background_color","#ff3838"],
        ["header_background_texture","03_highlight_soft.png"],
        ["header_background_percent","100"],
		["header_border_color","#000000"],
		["header_text_color","#000000"],
		["header_link_color","#000000"],
		["header_icon_color","#000000"],

        ["wcontent_background_color","#e7dada"],
        ["wcontent_background_texture","03_highlight_soft.png"],
        ["wcontent_background_percent","80"],
		["wcontent_border_color","#000000"],
		["wcontent_text_color","#000000"],
		["wcontent_link_color","#000000"],
		["wcontent_icon_color","#000000"],

        ["default_background_color","#ffffff"],
        ["default_background_texture","03_highlight_soft.png"],
        ["default_background_percent","80"],
		["default_border_color","#000000"],
		["default_text_color","#000000"],
		["default_link_color","#000000"],
		["default_icon_color","#000000"],

        ["highlight_background_color","#e7dada"],
        ["highlight_background_texture","03_highlight_soft.png"],
        ["highlight_background_percent","80"],
		["highlight_border_color","#000000"],
		["highlight_text_color","#000000"],
		["highlight_link_color","#000000"],
		["highlight_icon_color","#000000"],

        ["error_background_color","#CCCCCC"],
        ["error_background_texture","03_highlight_soft.png"],
        ["error_background_percent","80"],
		["error_border_color","#000000"],
		["error_text_color","#000000"],
		["error_link_color","#000000"],
		["error_icon_color","#000000"],

        ["active_background_color","#e7dada"],
        ["active_background_texture","03_highlight_soft.png"],
        ["active_background_percent","80"],
		["active_border_color","#000000"],
		["active_text_color","#000000"],
		["active_link_color","#000000"],
		["active_icon_color","#000000"],

        ["focus_background_color","#e7dada"],
        ["focus_background_texture","03_highlight_soft.png"],
        ["focus_background_percent","80"],
		["focus_border_color","#000000"],
		["focus_text_color","#000000"],
		["focus_link_color","#000000"],
		["focus_icon_color","#000000"],
]

EDIT_STYLE_ORDER = [
    ("Global",[
            ("Background","background_color"),
            ("Content background","content_background_color"),
            ("Corner radius","corner_radius"),
        ]),
    ("Fonts",[ 
            ("Font family","font_family"),
            ("Font size","font_size"),
        ]),
    ("Widget header",[
			("Border color","header_border_color"),
            ("Background color","header_background_color"),
            ("Background texture","header_background_texture"),
            ("Texture %","header_background_percent"),
			("Text color","header_text_color"),
			("Link color","header_link_color"),
			("Icon color","header_icon_color"),
        ]),
	("Widget content",[
			("Border color","wcontent_border_color"),
			("Background color","wcontent_background_color"),
			("Background texture","wcontent_background_texture"),
            ("Texture %","wcontent_background_percent"),
			("Text color","wcontent_text_color"),
			("Link color","wcontent_link_color"),
			("Icon color","wcontent_icon_color"),
		]),
	("Default state",[
			("Border color","default_border_color"),
			("Background color","default_background_color"),
			("Background texture","default_background_texture"),
            ("Texture %","default_background_percent"),
			("Text color","default_text_color"),
			("Link color","default_link_color"),
			("Icon color","default_icon_color"),
		]),
	("Focus state",[
			("Border color","focus_border_color"),
			("Background color","focus_background_color"),
			("Background texture","focus_background_texture"),
            ("Texture %","focus_background_percent"),
			("Text color","focus_text_color"),
			("Link color","focus_link_color"),
			("Icon color","focus_icon_color"),
		]),
	("Active state",[
			("Border color","active_border_color"),
			("Background color","active_background_color"),
			("Background texture","active_background_texture"),
            ("Texture %","active_background_percent"),
			("Text color","active_text_color"),
			("Link color","active_link_color"),
			("Icon color","active_icon_color"),
		]),
	("Highlight",[
			("Border color","highlight_border_color"),
			("Background color","highlight_background_color"),
			("Background texture","highlight_background_texture"),
            ("Texture %","highlight_background_percent"),
			("Text color","highlight_text_color"),
			("Link color","highlight_link_color"),
			("Icon color","highlight_icon_color"),
		]),
	("Error",[
			("Border color","error_border_color"),
			("Background color","error_background_color"),
			("Background texture","error_background_texture"),
            ("Texture %","error_background_percent"),
			("Text color","error_text_color"),
			("Link color","error_link_color"),
			("Icon color","error_icon_color"),
		]),
]
