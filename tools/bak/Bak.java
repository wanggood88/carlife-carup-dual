import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.dexbacked.DexBackedDexFile;
import com.android.tools.smali.baksmali.Baksmali;
import com.android.tools.smali.baksmali.BaksmaliOptions;
import java.io.*;

public class Bak {
    public static void main(String[] a) throws Exception {
        DexBackedDexFile dex = DexBackedDexFile.fromInputStream(Opcodes.getDefault(),
                new BufferedInputStream(new FileInputStream(a[0])));
        BaksmaliOptions o = new BaksmaliOptions();
        o.apiLevel = 16;
        Baksmali.disassembleDexFile(dex, new File(a[1]), 4, o);
        System.out.println("ok -> " + a[1]);
    }
}
