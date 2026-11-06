#!/usr/bin/env python3
"""Merge CarUp (com.carup.car) into CarLife (com.baidu.carlifevehicle) apktool project."""
import os, re, shutil, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("SRC_DIR") or os.path.join(ROOT, "work")
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")

BASE = SRC
SRC_CL = os.path.join(BASE, "dec_carlife")
SRC_CU = os.path.join(BASE, "dec_carup")
OUT = OUT_DIR
ENTRY_OFFSET = 0x400          # CarUp entries live above CarLife's (max 167)
FREE_TYPE_IDS = [13, 15, 16, 17, 18, 19, 20]

res_re = re.compile(r'<public type="([^"]+)" name="([^"]+)" id="0x([0-9a-fA-F]+)"')


def parse_public(path):
    out = []
    for m in re.finditer(res_re, open(path, encoding="utf-8").read()):
        out.append((m.group(1), m.group(2), int(m.group(3), 16)))
    return out


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC_CL, OUT, ignore=shutil.ignore_patterns("build", "dist", "original"))

    cl_pub = parse_public(os.path.join(SRC_CL, "res/values/public.xml"))
    cu_pub = parse_public(os.path.join(SRC_CU, "res/values/public.xml"))

    cl_type_by_name = {}
    for t, n, i in cl_pub:
        cl_type_by_name.setdefault(t, i >> 16)

    idmap = {}
    new_entries = []
    used_names = {(t, n) for t, n, _ in cl_pub}
    used_ids = {i for _, _, i in cl_pub}
    free_types = list(FREE_TYPE_IDS)
    type_of_new = {}

    for t, n, i in cu_pub:
        entry = i & 0xFFFF
        if t in cl_type_by_name:
            nt = cl_type_by_name[t]
        else:
            if t not in type_of_new:
                type_of_new[t] = free_types.pop(0)
            nt = type_of_new[t]
        nn = n
        if (t, n) in used_names:
            nn = "cu_" + n
        nid = (0x7F << 24) | (nt << 16) | (entry + ENTRY_OFFSET)
        assert nid not in used_ids, hex(nid)
        used_ids.add(nid)
        used_names.add((t, nn))
        idmap[i] = nid
        new_entries.append((t, nn, nid))

    # ---- merged public.xml
    lines = ['<?xml version="1.0" encoding="utf-8"?>', '<resources>']
    for t, n, i in cl_pub:
        lines.append('    <public type="%s" name="%s" id="0x%08x" />' % (t, n, i))
    for t, n, i in new_entries:
        lines.append('    <public type="%s" name="%s" id="0x%08x" />' % (t, n, i))
    lines.append('</resources>')
    open(os.path.join(OUT, "res/values/public.xml"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # ---- copy CarUp resources
    renames = {}   # (type,name) -> new name
    for t, n, i in cu_pub:
        if (t, n) in {(x, y) for x, y, _ in cl_pub}:
            renames[(t, n)] = "cu_" + n

    nmap_by_type = {}
    for t, n, i in cu_pub:
        nmap_by_type.setdefault(t, {})[n] = renames.get((t, n), n)

    for dirpath, _, files in os.walk(os.path.join(SRC_CU, "res")):
        rel = os.path.relpath(dirpath, os.path.join(SRC_CU, "res"))
        for f in files:
            src = os.path.join(dirpath, f)
            dst_dir = os.path.join(OUT, "res", rel) if rel != "." else os.path.join(OUT, "res")
            os.makedirs(dst_dir, exist_ok=True)
            if rel.split("-")[0] == "values":
                if f == "public.xml":
                    continue
                dst = os.path.join(dst_dir, "carup_" + f)
                txt = open(src, encoding="utf-8").read()
                # rename colliding value resources
                for (t, n), nn in renames.items():
                    if t == "string":
                        txt = re.sub(r'(<string name=")%s(")' % re.escape(n), r"\g<1>%s\g<2>" % nn, txt)
                # fix references to renamed resources inside value files
                for (t, n), nn in renames.items():
                    txt = txt.replace("@%s/%s" % (t, n), "@%s/%s" % (t, nn))
                open(dst, "w", encoding="utf-8").write(txt)
            else:
                shutil.copy2(src, os.path.join(dst_dir, f))

    # ---- copy CarUp smali (dex 2..4) with resource id rewriting
    smali_dirs = sorted([d for d in os.listdir(SRC_CU) if re.match(r"smali(_classes\d+)?$", d)])
    for idx, d in enumerate(smali_dirs, start=2):
        target = os.path.join(OUT, "smali_classes%d" % idx)
        shutil.copytree(os.path.join(SRC_CU, d), target)
        for dp, _, fs in os.walk(target):
            for f in fs:
                if not f.endswith(".smali"):
                    continue
                p = os.path.join(dp, f)
                txt = open(p, encoding="utf-8", errors="surrogateescape").read()
                if "0x7f" not in txt:
                    continue
                def rep(m):
                    v = int(m.group(1), 16)
                    if v in idmap:
                        return "0x%08x" % idmap[v]
                    return m.group(0)
                out_lines = []
                for line in txt.split("\n"):
                    if "0x7f" not in line:
                        out_lines.append(line)
                        continue
                    m2 = re.match(r"^(\s*)const/high16(/jumbo)?\s+(\S+),\s*0x(7f[0-9a-f]{6})\s*$", line)
                    if m2:
                        v = int(m2.group(4), 16)
                        if v in idmap:
                            nv = idmap[v]
                            if nv & 0xFFFF:
                                out_lines.append("%sconst%s %s, 0x%08x" % (m2.group(1), m2.group(2) or "", m2.group(3), nv))
                            else:
                                out_lines.append(line)
                            continue
                    out_lines.append(re.sub(r"0x(7f[0-9a-f]{6})", rep, line))
                new = "\n".join(out_lines)
                if new != txt:
                    open(p, "w", encoding="utf-8", errors="surrogateescape").write(new)

    # ---- native libs / assets / unknown files
    for d in ("lib", "assets"):
        s = os.path.join(SRC_CU, d)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(OUT, d), dirs_exist_ok=True)
    for f in ("kotlin-tooling-metadata.json", "DebugProbesKt.bin", "version.properties",
              "androidsupportmultidexversion.txt"):
        s = os.path.join(SRC_CU, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(OUT, f))

    json.dump({"idmap": {"0x%08x" % k: "0x%08x" % v for k, v in idmap.items()},
               "types": {t: n for t, n in type_of_new.items()}},
              open(os.path.join(ROOT, "build", "idmap.json"), "w"), indent=1)
    print("merged ->", OUT, "resources:", len(cl_pub), "+", len(new_entries))


if __name__ == "__main__":
    main()
