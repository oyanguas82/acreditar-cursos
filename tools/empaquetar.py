from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"plugins/acreditacion-cursos-unad"
S=P/"skills/acreditacion-unad"
def payload(path):
    if path.suffix in (".md", ".json", ".yaml", ".yml", ".csv", ".py", ".txt", ".svg") or path.name == "LICENSE":
        return path.read_text(encoding="utf-8").encode("utf-8")
    return path.read_bytes()
def build():
    version=json.loads((P/"plugin.json").read_text(encoding="utf-8"))["version"]
    dest=ROOT/"dist"
    dest.mkdir(exist_ok=True)
    files=sorted(p for p in P.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc")
    packages={}
    for platform in ("chatgpt","claude"):
        items={}
        for f in files:
            rel=f.relative_to(P).as_posix()
            if platform=="chatgpt" and rel.startswith(".claude-plugin/"): continue
            if platform=="claude" and (rel=="plugin.json" or rel.startswith(".codex-plugin/")): continue
            items["acreditacion-cursos-unad/"+rel]=payload(f)
        packages[f"acreditacion-cursos-unad-{platform}-{version}.zip"]=items
    items={"acreditacion-unad/"+f.relative_to(S).as_posix():payload(f) for f in files if f.is_relative_to(S)}
    for name in ("LICENSE","THIRD_PARTY_NOTICES.md"): items["acreditacion-unad/"+name]=payload(P/name)
    for extension in ("zip","skill"): packages[f"acreditacion-unad-{version}.{extension}"]=items
    hashes=[]
    for name,items in packages.items():
        path=dest/name
        with zipfile.ZipFile(path,"w") as z:
            for rel,content in sorted(items.items()):
                info=zipfile.ZipInfo(rel,(2026,11,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644<<16
                z.writestr(info,content)
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None and set(z.namelist())==set(items)
            assert all(z.read(k)==v for k,v in items.items())
        hashes.append(hashlib.sha256(path.read_bytes()).hexdigest()+"  "+name)
        print(name,len(items),path.stat().st_size)
    (dest/"SHA256SUMS.txt").write_text("\n".join(hashes)+"\n",encoding="utf-8")
if __name__=="__main__": build()
