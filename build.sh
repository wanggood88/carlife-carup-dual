#!/bin/bash
# 二合一 APK 构建流水线
#
# 前置：
#   work/dec_carlife   —— 用 apktool 反编译出来的 CarLife 车机端工程
#   work/dec_carup     —— 用 apktool 反编译出来的 CarUp 工程
#   build/keystore.jks —— 签名用（可用 keytool 自己生成）
#
# 环境变量：
#   PLATFORM_JAR / BUILD_TOOLS / APKTOOL
#   KEYSTORE / KS_PASS / KEY_ALIAS / KEY_PASS（不给则只产出未签名 APK）

set -e
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT"

: "${PLATFORM_JAR:?set PLATFORM_JAR}"
: "${BUILD_TOOLS:?set BUILD_TOOLS}"
: "${APKTOOL:?set APKTOOL}"

[ -d work/dec_carlife ] || { echo "缺少 work/dec_carlife"; exit 1; }
[ -d work/dec_carup ] || { echo "缺少 work/dec_carup"; exit 1; }

echo "== 1/7 合并资源与代码"
python3 tools/merge.py

echo "== 2/7 生成合并清单"
python3 tools/manifest.py > /dev/null

echo "== 3/7 生成图标"
mkdir -p build/merged/res/drawable-nodpi
python3 tools/gen_icons.py > /dev/null

echo "== 4/7 iOS 主题改造"
python3 tools/restyle.py

echo "== 5/7 方控监听方式增强（新增 carlife-mcu 源）"
python3 tools/patch_wheel.py

echo "== 6/7 编译自研类并注入"
tools/build-dex.sh
rm -rf build/merged/smali/com/baidu/carlifevehicle/ui build/merged/smali/com/shilapi
mkdir -p build/merged/smali/com/shilapi
cp -r build/dex/smali/com/shilapi/xcertplay build/merged/smali/com/shilapi/
cp -r build/dex/smali/com/baidu/carlifevehicle/ui build/merged/smali/com/baidu/carlifevehicle/
cp build/dex/smali/com/baidu/carlifevehicle/DualApplication.smali build/merged/smali/com/baidu/carlifevehicle/

echo "== 7/7 打包"
(cd build/merged && java -jar "$APKTOOL" b . -o "$ROOT/build/unsigned.apk")

if [ -n "${KEYSTORE:-}" ]; then
  "$BUILD_TOOLS/zipalign" -f -p 4 build/unsigned.apk build/aligned.apk
  "$BUILD_TOOLS/apksigner" sign \
      --ks "$KEYSTORE" --ks-pass "pass:$KS_PASS" \
      --ks-key-alias "${KEY_ALIAS:-dual}" --key-pass "pass:${KEY_PASS:-$KS_PASS}" \
      --min-sdk-version 16 \
      --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
      --out build/app-release.apk build/aligned.apk
  "$BUILD_TOOLS/apksigner" verify build/app-release.apk
  echo "SIGNED -> build/app-release.apk"
else
  echo "UNSIGNED -> build/unsigned.apk"
fi
