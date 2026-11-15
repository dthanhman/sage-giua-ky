"""Tim anh train gan nhat (theo noi dung) cho moi anh test SemanticRT.
Dac trung: anh RGB xam thu nho 40x32, chuan hoa; khoang cach = trung binh |hieu|.
Chay: python -I kiem_ro_noidung.py <thu_muc_SemanticRT_dataset>
"""
import sys, os, json
import numpy as np
from PIL import Image

goc = sys.argv[1]
doc = lambda f: [l.strip() for l in open(os.path.join(goc, f)) if l.strip()]
tr, va, te = doc('train.txt'), doc('val.txt'), doc('test.txt')

def dt(x):
    a = np.asarray(Image.open(os.path.join(goc, 'rgb', x + '.jpg')).convert('L').resize((40, 32)), dtype=np.float32).ravel()
    return (a - a.mean()) / (a.std() + 1e-6)

cache = 'semanticrt_dactrung.npz'
if os.path.exists(cache):
    z = np.load(cache); F_tr, F_va, F_te = z['tr'], z['va'], z['te']
else:
    F_tr = np.stack([dt(x) for x in tr]); F_va = np.stack([dt(x) for x in va]); F_te = np.stack([dt(x) for x in te])
    np.savez(cache, tr=F_tr, va=F_va, te=F_te)

def gan_nhat(A, B, cung=False):
    d_min = np.empty(len(A)); idx = np.empty(len(A), int)
    # khoang cach RMS = sqrt(|a|^2 + |b|^2 - 2ab)/sqrt(dim), tinh theo khoi nho cho nhe RAM
    nb = (B ** 2).sum(1)
    for i in range(0, len(A), 128):
        a = A[i:i+128]
        D = np.sqrt(np.maximum((a ** 2).sum(1)[:, None] + nb[None] - 2 * a @ B.T, 0) / A.shape[1])
        idx[i:i+128] = D.argmin(1); d_min[i:i+128] = D.min(1)
    return d_min, idx

d_te, i_te = gan_nhat(F_te, F_tr)
d_va, i_va = gan_nhat(F_va, F_tr)
# moc so sanh: khoang cach giua 2 anh ngau nhien
rng = np.random.default_rng(0)
a, b = rng.integers(0, len(F_tr), 3000), rng.integers(0, len(F_tr), 3000)
d_ng = np.sqrt(((F_tr[a] - F_tr[b]) ** 2).mean(-1))
print(f"Khoang cach 2 anh train ngau nhien: P1 {np.percentile(d_ng,1):.3f}, trung vi {np.median(d_ng):.3f}")
for ten, d in [('test', d_te), ('val', d_va)]:
    print(f"{ten} -> train gan nhat: trung vi {np.median(d):.3f}, P90 {np.percentile(d,90):.3f}")
    for ng in [0.10, 0.20, 0.30, 0.50]:
        print(f"   ty le < {ng}: {100*(d < ng).mean():.1f}%")

os.makedirs('ro_noidung', exist_ok=True)
thu_tu = np.argsort(d_te)
for k, j in enumerate(list(thu_tu[[0, len(thu_tu)//4, len(thu_tu)//2, 3*len(thu_tu)//4, -1]])):
    x, y = te[j], tr[i_te[j]]
    A = Image.open(os.path.join(goc, 'rgb', x + '.jpg')).resize((320, 256))
    B = Image.open(os.path.join(goc, 'rgb', y + '.jpg')).resize((320, 256))
    C = Image.new('RGB', (640, 256)); C.paste(A, (0, 0)); C.paste(B, (320, 0))
    C.save(f"ro_noidung/{k}_d{d_te[j]:.3f}_test_{x}__train_{y}.jpg")
json.dump({'test_ten': te, 'train_gan_nhat': [tr[i] for i in i_te], 'kc': d_te.round(4).tolist()},
          open('semanticrt_test_gan_nhat.json', 'w'))
print("Da luu vi du vao ro_noidung/ (sap tu giong nhat den khac nhat)")
