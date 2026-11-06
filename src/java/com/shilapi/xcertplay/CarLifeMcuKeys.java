package com.shilapi.xcertplay;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

/**
 * CarLife 方控广播桥。
 *
 * <p>CarUp 原本只监听三条路径：窗口 KeyEvent、MediaSession、MEDIA_BUTTON 广播。
 * 但相当一部分车机（长安 / 吉利 / 奇瑞 / 讯飞 / 阿达优 / NWD 等）并不发 Android
 * 标准按键，而是由 MCU 发一条厂商私有广播，带上自己的字符串或整数键值。
 * 百度 CarLife 支持这套广播（{@code com.baidu.carlifevehicle.audioplayer.buttoncontrol}
 * 下的 8 个 Receiver），CarUp 不支持，所以在这些车上 CarUp 的方控完全没反应。</p>
 *
 * <p>本类把 CarLife 支持的 8 种厂商广播全部接管，解析成 Android 标准媒体键码，
 * 再送进 CarUp 原有的方控处理链（学习页 / CarPlay 会话）。</p>
 */
public final class CarLifeMcuKeys {

    private static final String TAG = "DiPlayCarLifeKeys";

    /** 与二合一选择页共用的偏好文件。 */
    public static final String PREFS = "dual_wheel";
    public static final String KEY_ENABLED = "carlife_mcu_bridge";

    /* ---------------- 车机 MCU 方控广播 action（与 CarLife 完全一致） ---------------- */

    /** 长安 / 阿达优：key_value + key_state。 */
    private static final String A_OKL = "com.okl.android.MCU_KEY_IND_ACTION";
    /** 长安（联友）：Key_code + Key_state。 */
    private static final String A_COAGENT = "com.coagent.intent.action.KEY_CHANGED";
    /** 长安 C3 / 奇瑞：c3_hardkey_keycode + c3_hardkey_action。 */
    private static final String A_C3 = "android.intent.action.C3_HARDKEY";
    /** 吉利：value + state。 */
    private static final String A_SPD = "com.spd.system.key";
    /** 阿达优：key_value + key_state。 */
    private static final String A_ADAYO = "com.adayo.android.MCU_KEY_IND_ACTION";
    /** NWD：extra_key_value。 */
    private static final String A_NWD = "com.nwd.action.ACTION_KEY_VALUE";
    /** 讯飞：CLICK_KEY + STATUS_KEY。 */
    private static final String A_XFL = "IKeyClick.KEY_CLICK";

    /* ---------------- Android 标准键码 ---------------- */

    private static final int KEY_MEDIA_PREVIOUS = 88;
    private static final int KEY_MEDIA_NEXT = 87;
    private static final int KEY_MEDIA_PLAY = 126;
    private static final int KEY_MEDIA_PAUSE = 127;
    private static final int KEY_MEDIA_PLAY_PAUSE = 85;
    private static final int KEY_MEDIA_STOP = 86;
    private static final int KEY_MEDIA_FAST_FORWARD = 90;
    private static final int KEY_MEDIA_REWIND = 89;

    private static final Handler MAIN = new Handler(Looper.getMainLooper());
    /** 车机广播没有抬起事件，这里补一个，避免 CarUp 把长按键当成一直按住。 */
    private static final long RELEASE_DELAY_MS = 110L;

    private static BroadcastReceiver receiver;
    private static boolean installed;

    private CarLifeMcuKeys() {
    }

    /* ---------------- 开关 ---------------- */

    public static boolean isEnabled(Context context) {
        if (context == null) {
            return true;
        }
        try {
            SharedPreferences sp = context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
            return sp.getBoolean(KEY_ENABLED, true);
        } catch (Throwable t) {
            return true;
        }
    }

    public static void setEnabled(Context context, boolean enabled) {
        if (context == null) {
            return;
        }
        try {
            context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
                    .edit().putBoolean(KEY_ENABLED, enabled).apply();
        } catch (Throwable t) {
            Log.w(TAG, "cannot persist switch", t);
        }
        if (enabled) {
            install(context);
        } else {
            uninstall(context);
        }
    }

    /* ---------------- 注册 / 反注册 ---------------- */

    public static synchronized void install(Context context) {
        if (installed || context == null || !isEnabled(context)) {
            return;
        }
        Context app = context.getApplicationContext();
        if (app == null) {
            app = context;
        }
        try {
            IntentFilter filter = new IntentFilter();
            filter.addAction(A_OKL);
            filter.addAction(A_COAGENT);
            filter.addAction(A_C3);
            filter.addAction(A_SPD);
            filter.addAction(A_ADAYO);
            filter.addAction(A_NWD);
            filter.addAction(A_XFL);
            // 车机多按有序广播发送，CarLife 自己用 abortBroadcast 抢；这里只要排前面旁听，
            // 绝不 abort，避免影响 CarLife 通道本身。
            filter.setPriority(1000);

            BroadcastReceiver r = new Bridge();
            app.registerReceiver(r, filter);
            receiver = r;
            installed = true;
            Log.i(TAG, "carlife mcu bridge installed");
        } catch (Throwable t) {
            Log.e(TAG, "install failed", t);
        }
    }

    public static synchronized void uninstall(Context context) {
        if (!installed) {
            return;
        }
        Context app = context == null ? null : context.getApplicationContext();
        try {
            (app == null ? context : app).unregisterReceiver(receiver);
        } catch (Throwable t) {
            Log.w(TAG, "uninstall failed", t);
        }
        receiver = null;
        installed = false;
    }

    /* ---------------- 广播解析 ---------------- */

    private static final class Bridge extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            try {
                handle(intent);
            } catch (Throwable t) {
                Log.w(TAG, "handle failed", t);
            }
        }
    }

    private static void handle(Intent intent) {
        if (intent == null) {
            return;
        }
        String action = intent.getAction();
        if (action == null) {
            return;
        }

        int keyCode = 0;

        if (A_OKL.equals(action) || A_ADAYO.equals(action)) {
            // key_state=PRESS_DOWN 才算一次按下
            String state = stringExtra(intent, "key_state");
            if (state != null && !"PRESS_DOWN".equalsIgnoreCase(state)
                    && !"DOWN".equalsIgnoreCase(state)) {
                return;
            }
            keyCode = mediaCode(stringExtra(intent, "key_value"));

        } else if (A_COAGENT.equals(action)) {
            // CarLife 只在 Key_state=UP 时处理这条
            String state = stringExtra(intent, "Key_state");
            if (state != null && !"UP".equalsIgnoreCase(state)) {
                return;
            }
            keyCode = mediaCode(stringExtra(intent, "Key_code"));

        } else if (A_C3.equals(action)) {
            // action: 0=down
            if (intent.getIntExtra("android.intent.extra.c3_hardkey_action", -1) != 0) {
                return;
            }
            keyCode = c3Code(intent.getIntExtra("android.intent.extra.c3_hardkey_keycode", -1));

        } else if (A_SPD.equals(action)) {
            // state: 1=down
            if (intent.getIntExtra("state", -1) != 1) {
                return;
            }
            keyCode = spdCode(intent.getIntExtra("value", -1));

        } else if (A_NWD.equals(action)) {
            keyCode = mediaCode(stringExtra(intent, "extra_key_value"));

        } else if (A_XFL.equals(action)) {
            // STATUS_KEY: 0=按下；CLICK_KEY: 5=下一首 6=上一首
            if (intent.getIntExtra("STATUS_KEY", -1) != 0) {
                return;
            }
            int click = intent.getIntExtra("CLICK_KEY", -1);
            if (click == 5) {
                keyCode = KEY_MEDIA_NEXT;
            } else if (click == 6) {
                keyCode = KEY_MEDIA_PREVIOUS;
            }
        }

        if (keyCode != 0) {
            dispatch(keyCode);
        }
    }

    private static String stringExtra(Intent intent, String name) {
        try {
            String v = intent.getStringExtra(name);
            if (v == null) {
                // 少数车机把字符串键值塞在整数 extra 里
                int iv = intent.getIntExtra(name, Integer.MIN_VALUE);
                if (iv != Integer.MIN_VALUE) {
                    return String.valueOf(iv);
                }
            }
            return v;
        } catch (Throwable t) {
            return null;
        }
    }

    /** 字符串键值 → 标准键码（与 CarLife 的字符串判断表等价）。 */
    private static int mediaCode(String raw) {
        if (raw == null) {
            return 0;
        }
        String s = raw.trim().toUpperCase();
        StringBuilder sb = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c != '_' && c != '-' && c != ' ' && c != '.') {
                sb.append(c);
            }
        }
        s = sb.toString();
        if (s.isEmpty()) {
            return 0;
        }
        if (s.startsWith("NEXT") || s.equals("NEXTSONG")) {
            return KEY_MEDIA_NEXT;
        }
        if (s.startsWith("PREV") || s.equals("PRE") || s.equals("PREVIOUSSONG")
                || s.equals("LAST")) {
            return KEY_MEDIA_PREVIOUS;
        }
        if (s.equals("PLAYPAUSE") || s.equals("PAUSEPLAY") || s.equals("PP")
                || s.equals("TOGGLEPLAYPAUSE")) {
            return KEY_MEDIA_PLAY_PAUSE;
        }
        if (s.startsWith("PLAY")) {
            return KEY_MEDIA_PLAY;
        }
        if (s.startsWith("PAUSE")) {
            return KEY_MEDIA_PAUSE;
        }
        if (s.startsWith("STOP")) {
            return KEY_MEDIA_STOP;
        }
        if (s.equals("FF") || s.startsWith("FASTFORWARD")) {
            return KEY_MEDIA_FAST_FORWARD;
        }
        if (s.equals("REW") || s.startsWith("REWIND")) {
            return KEY_MEDIA_REWIND;
        }
        return 0;
    }

    /** C3_HARDKEY 的数字键码（长安 / 奇瑞共用一套）。 */
    private static int c3Code(int code) {
        switch (code) {
            case 0xF3:
            case 0xF5:
                return KEY_MEDIA_NEXT;
            case 0xF4:
            case 0xF6:
                return KEY_MEDIA_PREVIOUS;
            case 0xEF:
                return KEY_MEDIA_PLAY_PAUSE;
            default:
                return 0;
        }
    }

    /** 吉利（com.spd.system.key）的数字键码。 */
    private static int spdCode(int value) {
        switch (value) {
            case 0x12:
                return KEY_MEDIA_PLAY_PAUSE;
            case 0x13:
            case 0x32:
                return KEY_MEDIA_PREVIOUS;
            case 0x14:
            case 0x33:
                return KEY_MEDIA_NEXT;
            default:
                return 0;
        }
    }

    /* ---------------- 送入 CarUp 现有链路 ---------------- */

    private static void dispatch(int keyCode) {
        // 1) 正在学习方控：记进学习页，让用户按一下就能学到这个键
        try {
            if (WheelKeysActivity.inFront != null) {
                Object page = WheelKeysActivity.inFront.get();
                if (page instanceof WheelKeysActivity) {
                    WheelKeysActivity activity = (WheelKeysActivity) page;
                    activity.logKey(new WheelKeyInput(keyCode, 0, true, WheelKeySource.CARLIFE));
                    activity.onKey(keyCode);
                    Log.i(TAG, "learned keyCode=" + keyCode);
                    return;
                }
            }
        } catch (Throwable t) {
            Log.w(TAG, "learn sink failed", t);
        }

        // 2) 正常使用：交给 CarPlayMediaKeys 原有的按键执行器
        try {
            final CarPlayMediaKeys keys = CarPlayMediaKeys.INSTANCE;
            if (keys == null) {
                return;
            }
            final boolean handled = keys.onWheelKey(keyCode, true, false);
            Log.i(TAG, "keyCode=" + keyCode + " handled=" + handled);
            if (handled) {
                // 车机 MCU 广播只有按下，没有抬起；补一个抬起事件，
                // 否则「下一首」这类按住类按键会一直保持按下状态。
                MAIN.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            keys.onWheelKey(keyCode, false, true);
                        } catch (Throwable t) {
                            Log.w(TAG, "release failed", t);
                        }
                    }
                }, RELEASE_DELAY_MS);
            }
        } catch (Throwable t) {
            Log.w(TAG, "dispatch failed", t);
        }
    }
}
