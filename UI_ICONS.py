from JN_PKG import *
import platform

class UI_Icon():

    def __init__(self):
         # Assume the system is a Linux system and uses a / instead of a \ for file handling
        slash = '/'
        os_type = platform.system()
        print(os_type)
        if os_type == "Windows":
            # \\ is used as a single \ is a string escape characer
            slash = '\\'

        # Use a relative path from the code folder to get to the resources folder
        resources_path = f".{slash}Resources"
       
        

        self.border_small = JN_Icon( 
            file = f"{resources_path}{slash}Border{slash}Border-Small_AssetExport.svg",
            pos = QPoint( 23+3, 26 )
        )

        self.border_large = JN_Icon(
            file = f"{resources_path}{slash}Border{slash}Border-Large_AssetExport.svg",
            pos = QPoint( 10, 10 )
        )

        self.lock_locked = JN_Icon(
            file = f"{resources_path}{slash}Lock{slash}Locked-Icon_AssetExport.svg",
            pos = QPoint( 172-2, 304 )
            # pos = QPoint( 0, 0 )
        )

        self.lock_unlocked = JN_Icon(
            file = f"{resources_path}{slash}Lock{slash}Unlocked-Icon_AssetExport.svg",
            pos = QPoint( 158-5, 313 )
        )

        self.ring_green = JN_Icon(
            file = f"{resources_path}{slash}Ring{slash}GreenRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 ),
        )

        self.ring_yellow = JN_Icon(
            file = f"{resources_path}{slash}Ring{slash}YellowRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 )
        )

        self.ring_red = JN_Icon(
            file = f"{resources_path}{slash}Ring{slash}RedRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 )
        )

        self.keypad_zero = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyZero_AssetExport.svg",
            pos = QPoint( 190, 662-15 )
        )   

        self.keypad_one = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyOne_AssetExport.svg",
            pos = QPoint( 70, 298-15 )
        )

        self.keypad_two = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyTwo_AssetExport.svg",
            pos = QPoint( 190, 298-15 )
        )

        self.keypad_three = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyThree_AssetExport.svg",
            pos = QPoint( 310, 298-15 )
        )

        self.keypad_four = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyFour_AssetExport.svg",
            pos = QPoint( 70, 417-15 )
        )

        self.keypad_five = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyFive_AssetExport.svg",
            pos = QPoint( 190, 418-15 )
        )

        self.keypad_six = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeySix_AssetExport.svg",
            pos = QPoint( 310, 418-15 )
        )

        self.keypad_seven = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeySeven_AssetExport.svg",
            pos = QPoint( 70, 538-15 )
        )

        self.keypad_eight = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyEight_AssetExport.svg",
            pos = QPoint( 190, 538-15 )
        )

        self.keypad_nine = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyNine_AssetExport.svg",
            pos = QPoint( 310, 538-15 )
        )

        self.keypad_enter = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyEnter_AssetKey.svg",
            pos = QPoint( 310, 662-15 )
        )

        self.keypad_reset = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyReset_AssetExport.svg",
            pos = QPoint( 70, 661-15 )
        )

        self.keypad_correct = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyCorrectIcon_AssetExport.svg",
            pos = QPoint( 310, 662-15 )
        )

        self.keypad_wrong = JN_Icon(
            file = f"{resources_path}{slash}Key{slash}KeyWrongIcon_AssetExport.svg",
            pos = QPoint( 310, 662-15 )
        )

        self.nfc_ring = JN_Icon(
            file = f"{resources_path}{slash}NFC{slash}NFC-Ring_AssetExport.svg",
            pos = QPoint( 137, 325 )
        )

        self.nfc_symbol = JN_Icon(
            file = f"{resources_path}{slash}NFC{slash}NFC-Symbol_AssetExport.svg",
            pos = QPoint( 199, 348 )
        )

        self.fp_ring = JN_Icon(
            file = f"{resources_path}{slash}FP{slash}FP-Ring_AssetExport.svg",
            pos = QPoint( 185, 329 )
        )

        self.fp_symbol = JN_Icon(
            file = f"{resources_path}{slash}FP{slash}FP-Symbol_AssetExport.svg",
            pos = QPoint( 198, 346 )
        )

        self.path_bg = f"{resources_path}{slash}GradientMainBG_AssetExport.png"