"""Convert a ComfyUI *UI* workflow (nodes/links) into an API graph for /prompt.

    python ui_to_api.py <workflow.json>            # prints the API json
    python ui_to_api.py <workflow.json> -o out.json

Widget names are resolved through /object_info, so the mapping is not guessed.
"""
import argparse
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8188"


def object_info(cls):
    with urllib.request.urlopen(f"{BASE}/object_info/{cls}") as fh:
        return json.load(fh)[cls]


def widget_names(cls):
    """Ordered list of widget input names for a node class."""
    info = object_info(cls)
    order = info.get("input_order") or {}
    names = []
    for section in ("required", "optional"):
        for name in order.get(section, []):
            spec = info["input"][section][name]
            kind = spec[0] if isinstance(spec, list) else spec
            if isinstance(kind, list):          # combo widget
                names.append(name)
            elif kind in ("INT", "FLOAT", "STRING", "BOOLEAN"):
                names.append(name)
    return names


def convert(workflow):
    cache, api = {}, {}
    for node in workflow["nodes"]:
        cls = node["type"]
        if cls in ("Note", "MarkdownNote", "Reroute", "PrimitiveNode"):
            continue
        if cls not in cache:
            cache[cls] = widget_names(cls)
        inputs = {}
        linked = {}
        for item in node.get("inputs") or []:
            if item.get("link") is not None:
                linked[item["name"]] = item["link"]
        # widgets_values are positional over the class's widget inputs
        for name, value in zip(cache[cls], node.get("widgets_values") or []):
            if name in linked:
                continue
            inputs[name] = value
        api[str(node["id"])] = {"class_type": cls, "inputs": inputs}

    for link in workflow["links"]:
        _lid, origin, origin_slot, target, _tslot, _type = link[:6]
        target_node = next(n for n in workflow["nodes"] if n["id"] == target)
        tname = None
        for item in target_node.get("inputs") or []:
            if item.get("link") == _lid:
                tname = item["name"]
        if tname:
            api[str(target)]["inputs"][tname] = [str(origin), origin_slot]
    return api


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workflow")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()
    wf = json.load(open(args.workflow, encoding="utf-8-sig"))
    api = convert(wf)
    text = json.dumps(api, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(text)
        print("wrote", args.out, len(api), "nodes")
    else:
        print(text)


if __name__ == "__main__":
    main()
