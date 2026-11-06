package com.baidu.carlifevehicle;

import android.app.Application;
import android.content.Context;

import com.shilapi.xcertplay.FreeAutoApplication;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;

/**
 * Unified application object.
 *
 * <p>CarUp's original {@code FreeAutoApplication} owns the CarPlay stack, the native libraries,
 * the multi-dex bootstrap and the update/wipe logic, so the merged app keeps it as the base class.
 * CarLife's {@code CarLifeApplication} only stores a global context and initialises two singletons,
 * so we replay exactly that work here (a second real Application instance would never be attached
 * to the process by the framework).</p>
 */
public class DualApplication extends FreeAutoApplication {

    private Application carlifeApp;

    @Override
    public void onCreate() {
        super.onCreate();
        if (!initCarLifeByInstance()) {
            initCarLifeDirect();
        }
        // 把 CarLife 的车机 MCU 方控广播接进 CarUp 的方控链路
        try {
            com.shilapi.xcertplay.CarLifeMcuKeys.install(this);
        } catch (Throwable t) {
            android.util.Log.w("DualApplication", "wheel bridge install failed: " + t);
        }
    }

    /** Preferred path: run CarLifeApplication's own lifecycle on a private instance. */
    private boolean initCarLifeByInstance() {
        try {
            Class<?> cls = Class.forName("com.baidu.carlifevehicle.CarLifeApplication");
            Constructor<?> ctor = cls.getDeclaredConstructor();
            ctor.setAccessible(true);
            Application app = (Application) ctor.newInstance();
            Method attach = Application.class.getDeclaredMethod("attachBaseContext", Context.class);
            attach.setAccessible(true);
            attach.invoke(app, getBaseContext());
            Method onCreate = cls.getMethod("onCreate");
            onCreate.invoke(app);
            carlifeApp = app;
            return true;
        } catch (Throwable t) {
            android.util.Log.w("DualApplication", "carlife app instance path failed: " + t);
            return false;
        }
    }

    /** Fallback: set the global context field and run the two singleton initialisers directly. */
    private void initCarLifeDirect() {
        try {
            Field f = Class.forName("com.baidu.carlifevehicle.CarLifeApplication")
                    .getDeclaredField("mGlobalContext");
            f.setAccessible(true);
            f.set(null, this);
        } catch (Throwable t) {
            android.util.Log.e("DualApplication", "cannot set carlife global context", t);
        }
        initSingleton("com.baidu.carlifevehicle.util.CarlifeConfUtil");
        initSingleton("com.baidu.carlifevehicle.util.PhoneUtil");
    }

    private void initSingleton(String className) {
        try {
            Class<?> cls = Class.forName(className);
            Object instance = cls.getMethod("getInstance").invoke(null);
            cls.getMethod("init").invoke(instance);
        } catch (Throwable t) {
            android.util.Log.e("DualApplication", "init failed: " + className, t);
        }
    }

    public Application getCarlifeApplication() {
        return carlifeApp;
    }
}
