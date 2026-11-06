#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iOS 主题资源：颜色表与 styles.xml。"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")
RES = os.path.join(OUT_DIR, "res")


def w(path, text):
    p = os.path.join(RES, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


COLORS = {
    "bg_blue": "#FF007AFF",
    "black": "#FF000000",
    "cl_bg_c_main": "#FFF2F2F7",
    "cl_bg_e_dialog": "#FFFFFFFF",
    "cl_btn_b": "#FF007AFF",
    "cl_btn_c": "#FFFF3B30",
    "cl_btn_d": "#FF34C759",
    "cl_line_a1_item": "#FFE5E5EA",
    "cl_line_a4": "#FFD1D1D6",
    "cl_line_b_leftbar": "#FFE5E5EA",
    "cl_line_c": "#33FF3B30",
    "cl_line_d_dialog": "#FFE5E5EA",
    "cl_other_c_highlight": "#FF007AFF",
    "cl_press_b": "#1A007AFF",
    "cl_press_c": "#1AFF3B30",
    "cl_press_d": "#1A34C759",
    "cl_press_e_dialog": "#FFEFEFF4",
    "cl_text_a0_title": "#993C3C43",
    "cl_text_a2_content": "#993C3C43",
    "cl_text_a4_bgtext": "#FF3C3C43",
    "cl_text_a4_title": "#FF3C3C43",
    "cl_text_a5_content": "#FF000000",
    "cl_text_a5_title": "#FF000000",
    "cl_text_b_dialog": "#FF000000",
    "cl_text_c_btn_dialog": "#FF8A8A8E",
    "com_titlebar_bg": "#FFFFFFFF",
    "com_titlebar_bg_night": "#FFFFFFFF",
    "com_titlebar_middle_text": "#FF000000",
    "com_titlebar_middle_text_night": "#FF000000",
    "common_black": "#FF1C1C1E",
    "common_list_main_text_color": "#FF000000",
    "common_list_second_text_color": "#FF8A8A8E",
    "common_title_color_title": "#FF000000",
    "cp_bt_bg": "#FFF2F2F7",
    "cp_click_c": "#1A007AFF",
    "cp_click_e": "#FFEFEFF4",
    "cp_cont_a": "#FF8A8A8E",
    "cp_cont_b": "#FF6C6C70",
    "cp_cont_bg": "#FFFFFFFF",
    "cp_cont_c": "#FF8A8A8E",
    "cp_cont_d": "#FF8A8A8E",
    "cp_cont_e": "#FFC7C7CC",
    "cp_cont_f": "#FF000000",
    "cp_cont_g": "#FF007AFF",
    "cp_cont_h": "#FFFF3B30",
    "cp_cont_i": "#993C3C43",
    "cp_cont_m": "#FF1C1C1E",
    "cp_cont_n": "#FF8A8A8E",
    "cp_cont_u": "#FF3C3C43",
    "cp_label_bg": "#FFFFFFFF",
    "cp_line_a": "#FFE5E5EA",
    "cp_line_b": "#FFD1D1D6",
    "cp_line_c": "#1F000000",
    "cp_line_d": "#FFE5E5EA",
    "cp_line_e": "#0F000000",
    "cp_line_f": "#0D000000",
    "cp_line_g": "#1A000000",
    "cp_normal_bg": "#FFFFFFFF",
    "cp_other_a": "#FF0A84FF",
    "cp_other_b": "#FFFF3B30",
    "cp_other_c": "#FF007AFF",
    "cp_other_d": "#FF5AC8FA",
    "cp_press_a": "#FFE9EDF5",
    "cp_press_b": "#0F000000",
    "cp_press_e": "#FFEFEFF4",
    "cp_tab_bg": "#FFFFFFFF",
    "frag_default_background_color": "#FFF2F2F7",
    # iOS design tokens
    "ios_bg": "#FFF2F2F7",
    "ios_card": "#FFFFFFFF",
    "ios_separator": "#FFE5E5EA",
    "ios_blue": "#FF007AFF",
    "ios_label": "#FF000000",
    "ios_secondary": "#FF8A8A8E",
    "ios_tertiary": "#FFC7C7CC",
    "ios_green": "#FF34C759",
    "ios_red": "#FFFF3B30",
}


def colors_xml():
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
    for k, v in COLORS.items():
        lines.append('    <color name="%s">%s</color>' % (k, v))
    lines.append("</resources>")
    w("values/colors.xml", "\n".join(lines) + "\n")


STYLES = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppBaseTheme" parent="@android:style/Theme.Light">
        <item name="android:windowBackground">@color/ios_bg</item>
        <item name="android:colorAccent">@color/ios_blue</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
    <style name="AppTheme" parent="@style/AppBaseTheme" />
    <style name="CarlifeDialog" parent="@android:style/Theme.Dialog">
        <item name="android:windowBackground">@android:color/transparent</item>
        <item name="android:windowFrame">@null</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowIsFloating">true</item>
        <item name="android:windowContentOverlay">@null</item>
        <item name="android:windowAnimationStyle">@android:style/Animation.Dialog</item>
        <item name="android:windowSoftInputMode">adjustPan</item>
        <item name="android:backgroundDimAmount">0.22</item>
    </style>
    <style name="CarlifeRoundProgress" parent="@android:style/Theme.Dialog">
        <item name="android:windowBackground">@android:color/transparent</item>
        <item name="android:windowFrame">@null</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowIsFloating">true</item>
        <item name="android:windowContentOverlay">@null</item>
        <item name="android:windowAnimationStyle">@android:style/Animation.Dialog</item>
        <item name="android:windowSoftInputMode">adjustPan</item>
    </style>
    <style name="CustomTheme" parent="@style/AppBaseTheme">
        <item name="android:windowBackground">@drawable/background_center</item>
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowContentOverlay">@null</item>
    </style>
    <style name="Spinner1Style">
        <item name="android:textSize">18.0sp</item>
    </style>
    <style name="Spinner2Style">
        <item name="android:textSize">30.0sp</item>
    </style>
</resources>
"""

# ------------------------------------------------------------------ drawables
