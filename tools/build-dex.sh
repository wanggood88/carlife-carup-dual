#!/bin/bash
# 编译本项目新增的 Java 类 -> dex -> smali
#
# 依赖（用环境变量指定）：
#   PLATFORM_JAR  android.jar（bootclasspath，用于 javac）
#   BUILD_TOOLS   build-tools 目录（提供 d8）
#   APKTOOL       apktool.jar（复用其中的 baksmali）
#
# 产物：build/dex/

set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PLATFORM_JAR=${PLATFORM_JAR:?please set PLATFORM_JAR to android.jar}
BUILD_TOOLS=${BUILD_TOOLS:?please set BUILD_TOOLS to the build-tools dir}
APKTOOL=${APKTOOL:?please set APKTOOL to apktool.jar}
DEX_OUT="$ROOT/build/dex"

rm -rf "$ROOT/build/classes" "$ROOT/build/classes_stub" "$DEX_OUT"
mkdir -p "$ROOT/build/classes" "$ROOT/build/classes_stub" "$DEX_OUT"

# 1) 桩类：仅用于编译期解析 CarUp 混淆后的签名，不进入产物
find "$ROOT/src/stubs" -name '*.java' > "$ROOT/build/stubs.list"
javac -source 8 -target 8 -nowarn -bootclasspath "$PLATFORM_JAR" \
      -d "$ROOT/build/classes_stub" @"$ROOT/build/stubs.list" 2>&1 | grep -v "^Note:" || true

# 2) 真实源码
find "$ROOT/src/java" -name '*.java' > "$ROOT/build/src.list"
javac -source 8 -target 8 -nowarn -bootclasspath "$PLATFORM_JAR" \
      -cp "$PLATFORM_JAR:$ROOT/build/classes_stub" \
      -d "$ROOT/build/classes" @"$ROOT/build/src.list" 2>&1 | grep -v "^Note:" || true

# 3) d8
find "$ROOT/build/classes" -name '*.class' > "$ROOT/build/classes.list"
"$BUILD_TOOLS/d8" --min-api 16 --lib "$PLATFORM_JAR" --output "$DEX_OUT" @"$ROOT/build/classes.list"

# 4) baksmali（apktool 内置）
mkdir -p "$ROOT/build/baktool"
javac -nowarn -cp "$APKTOOL" -d "$ROOT/build/baktool" "$ROOT/tools/bak/Bak.java" 2>&1 | grep -v "^Note:" || true
java -cp "$ROOT/build/baktool:$APKTOOL" Bak "$DEX_OUT/classes.dex" "$DEX_OUT/smali"

echo "DEX OK -> $DEX_OUT/smali"
