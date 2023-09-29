from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtSvg import *
from enum import Enum

def jn_disconnectSignals( signal : SignalInstance ):
    try:
        signal.disconnect()
    except: pass
    

class JN_Icon( QIcon ):

    class Type( Enum ):
        LOCKED = 0
        UNLOCKED = 1

    def __init__(self, file:str, pos:QPoint) -> None:
        super().__init__(file)
        self.svg_file   : str   = file
        self.icon_geo   : QRect = None
        self.size : QSize = None
        self.jsetPosition( pos )
        
        
    def jgetIcon(self) -> QIcon:
        return self

    def jgetSize(self) -> QSize:
        return self.size
    
    # Position
    # set x y position of geo 
    # set w h to size of icon
    # Default setup from init
    def jsetPosition(self, pos:QPoint) -> None:
        self.size = QSvgRenderer(self.svg_file).defaultSize()
        x = pos.x()
        y = pos.y()
        w = self.size.width()
        h = self.size.height()
        self.jsetGeometry( QRect(x, y, w, h) )


    # SVG File
    def jgetSVGFile(self) -> str:
        return self.svg_file
    
    def jsetSVGFile(self, file:str) -> None:
        self.svg_file = file

    # Geometry
    # Discards changes by setPosition
    def jgetGeometry(self) -> QRect:
        return self.icon_geo
    
    def jsetGeometry(self, geo:QRect) -> None:
        self.icon_geo = geo


class JN_SVG_Widget():

    def __init__(self, parent=None) -> None:  
        # Feature Enablers
        self.en_click           :bool   = True
        self.en_hold            :bool   = False
        self.en_glow            :bool   = False
        self.en_glow_anim       :bool   = False
        self.en_shadow          :bool   = True  # ON by default
        self.en_scale           :bool   = False
        self.en_scale_anim      :bool   = False

        # Settings - Glow & Shadows - FX
        self.glow_upValue       :float  = 15.0
        self.glow_downValue     :float  = 0
        self.glow_color         :str    = "#FFFFFF" # White
        self.glow_animDuration  :int    = 200
        self.shadow_color       :str    = "#292929" # Gray
        self.shadow_blur        :float  = 5.0
        self.shadow_offset      :tuple[int,int] = (5,5)

        # Settings - Scale
        self.scale_upValue      :QSize  = None # To be set by icon
        self.scale_downValue    :QSize  = None # To be set by icon
        self.scale_animDuration :int    = 200

        # Settings - Entrance Exit Animation
        self.entrance_duration  :int    = 500
        self.exit_duration      :int    = 500

        # BUTTON WIDGET
        self.WIDGET = QPushButton( parent )
        self.WIDGET.setFlat(True)
        self.WIDGET.pressed.connect( self.__press__ )
        self.WIDGET.released.connect( self.__release__ )
        # Geometry
        self.geo = QRect(0,0,0,0)
        # Icon
        self.icon : JN_Icon = None
        # Effects
        self.glow = QGraphicsDropShadowEffect( self.WIDGET )
        self.WIDGET.setGraphicsEffect( self.glow )
        self.glow.setOffset(0,0)  
        self.glow.setEnabled(False)
        self.glow_anim = QPropertyAnimation( self.glow, b"blurRadius" )
        self.scale_anim = QPropertyAnimation( self.WIDGET, b"iconSize" )
        

        self.j_showShadow()

        # CALLBACKS
        self.press_cb:tuple[object] = None
        self.release_cb:tuple[object] = None
        self.afterEntrance_cb = None
        self.afterExit_cb = None



        # ...
        self._glow_finSig_connected = False
        self._scale_finSig_connected = False

    def _ignore(): pass
    def _bg_trans(self):
        self.WIDGET.setStyleSheet( "background-color: transparent" )

    def jn_disconnectSignals( self, sig:SignalInstance ):
        try:
            sig.disconnect()
        except:
            pass

    ###########

    def j_iconSet( self, icon : JN_Icon = None ):
        
        self.icon = icon
        self.WIDGET.setIcon( self.icon.jgetIcon() )
        self.WIDGET.setIconSize( self.icon.jgetSize() )
        
        self.scale_upValue = self.icon.jgetSize()
        self.scale_downValue = self.icon.jgetSize()

        self.j_updateGeometry()
        
    ###########

    def j_featureSet( 
        self,  

        glow_onPR:bool = None,
        glow_anim:bool = None,
        glow_upValue:float = None,
        glow_downValue:float = None,
        glow_color:str = None,
        glow_animDuration:int = None,

        shadow_on:bool = None,
        shadow_color:str = None,
        shadow_blur:float = None,
        shadow_offset:tuple[int,int] = None,

        scale_onPR:bool = None,
        scale_anim:bool = None,
        scale_upValue:QSize = None,
        scale_downValue:QSize = None,
        scale_animDuration:int = None,

        entrance_duration:int = None,
        exit_duration:int = None


    ):
        
        #   GLOW PROPERTIES

        if not glow_onPR == None:  
            self.en_glow = glow_onPR 
            self.glow.setBlurRadius(0)
            self.glow.setColor(QColor( self.glow_color ))
            self.glow.setEnabled( False )

        if glow_onPR and not glow_anim == None:   # glow must be enabled before this
            self.en_glow_anim = glow_anim

        if not shadow_on == None:               
            self.en_shadow = shadow_on
        if self.en_shadow: self.j_showShadow()
            
            
        if not glow_upValue == None:            self.glow_upValue       = glow_upValue  

        if not glow_downValue == None:          self.glow_downValue     = glow_downValue

        if not glow_color == None:              self.glow_color         = glow_color

        if not glow_animDuration == None:       self.glow_animDuration  = glow_animDuration

        if not shadow_color == None:            self.shadow_color       = shadow_color

        if not shadow_blur == None:             self.shadow_blur        = shadow_blur

        if not shadow_offset == None:           self.shadow_blur        = shadow_offset

        #   SCALE PROPERTIES

        if not scale_onPR == None:              
            self.en_scale = scale_onPR

        if self.en_scale and not scale_anim == None:
            self.en_scale_anim = scale_anim

        if not scale_upValue == None:           
            self.scale_upValue = scale_upValue
            self.j_updateGeometry()

        if not scale_downValue == None:         self.scale_downValue    = scale_downValue

        if not scale_animDuration == None:      self.scale_animDuration = scale_animDuration

        if not entrance_duration == None:       self.entrance_duration = entrance_duration

        if not exit_duration == None:           self.exit_duration = exit_duration

    ###########
            
    def j_updateGeometry(self):
        self.geo = self.icon.jgetGeometry()
        self.geo.setSize( self.scale_upValue )

        increase = self.scale_upValue - self.icon.jgetSize()
        
        x = self.icon.jgetGeometry().x() - (increase.width()/2)
        y = self.icon.jgetGeometry().y() - (increase.height()/2)

        self.geo.setX( x )
        self.geo.setY( y )

        self.WIDGET.setGeometry( self.geo )

    def j_showShadow(self):
        if self.en_shadow:
            self.glow.setBlurRadius(self.shadow_blur)
            self.glow.setColor(QColor( self.shadow_color))
            self.glow.setOffset( self.shadow_offset[0], self.shadow_offset[1] )
            self.glow.setEnabled( True )
        
    ###########

    def j_callbackPress( self, cb = None ): 
        if cb == None:
            self.press_cb = None
            jn_disconnectSignals( self.WIDGET.pressed )
            self.WIDGET.pressed.connect( self._bg_trans )
        else:
            jn_disconnectSignals( self.WIDGET.pressed )
            self.WIDGET.pressed.connect( self.__press__ )
            self.press_cb = cb
    
    def j_callbackRelease( self, cb = None ): 
        if cb == None:
            self.release_cb = None
            jn_disconnectSignals( self.WIDGET.released )
        else:
            jn_disconnectSignals( self.WIDGET.released )
            self.WIDGET.released.connect( self.__release__ )
            self.release_cb = cb

    def j_setEntryExitCallbacks( self, entry = None, exit = None, clear:bool = False ):
        if not clear:
            if not entry == None:   self.afterEntrance_cb = entry
            if not exit == None:    self.afterExit_cb = exit
        else:
            self.afterEntrance_cb = None
            self.afterExit_cb = None

    ###########

    def j_enableClick( self, enable = True ):
        self.en_click = enable


    def j_bringFront( self ):
        self.WIDGET.raise_()

    ###########
    
    def __press__( self ):

        self._bg_trans()
  
        if self.en_click:

            # GLOW & SHADOW 
            if self.en_glow and self.en_glow_anim: # Animate Glow
                self.j_animateGlow(
                    blur_start = self.glow_downValue,
                    blur_end = self.glow_upValue,
                    duration = self.glow_animDuration,
                    color = self.glow_color,
                    offset = (0,0)
                )

            elif self.en_glow: # Glow Only
                self.glow.setBlurRadius( self.glow_upValue )
                self.glow.setColor( self.glow_color )
                self.glow.setOffset( 0,0 )
                self.glow.setEnabled(True)

            else: #Shadow Only
                if self.en_shadow: self.j_showShadow()
            
            # SCALE
            if self.en_scale and self.en_scale_anim:

                self.j_animateScale( 
                    size_end = self.scale_upValue,
                    duration = self.scale_animDuration
                )

            try:
                self.press_cb()
            except: 
                pass

    def __release__( self ):
        
        if self.en_click:
            # GLOW AND SHADOW
            if self.en_glow and self.en_glow_anim:
                self.j_animateGlow(
                    blur_end = self.glow_downValue,
                    duration = self.glow_animDuration,
                    color = self.glow_color,
                    offset = (0,0),
                    animFinish_cb = self.j_showShadow
                )
            elif self.en_glow:
                self.glow.setBlurRadius( self.glow_downValue )
                self.glow.setColor( self.glow_color )
                self.glow.setOffset( 0,0 )
                self.glow.setEnabled(True)
            
            if self.en_shadow and not self.en_glow_anim:
                self.j_showShadow()

            # SCALE
            if self.en_scale and self.en_scale_anim:
                self.j_animateScale( 
                    size_end = self.scale_downValue,
                    duration = self.scale_animDuration
                )

            try:
                self.release_cb()
            except:
                pass
        
    ###########

    def j_animateGlow(
        self, 
        blur_start : float = None,
        blur_end : float = 15.0,
        duration : int = 200, 
        color : str = "#FFFFFF",
        offset : tuple = (0,0),
        animFinish_cb = None    
    ):  
        
        if blur_start == None:
            blur_start = self.glow.blurRadius()

        self.glow.setColor( QColor( color ) )
        self.glow.setOffset( offset[0], offset[1] )
        self.glow.setEnabled(True)

        self.glow_anim.stop()
        self.glow_anim.setDuration( duration )
        self.glow_anim.setStartValue( blur_start )
        self.glow_anim.setEndValue( blur_end )

        self.glow_anim.finished.connect( animFinish_cb )
        jn_disconnectSignals( self.glow_anim.finished )

        self.glow_anim.start() 

    ###########

    def j_animateScale(
        self,
        size_end : QSize = None,
        duration : int = 200,
        animFinish_cb : object = None
    ): 
        if size_end == None: size_end = self.scale_upValue
        self.scale_anim.stop()
        self.scale_anim.setEasingCurve( QEasingCurve.Type.Linear )
        self.scale_anim.setDuration( duration )
        self.scale_anim.setStartValue( self.WIDGET.iconSize() )     
        self.scale_anim.setEndValue( size_end )


        jn_disconnectSignals( self.scale_anim.finished )
        self.scale_anim.finished.connect( animFinish_cb )


        self.scale_anim.start()

    ###########

    def j_Entrance( self, animate:bool = False ):
        
        if animate:
            self.j_animateScale( 
                size_end = self.icon.jgetSize(),
                duration = self.entrance_duration,
                animFinish_cb = self.afterEntrance_cb
            )
        else:
            if self.en_shadow:  self.j_showShadow()
            self.WIDGET.setIconSize( self.icon.jgetSize() )

            jn_disconnectSignals( self.scale_anim.finished )
            jn_disconnectSignals( self.glow_anim.finished )
            try:
                self.afterEntrance_cb
            except: pass

    def j_Exit( self, animate:bool = False ):

        if animate:
            self.j_animateScale( 
                size_end = QSize( 0 , 0 ),
                duration = self.exit_duration,
                animFinish_cb = self.afterExit_cb
            )
        else:
            self.glow_anim.stop()
            self.scale_anim.stop()
        
            self.WIDGET.setIconSize( QSize( 0, 0 ) )

            jn_disconnectSignals( self.scale_anim.finished )
            jn_disconnectSignals( self.glow_anim.finished )

            try:
                self.afterExit_cb
            except: pass
    