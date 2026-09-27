"""Bench patch for Part 3 (#16368) on a main that requires #[warehouse(...)] on every
WarehouseSpecificNodeConfig field (the per-resource-type applicability table): each field without
one gets #[warehouse(valid(all_nodes))], so the Athena keys are accepted on every node type.
Usage: warehouse_all_nodes.py <common.rs>. A no-op when main has no such attribute."""
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
lines = path.read_text().split("\n")
start = next(i for i, line in enumerate(lines) if line.startswith("pub struct WarehouseSpecificNodeConfig"))
if not any("#[warehouse" in line for line in lines[max(0, start - 12):start]):
    sys.exit(0)
out, pending = lines[: start + 1], []
i = start + 1
while not lines[i].startswith("}"):
    line, stripped = lines[i], lines[i].strip()
    if not stripped or stripped.startswith(("#[", "//")):
        pending.append(line)
    else:
        if stripped.startswith("pub ") and not any("#[warehouse" in p for p in pending):
            pending.append("    #[warehouse(valid(all_nodes))]")
        out += pending + [line]
        pending = []
    i += 1
path.write_text("\n".join(out + pending + lines[i:]))
