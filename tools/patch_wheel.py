#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 CarUp 的 WheelKeySource 枚举补一个 CARLIFE 监听源（label: carlife-mcu）。

CarUp 原有的方控监听方式只有：
    window / media-session / media-button-receiver / volume / broadcast
后者（broadcast）只对应 android.intent.action.MEDIA_BUTTON。

CarLife 走的是完全不同的路子 —— 车机 MCU 发厂商私有广播（长安、吉利、奇瑞、
讯飞、阿达优、NWD 等 8 种 action），所以这里新增一个独立来源，学习页和日志里
能直接看出按键是从车机方控广播来的。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("SRC_DIR") or os.path.join(ROOT, "work")
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")

import sys

TARGET = os.path.join(OUT_DIR, "smali_classes2/com/shilapi/xcertplay/WheelKeySource.smali")


def patch(path=TARGET):
    if not os.path.exists(path):
        print("skip: %s not found" % path)
        return False

    s = open(path, encoding="utf-8").read()
    if "CARLIFE:Lcom/shilapi/xcertplay/WheelKeySource;" in s:
        print("already patched")
        return False

    # 1) 新增枚举常量字段
    s = s.replace(
        ".field public static final enum BROADCAST:Lcom/shilapi/xcertplay/WheelKeySource;\n",
        ".field public static final enum BROADCAST:Lcom/shilapi/xcertplay/WheelKeySource;\n\n"
        ".field public static final enum CARLIFE:Lcom/shilapi/xcertplay/WheelKeySource;\n")

    # 2) clinit 需要更多寄存器
    s = s.replace(".method static constructor <clinit>()V\n    .locals 12",
                  ".method static constructor <clinit>()V\n    .locals 16")

    # 3) 构造 CARLIFE 实例（紧接 BROADCAST 之后）
    anchor = ("    sput-object v6, Lcom/shilapi/xcertplay/WheelKeySource;->BROADCAST:"
              "Lcom/shilapi/xcertplay/WheelKeySource;\n")
    if anchor not in s:
        print("anchor missing, abort")
        return False
    s = s.replace(anchor, anchor + """
    .line 60
    .line 61
    new-instance v14, Lcom/shilapi/xcertplay/WheelKeySource;

    const-string v13, "carlife-mcu"

    const-string v15, "CARLIFE"

    const/16 v12, 0x5

    invoke-direct {v14, v15, v12, v13}, Lcom/shilapi/xcertplay/WheelKeySource;-><init>(Ljava/lang/String;ILjava/lang/String;)V

    sput-object v14, Lcom/shilapi/xcertplay/WheelKeySource;->CARLIFE:Lcom/shilapi/xcertplay/WheelKeySource;
""")

    # 4) 重建 $VALUES 数组（长度 5 -> 6）
    start = s.index("    .line 61\n    const/4 v8, 0x5\n")
    end = s.index("    sput-object v0, Lcom/shilapi/xcertplay/WheelKeySource;->$ENTRIES:"
                  "Lkotlin/enums/EnumEntries;")
    new_array = """    .line 61
    .line 62
    const/4 v12, 0x6

    new-array v12, v12, [Lcom/shilapi/xcertplay/WheelKeySource;

    const/4 v13, 0x0

    aput-object v0, v12, v13

    const/4 v13, 0x1

    aput-object v1, v12, v13

    const/4 v13, 0x2

    aput-object v2, v12, v13

    const/4 v13, 0x3

    aput-object v4, v12, v13

    const/4 v13, 0x4

    aput-object v6, v12, v13

    const/4 v13, 0x5

    aput-object v14, v12, v13

    .line 73
    .line 74
    sput-object v12, Lcom/shilapi/xcertplay/WheelKeySource;->$VALUES:[Lcom/shilapi/xcertplay/WheelKeySource;

    .line 75
    .line 76
    new-instance v0, Lkotlin/enums/EnumEntriesList;

    .line 77
    .line 78
    invoke-direct {v0, v12}, Lkotlin/enums/EnumEntriesList;-><init>([Ljava/lang/Enum;)V

    .line 79
    .line 80
    .line 81
"""
    s = s[:start] + new_array + s[end:]

    open(path, "w", encoding="utf-8").write(s)
    print("patched %s" % path)
    return True


if __name__ == "__main__":
    patch()
