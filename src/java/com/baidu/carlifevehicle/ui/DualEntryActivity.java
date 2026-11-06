package com.baidu.carlifevehicle.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RadialGradient;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

/**
 * Unified launcher. Shows an iOS style chooser so the user decides which of the
 * two merged services to enter: CarLife (Baidu phone projection) or CarUp
 * (wireless CarPlay host).
 */
public class DualEntryActivity extends Activity {

    public static final String PREFS = "dual_entry";
    public static final String KEY_REMEMBER = "remember";
    public static final String KEY_LAST = "last";

    private static final String TARGET_CARLIFE = "com.baidu.carlifevehicle.CarlifeActivity";
    private static final String TARGET_CARUP = "com.shilapi.xcertplay.DiPlayActivity";

    private static final int ACCENT = 0xFF007AFF;
    private static final int INK = 0xFF0B0B0C;
    private static final int SUB = 0xFF8A8A8E;

    private float density;
    private IosSwitch rememberSwitch;
    private LinearLayout content;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        density = getResources().getDisplayMetrics().density;
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN);
        if (Build.VERSION.SDK_INT >= 21) {
            getWindow().setStatusBarColor(Color.TRANSPARENT);
            getWindow().setNavigationBarColor(Color.TRANSPARENT);
        }

        setContentView(buildUi());
        animateIn();
    }

    // ---------------------------------------------------------------- UI

    private View buildUi() {
        FrameLayout root = new FrameLayout(this);
        GradientDrawable bg = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,
                new int[]{0xFFFFFFFF, 0xFFF4F6FB, 0xFFEDF1F9});
        root.setBackground(bg);

        root.addView(new Blob(this, 0x335AC8FA, 0.10f, 0.02f, 0.55f));
        root.addView(new Blob(this, 0x33BF5AF2, 0.92f, 0.98f, 0.50f));

        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        int padH = dp(46), padV = dp(24);
        content.setPadding(padH, padV, padH, padV);
        root.addView(content, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        // ---------- header
        LinearLayout header = new LinearLayout(this);
        header.setOrientation(LinearLayout.VERTICAL);

        LinearLayout badgeRow = new LinearLayout(this);
        badgeRow.setOrientation(LinearLayout.HORIZONTAL);

        TextView badge = text("CARLIFE + CARUP", 9.5f, ACCENT, Typeface.BOLD);
        if (Build.VERSION.SDK_INT >= 21) {
            badge.setLetterSpacing(0.16f);
        }
        GradientDrawable pill = new GradientDrawable();
        pill.setColor(0xFFEAF2FF);
        pill.setCornerRadius(dp(9));
        badge.setBackground(pill);
        badge.setPadding(dp(10), dp(5), dp(10), dp(5));
        badgeRow.addView(badge);

        TextView badge2 = text("二合一", 9.5f, 0xFF8A8A8E, Typeface.BOLD);
        GradientDrawable pill2 = new GradientDrawable();
        pill2.setColor(0xFFF2F2F7);
        pill2.setCornerRadius(dp(9));
        badge2.setBackground(pill2);
        badge2.setPadding(dp(9), dp(5), dp(9), dp(5));
        LinearLayout.LayoutParams b2 = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        b2.leftMargin = dp(6);
        badgeRow.addView(badge2, b2);

        header.addView(badgeRow);

        TextView title = text("选择互联方式", 30f, INK, Typeface.BOLD);
        if (Build.VERSION.SDK_INT >= 21) {
            title.setLetterSpacing(-0.02f);
        }
        LinearLayout.LayoutParams tlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        tlp.topMargin = dp(10);
        header.addView(title, tlp);

        TextView sub = text("两个应用已合并为一个，先选择本次要进入的界面，之后可随时返回切换。",
                13f, SUB, Typeface.NORMAL);
        sub.setLineSpacing(dp(3), 1f);
        LinearLayout.LayoutParams slp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        slp.topMargin = dp(4);
        header.addView(sub, slp);
        content.addView(header);

        // ---------- cards
        View topSpacer = new View(this);
        content.addView(topSpacer, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        LinearLayout cards = new LinearLayout(this);
        cards.setOrientation(LinearLayout.HORIZONTAL);
        LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        clp.topMargin = dp(18);
        content.addView(cards, clp);

        SharedPreferences sp = getSharedPreferences(PREFS, MODE_PRIVATE);
        String last = sp.getBoolean(KEY_REMEMBER, true) ? sp.getString(KEY_LAST, null) : null;
        View carlife = buildCard("ic_dual_carlife", "CarLife 互联",
                "百度 CarLife+ 通道\nUSB / Wi-Fi 连接手机，导航音乐投屏", "进入 CarLife", TARGET_CARLIFE,
                TARGET_CARLIFE.equals(last));
        View carup = buildCard("ic_dual_carup", "CarUp 互联",
                "无线 CarPlay 通道\n支持原车旋钮、HUD 与方向盘按键", "进入 CarUp", TARGET_CARUP,
                TARGET_CARUP.equals(last));

        LinearLayout.LayoutParams lp1 = new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        lp1.rightMargin = dp(9);
        LinearLayout.LayoutParams lp2 = new LinearLayout.LayoutParams(0,
                ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        lp2.leftMargin = dp(9);
        cards.addView(carlife, lp1);
        cards.addView(carup, lp2);

        View midSpacer = new View(this);
        content.addView(midSpacer, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        // ---------- footer
        LinearLayout footer = new LinearLayout(this);
        footer.setOrientation(LinearLayout.HORIZONTAL);
        footer.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout.LayoutParams flp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        flp.topMargin = dp(16);
        content.addView(footer, flp);

        rememberSwitch = new IosSwitch(this);
        rememberSwitch.setCheckedSilently(sp.getBoolean(KEY_REMEMBER, true));
        footer.addView(rememberSwitch);

        TextView rememberLabel = text("高亮上次使用的通道", 12f, 0xFF3C3C43, Typeface.NORMAL);
        LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        rlp.leftMargin = dp(8);
        footer.addView(rememberLabel, rlp);

        View spacer = new View(this);
        footer.addView(spacer, new LinearLayout.LayoutParams(0, 1, 1f));

        TextView version = text("CarLife 3.3.9  ·  CarUp 3.0", 11f, 0xFFB0B0B5, Typeface.NORMAL);
        footer.addView(version);

        TextView tip = text("两个通道互不影响，随时回到此页切换即可。", 11f, 0xFFB0B0B5, Typeface.NORMAL);
        LinearLayout.LayoutParams tpl = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        tpl.topMargin = dp(7);
        content.addView(tip, tpl);

        return root;
    }

    private View buildCard(String iconName, final String title, String desc,
                           String action, final String target, boolean highlighted) {
        final LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(dp(22), dp(20), dp(22), dp(18));
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(Color.WHITE);
        shape.setCornerRadius(dp(22));
        if (highlighted) {
            shape.setStroke(Math.max(2, (int) dp(1.6f)), 0xFF007AFF);
        } else {
            shape.setStroke(Math.max(1, (int) dp(0.7f)), 0x14000000);
        }
        card.setBackground(shape);
        if (Build.VERSION.SDK_INT >= 21) {
            card.setElevation(dp(10));
        }

        LinearLayout topRow = new LinearLayout(this);
        topRow.setOrientation(LinearLayout.HORIZONTAL);
        topRow.setGravity(Gravity.CENTER_VERTICAL);

        ImageView icon = new ImageView(this);
        int id = getResources().getIdentifier(iconName, "drawable", getPackageName());
        if (id != 0) {
            icon.setImageResource(id);
        }
        topRow.addView(icon, new LinearLayout.LayoutParams(dp(62), dp(62)));

        View grow = new View(this);
        topRow.addView(grow, new LinearLayout.LayoutParams(0, 1, 1f));

        if (highlighted) {
            TextView tag = text("上次使用", 9.5f, ACCENT, Typeface.BOLD);
            GradientDrawable tagBg = new GradientDrawable();
            tagBg.setColor(0xFFEAF2FF);
            tagBg.setCornerRadius(dp(8));
            tag.setBackground(tagBg);
            tag.setPadding(dp(8), dp(4), dp(8), dp(4));
            topRow.addView(tag);
        }
        card.addView(topRow);

        TextView t = text(title, 21f, INK, Typeface.BOLD);
        LinearLayout.LayoutParams tlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        tlp.topMargin = dp(12);
        card.addView(t, tlp);

        TextView d = text(desc, 13f, SUB, Typeface.NORMAL);
        d.setLineSpacing(dp(3), 1f);
        LinearLayout.LayoutParams dlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        dlp.topMargin = dp(5);
        card.addView(d, dlp);

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        TextView a = text(action, 14f, ACCENT, Typeface.BOLD);
        row.addView(a);
        TextView chev = text("›", 18f, ACCENT, Typeface.NORMAL);
        LinearLayout.LayoutParams chlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        chlp.leftMargin = dp(3);
        row.addView(chev, chlp);
        LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        rlp.topMargin = dp(8);
        card.addView(row, rlp);

        card.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                choose(target);
            }
        });
        card.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    v.animate().scaleX(0.975f).scaleY(0.975f).setDuration(90).start();
                } else if (event.getAction() == MotionEvent.ACTION_UP
                        || event.getAction() == MotionEvent.ACTION_CANCEL) {
                    v.animate().scaleX(1f).scaleY(1f).setDuration(140).start();
                }
                return false;
            }
        });
        return card;
    }

    private void choose(String target) {
        SharedPreferences sp = getSharedPreferences(PREFS, MODE_PRIVATE);
        boolean remember = rememberSwitch == null || rememberSwitch.isChecked();
        SharedPreferences.Editor e = sp.edit();
        e.putBoolean(KEY_REMEMBER, remember);
        if (remember) {
            e.putString(KEY_LAST, target);
        } else {
            e.remove(KEY_LAST);
        }
        e.apply();
        launch(target, true);
    }

    private void launch(String target, boolean withAnimation) {
        final Intent intent = new Intent();
        intent.setClassName(this, target);
        intent.addFlags(Intent.FLAG_ACTIVITY_NO_ANIMATION);
        if (!withAnimation) {
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    startActivity(intent);
                    overridePendingTransition(0, 0);
                    finish();
                }
            }, 120);
            return;
        }
        if (content != null) {
            content.animate().alpha(0f).translationY(-dp(10)).setDuration(180).start();
        }
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                try {
                    startActivity(intent);
                    overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
                } catch (Throwable t) {
                    android.util.Log.e("DualEntry", "launch failed", t);
                }
                finish();
            }
        }, 160);
    }

    private void animateIn() {
        content.setAlpha(0f);
        content.setTranslationY(dp(18));
        content.animate().alpha(1f).translationY(0f).setDuration(380)
                .setInterpolator(new android.view.animation.DecelerateInterpolator(2f)).start();
    }

    // ---------------------------------------------------------------- helpers

    private TextView text(String s, float sp, int color, int style) {
        TextView t = new TextView(this);
        t.setText(s);
        t.setTextSize(TypedValue.COMPLEX_UNIT_SP, sp);
        t.setTextColor(color);
        t.setTypeface(Typeface.create(style == Typeface.BOLD ? "sans-serif-medium" : "sans-serif", style));
        t.setIncludeFontPadding(false);
        return t;
    }

    private int dp(float v) {
        return (int) (v * density + 0.5f);
    }

    /** Soft colour blob used to fake an iOS style blurred gradient background. */
    private static class Blob extends View {
        private final int color;
        private final float cx, cy, r;
        Blob(Context c, int color, float cx, float cy, float r) {
            super(c);
            this.color = color;
            this.cx = cx;
            this.cy = cy;
            this.r = r;
        }

        @Override
        protected void onDraw(Canvas canvas) {
            float radius = Math.min(getWidth(), getHeight()) * r;
            RadialGradient g = new RadialGradient(getWidth() * cx, getHeight() * cy, radius,
                    new int[]{color, 0x00FFFFFF}, new float[]{0f, 1f}, Shader.TileMode.CLAMP);
            Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
            p.setShader(g);
            canvas.drawRect(0, 0, getWidth(), getHeight(), p);
        }
    }
}
