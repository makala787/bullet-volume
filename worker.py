import json
import FreeCAD
import Part
print("FREECAD_OK")
job = json.load(open("/output/inbox/job.json"))
doc = FreeCAD.openDocument("/templates/" + job["template"])
doc.recompute()
sheet = doc.getObject("Spreadsheet")
obj = doc.getObject("Body")
s = obj.Shape
print("BODY_VOL_MM3", float(s.Volume))
g1 = float(sheet.getContents("G1_1"))
l3 = float(sheet.getContents("L3_1"))
print("G1_1", g1)
print("L3_1", l3)
r = g1 / 2.0
bb = s.BoundBox
start = FreeCAD.Vector(bb.XMin, (bb.YMin+bb.YMax)/2.0, (bb.ZMin+bb.ZMax)/2.0)
axis = FreeCAD.Vector(1, 0, 0)
cyl = Part.makeCylinder(r, l3, start, axis)
print("CYL_VOL_MM3", float(cyl.Volume))
try:
    cut = s.cut(cyl)
    print("CUT_VOL_MM3", float(cut.Volume))
    print("INSIDE_MM3", float(s.Volume) - float(cut.Volume))
except Exception as e:
    print("CUT_ERR", str(e))
out = {"body_mm3": float(s.Volume), "g1": g1, "l3": l3, "cyl_mm3": float(cyl.Volume)}
json.dump(out, open("/output/" + job.get("out_prefix","out") + ".inside.json", "w"), indent=2)
print("INSIDE_WRITTEN")
