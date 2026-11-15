"""Kiem tra nhanh SemanticRT: so anh, split, kich thuoc, lop, nguon (LLVIP/OSU/INO), trung lap giua split.
Chay: python -I kiem_semanticrt.py <thu_muc_SemanticRT_dataset>
"""
import sys, os, re, json, collections
import numpy as np
from PIL import Image

goc = sys.argv[1]
out = {}
print("Thu muc:", sorted(os.listdir(goc)))

# 1. split
splits = {}
for f in sorted(os.listdir(goc)):
    if f.endswith('.txt'):
        dong = [l.strip() for l in open(os.path.join(goc, f), encoding='utf-8', errors='ignore') if l.strip()]
        splits[f[:-4]] = dong
        print(f"{f}: {len(dong)} dong, vi du: {dong[:3]}, trung trong file: {len(dong)-len(set(dong))}")
out['split'] = {k: len(v) for k, v in splits.items()}

# 2. thu muc anh
thu_muc = {}
for d in ['rgb', 'thermal', 'labels']:
    p = os.path.join(goc, d)
    if os.path.isdir(p):
        ds = sorted(os.listdir(p))
        thu_muc[d] = ds
        ext = collections.Counter(os.path.splitext(x)[1] for x in ds)
        print(f"{d}: {len(ds)} file, duoi: {dict(ext)}, vi du: {ds[:3]} ... {ds[-3:]}")
out['so_file'] = {k: len(v) for k, v in thu_muc.items()}

ten = lambda x: os.path.splitext(x)[0]
if thu_muc:
    bo = [set(map(ten, v)) for v in thu_muc.values()]
    print("Cap du ca 3:", len(set.intersection(*bo)), "| hop:", len(set.union(*bo)))

# 3. giao giua split
for a in ['train', 'val', 'test']:
    for b in ['train', 'val', 'test']:
        if a < b and a in splits and b in splits:
            g = set(splits[a]) & set(splits[b])
            print(f"Giao {a}-{b}: {len(g)}")
for k in splits:
    if k.startswith('test_') and 'test' in splits:
        print(f"{k} nam trong test: {len(set(splits[k]) & set(splits['test']))}/{len(splits[k])}")

# 4. nguon: doan theo tien to ten file
tien_to = collections.Counter(re.sub(r'\d+', '#', ten(x)) for x in thu_muc.get('rgb', []))
print("Mau ten file:", tien_to.most_common(15))
for k in ['train', 'val', 'test']:
    if k in splits:
        print(k, "mau ten:", collections.Counter(re.sub(r'\d+', '#', s) for s in splits[k]).most_common(8))

# 5. kich thuoc, kenh, lop (mau 400 anh rai deu)
import random
random.seed(0)
ds = thu_muc.get('rgb', [])
mau = ds[::max(1, len(ds)//400)]
kt = collections.Counter(); kenh = collections.Counter(); ir_giong = 0; n_ir = 0
for x in mau:
    im = Image.open(os.path.join(goc, 'rgb', x)); kt[('rgb', im.size, im.mode)] += 1
    tf = [t for t in thu_muc.get('thermal', []) if ten(t) == ten(x)]
    if tf:
        it = Image.open(os.path.join(goc, 'thermal', tf[0])); kt[('thermal', it.size, it.mode)] += 1
        a = np.asarray(it)
        if a.ndim == 3:
            n_ir += 1; ir_giong += int((a[..., 0] == a[..., 1]).all() and (a[..., 1] == a[..., 2]).all())
print("Kich thuoc/mode:", kt.most_common(10))
print(f"IR 3 kenh giong nhau: {ir_giong}/{n_ir}")

dem_px = collections.Counter(); dem_anh = {k: collections.Counter() for k in ['train', 'val', 'test']}
nhan_ds = thu_muc.get('labels', [])
nhan_theo_ten = {ten(x): x for x in nhan_ds}
lab_mode = collections.Counter()
for k in ['train', 'val', 'test']:
    for s in splits.get(k, []):
        n = nhan_theo_ten.get(ten(os.path.basename(s)))
        if not n:
            continue
        L = Image.open(os.path.join(goc, 'labels', n)); lab_mode[(L.mode, L.size)] += 1
        a = np.asarray(L)
        if a.ndim == 3:
            a = a[..., 0]
        v, c = np.unique(a, return_counts=True)
        for vi, ci in zip(v.tolist(), c.tolist()):
            dem_px[vi] += ci; dem_anh[k][vi] += 1
print("Nhan mode/size:", lab_mode.most_common(5))
tong = sum(dem_px.values())
print("Gia tri nhan | %pixel | so anh train/val/test")
for v in sorted(dem_px):
    print(f"  {v:3d} | {100*dem_px[v]/tong:6.2f}% | {dem_anh['train'][v]}/{dem_anh['val'][v]}/{dem_anh['test'][v]}")
out['lop'] = {str(v): {'pct': round(100*dem_px[v]/tong, 3), **{k: dem_anh[k][v] for k in dem_anh}} for v in sorted(dem_px)}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'semanticrt_tom_tat.json'), 'w'), indent=1)
