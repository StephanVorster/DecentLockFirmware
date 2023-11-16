from JN_PKG import *
from UI_ICONS import *
from UI_SCREENS.COLORS import *


class UI_LOADING():

    """
    ??
    """

    def __init__( self, parent = None ) -> None:

        """
        ??
        """

        self.appearance = False

        # Callbacks
        self.EXTCB_ENTRANCE = None
        self.EXTCB_EXIT = None

        self.label = QLabel(parent=parent)
        self.label.setFont(QFont("Calibri", 12))
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.label.setAlignment( Qt.AlignmentFlag.AlignHCenter )

        self.SET_COORDINATE()
        self.SET_FONT_COLOR()

        # self.EXIT()


    def ENTRANCE(self):
        self.appearance = True
        self.label.show()
        FUNC_TRY_CALLING( self.EXTCB_ENTRANCE )

    def EXIT(self):
        self.appearance = False
        self.label.hide()
        FUNC_TRY_CALLING( self.EXTCB_EXIT )

    def SET_TEXT(self, text:str, color:UI_Color = None):

        self.label.setText( text )
        if color is not None:
            self.SET_FONT_COLOR( color )
        
    def SET_FONT_COLOR( self, color:UI_Color = UI_Color.WHITE ):
        self.label.setStyleSheet(f"""
            color : {color.value}; 
            background-color : transparent;
        """)

    def SET_COORDINATE( self, x:int = 40, y:int = 449 ):
        self.label.setGeometry( QRect( x, y, 400, 100 ) )

    def SET_PROPERTIES(
        self,
        color       :UI_Color           = None,
        bg_color    :UI_Color           = None,
        family      :str                = None,
        text_size   :str                = None,
        geo_x       :int                = None,
        geo_y       :int                = None,
        geo_w       :int                = None,
        geo_h       :int                = None,
        text_wrap   :bool               = None,
        alignment   :Qt.AlignmentFlag   = None
    ):
        # Set font color
        if color is not None:
            self.SET_FONT_COLOR(color)

        # Set background color
        bg_color_value = bg_color.value if bg_color is not None else "transparent"
        self.label.setStyleSheet(f"color: {self.label.styleSheet().split(';')[0].split(':')[1]}; background-color: {bg_color_value};")

        # Set font family and size
        if family is not None or text_size is not None:
            current_font = self.label.font()
            if family is not None:
                current_font.setFamily(family)
            if text_size is not None:
                current_font.setPointSize(int(text_size))
            self.label.setFont(current_font)

        # Set geometry
        if geo_x is not None or geo_y is not None or geo_w is not None or geo_h is not None:
            current_geo = self.label.geometry()
            
            if geo_x is not None:
                current_geo.setX( geo_x )
            if geo_y is not None:
                current_geo.setX( geo_y )
            if geo_w is not None:
                current_geo.setWidth( geo_w )
            if geo_h is not None:
                current_geo.setHeight( geo_h )

            self.label.setGeometry( current_geo )

        # Set word wrap
        if text_wrap is not None:
            self.label.setWordWrap(text_wrap)

        # Set alignment
        if alignment is not None:
            self.label.setAlignment(alignment)

    def SET_EXTCB_ENTRANCE(self, cb = None):
        if cb is None:
            self.EXTCB_ENTRANCE = None
        else:
            self.EXTCB_ENTRANCE = cb

    def SET_EXTCB_EXIT(self, cb = None):
        if cb is None:
            self.EXTCB_EXIT = None
        else:
            self.EXTCB_EXIT = cb
        


