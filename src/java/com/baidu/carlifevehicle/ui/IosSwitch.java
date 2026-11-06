package com.baidu.carlifevehicle.ui;

import android.animation.ValueAnimator;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.os.Build;
import android.util.AttributeSet;
import android.view.View;
import android.view.animation.DecelerateInterpolator;

/** Minimal iOS style UISwitch drawn with the canvas API. */
public class IosSwitch extends View {

    public interface OnCheckedChangeListener {
        void onCheckedChanged(IosSwitch view, boolean checked);
    }

    private final Paint trackPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint knobPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint shadowPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final RectF rect = new RectF();

    private boolean checked = true;
    private float progress = 1f;
    private ValueAnimator animator;
    private OnCheckedChangeListener listener;

    public IosSwitch(Context context) {
        super(context);
        init();
    }

    public IosSwitch(Context context, AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        trackPaint.setStyle(Paint.Style.FILL);
        knobPaint.setStyle(Paint.Style.FILL);
        knobPaint.setColor(Color.WHITE);
        knobPaint.setShadowLayer(getResources().getDisplayMetrics().density * 2f, 0f,
                getResources().getDisplayMetrics().density * 1f, 0x33000000);
        shadowPaint.setStyle(Paint.Style.FILL);
        shadowPaint.setColor(0x14000000);
        if (Build.VERSION.SDK_INT >= 11) {
            setLayerType(LAYER_TYPE_SOFTWARE, null);
        }
        setClickable(true);
    }

    public void setOnCheckedChangeListener(OnCheckedChangeListener l) {
        listener = l;
    }

    public boolean isChecked() {
        return checked;
    }

    public void setChecked(boolean value) {
        if (checked == value) {
            return;
        }
        checked = value;
        animateTo(value ? 1f : 0f);
        if (listener != null) {
            listener.onCheckedChanged(this, checked);
        }
    }

    public void setCheckedSilently(boolean value) {
        checked = value;
        progress = value ? 1f : 0f;
        invalidate();
    }

    private void animateTo(float target) {
        if (animator != null) {
            animator.cancel();
        }
        animator = ValueAnimator.ofFloat(progress, target);
        animator.setDuration(220);
        animator.setInterpolator(new DecelerateInterpolator(2f));
        animator.addUpdateListener(new ValueAnimator.AnimatorUpdateListener() {
            @Override
            public void onAnimationUpdate(ValueAnimator animation) {
                progress = (Float) animation.getAnimatedValue();
                invalidate();
            }
        });
        animator.start();
    }

    @Override
    public boolean performClick() {
        setChecked(!checked);
        return true;
    }

    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int w = (int) (getResources().getDisplayMetrics().density * 51f);
        int h = (int) (getResources().getDisplayMetrics().density * 31f);
        setMeasuredDimension(resolveSize(w, widthMeasureSpec), resolveSize(h, heightMeasureSpec));
    }

    @Override
    protected void onDraw(Canvas canvas) {
        float w = getWidth();
        float h = getHeight();
        float r = h / 2f;
        // off colour -> on colour interpolation (iOS system green)
        int off = 0xFFE9E9EB;
        int on = 0xFF34C759;
        int color = blend(off, on, progress);
        trackPaint.setColor(color);
        rect.set(0, 0, w, h);
        canvas.drawRoundRect(rect, r, r, trackPaint);

        float d = h - dp(4);
        float travel = w - d - dp(4);
        float left = dp(2) + travel * progress;
        shadowPaint.setAlpha((int) (18 * progress));
        if (Build.VERSION.SDK_INT < 11) {
            canvas.drawCircle(left + d / 2f, h / 2f + dp(1.5f), d / 2f, shadowPaint);
        }
        canvas.drawCircle(left + d / 2f, h / 2f, d / 2f, knobPaint);
    }

    private int blend(int from, int to, float t) {
        int a = (int) (Color.alpha(from) + (Color.alpha(to) - Color.alpha(from)) * t);
        int r = (int) (Color.red(from) + (Color.red(to) - Color.red(from)) * t);
        int g = (int) (Color.green(from) + (Color.green(to) - Color.green(from)) * t);
        int b = (int) (Color.blue(from) + (Color.blue(to) - Color.blue(from)) * t);
        return Color.argb(a, r, g, b);
    }

    private float dp(float v) {
        return v * getResources().getDisplayMetrics().density;
    }
}
