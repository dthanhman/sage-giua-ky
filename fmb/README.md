# FMB – dữ liệu chính (slide 4)

Kết quả kiểm dữ liệu (audit, 3–4/11) và cách chia train/dev/test của nhóm. Số trên slide 4 lấy từ đây.

## 1. Tóm tắt

| Mục | Kết quả |
|---|---|
| Số cặp | **1.500** = 1.220 train + 280 test. Không lỗi ghép cặp, không ảnh hỏng |
| Kích thước | Tất cả 800×600 |
| Ảnh | VIS 3 kênh. IR lưu 3 kênh nhưng 3 kênh giống hệt nhau (1.500/1.500) → đọc 1 kênh |
| Nhãn | 1 kênh, giá trị 0–14 (0 = chưa gán nhãn). Thư mục `color` là nhãn tô màu, **không phải ảnh VIS** |
| Lớp | 14 lớp vật thể + nền: road, sidewalk, building, traffic_light, traffic_sign, vegetation, sky, person, car, truck, bus, motorcycle, bicycle, pole |
| Lớp vắng ở test | **bicycle**: 12 ảnh train, 0 ảnh test → mIoU tính trên 13 lớp |
| Lớp hiếm (< 0,5% pixel) | traffic_light, traffic_sign, truck, motorcycle, bicycle → dùng mIoU, mỗi lớp tính ngang nhau |

Số liệu gốc: [`so_lieu/8_tom_tat.json`](so_lieu/8_tom_tat.json), [`so_lieu/2_so_anh_theo_split.csv`](so_lieu/2_so_anh_theo_split.csv), [`so_lieu/4_phan_bo_lop.csv`](so_lieu/4_phan_bo_lop.csv). Hình phân bố lớp: [`hinh/phan_bo_lop.png`](hinh/phan_bo_lop.png).

## 2. Rò dữ liệu: 7 ảnh test

FMB cắt từ video, nên ảnh liền nhau gần như giống hệt. **7/280 ảnh test (2,5%)** là khung hình kề với ảnh train cùng video:

| Cụm | Ảnh test | Ảnh train gần nhất |
|---|---|---|
| A – đường đêm, tòa nhà + vách đá | 00587, 00588, 00589, 00590 | 00489–00500 |
| B – phố chung cư có sương | 00631, 00632, 00633 | 00586 |

- Cách tìm: so mã băm ảnh (dHash) giữa test và train, rồi **chốt bằng mắt**. dHash trên IR không dùng được vì ảnh đêm nhiễu.
- Xử lý: **không xóa**, chỉ gắn cờ `leak=True` trong `test.csv`. Kết quả chính báo trên **273 ảnh** (có báo kèm 280).
- Danh sách: [`so_lieu/5_anh_test_ro_da_chot.csv`](so_lieu/5_anh_test_ro_da_chot.csv). Hình xem bằng mắt: [`hinh/anh_test_ro.png`](hinh/anh_test_ro.png).

## 3. Chia train / dev / test

| File | Số ảnh | Ghi chú |
|---|---:|---|
| [`manifests/train.csv`](manifests/train.csv) | 1.045 | Train chính thức trừ dev |
| [`manifests/dev.csv`](manifests/dev.csv) | 175 | 14,3% của train, gồm 5 khối id liền nhau |
| [`manifests/test.csv`](manifests/test.csv) | 280 | Đủ test chính thức; 7 ảnh có `leak=True` |

- **Chấm SAGE (slide 5–8):** SegFormer train trên **đủ 1.220 ảnh** (train + dev), giống bài.
- **Dev 175 ảnh** để dành cho phần cải tiến: chỉnh tham số trên dev, không nhìn test.
- Dev cắt **theo khối id liền nhau**, không bốc ngẫu nhiên, để ảnh dev không có "anh em sinh đôi" trong train.
- Chi tiết cách chọn khối và cách kiểm: [`manifests/README.md`](manifests/README.md).

Đọc `image_id` dạng chuỗi để giữ số 0 đầu: `pd.read_csv(path, dtype={"image_id": str})`. Lọc `leak == False` để có 273 ảnh.

## 4. Ảnh minh họa trên slide

Đêm (train 00598), sương (train 01132), khói (test 00089), mỗi cảnh có VIS, IR, nhãn. Bộ minh họa đầy đủ: [`hinh/bo_anh_minh_hoa.png`](hinh/bo_anh_minh_hoa.png).

## 5. Nguồn

- Bài tạo ra FMB: SegMiF (ICCV 2023), arXiv 2308.02097. Dữ liệu tải theo hướng dẫn ở repo https://github.com/JinyuanLiu-CV/SegMiF.
- Notebook audit gốc: `FMB_audit_gop.ipynb` (chạy trên Colab, kết quả đã chốt 3–4/11).
