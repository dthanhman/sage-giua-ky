"""Kiem ro ri train-test SemanticRT: anh test co anh train lien so khong, va giong nhau den muc nao.
Chay: python -I kiem_ro_semanticrt.py <thu_muc_SemanticRT_dataset>
"""
import sys, os, re, random
import numpy as np
from PIL import Image

goc = sys.argv[1]
doc = lambda f: [l.strip() for l in open(os.path.join(goc, f)) if l.strip()]
tr, va, te = doc('train.txt'), doc('val.txt'), doc('test.txt')
so = lambda s: int(re.match(r'img_(\d+)', s).group(1))
s_tr = set(so(x) for x in tr if x.count('_') == 1)
te_don = [x for x in te if x.count('_') == 1]

for k in [1, 2, 5]:
    n = sum(any((so(x) + d) in s_tr for d in range(-k, k + 1) if d) for x in te_don)
    print(f"Anh test co anh train trong khoang +-{k} so: {n}/{len(te_don)} ({100*n/len(te_don):.1f}%)")

def nho(x):
    a = np.asarray(Image.open(os.path.join(goc, 'thermal', x + '.jpg')).convert('L').resize((80, 64)), dtype=np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)

random.seed(0)
mau = random.sample(te_don, 300)
d_ke, d_ngau = [], []
tr_list = sorted(s_tr)
for x in mau:
    n = so(x)
    ke = [n + d for d in (-1, 1, -2, 2) if (n + d) in s_tr]
    if ke:
        d_ke.append(np.abs(nho(x) - nho(f"img_{ke[0]:05d}")).mean())
    d_ngau.append(np.abs(nho(x) - nho(f"img_{random.choice(tr_list):05d}")).mean())
d_ke, d_ngau = np.array(d_ke), np.array(d_ngau)
print(f"Sai khac IR (chuan hoa) test vs train lien so: trung vi {np.median(d_ke):.3f}, n={len(d_ke)}")
print(f"Sai khac IR test vs train ngau nhien:        trung vi {np.median(d_ngau):.3f}")
nguong = np.percentile(d_ngau, 1)
print(f"Ty le cap lien so giong hon 99% cap ngau nhien (< {nguong:.3f}): {100*(d_ke < nguong).mean():.1f}%")

# cap vi du de xem bang mat
os.makedirs('ro_vi_du', exist_ok=True)
for x in mau[:6]:
    n = so(x)
    ke = [n + d for d in (-1, 1) if (n + d) in s_tr]
    if not ke:
        continue
    a = Image.open(os.path.join(goc, 'rgb', x + '.jpg')).resize((320, 256))
    b = Image.open(os.path.join(goc, 'rgb', f"img_{ke[0]:05d}.jpg")).resize((320, 256))
    c = Image.new('RGB', (640, 256)); c.paste(a, (0, 0)); c.paste(b, (320, 0))
    c.save(f"ro_vi_du/test_{n:05d}__train_{ke[0]:05d}.jpg")
print("Da luu cap vi du vao ro_vi_du/")
