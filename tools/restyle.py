#!/usr/bin/env python3
"""iOS-style restyle for the merged CarLife resources."""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("SRC_DIR") or os.path.join(ROOT, "work")
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")

RES = os.path.join(OUT_DIR, "res")


def w(path, text):
    p = os.path.join(RES, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


# ------------------------------------------------------------------ colours
from theme_assets import *  # noqa: F401,F403
from theme_layouts import *  # noqa: F401,F403

def patch_setting_main(relpath="layout/setting_main.xml", inset="64.0dip"):
    p = os.path.join(RES, relpath)
    if not os.path.exists(p):
        return
    s = open(p, encoding="utf-8").read()
    # drop the empty spacers that used to inset every row
    s = re.sub(r'<FrameLayout android:layout_width="\d+\.0dip" android:layout_height="\d+\.0dip" />', "", s)
    # group card
    s = re.sub(r'<ScrollView android:layout_width="fill_parent" android:layout_height="wrap_content" android:layout_marginTop="(\d+\.0dip)">',
               lambda m: '<ScrollView android:layout_width="fill_parent" android:layout_height="wrap_content" android:layout_marginTop="%s" '
                         'android:layout_marginLeft="%s" android:layout_marginRight="%s" android:background="@drawable/ios_group_bg" android:scrollbars="none">'
                         % (m.group(1), inset, inset), s)
    # iOS radio buttons
    s = s.replace('android:textColor="@color/cl_text_a5_content" android:id="@id/',
                  'android:textColor="@color/ios_radio_text" android:button="@drawable/ios_radio" android:paddingLeft="4.0dip" android:id="@id/')
    s = re.sub(r'(<RadioButton[^>]*?)android:textSize="30\.0sp"', r'\1android:textSize="24.0sp"', s)
    s = s.replace('<RadioButton android:textSize="30.0sp"', '<RadioButton android:textSize="24.0sp"')
    s = s.replace('<RadioButton android:textSize="24.0sp" android:textColor="@color/cl_text_a5_content"',
                  '<RadioButton android:textSize="24.0sp" android:textColor="@color/ios_radio_text" android:button="@drawable/ios_radio" android:paddingLeft="4.0dip"')
    # separators inset
    s = s.replace('android:layout_marginLeft="108.0dip" android:layout_marginRight="108.0dip"',
                  'android:layout_marginLeft="26.0dip" android:layout_marginRight="26.0dip"')
    s = s.replace('android:layout_height="96.0dip" android layout', 'android:layout_height="96.0dip" android layout')
    open(p, "w", encoding="utf-8").write(s)


def patch_activity_main():
    p = os.path.join(RES, "layout/activity_main.xml")
    s = open(p, encoding="utf-8").read()
    s = s.replace('android:background="@color/cl_bg_c_main"', 'android:background="@drawable/ios_page_bg"')
    open(p, "w", encoding="utf-8").write(s)


def patch_launch():
    p = os.path.join(RES, "layout/frag_launch.xml")
    s = open(p, encoding="utf-8").read()
    s = s.replace('android:background="@color/cl_bg_c_main"', 'android:background="@drawable/ios_page_bg"')
    open(p, "w", encoding="utf-8").write(s)


def main():
    colors_xml()
    w("values/styles.xml", STYLES)
    w("drawable/shape_btn_normal.xml", SHAPE_BTN_NORMAL)
    w("drawable/shape_btn_press.xml", SHAPE_BTN_PRESS)
    w("drawable/com_bg_btn_circle.xml", BTN_CIRCLE)
    w("drawable/com_bg_item_selector.xml", ITEM_SELECTOR)
    w("drawable/com_dialog_bg.xml", DIALOG_BG)
    w("drawable/shape_edittext.xml", EDIT_BG)
    w("drawable/background_center.xml", BACKGROUND_CENTER)
    w("drawable/ios_page_bg.xml", IOS_PAGE_BG)
    w("drawable/ios_card_bg.xml", IOS_CARD_BG)
    w("drawable/ios_group_bg.xml", IOS_GROUP_BG)
    w("drawable/ios_row_selector.xml", IOS_ROW_SELECTOR)
    w("drawable/ios_radio_on.xml", IOS_RADIO_ON)
    w("drawable/ios_radio_off.xml", IOS_RADIO_OFF)
    w("drawable/ios_radio.xml", IOS_RADIO)
    w("color/ios_radio_text.xml", IOS_RADIO_TEXT)
    w("layout/frag_main.xml", frag_main(BIG))
    w("layout-hdpi-v4/frag_main.xml", frag_main(SMALL))
    w("layout/carlife_common_title_bar_new.xml", TITLE_BAR)
    if os.path.exists(os.path.join(RES, "layout-hdpi-v4/carlife_common_title_bar_new.xml")):
        w("layout-hdpi-v4/carlife_common_title_bar_new.xml", TITLE_BAR)
    patch_setting_main()
    patch_setting_main("layout-hdpi-v4/setting_main.xml", "40.0dip")
    patch_activity_main()
    patch_launch()
    # dialogs: white card + iOS typography
    for name in ("dialog_carlife.xml", "dialog_carlife_message.xml"):
        p = os.path.join(RES, "layout", name)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        s = s.replace('android:textColor="@color/common_black"', 'android:textColor="@color/ios_label"')
        open(p, "w", encoding="utf-8").write(s)
    print("restyled")


if __name__ == "__main__":
    main()
