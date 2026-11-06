package com.shilapi.xcertplay;
public final class WheelKeyInput {
    public final int keyCode;
    public final int scanCode;
    public final boolean down;
    public final WheelKeySource source;
    public WheelKeyInput(int keyCode, int scanCode, boolean down, WheelKeySource source) {
        this.keyCode = keyCode;
        this.scanCode = scanCode;
        this.down = down;
        this.source = source;
    }
}
