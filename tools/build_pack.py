"""Build the asset stash folders from the pinned npm packages in tools/package.json.

Usage: python3 -I build_pack.py <node_modules dir> <output dir> <hero names json>
"""
import json
import re
import shutil
import sys
from pathlib import Path

NM = Path(sys.argv[1])
PACK = Path(sys.argv[2])
HERO_NAMES = Path(sys.argv[3])
SFX = NM / "uisfx"

M = {"icons": [], "emoji": [], "brands": [], "flags": [], "fonts": [],
     "sounds": [], "backgrounds": [], "retro": []}


def ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def copy_tree(src: Path, dst: Path, skip_suffix=(".map", ".ejs", ".sketch")):
    for f in src.rglob("*"):
        if f.is_file() and f.suffix not in skip_suffix:
            t = dst / f.relative_to(src)
            ensure(t.parent)
            shutil.copy2(f, t)


# ---------------------------------------------------------------- iconify sets
def export_iconify(prefix, outdir, keep=None):
    pkg = NM / "@iconify-json" / prefix
    d = json.loads((pkg / "icons.json").read_text(encoding="utf-8"))
    info = json.loads((pkg / "info.json").read_text(encoding="utf-8"))
    W, H = d.get("width", 16), d.get("height", 16)
    out = ensure(PACK / outdir)
    names = []
    for name, ic in d["icons"].items():
        if keep and not keep(name):
            continue
        w, h = ic.get("width", W), ic.get("height", H)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
               f'width="1em" height="1em">{ic["body"]}</svg>\n')
        (out / f"{name}.svg").write_text(svg, encoding="utf-8")
        names.append(name)
    lic = pkg / "LICENSE"
    if lic.exists():
        shutil.copy2(lic, out / "LICENSE.txt")
    (out / "SOURCE-AND-LICENSE.txt").write_text(
        f"{info['name']}\n"
        f"Author: {info['author']['name']} ({info['author'].get('url', '')})\n"
        f"License: {info['license']['title']} ({info['license'].get('url', '')})\n"
        f"Converted from the @iconify-json/{prefix} npm package.\n",
        encoding="utf-8")
    return names, info


def colorable(prefix):
    return prefix not in ("fluent-emoji-flat",)


ICONSETS = [
    # prefix, folder, group, title, keep-filter, note
    ("game-icons", "icons/game-icons", "icons", "Game Icons (rank, huy hiệu, RPG)", None,
     "Đơn sắc, đổi màu bằng CSS. CẦN ghi nguồn (CC BY 3.0)."),
    ("pixelarticons", "icons/pixelarticons", "icons", "Pixelarticons (pixel 24px)", None,
     "Đơn sắc, pixel art."),
    ("pixel", "icons/pixel-icon-library", "icons", "Pixel Icon Library (HackerNoon)", None,
     "Đơn sắc, pixel art. CẦN ghi nguồn (CC BY 4.0)."),
    ("tabler", "icons/tabler", "icons", "Tabler Icons (UI chung, outline + filled)", None,
     "Nét 2px, đổi màu bằng CSS."),
    ("ph", "icons/phosphor", "icons", "Phosphor (regular, bold, fill)",
     lambda n: not (n.endswith("-thin") or n.endswith("-light") or n.endswith("-duotone")),
     "Đã bỏ biến thể thin/light/duotone cho gọn."),
    ("fluent-emoji-flat", "emoji/fluent-flat", "emoji", "Fluent Emoji Flat (Microsoft)", None,
     "Emoji màu, kèm các biến thể màu da."),
]

for prefix, folder, group, title, keep, note in ICONSETS:
    names, info = export_iconify(prefix, folder, keep)
    M[group].append({
        "id": folder.split("/")[-1], "title": title, "dir": folder, "note": note,
        "license": info["license"]["title"],
        "attribution": info["license"]["spdx"].startswith("CC-BY"),
        "author": info["author"]["name"], "source": info["author"].get("url", ""),
        "mono": colorable(prefix), "names": sorted(names),
    })
    print(f"{folder}: {len(names)}")

# ---------------------------------------------------------------- simple-icons
si = NM / "simple-icons"
si_out = ensure(PACK / "icons" / "brands")
names = []
for f in sorted((si / "icons").glob("*.svg")):
    shutil.copy2(f, si_out / f.name)
    names.append(f.stem)
shutil.copy2(si / "LICENSE.md", si_out / "LICENSE.md")
shutil.copy2(si / "DISCLAIMER.md", si_out / "DISCLAIMER.md")
M["brands"].append({
    "id": "brands", "title": "Simple Icons (logo thương hiệu: Discord, GitHub, TikTok...)",
    "dir": "icons/brands", "license": "CC0-1.0", "attribution": False,
    "note": "Logo là nhãn hiệu của chủ sở hữu, đọc DISCLAIMER.md. Mặc định màu đen.",
    "author": "Simple Icons contributors", "source": "https://simpleicons.org",
    "mono": True, "names": names})
print("brands:", len(names))

# ---------------------------------------------------------------- flags
fi = NM / "flag-icons"
fl_out = ensure(PACK / "flags")
shutil.copytree(fi / "flags", fl_out / "flags", dirs_exist_ok=True)
ensure(fl_out / "css")
shutil.copy2(fi / "css" / "flag-icons.css", fl_out / "css" / "flag-icons.css")
shutil.copy2(fi / "css" / "flag-icons.min.css", fl_out / "css" / "flag-icons.min.css")
shutil.copy2(fi / "LICENSE", fl_out / "LICENSE.txt")
shutil.copy2(fi / "country.json", fl_out / "country.json")
codes = sorted(p.stem for p in (fi / "flags" / "4x3").glob("*.svg"))
M["flags"].append({
    "id": "flags", "title": "Cờ quốc gia (flag-icons)", "dir": "flags/flags/4x3",
    "dir_square": "flags/flags/1x1", "license": "MIT", "attribution": False,
    "note": "Tỉ lệ 4:3 và vuông 1:1. Có sẵn css: <span class=\"fi fi-vn\"></span>.",
    "author": "Panayiotis Lipiridis", "source": "https://github.com/lipis/flag-icons",
    "names": codes})
print("flags:", len(codes))

# ---------------------------------------------------------------- fonts
SUBSETS = ("latin-ext", "latin", "vietnamese")
BLOCK = re.compile(r"/\*[^*]*\*/\s*(@font-face\s*\{.*?\})", re.S)


def subset_of(fn: str):
    if "-latin-ext-" in fn:
        return "latin-ext"
    if "-latin-" in fn:
        return "latin"
    if "-vietnamese-" in fn:
        return "vietnamese"
    return None


def build_font(pkg_name, folder, label, kind, note):
    pdir = NM / pkg_name
    out = ensure(PACK / "fonts" / folder)
    files_out = ensure(out / "files")
    if kind == "variable":
        css_files = [pdir / "index.css"]
    else:
        ws = sorted(int(p.stem) for p in pdir.glob("*.css") if p.stem.isdigit())
        ws = [w for w in ws if w in (300, 400, 500, 600, 700, 800)] or ws[:1]
        css_files = [pdir / f"{w}.css" for w in ws]
    blocks, family, subsets_seen, weights = [], None, set(), set()
    for cf in css_files:
        for blk in BLOCK.findall(cf.read_text(encoding="utf-8")):
            m = re.search(r"url\(\./files/([^)]+?\.woff2)\)", blk)
            if not m:
                continue
            fn = m.group(1)
            sub = subset_of(fn)
            if sub is None or "italic" in fn:
                continue
            blk = re.sub(
                r"src:\s*url\((\./files/[^)]+\.woff2)\)\s*format\('woff2'\)\s*,\s*url\([^)]+\.woff\)\s*format\('woff'\);",
                r"src: url(\1) format('woff2');", blk)
            shutil.copy2(pdir / "files" / fn, files_out / fn)
            family = re.search(r"font-family:\s*'([^']+)'", blk).group(1)
            wt = re.search(r"font-weight:\s*([^;]+);", blk).group(1).strip()
            subsets_seen.add(sub)
            weights.add(wt)
            blocks.append(f"/* {sub} {wt} */\n{blk}\n")
    header = (f"/* {label} ({family}) - subsets: {', '.join(sorted(subsets_seen))}\n"
              f"   Dùng: @import url('fonts/{folder}/fonts.css'); font-family: '{family}', sans-serif; */\n\n")
    (out / "fonts.css").write_text(header + "\n".join(blocks), encoding="utf-8")
    shutil.copy2(pdir / "LICENSE", out / "LICENSE.txt")
    has_vi = "vietnamese" in subsets_seen
    wts = sorted(weights, key=lambda x: int(re.match(r"\d+", x).group(0)))
    M["fonts"].append({
        "id": folder, "title": label, "family": family, "css": f"fonts/{folder}/fonts.css",
        "weights": wts, "vietnamese": has_vi, "variable": kind == "variable",
        "license": "OFL-1.1", "note": note})
    print(f"font {folder}: family={family} vi={has_vi} weights={wts} files={len(list(files_out.iterdir()))}")


FONTS = [
    ("@fontsource/be-vietnam-pro", "be-vietnam-pro", "Be Vietnam Pro", "static", "Font thiết kế cho tiếng Việt, rất hợp UI."),
    ("@fontsource-variable/nunito", "nunito", "Nunito", "variable", "Bo tròn, thay SF Pro Rounded."),
    ("@fontsource-variable/quicksand", "quicksand", "Quicksand", "variable", "Bo tròn, hình học, nhẹ."),
    ("@fontsource-variable/baloo-2", "baloo-2", "Baloo 2", "variable", "Bo tròn, dày, vui."),
    ("@fontsource-variable/lexend", "lexend", "Lexend", "variable", "Dễ đọc, hiện đại."),
    ("@fontsource-variable/bricolage-grotesque", "bricolage-grotesque", "Bricolage Grotesque", "variable", "Tiêu đề có cá tính."),
    ("@fontsource-variable/plus-jakarta-sans", "plus-jakarta-sans", "Plus Jakarta Sans", "variable", "Font của trang Thay Ảnh."),
    ("@fontsource-variable/space-grotesk", "space-grotesk", "Space Grotesk", "variable", "Tiêu đề kiểu tech."),
    ("@fontsource-variable/inter", "inter", "Inter", "variable", "Chữ thân bài đa dụng."),
    ("@fontsource-variable/jetbrains-mono", "jetbrains-mono", "JetBrains Mono", "variable", "Monospace cho code."),
    ("@fontsource/vt323", "vt323", "VT323", "static", "Terminal retro, có dấu tiếng Việt."),
    ("@fontsource/pixelify-sans", "pixelify-sans", "Pixelify Sans", "static", "Pixel. KHÔNG có dấu tiếng Việt."),
    ("@fontsource/press-start-2p", "press-start-2p", "Press Start 2P", "static", "Pixel 8-bit. KHÔNG có dấu tiếng Việt."),
    ("@fontsource/silkscreen", "silkscreen", "Silkscreen", "static", "Pixel nhỏ. KHÔNG có dấu tiếng Việt."),
]
for args in FONTS:
    build_font(*args)

# ---------------------------------------------------------------- retro css
retro = ensure(PACK / "css-retro")
for pkg, folder, title, demo, note in [
    ("98.css", "98.css", "98.css (Windows 98)", "dist/index.html", "Link: dist/98.css"),
    ("xp.css", "xp.css", "XP.css (Windows XP, kèm theme 98)", "dist/index.html", "Link: dist/XP.css"),
    ("7.css", "7.css", "7.css (Windows 7)", None, "Link: dist/7.css"),
    ("nes.css", "nes.css", "NES.css (8-bit Nintendo)", None, "Link: css/nes.min.css (dùng với font Press Start 2P)"),
]:
    src, dst = NM / pkg, ensure(retro / folder)
    if pkg == "nes.css":
        copy_tree(src / "css", dst / "css")
        copy_tree(src / "assets", dst / "assets")
    else:
        copy_tree(src / "dist", dst / "dist")
    shutil.copy2(src / "LICENSE", dst / "LICENSE.txt")
    M["retro"].append({"id": folder, "title": title, "dir": f"css-retro/{folder}",
                       "demo": f"css-retro/{folder}/{demo}" if demo else None,
                       "license": "MIT", "note": note})

# ---------------------------------------------------------------- sounds
snd_root = ensure(PACK / "sounds" / "ui-sfx")
packs = {}
for pdir in sorted((SFX / "sounds").iterdir()):
    if not pdir.is_dir():
        continue
    dst = ensure(snd_root / pdir.name)
    cues = []
    for f in sorted(pdir.glob("*.mp3")):
        shutil.copy2(f, dst / f.name)
        cues.append(f.stem)
    packs[pdir.name] = cues
shutil.copy2(SFX / "LICENSE-AUDIO", snd_root / "LICENSE-AUDIO.txt")
M["sounds"].append({"id": "ui-sfx", "title": "UI SFX (click, success, error, hover... 12 phong cách)",
                    "dir": "sounds/ui-sfx", "license": "CC0-1.0", "attribution": False,
                    "note": "Âm thanh giao diện, không phải nhạc nền. Tác giả: Romain Simon (uisfx).",
                    "packs": packs})
print("sounds:", {k: len(v) for k, v in packs.items()})

# ---------------------------------------------------------------- backgrounds
names = json.loads(HERO_NAMES.read_text())
M["backgrounds"].append({"id": "hero-patterns", "title": "Hero Patterns (nền SVG lặp)",
                         "dir": "backgrounds/hero-patterns", "license": "CC BY 4.0", "attribution": True,
                         "note": "Tác giả Steve Schoger. Màu mặc định #9C92AC, opacity .4, sửa trực tiếp trong file SVG.",
                         "names": sorted(names)})

(PACK / "manifest.js").write_text(
    "window.STASH = " + json.dumps(M, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print("manifest written")
