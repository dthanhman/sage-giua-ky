"""Gom canh SemanticRT, ban 2: dac trung duong bien (it phu thuoc do sang ngay/dem).
1) dac trung = do lon gradient Sobel tren anh xam lam mo, thu nho 48x40, chuan hoa
2) noi canh k-NN (k=10) neu khoang cach < nguong -> thanh phan lien thong
3) cum < 30 anh: gan vao cum lon gan nhat (theo lang gieng gan nhat thuoc cum lon)
Chay: python -I gom_canh_v2.py <thu_muc_SemanticRT_dataset>
"""
import sys, os, json
import numpy as np
from PIL import Image, ImageFilter

goc = sys.argv[1]
doc = lambda f: [l.strip() for l in open(os.path.join(goc, f)) if l.strip()]
tr, va, te = doc('train.txt'), doc('val.txt'), doc('test.txt')
ten = tr + va + te
nhom = np.array(['train'] * len(tr) + ['val'] * len(va) + ['test'] * len(te))

def dt(x):
    im = Image.open(os.path.join(goc, 'rgb', x + '.jpg')).convert('L').resize((192, 160)).filter(ImageFilter.GaussianBlur(2))
    a = np.asarray(im, np.float32)
    gx = np.abs(np.diff(a, axis=1))[:-1]; gy = np.abs(np.diff(a, axis=0))[:, :-1]
    g = np.sqrt(gx ** 2 + gy ** 2)
    g = np.asarray(Image.fromarray(g).resize((48, 40), Image.BILINEAR)).ravel()
    g = np.log1p(g)
    return (g - g.mean()) / (g.std() + 1e-6)

cache = 'semanticrt_dactrung_bien.npy'
if os.path.exists(cache):
    F = np.load(cache)
else:
    F = np.stack([dt(x) for x in ten]).astype(np.float32); np.save(cache, F)
N, dim = F.shape
nb = (F ** 2).sum(1)
K = 10
kn_i = np.empty((N, K), np.int32); kn_d = np.empty((N, K), np.float32)
for i in range(0, N, 128):
    a = F[i:i+128]
    D = np.sqrt(np.maximum(nb[i:i+128, None] + nb[None] - 2 * a @ F.T, 0) / dim)
    D[np.arange(len(a)), np.arange(i, i + len(a))] = np.inf
    j = np.argpartition(D, K, axis=1)[:, :K]
    kn_i[i:i+128] = j; kn_d[i:i+128] = np.take_along_axis(D, j, 1)

def cum(ng):
    cha = np.arange(N)
    def tim(x):
        while cha[x] != x:
            cha[x] = cha[cha[x]]; x = cha[x]
        return x
    for i in range(N):
        for j, d in zip(kn_i[i], kn_d[i]):
            if d < ng:
                a, b = tim(i), tim(j)
                if a != b: cha[a] = b
    return np.array([tim(i) for i in range(N)])

for ng in [0.5, 0.6, 0.7, 0.8, 0.9]:
    _, c = np.unique(cum(ng), return_counts=True); c = np.sort(c)[::-1]
    print(f"nguong {ng}: {len(c)} cum | >=30 anh: {(c>=30).sum()} (chua {c[c>=30].sum()}) | lon nhat {c[:6].tolist()} | le: {(c==1).sum()}")

NG = float(os.environ.get('NG', 0.7))
r = cum(NG)
u, c = np.unique(r, return_counts=True)
lon = set(u[c >= 30].tolist())
# gan anh thuoc cum nho vao cum lon cua lang gieng gan nhat (tinh lai lang gieng chi trong anh thuoc cum lon)
m_lon = np.isin(r, list(lon))
idx_lon = np.where(m_lon)[0]
G = F[idx_lon]; nG = nb[idx_lon]
r2 = r.copy()
for i0 in range(0, N, 128):
    ids = [i for i in range(i0, min(i0 + 128, N)) if not m_lon[i]]
    if not ids: continue
    a = F[ids]
    D = nb[ids][:, None] + nG[None] - 2 * a @ G.T
    r2[ids] = r[idx_lon[D.argmin(1)]]
u, c = np.unique(r2, return_counts=True)
thu_tu = u[np.argsort(-c)]
cid = np.array([{g: k for k, g in enumerate(thu_tu)}[g] for g in r2])
print(f"\nNguong {NG}: {len(u)} canh sau khi gan anh le. So anh moi canh (train/val/test goc):")
for k in range(len(u)):
    m = cid == k
    print(f"  canh {k:2d}: {m.sum():5d}  [{(m&(nhom=='train')).sum()}, {(m&(nhom=='val')).sum()}, {(m&(nhom=='test')).sum()}]")
json.dump({'nguong': NG, 'ten': ten, 'split_goc': nhom.tolist(), 'canh': cid.tolist()}, open('semanticrt_canh.json', 'w'))

cot = 6; hang = (len(u) + cot - 1) // cot
o = Image.new('RGB', (cot * 213, hang * 170))
for k in range(len(u)):
    x = ten[int(np.where(cid == k)[0][len(np.where(cid == k)[0]) // 2])]
    im = Image.open(os.path.join(goc, 'rgb', x + '.jpg')).convert('RGB').resize((213, 170))
    o.paste(im, ((k % cot) * 213, (k // cot) * 170))
o.save('semanticrt_canh_dai_dien.jpg')
print("Da luu semanticrt_canh.json, semanticrt_canh_dai_dien.jpg")
