from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from FUNCTIONS import *



# ICON CLASSS
class JN_Icon(QIcon):
    """
    For setting up icon for the JN_SVG_WIDGET class. 

    ## Note:
    Functions that starts with `j` can be use publicly. Only use these functions

    ## Instruction:
    1. Initiate buy calling `__init__(file, pos)`
    
    ## Functions:
    `jgetIcon()`            Returns QIcon\n
    `jgetSize()`            Returns QSize of the image.\n
    `jsetPosition(pos)`     Set position ICON on UI\n
    `jgetSVGFile()`         Returns filepath of image file\n
    `jsetSVGFile(file)`     Sets image of icon\n
    `jgetGeometry()`        Returns geometry attribute.\n
    `jsetGeometry(geo)`     Sets geometry attribute\n

    `Author: Justine Nagdaparan`
    `Date:   2023-10-19 (YYYY-MM-DD)`

    """
    
    def __init__(self, file: str, pos: QPoint, pref_pos = False ) -> None:
        """
        Must initiate\n

        file : string -- The real part (default 0.0)
        pos : QPoint -- Coordinate of the icon on the UI
        
        """
        super().__init__(file)
        self.svg_file: str = file
        self.icon_geo: QRect = None
        self.size: QSize = None
        self.preferred_position = pref_pos
        self.jsetPosition(pos)

        self.svg_file = "/home/nagda/Applock/" + self.svg_file

    # Note: functions that start at j can be use publicly

    def jgetIcon(self) -> QIcon:
        """Returns the QIcon object"""
        return self

    
    def jgetSize(self) -> QSize:
        """
        Returns the actual size of the image.\n
        QSize is a tuple( width, height )
        """
        return self.size

    
    def jsetPosition(self, pos: QPoint) -> None:
        """
        Manually set the position of the ICON on the UI\n
        pos : QPoint -- QPoint(x,y) Coordinate of the icon on the UI
        """
        renderer = QSvgRenderer(self.svg_file)
        self.size = renderer.defaultSize()
        x = pos.x()
        y = pos.y()
        w = self.size.width()
        h = self.size.height()
        self.jsetGeometry(QRect(x, y, w, h))

    def jgetSVGFile(self) -> str:
        """Returns the filepath to the image file"""
        return self.svg_file

    def jsetSVGFile(self, file: str) -> None:
        """Sets the image of the icon manually"""
        self.svg_file = file

    def jgetGeometry(self) -> QRect:
        """
        Returns the geometry obj of the QIcon. \n
        Geometry holds x and y coord and length width size.
        """
        return self.icon_geo

    def jsetGeometry(self, geo: QRect) -> None:
        """
        Manually Sets the geometry attribute of the icon\n
        geo : QRect -- QRect(x,y,w,h)
        """
        self.icon_geo = geo

class JN_PUSHBUTTON( QPushButton ):
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:

        # print( event.type().__str__() )

        # if event.type() == QEvent.Type.Enter:
        #     self.pressed.emit()
        #     return True
        # if event.type() == QEvent.Type.Leave:
        #     self.released.emit()
        #     return True
        
        return super().eventFilter(watched, event)


class JN_SVG_Widget():

    ObjectIdOnPressed: str = ""
    
    def __init__(self, parent=None) -> None:

        self.en_debug:  bool = False

        # Enablers - Defaults
        self.en_appearance: bool = False
        self.ds_click: bool = False
        self.en_click: bool = False
        self.en_hold: bool = False
        self.en_glow: bool = False
        self.en_glow_anim: bool = False
        self.en_shadow: bool = False
        self.en_scale: bool = False
        self.en_scale_anim: bool = False

        # Glow Config - Defaults
        self.glow_upValue: float = 15.0
        self.glow_downValue: float = 0
        self.glow_color: str = "#FFFFFF"
        self.glow_animDuration: int = 200

        # Shadow Config - Defaults
        self.shadow_color: str = "#292929"
        self.shadow_blur: float = 5.0
        self.shadow_offset: tuple[int, int] = (5, 5)    # x , y

        # Scale Config - Defaults
        self.scale_upValue: QSize = None
        self.scale_downValue: QSize = None
        self.scale_animDuration: int = 500  # milliseconds

        # Button Press Release Checkers
        self.button_alreadyPressed = False      # Reset upon first release
        self.button_alreadyReleased = True      # Reset upon first press

        # Hold Duration
        self.hold_duration : int = 0            # Hold duration in seconds
        self.hold_timer : QTimer = QTimer()
        self.hold_timer.setSingleShot( True )
        self.hold_timer.timeout.connect( self.INTER_HOLD_HANDLER )

        # Button -- MASTER WIDGET
        self.M_WIDGET = JN_PUSHBUTTON(parent)
        self.M_WIDGET.setFlat(True)
        self.M_WIDGET.installEventFilter( self.M_WIDGET )
        self.M_WIDGET.setAttribute( Qt.WidgetAttribute.WA_AcceptTouchEvents, True )
        self.M_WIDGET.pressed.connect(self.INTER_PRESS_HANDLER)
        self.M_WIDGET.released.connect(self.INTER_RELEASE_HANDLER)
        self.M_WIDGET.setStyleSheet(
            """
                border: None;
                background: transparent;
            """
        )

        # Main Geometry - Coordinates(x,y) & Size(w,h)
        self.M_GEOMETRY : QRect     = QRect(0, 0, 0, 0)                                                          
        self.M_ICON     : JN_Icon   = None

        # Glow 
        self.M_GLOW = QGraphicsDropShadowEffect(self.M_WIDGET)  
        self.M_GLOW.setOffset(0, 0)
        self.M_GLOW.setEnabled(False)
        self.M_WIDGET.setGraphicsEffect(self.M_GLOW)

        # Animation
        self.M_GLOW_ANIM    = QPropertyAnimation(self.M_GLOW, b"blurRadius")
        self.M_SCALE_ANIM   = QPropertyAnimation(self.M_WIDGET, b"iconSize")

        # Main External Callbacks
        self.EXTCB_PRESS = None
        self.EXTCB_RELEASE = None
        self.EXTCB_HOLD = None
        self.EXTCB_AFTER_ENTRANCE = None
        self.EXTCB_AFTER_EXIT = None
        

        # Initiately do not show
        self.j_Exit(animate=False)

    def inter_showGlow( self, show : bool = True, animate: bool = False, callback = None ) -> bool:

        """
        Will show and perform animation based on param: `show` and `animate`.\n
        ### If `show=False` and glow is still enabled:\n
            - `glow_downValue` will be set.\n
            - However if `glow_downValue` is between 0 to 1, show shadow.\n
        ### If `show=False` and glow is disabled:\n
            - If shadow is still enabled, show shadow.\n
            - Else, disable all glow\n
        ### Return\n
        Return False if glow is disabled
        """

        if self.en_debug: print( "ShowGlow", show, self.en_glow, self.en_appearance )

        # GLOW UP
        if show and self.en_glow and self.en_appearance:
            # Check if glow animation is enabled
            if animate and self.en_glow_anim:
                self.j_animateGlow(
                    blur_end=self.glow_upValue,
                    duration=self.glow_animDuration,
                    color=self.glow_color,
                    offset=(0, 0),
                    animFinish_cb=callback
                )
            # If not, no animation
            else:    
                
                self.M_GLOW.setBlurRadius(self.glow_upValue)
                self.M_GLOW.setColor(QColor(self.glow_color))
                self.M_GLOW.setOffset(0,0)
                self.M_GLOW.setEnabled(True)
                FUNC_TRY_CALLING( callback )

            return True

        # GLOW DOWN
        elif not show and self.en_glow:
            # Check if glow animation is enabled
            if animate and self.en_glow_anim:
                # If glow downvalue is between 0 to 1, show shadow instead
                if FUNC_BETWEEN( self.glow_downValue, 0.0, 1.0 ) and self.en_shadow: 
                    self.inter_showShadow( True, animate=animate, callback=callback ) # Animate when showing shadow
                # Remove Glow with animation
                else:
                    
                    self.j_animateGlow(
                        blur_end=self.glow_downValue,
                        duration=self.glow_animDuration,
                        color=self.glow_color,
                        offset=(0, 0),
                        animFinish_cb=callback
                    )
            # If no animation
            else:  
                # If glow downvalue is between 0 to 1, show shadow instead
                if FUNC_BETWEEN( self.glow_downValue, 0.0, 1.0 ) and self.en_shadow:    
                    self.inter_showShadow( True, animate=animate, callback=callback ) # Animate when showing shadow 
                # Remove Glow without animation
                else:
                    self.M_GLOW.setBlurRadius(self.glow_downValue)
                    self.M_GLOW.setColor(QColor(self.glow_color))
                    self.M_GLOW.setOffset(0,0)
                    self.M_GLOW.setEnabled(True)
                    FUNC_TRY_CALLING( callback )
                
        # REMOVE
        else:
            # Show shadow if enabled
            if not self.inter_showShadow( True, animate=animate, callback=callback ):   
                self.M_GLOW_ANIM.stop()         # Else, abort glow animation
                self.M_GLOW.setEnabled(False)   # Else, disabled all glow
        
        return False


    def inter_showShadow( self, show: bool = True, animate: bool = False, callback = None ) -> bool:


        """
        Show the shadow and perform animation based on parameter `show` and `animate`\n
        Callback will be called after shown or animation\n
        Returns False if shadow is disabled or not shown due to param `show=False`
        """

        if self.en_debug: print( "ShowShadow", show, self.en_shadow, self.en_appearance )

        # Check if shadow enabled
        if show and self.en_shadow and self.en_appearance:
            # Shadow with Animation
            if animate: 
                # Called after glow down animation then 
                def afterThisAnimCB():
                    self.M_GLOW.setBlurRadius(self.shadow_blur)
                    self.M_GLOW.setColor(QColor(self.shadow_color))
                    self.M_GLOW.setOffset(self.shadow_offset[0], self.shadow_offset[1])
                    self.M_GLOW.setEnabled(True)
                    FUNC_TRY_CALLING(callback)
                self.j_animateGlow(
                    blur_end=0.0,
                    duration=self.glow_animDuration,
                    color=self.glow_color,
                    animFinish_cb=afterThisAnimCB
                )
            # Shadow without animation
            else: 
                self.M_GLOW.setBlurRadius(self.shadow_blur)
                self.M_GLOW.setColor(QColor(self.shadow_color))
                self.M_GLOW.setOffset(self.shadow_offset[0], self.shadow_offset[1])
                self.M_GLOW.setEnabled(True)
                FUNC_TRY_CALLING(callback)

            return True

        else: return False

    
    def inter_showScale( self, scaleUp : bool = None, animate: bool = False, after_anim_cb = None ) -> bool:

        """
        Perform scaling with animation based on boolean parameters `scaleUp` and `animate`.\n
        Callback param `after_anim_cb` will be called scalling or animation\n
        Scaling animation uses:\n
        - `scale_upValue`\n
        - `scale_animDuration`\n
        Scaling will always start from current size of icon
        ### Return
        Returns False if scale is disabled
        """

        if self.en_debug: print( "Show Scale", scaleUp, self.en_scale, self.en_appearance )
        

        # SCALE UP
        if scaleUp and self.en_scale and self.en_appearance:
            # Scale with animation
            if animate and self.en_scale_anim:
                if self.en_debug: print( self.M_WIDGET.iconSize() )
                self.j_animateScale(
                    size_end=self.scale_upValue,
                    duration=self.scale_animDuration,
                    animFinish_cb=after_anim_cb
                )
            # Scale without animation
            else:
                self.M_WIDGET.setIconSize( self.scale_upValue )
                FUNC_TRY_CALLING( after_anim_cb )

        # SCALE DOWN
        elif not scaleUp and self.en_scale and self.en_appearance:
            
            # Scale with animation
            if animate and self.en_scale_anim:
                self.j_animateScale(
                    size_end=self.scale_downValue,
                    duration=self.scale_animDuration,
                    animFinish_cb=after_anim_cb
                )
            # Scale without animation
            else:
                self.M_WIDGET.setIconSize( self.scale_downValue )
                FUNC_TRY_CALLING( after_anim_cb )

        # VANISH
        else:
            # Scale with animation
            if animate and self.en_scale_anim:
                self.j_animateScale(
                    size_end=QSize(0,0),
                    duration=self.scale_animDuration,
                    animFinish_cb=after_anim_cb
                )
            # Scale without animation
            else:
                self.M_WIDGET.setIconSize( QSize(0,0) )
                FUNC_TRY_CALLING( after_anim_cb )
        
        return True



    def j_iconSet(self, icon:JN_Icon=None):

        self.M_ICON : JN_Icon = icon
        self.M_WIDGET.setIcon(self.M_ICON.jgetIcon())
        self.M_WIDGET.setIconSize(self.M_ICON.jgetSize())

        if self.scale_upValue is None: # Default is original + 20
            self.scale_upValue = self.M_ICON.jgetSize()

        if self.scale_downValue is None: # Default is original
            self.scale_downValue = self.M_ICON.jgetSize()

        self.inter_updateGeometry()

    def j_featureSet(

        self,

        glow_onPR           = None,
        glow_anim           = None,
        glow_upValue        = None,
        glow_downValue      = None,
        glow_color          = None,
        glow_animDuration   = None,

        shadow_on           = None,
        shadow_color        = None,
        shadow_blur         = None,
        shadow_offset       = None,

        scale_onPR          = None,
        scale_anim          = None,
        scale_upValue       = None,
        scale_downValue     = None,
        scale_animDuration  = None

    ):

        if self.en_debug: print("feature")

        # GLOW ON PRESS
        if glow_onPR is not None:
            self.en_glow = glow_onPR
            # = Disabled
            if not self.en_glow:
                self.inter_showGlow( show=False, animate=self.en_glow_anim )

        # GLOW ANIMATION
        if glow_anim is not None:
            if self.en_glow and glow_anim:      # GLOW = Enabled and glow anim = True
                self.en_glow_anim = glow_anim
            else:                               # Disable animation as glow must be enabled for animation to work
                self.en_glow_anim = False

        # SHADOW 
        if shadow_on is not None:
            self.en_shadow = shadow_on
            # Turn on/off Shadow Immidiately
            self.inter_showShadow( show=shadow_on, animate=self.en_glow_anim )

        # GLOW CONFIGURATION
        if glow_upValue is not None: # ---------------- UP VALUE
            self.glow_upValue = glow_upValue
        if glow_downValue is not None: # -------------- DOWN VALUE
            self.glow_downValue = glow_downValue
        if glow_color is not None: # ------------------ COLOR
            self.glow_color = glow_color
            # Update Color now
            self.M_GLOW.setColor( QColor( self.glow_color ) )
        if glow_animDuration is not None: # ----------- DURATION
            self.glow_animDuration = glow_animDuration

        # SHAODW CONFIGURATION
        if shadow_color is not None: # ---------------- SHADOW COLOR
            self.shadow_color = shadow_color
        if shadow_blur is not None: # ----------------- SHADOW BLUR
            self.shadow_blur = shadow_blur
        if shadow_offset is not None: # --------------- SHODOW OFFSET
            self.shadow_blur = shadow_offset

        # SCALE ON PRESS
        if scale_onPR is not None:
            self.en_scale = scale_onPR
            # If disabled, Revert to original size immediately if
            if not self.en_scale:
                self.inter_showScale( scaleUp=False, animate=self.en_scale_anim )
        
        # SCALE AMNIMATION
        if self.en_scale and scale_anim is not None:
            self.en_scale_anim = scale_anim
            # IF FALSE
            # If scaling up -> Immediately set to scaled up size - Vice Versa

        # SCALE CONFIGURATION
        if scale_upValue is not None: # --------------- UP VALUE
            self.scale_upValue = scale_upValue
            self.inter_updateGeometry()
        if scale_downValue is not None: # ------------- DOWN VALUE
            self.scale_downValue = scale_downValue
        if scale_animDuration is not None: # ---------- DURATION
            self.scale_animDuration = scale_animDuration

    def j_enableHold( self, duration : int = 3000 ):
        self.hold_duration = duration

    def j_getOriginalSize(self) -> QSize:
        return self.M_ICON.jgetSize()

    def j_increasedSize( self, increase:int ) -> QSize:
        """This does not affect anything in the object"""
        return self.M_ICON.jgetSize() + QSize( increase, increase );

    def inter_updateGeometry(self):
        
        self.M_GEOMETRY = self.M_ICON.jgetGeometry()
        
        increase_W: QSize = self.scale_upValue.width() - self.M_ICON.jgetSize().width()
        increase_H: QSize = self.scale_upValue.height() - self.M_ICON.jgetSize().height()

        self.M_GEOMETRY.setWidth( self.M_ICON.jgetSize().width() + increase_W )
        self.M_GEOMETRY.setHeight( self.M_ICON.jgetSize().height() + increase_H )

        x = 0
        y = 0

        if self.M_ICON.preferred_position:
            x = self.M_ICON.jgetGeometry().x()
            y = self.M_ICON.jgetGeometry().y()
        else:
            x = int(self.M_ICON.jgetGeometry().x() - (increase_W/2))
            y = int(self.M_ICON.jgetGeometry().y() - (increase_H/2))
        

        self.M_GEOMETRY.setX(x)
        self.M_GEOMETRY.setY(y)

        self.M_WIDGET.setGeometry(self.M_GEOMETRY)


    def j_setPressCallback(self, press_cb=None):
        
        """
        Assigns a callback function to `EXTCB_PRESS` which is called whenever a press action occurs.\n
        Used Publicly for external use.\n
        If `press_cb` is left None, it will clear callback for this event\n
        """

        if press_cb is None: # Clear out signal
            self.EXTCB_PRESS = None
        else: # Attached callback to signal
            self.EXTCB_PRESS = press_cb
            

    def j_setReleaseCallback(self, rel_cb=None):

        """
        Assigns a callback function to `EXTCB_RELEASE` which is called whenever a release action occurs.\n
        Used Publicly for external use.\n
        If `rel_cb` is left None, it will clear callback for this event\n
        """

        if rel_cb is None: # Clear out signal
            self.EXTCB_RELEASE = None
        else: # Attached callback to signal
            self.EXTCB_RELEASE = rel_cb


    def j_setHoldCallback( self, hol_cb=None ):
        """
        Assigns a callback function to `EXTCB_HOLD` which is called whenever a hold action occurs.\n
        Used Publicly for external use.\n
        If `hol_cb` is left None, it will clear callback for this event\n
        """

        if hol_cb is None: # Clear out signal
            self.EXTCB_HOLD = None
        else: # Attached callback to signal
            self.EXTCB_HOLD = hol_cb

            
    def j_setEntryCallback(self, entry_cb=None):

        """
        Assigns a callback function to `EXTCB_AFTER_ENTRANCE` which is called whenever a successfull entrance.\n
        Used Publicly for external use.\n
        If `entry_cb` is left None, it will clear callback for this event\n
        """

        if entry_cb is not None:
            self.EXTCB_AFTER_ENTRANCE = entry_cb
        else: # Clear out signal
            self.EXTCB_AFTER_ENTRANCE = None


    def j_setExitCallback(self, exit_cb=None):

        """
        Assigns a callback function to `EXTCB_AFTER_EXIT` which is called whenever a successfull exit.\n
        Used Publicly for external use.\n
        If `exit_cb` is left None, it will clear callback for this event\n
        """

        if exit_cb is not None:
            self.EXTCB_AFTER_EXIT = exit_cb
        else: # Clear out signal
            self.EXTCB_AFTER_EXIT = None


    def j_enableClick(self, clickable=True):

        """A very simple method to disable/enable click actions. Without param is enable"""

        self.en_click = clickable


    def j_bringFront(self):

        """A very simple method to put this object on top of other UI elements"""

        self.M_WIDGET.raise_()

    
    def INTER_HOLD_HANDLER(self):

        if self.en_debug: print( "HOLD" )

        """
        ?
        """

        if self.en_click and self.en_appearance and not self.ds_click:
            # Callback when pressed
            FUNC_TRY_CALLING( self.EXTCB_HOLD )




    def INTER_PRESS_HANDLER(self):

        if self.en_debug: print( "Press" )

        """
        Called whenever a press event occured.\n
        Sets BG to transparent\n
        If features enabled, 
            - animate scale to original or upvalue
            - animate glow to original or upvalue\n
        Else, no animation
        """

        

        # 1st - Check if Clickable
        #   Clickable       ->
        #   Appearance      ->
        # ! Click Disabled  ->
        # ! Already Press   ->
        if self.en_click and self.en_appearance and not self.ds_click and not self.button_alreadyPressed:   

            self.hold_timer.start( self.hold_duration )

            self.button_alreadyPressed = True
            self.button_alreadyReleased = False

            # Animate glow. The function will handle the checking
            self.inter_showGlow( show=True, animate=self.en_glow_anim )
            
            # Animate Scale. The function will handle the checking
            self.inter_showScale( scaleUp=True, animate=self.en_scale_anim )
            
            # Callback when pressed
            FUNC_TRY_CALLING( self.EXTCB_PRESS )


    def INTER_RELEASE_HANDLER(self):

        if self.en_debug: print( "Release" )

        """
        Called whenever a release event occured.\n
        If features enabled,
            - animate scale to original or down value
            - animate glow to shadow or down value\n
        Else, no animation.
        """

        # 1st - Check if Clickable, appearance, and if temp... not clickable
        if self.en_click and self.en_appearance and not self.ds_click and not self.button_alreadyReleased:

            
            self.hold_timer.stop()
           
            self.button_alreadyPressed = False
            self.button_alreadyReleased = True

            # Animate glow. The function will handle the checking
            self.inter_showGlow( show=False, animate=self.en_glow_anim )
            
            # Animate Scale. The function will handle the checking
            self.inter_showScale( scaleUp=False, animate=self.en_scale_anim )
            
            # Callback when pressed
            FUNC_TRY_CALLING( self.EXTCB_RELEASE )


    def j_animateGlow(
        self,
        blur_start=None,
        blur_end=15.0,
        duration=100,
        color="#FFFFFF",
        offset=(0,0),
        animFinish_cb=None
    ):
        
        if self.en_debug: print("GlowAnimation")

        if blur_start is None:
            blur_start = self.M_GLOW.blurRadius()

        self.M_GLOW_ANIM.stop()

        self.M_GLOW.setColor(QColor(color))
        self.M_GLOW.setOffset(offset[0], offset[1])
        self.M_GLOW.setEnabled(True)

        self.M_GLOW_ANIM.setDuration(duration)
        self.M_GLOW_ANIM.setStartValue(blur_start)
        self.M_GLOW_ANIM.setEndValue(blur_end)

        FUNC_DISCONNECT_EVENTSIGNAL(self.M_GLOW_ANIM.finished)
        if animFinish_cb is not None:
            self.M_GLOW_ANIM.finished.connect(animFinish_cb)

        self.M_GLOW_ANIM.start()



    def j_animateScale(
        self,
        size_end=None,
        duration=100,
        animFinish_cb=None
    ):
        
        if self.en_debug: print("ScaleAnim")

        if size_end is None:
            size_end = self.scale_upValue

        self.M_SCALE_ANIM.stop()
        self.M_SCALE_ANIM.setEasingCurve(QEasingCurve.Linear)
        self.M_SCALE_ANIM.setDuration(duration)
        self.M_SCALE_ANIM.setStartValue(self.M_WIDGET.iconSize())
        self.M_SCALE_ANIM.setEndValue(size_end)

        FUNC_DISCONNECT_EVENTSIGNAL(self.M_SCALE_ANIM.finished)
        if animFinish_cb is not None:
            self.M_SCALE_ANIM.finished.connect(animFinish_cb)

        self.M_SCALE_ANIM.start()

    def j_animateScaleStop(self):
        self.M_SCALE_ANIM.stop()

    def j_Entrance(self, animate=False):

        if self.en_debug: print("Entrance", self.en_appearance)

        self.en_appearance = True
        self.M_WIDGET.show()

        def afterAnimHandler():
            FUNC_TRY_CALLING(self.EXTCB_AFTER_ENTRANCE)
            self.ds_click = False   # Clickable again

        self.ds_click = True    # Disable click temporarily during Entrance Animation
        
        self.M_WIDGET.setIconSize( QSize( 0,0 ) )
        self.inter_showScale( scaleUp=False, animate=animate, after_anim_cb=afterAnimHandler )

        self.inter_showShadow( show=True, animate=animate )

        if not animate: self.ds_click = False



    def j_Exit(self, animate=False):

        if self.en_debug: print("Exit", self.en_appearance)

        self.en_appearance = False

        def afterAnimHandler():
            self.ds_click = False
            FUNC_TRY_CALLING( self.EXTCB_AFTER_EXIT )
            self.M_GLOW_ANIM.stop()
            self.M_SCALE_ANIM.stop()
            self.inter_showGlow( show=False )
            self.M_WIDGET.hide()

        self.ds_click = True

        self.inter_showScale( scaleUp=None, animate=animate, after_anim_cb=afterAnimHandler )

        if not animate: self.ds_click = False
