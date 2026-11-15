"""Gop cac cum canh co anh trung binh giong nhau (cung goc may). Doc semanticrt_canh.json.
Chay: python -I gop_cum.py <thu_muc_SemanticRT_dataset>"""
import sys, os, json
import numpy as np
from PIL import Image
goc = sys.argv[1]
z = json.load(open('semanticrt_canh.json')); ten = z['ten']; cid = np.array(z['canh']); sp = np.array(z['split_goc'])
C = cid.max() + 1
# anh trung binh moi cum (xam, 64x52), lay toi da 60 anh, roi dac trung bien
from PIL import ImageFilter
def tb(k):
    ids = np.where(cid == k)[0][:60]
    a = np.mean([np.asarray(Image.open(os.path.join(goc, 'rgb', ten[i] + '.jpg')).convert('L').resize((128, 104)), np.float32) for i in ids], 0)
    gx = np.abs(np.diff(a, axis=1))[:-1]; gy = np.abs(np.diff(a, axis=0))[:, :-1]
    g = np.log1p(np.sqrt(gx**2 + gy**2)).ravel()
    return (g - g.mean()) / g.std(), a
T = [tb(k) for k in range(C)]
F = np.stack([t[0] for t in T])
D = np.sqrt(((F[:, None] - F[None]) ** 2).mean(-1))
np.fill_diagonal(D, np.inf)
print("Cap cum gan nhat:")
for k in range(C):
    j = D[k].argmin(); print(f"  {k:2d} -> {j:2d}  d={D[k, j]:.3f}")
ng = float(os.environ.get('NG', 0.8))
cha = list(range(C))
def tim(x):
    while cha[x] != x: x = cha[x]
    return x
for a in range(C):
    for b in range(C):
        if D[a, b] < ng: cha[tim(a)] = tim(b)
g = np.array([tim(k) for k in range(C)])
u = sorted(set(g), key=lambda x: -sum((cid == k).sum() for k in range(C) if g[k] == x))
moi = {x: i for i, x in enumerate(u)}
cam = np.array([moi[g[k]] for k in cid])
print(f"\nNguong gop {ng}: {len(u)} goc may")
for i in range(len(u)):
    m = cam == i; ks = [k for k in range(C) if moi[g[k]] == i]
    print(f"  may {i:2d}: {m.sum():5d} anh  cum {ks}")
json.dump({'ten': ten, 'split_goc': sp.tolist(), 'canh': cid.tolist(), 'may': cam.tolist(), 'nguong_gop': ng}, open('semanticrt_may.json', 'w'))
cot = 6; hang = (len(u) + cot - 1) // cot
o = Image.new('L', (cot * 213, hang * 170))
for i in range(len(u)):
    ks = [k for k in range(C) if moi[g[k]] == i]
    o.paste(Image.fromarray(T[ks[0]][1].astype(np.uint8)).resize((213, 170)), ((i % cot) * 213, (i // cot) * 170))
o.save('semanticrt_may_dai_dien.jpg')
