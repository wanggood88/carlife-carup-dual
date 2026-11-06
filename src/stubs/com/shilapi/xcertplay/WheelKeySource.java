package com.shilapi.xcertplay;
public enum WheelKeySource {
    WINDOW("window"),
    MEDIA_SESSION("media-session"),
    MEDIA_BUTTON_RECEIVER("media-button-receiver"),
    VOLUME("volume"),
    BROADCAST("broadcast"),
    CARLIFE("carlife-mcu");
    private final String label;
    WheelKeySource(String label) { this.label = label; }
    public String getLabel() { return label; }
}
