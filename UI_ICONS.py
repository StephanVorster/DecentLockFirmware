from JN_PKG import *

class UI_Icon():

    def __init__(self):
        base_path = "/home/nagda/AppLock/"

        self.border_small = JN_Icon( 
            file = base_path + "Resources/Border/Border-Small_AssetExport.svg",
            pos = QPoint( 23+3, 26 )
        )

        self.border_large = JN_Icon(
            file = base_path + "Resources/Border/Border-Large_AssetExport.svg",
            pos = QPoint( 10, 10 )
        )

        self.lock_locked = JN_Icon(
            file = base_path + "Resources/Lock/Locked-Icon_AssetExport.svg",
            pos = QPoint( 172-2, 304 )
        )

        self.lock_unlocked = JN_Icon(
            file = base_path + "Resources/Lock/Unlocked-Icon_AssetExport.svg",
            pos = QPoint( 158-5, 313 )
        )

        self.ring_green = JN_Icon(
            file = base_path + "Resources/Ring/GreenRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 ),
        )

        self.ring_yellow = JN_Icon(
            file = base_path + "Resources/Ring/YellowRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 )
        )

        self.ring_red = JN_Icon(
            file = base_path + "Resources/Ring/RedRing_AssetExport.svg",
            pref_pos = True,
            pos = QPoint( 84, 244 )
        )

        self.keypad_zero = JN_Icon(
            file = base_path + "Resources/Key/KeyZero_AssetExport.svg",
            pos = QPoint( 190, 662 )
        )   

        self.keypad_one = JN_Icon(
            file = base_path + "Resources/Key/KeyOne_AssetExport.svg",
            pos = QPoint( 70, 298 )
        )

        self.keypad_two = JN_Icon(
            file = base_path + "Resources/Key/KeyTwo_AssetExport.svg",
            pos = QPoint( 190, 298 )
        )

        self.keypad_three = JN_Icon(
            file = base_path + "Resources/Key/KeyThree_AssetExport.svg",
            pos = QPoint( 310, 298 )
        )

        self.keypad_four = JN_Icon(
            file = base_path + "Resources/Key/KeyFour_AssetExport.svg",
            pos = QPoint( 70, 417 )
        )

        self.keypad_five = JN_Icon(
            file = base_path + "Resources/Key/KeyFive_AssetExport.svg",
            pos = QPoint( 190, 418 )
        )

        self.keypad_six = JN_Icon(
            file = base_path + "Resources/Key/KeySix_AssetExport.svg",
            pos = QPoint( 310, 418 )
        )

        self.keypad_seven = JN_Icon(
            file = base_path + "Resources/Key/KeySeven_AssetExport.svg",
            pos = QPoint( 70, 538 )
        )

        self.keypad_eight = JN_Icon(
            file = base_path + "Resources/Key/KeyEight_AssetExport.svg",
            pos = QPoint( 190, 538 )
        )

        self.keypad_nine = JN_Icon(
            file = base_path + "Resources/Key/KeyNine_AssetExport.svg",
            pos = QPoint( 310, 538 )
        )

        self.keypad_enter = JN_Icon(
            file = base_path + "Resources/Key/KeyEnter_AssetKey.svg",
            pos = QPoint( 310, 662 )
        )

        self.keypad_reset = JN_Icon(
            file = base_path + "Resources/Key/KeyReset_AssetExport.svg",
            pos = QPoint( 70, 661 )
        )

        self.keypad_correct = JN_Icon(
            file = base_path + "Resources/Key/KeyCorrectIcon_AssetExport.svg",
            pos = QPoint( 310, 662 )
        )

        self.keypad_wrong = JN_Icon(
            file = base_path + "Resources/Key/KeyWrongIcon_AssetExport.svg",
            pos = QPoint( 310, 662 )
        )

        self.nfc_ring = JN_Icon(
            file = base_path + "Resources/NFC/NFC-Ring_AssetExport.svg",
            pos = QPoint( 137, 325 )
        )

        self.nfc_symbol = JN_Icon(
            file = base_path + "Resources/NFC/NFC-Symbol_AssetExport.svg",
            pos = QPoint( 199, 348 )
        )

        self.fp_ring = JN_Icon(
            file = base_path + "Resources/FP/FP-Ring_AssetExport.svg",
            pos = QPoint( 185, 329 )
        )

        self.fp_symbol = JN_Icon(
            file = base_path + "Resources/FP/FP-Symbol_AssetExport.svg",
            pos = QPoint( 198, 346 )
        )

        self.path_bg = base_path + "Resources/GradientMainBG_AssetExport.png"
