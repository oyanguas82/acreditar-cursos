from pathlib import Path
import argparse,ast,hashlib,json,re,zipfile
import xml.etree.ElementTree as ET
import yaml
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"plugins/acreditacion-cursos-unad"
S=P/"skills/acreditacion-unad"
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def validate(archives=False):
    manifest=read(P/"plugin.json")
    assert manifest["$schema"]=="https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert manifest["name"]==P.name
    for rel in (".claude-plugin/plugin.json",".codex-plugin/plugin.json"):
        other=read(P/rel)
        assert (other["name"],other["version"])==(manifest["name"],manifest["version"])
    for rel in (".claude-plugin/marketplace.json",".agents/plugins/marketplace.json"):
        source=read(ROOT/rel)["plugins"][0]["source"]
        if isinstance(source,dict): source=source["path"]
        assert (ROOT/source).resolve()==P
    interface=manifest["extensions"]["com.openai"]["interface"]
    assert len(interface["shortDescription"])<=30
    for key in ("logo","composerIcon"): ET.parse(P/interface[key])
    front=yaml.safe_load((S/"SKILL.md").read_text(encoding="utf-8").split("---",2)[1])
    assert front["name"]==S.name and isinstance(front["description"],str)
    agent=yaml.safe_load((S/"agents/openai.yaml").read_text(encoding="utf-8"))
    assert isinstance(agent["policy"]["allow_implicit_invocation"],bool)
    for f in P.rglob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)",f.read_text(encoding="utf-8")):
            if target.startswith(("https:","http:","#")): continue
            actual=(f.parent/target.strip("<>").split("#")[0]).resolve()
            assert actual.is_relative_to(P) and actual.exists(),(f,target)
    for f in S.rglob("*.py"): ast.parse(f.read_text(encoding="utf-8"))
    catalog=read(S/"assets/catalogo-formatos.json")
    assert len(catalog)==18
    for item in catalog:
        f=S/item["ruta"]
        assert f.stat().st_size==item["bytes"] and hashlib.sha256(f.read_bytes()).hexdigest()==item["sha256"]
        if f.suffix in (".docx",".xlsx",".pptx"):
            with zipfile.ZipFile(f) as z:
                assert z.testzip() is None
                for name in z.namelist():
                    if name.endswith((".xml",".rels")): ET.fromstring(z.read(name))
    if archives:
        checks=(ROOT/"dist/SHA256SUMS.txt").read_text().splitlines()
        assert len(checks)==4
        for line in checks:
            digest,name=line.split("  ")
            f=ROOT/"dist"/name
            assert hashlib.sha256(f.read_bytes()).hexdigest()==digest
            with zipfile.ZipFile(f) as z:
                assert z.testzip() is None
                assert all(".." not in Path(p).parts and not p.startswith("/") and "__pycache__" not in p for p in z.namelist())
                prefix="acreditacion-cursos-unad/skills/acreditacion-unad/" if "-chatgpt-" in name or "-claude-" in name else "acreditacion-unad/"
                for item in catalog: assert hashlib.sha256(z.read(prefix+item["ruta"])).hexdigest()==item["sha256"]
                if "-chatgpt-" in name: assert "acreditacion-cursos-unad/plugin.json" in z.namelist()
                if "-claude-" in name: assert "acreditacion-cursos-unad/.claude-plugin/plugin.json" in z.namelist()
    print("VALIDO: manifiestos, enlaces y 18 formatos"+("; cuatro paquetes" if archives else ""))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archives",action="store_true")
    validate(p.parse_args().archives)
