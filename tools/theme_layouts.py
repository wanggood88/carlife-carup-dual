#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iOS 主题资源：drawable 形状与布局 XML。"""

SHAPE_BTN_NORMAL = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/ios_blue" />
    <corners android:radius="24.0dip" />
</shape>
"""

SHAPE_BTN_PRESS = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FF0062CC" />
    <corners android:radius="24.0dip" />
</shape>
"""

BTN_CIRCLE = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="oval" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#1A007AFF" />
</shape>
"""

ITEM_SELECTOR = """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true" android:drawable="@color/cp_press_e" />
    <item android:state_focused="true" android:drawable="@color/cp_press_e" />
    <item android:state_selected="true" android:drawable="@color/cp_press_e" />
    <item android:drawable="@android:color/transparent" />
</selector>
"""

DIALOG_BG = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="@color/ios_card" />
    <corners android:radius="20.0dip" />
</shape>
"""

EDIT_BG = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFF2F2F7" />
    <corners android:radius="10.0dip" />
    <padding android:left="12.0dip" android:top="4.0dip" android:right="12.0dip" android:bottom="4.0dip" />
</shape>
"""

IOS_PAGE_BG = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <gradient android:angle="270" android:startColor="#FFFFFFFF" android:centerColor="#FFF6F8FC" android:endColor="#FFEDF1F9" />
</shape>
"""

IOS_CARD_BG = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFFFFFFF" />
    <corners android:radius="24.0dip" />
    <stroke android:width="1.0dip" android:color="#14000000" />
</shape>
"""

IOS_GROUP_BG = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="rectangle" xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFFFFFFF" />
    <corners android:radius="18.0dip" />
    <stroke android:width="1.0dip" android:color="#0F000000" />
</shape>
"""

IOS_ROW_SELECTOR = """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_pressed="true" android:drawable="@color/cp_press_e" />
    <item android:state_focused="true" android:drawable="@color/cp_press_e" />
    <item android:drawable="@android:color/transparent" />
</selector>
"""

IOS_RADIO_ON = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape android:shape="oval">
            <size android:width="22.0dip" android:height="22.0dip" />
            <solid android:color="@color/ios_blue" />
        </shape>
    </item>
    <item android:top="6.0dip" android:left="6.0dip" android:right="6.0dip" android:bottom="6.0dip">
        <shape android:shape="oval">
            <solid android:color="#FFFFFFFF" />
        </shape>
    </item>
</layer-list>
"""

IOS_RADIO_OFF = """<?xml version="1.0" encoding="utf-8"?>
<shape android:shape="oval" xmlns:android="http://schemas.android.com/apk/res/android">
    <size android:width="22.0dip" android:height="22.0dip" />
    <solid android:color="#00FFFFFF" />
    <stroke android:width="1.4dip" android:color="#FFC7C7CC" />
</shape>
"""

IOS_RADIO = """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:drawable="@drawable/ios_radio_on" />
    <item android:drawable="@drawable/ios_radio_off" />
</selector>
"""

IOS_RADIO_TEXT = """<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:state_checked="true" android:color="#FF007AFF" />
    <item android:color="#FF3C3C43" />
</selector>
"""

BACKGROUND_CENTER = """<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item>
        <shape android:shape="rectangle">
            <gradient android:angle="270" android:startColor="#FFFFFFFF" android:centerColor="#FFF6F8FC" android:endColor="#FFE8EEF9" />
        </shape>
    </item>
    <item android:gravity="center">
        <bitmap android:gravity="center" android:src="@drawable/cailife_logo" android:tileMode="disabled" />
    </item>
</layer-list>
"""

# ------------------------------------------------------------------ frag_main
FRAG_MAIN_TMPL = """<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout android:id="@id/main_layout" android:background="@drawable/ios_page_bg" android:layout_width="fill_parent" android:layout_height="fill_parent"
  xmlns:android="http://schemas.android.com/apk/res/android" xmlns:android_custom="http://schemas.android.com/apk/res-auto">
    <RelativeLayout android:id="@id/rellayout_bar" android:layout_width="fill_parent" android:layout_height="{bar}">
        <ImageButton android:id="@id/exit_img_btn" android:background="@drawable/com_bg_btn_selector" android:layout_width="{ex}" android:layout_height="{ex}" android:layout_marginLeft="{exm}" android:layout_centerVertical="true" android:padding="{expad}" android:src="@drawable/ios_ic_back" android:scaleType="fitCenter" android:layout_alignParentLeft="true" />
        <TextView android:textSize="{ts}sp" android:textColor="@color/ios_label" android:gravity="center_vertical" android:layout_width="wrap_content" android:layout_height="fill_parent" android:layout_marginLeft="{tl}" android:text="CarLife" android:fontFamily="sans-serif-medium" />
        <TextView android:textSize="{caps}sp" android:textColor="@color/ios_secondary" android:gravity="center_vertical" android:layout_width="wrap_content" android:layout_height="fill_parent" android:layout_marginLeft="{capl}" android:text="车机端" />
        <TextView android:textSize="{bs}sp" android:textColor="@color/ios_blue" android:gravity="center" android:id="@id/main_btn_wza" android:background="@drawable/com_bg_btn_selector" android:layout_width="{bwza}" android:layout_height="{bh}" android:layout_marginRight="{m1}" android:text="@string/wza" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <TextView android:textSize="{bs}sp" android:textColor="@color/ios_blue" android:gravity="center" android:id="@id/main_btn_fk" android:background="@drawable/com_bg_btn_selector" android:layout_width="{bw}" android:layout_height="{bh}" android:layout_marginRight="{m2}" android:text="@string/fk" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <TextView android:textSize="{bs}sp" android:textColor="@color/ios_blue" android:gravity="center" android:id="@id/main_btn_qx" android:background="@drawable/com_bg_btn_selector" android:layout_width="{bw}" android:layout_height="{bh}" android:layout_marginRight="{m3}" android:text="@string/qx" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <TextView android:textSize="{bs}sp" android:textColor="@color/ios_blue" android:gravity="center" android:id="@id/main_btn_setting" android:background="@drawable/com_bg_btn_selector" android:layout_width="{bw}" android:layout_height="{bh}" android:layout_marginRight="{m4}" android:text="@string/setting" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <TextView android:textSize="{bs}sp" android:textColor="@color/ios_blue" android:gravity="center" android:id="@id/main_btn_help" android:background="@drawable/com_bg_btn_selector" android:layout_width="{bw}" android:layout_height="{bh}" android:layout_marginRight="{m5}" android:text="@string/baidu_help" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <View android:background="@color/ios_separator" android:layout_width="fill_parent" android:layout_height="1.0dip" android:layout_alignParentBottom="true" />
    </RelativeLayout>
    <RelativeLayout android:id="@id/main_rellayout_status" android:layout_width="fill_parent" android:layout_height="fill_parent" android:layout_below="@id/rellayout_bar">
        <LinearLayout android:orientation="vertical" android:background="@drawable/ios_card_bg" android:gravity="center_horizontal" android:paddingLeft="{cp}" android:paddingTop="{cpt}" android:paddingRight="{cp}" android:paddingBottom="{cpb}" android:layout_width="{cw}" android:layout_height="wrap_content" android:layout_centerInParent="true">
            <ImageView android:id="@id/main_img_view" android:layout_width="{icon}" android:layout_height="{icon}" android:src="@drawable/ios_ic_connect" android:scaleType="fitCenter" />
            <TextView android:textSize="{isz}sp" android:textColor="@color/ios_secondary" android:gravity="center" android:id="@id/main_info_text_view" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="{imt}" android:text="@string/usb_not_connected" />
            <Button android:textSize="{rs}sp" android:textColor="#FFFFFFFF" android:id="@id/main_retry_btn" android:background="@drawable/selector_btn_retry" android:visibility="invisible" android:layout_width="{rw}" android:layout_height="{rh}" android:layout_marginTop="{rmt}" android:text="@string/usb_connect_btn_retry" />
        </LinearLayout>
    </RelativeLayout>
    <com.baidu.carlifevehicle.view.LoadingProgressBar android:id="@id/main_load_round_progress" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_centerInParent="true" />
</RelativeLayout>
"""

BIG = dict(bar="76.0dip", ex="44.0dip", exm="16.0dip", expad="10.0dip", ts="20", tl="68.0dip", caps="12", capl="148.0dip",
           bs="15", bh="38.0dip", bw="68.0dip", bwza="84.0dip",
           m1="324.0dip", m2="248.0dip", m3="172.0dip", m4="96.0dip", m5="16.0dip",
           cw="500.0dip", cp="44.0dip", cpt="34.0dip", cpb="34.0dip",
           icon="168.0dip", isz="16", imt="14.0dip", rs="15", rw="220.0dip", rh="44.0dip", rmt="20.0dip")
SMALL = dict(bar="62.0dip", ex="38.0dip", exm="12.0dip", expad="9.0dip", ts="18", tl="58.0dip", caps="11", capl="126.0dip",
             bs="14", bh="34.0dip", bw="60.0dip", bwza="76.0dip",
             m1="288.0dip", m2="216.0dip", m3="148.0dip", m4="80.0dip", m5="12.0dip",
             cw="420.0dip", cp="34.0dip", cpt="24.0dip", cpb="24.0dip",
             icon="132.0dip", isz="15", imt="12.0dip", rs="14", rw="200.0dip", rh="40.0dip", rmt="16.0dip")


def frag_main(cfg):
    return FRAG_MAIN_TMPL.format(**cfg)


# ------------------------------------------------------------------ title bar
TITLE_BAR = """<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout android:layout_width="fill_parent" android:layout_height="wrap_content"
  xmlns:android="http://schemas.android.com/apk/res/android">
    <RelativeLayout android:layout_width="fill_parent" android:layout_height="@dimen/common_title_bar_height" android:layout_marginTop="32.0dip">
        <ImageButton android:id="@id/ib_left" android:background="@drawable/com_bg_btn_selector" android:layout_width="44.0dip" android:layout_height="44.0dip" android:layout_marginLeft="20.0dip" android:padding="10.0dip" android:src="@drawable/ios_ic_back" android:scaleType="fitCenter" android:layout_centerVertical="true" />
        <TextView android:textSize="22.0sp" android:textColor="@color/ios_label" android:fontFamily="sans-serif-medium" android:id="@id/tv_title" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginLeft="16.0dip" android:maxWidth="420.0dip" android:singleLine="true" android:layout_toRightOf="@id/ib_left" android:layout_centerVertical="true" />
        <TextView android:textSize="13.0sp" android:textColor="@color/ios_secondary" android:paddingTop="2.0dip" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginLeft="8.0dip" android:layout_toRightOf="@id/tv_title" android:layout_centerVertical="true" />
        <ImageButton android:layout_gravity="right" android:background="@drawable/com_bg_btn_selector" android:visibility="gone" android:layout_width="@dimen/common_icon_small" android:layout_height="@dimen/common_icon_small" android:layout_marginRight="20.0dip" android:layout_alignParentRight="true" />
        <TextView android:textSize="17.0sp" android:textColor="@color/ios_blue" android:gravity="center" android:background="@drawable/com_bg_btn_selector" android:paddingLeft="10.0dip" android:paddingRight="10.0dip" android:focusable="true" android:visibility="gone" android:layout_width="wrap_content" android:layout_height="44.0dip" android:layout_marginRight="10.0dip" android:layout_alignParentRight="true" android:layout_centerVertical="true" />
        <View android:background="@color/ios_separator" android:layout_width="fill_parent" android:layout_height="1.0dip" android:layout_alignParentBottom="true" />
    </RelativeLayout>
</RelativeLayout>
"""
