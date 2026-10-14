import json

d = json.load(open(r"/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_structure_quine_lutter.json", encoding="utf-8"))

print("-- comparacion con Walbolge --")
print("jumps (op 4 = i):", "{:,}".format(d["jumps"]["total"]), "(Walbolge i: 23.9M)")
print("DLOAD (op 40 = j):", "{:,}".format(d["opcodes_total"]["40"]), "(Walbolge j: 6.6M)")
print("saltos totales:", "{:,}".format(d["jumps"]["total"] + d["opcodes_total"]["40"]))
print("nunca ejecutadas:", d["never_executed_cells"], "(Walbolge: 31,741)")
print("output:", d["run"]["output_len"], "steps:", d["run"]["steps"])

print()
print("-- anatomia del quine --")
regs = d["regions"]
total = d["run"]["steps"]
for reg, info in regs.items():
    print(reg, "pasos:", "{:,}".format(info["steps"]), "({:.2f}%)".format(100.0 * info["steps"] / total))

print()
print("-- opcodes validos totales --")
ops = d["opcodes_total"]
total_ops = sum(ops.values())
valid_names = {4: "JMP", 5: "OUT", 23: "IN", 39: "ROT", 40: "DLOAD", 62: "CRAZY", 68: "NOP", 81: "END"}
for op, n in sorted(ops.items()):
    name = valid_names.get(int(op), "ILLEGAL")
    print("{:8s} (op {:3s}): {:12,} ({:5.2f}%)".format(name, op, n, 100.0 * n / total_ops))
