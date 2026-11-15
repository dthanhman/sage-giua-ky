# SAGE – tài liệu giữa kỳ (CS406)

**Đề tài:** Hợp nhất ảnh hồng ngoại và ảnh thường phục vụ bài toán hiểu ngữ cảnh – tái lập và đánh giá SAGE trên FMB.

Repo này gom **mọi nội dung có trên slide giữa kỳ**, mỗi ý trên slide đều có chỗ để xem giải thích và bằng chứng (số liệu, hình, code). Không có code huấn luyện mới, không có dữ liệu gốc.

**Slide (Canva, chỉ xem):** _(dán link chỉ xem vào đây)_

## Đọc gì trước

1. **[`giai-thich-slide.md`](giai-thich-slide.md)**: giải thích từng slide cho dễ hiểu, lời nói mẫu (~7 phút), câu hỏi thầy có thể hỏi. **Đọc file này là đủ để trình bày.**
2. Muốn biết sâu một slide nào thì tra bảng dưới.

## Một câu

Nhóm chấm lại SAGE trên FMB bằng đúng mạng chấm của bài (SegFormer-B3, 3 lần chạy). Ảnh nhiệt giúp thật (nhất là lớp người), nhưng SAGE chỉ hơn ảnh thường **+0,8** (bài ghi +12,1), và cách ghép trung bình đơn giản không thua SAGE. Từ đó nhóm đặt 3 câu hỏi nghiên cứu.

**Mạch:** vấn đề → SAGE → bài khác nói gì → dữ liệu → cách chấm → kết quả → so với bài → khoảng trống và câu hỏi.

## Slide nào xem ở đâu

| Slide | Nội dung | Giải thích | Bằng chứng / chi tiết |
|---|---|---|---|
| 1. Vấn đề và bài toán | VIS mù khi tối/khói, IR thấy nhiệt; chấm gián tiếp bằng phân đoạn | [Slide 1](giai-thich-slide.md#slide-1--vấn-đề-và-bài-toán) | Ảnh test 00089: [`fmb/hinh/bo_anh_minh_hoa.png`](fmb/hinh/bo_anh_minh_hoa.png) |
| 2. Phương pháp SAGE | Teacher + SAM, Student 0,136M; theo bài 49,1 → 61,2 | [Slide 2](giai-thich-slide.md#slide-2--phương-pháp-sage-cvpr-2025) | Bài: arXiv 2503.01210, code `RollingPlain/SAGE_IVIF` |
| 3. Nghiên cứu liên quan | SegMiF, PIAFusion, AMFusion, SEA; 6 bài chấm lại SAGE | [Slide 3](giai-thich-slide.md#slide-3--các-nghiên-cứu-liên-quan) | [`bai-bao-lien-quan.md`](bai-bao-lien-quan.md) |
| 4. Dataset FMB | 1.500 cặp, 7 ảnh rò → 273 ảnh, Dev 175, 13 lớp | [Slide 4](giai-thich-slide.md#slide-4--dataset-fmb-và-cách-chia-dữ-liệu) | [`fmb/`](fmb/README.md): số liệu audit, danh sách ảnh rò, manifest train/dev/test |
| 4b. SemanticRT | Dataset mở rộng; split gốc rò 347/2.836; ~22 góc máy | [Slide 4b](giai-thich-slide.md#slide-4b--dataset-mở-rộng-semanticrt) | [`semanticrt/`](semanticrt/README.md): cách kiểm, kết quả, script |
| 5. Baseline và đánh giá | VIS / IR / Ghép TB / SAGE; 2 mức chấm; 3 seed, khoảng tin cậy | [Slide 5](giai-thich-slide.md#slide-5--baseline-và-cách-đánh-giá) | [`cham_b3/README.md`](cham_b3/README.md) mục 2 |
| 6. Cấu hình SegFormer-B3 | 10 mục cấu hình, bài ghi gì; 6 bước kiểm lỗi | [Slide 6](giai-thich-slide.md#slide-6--cấu-hình-chấm-segformer-b3) | [`cham_b3/README.md`](cham_b3/README.md) mục 3 và 7; [`cham_b3/b3_fmb_seg.yaml`](cham_b3/b3_fmb_seg.yaml) |
| 7. Kết quả | Chỉ số ghép; mIoU 62,6 / 56,4 / 64,4 / 63,4; +0,8, +1,05, +10,9 | [Slide 7](giai-thich-slide.md#slide-7--kết-quả-trên-273-ảnh-test) | [`cham_b3/README.md`](cham_b3/README.md) mục 4; [`cham_b3/so_sanh_b3.txt`](cham_b3/so_sanh_b3.txt) |
| 8. So với bài (7 lớp) | VIS khớp bài, SAGE thấp hơn bài, lệch ở xe buýt | [Slide 8](giai-thich-slide.md#slide-8--so-với-số-của-bài-báo-7-lớp) | [`cham_b3/README.md`](cham_b3/README.md) mục 5; [`cham_b3/tong_hop.txt`](cham_b3/tong_hop.txt) |
| 9. Khoảng trống và RQ | 3 khoảng trống, 3 câu hỏi nghiên cứu (tạm) | [Slide 9](giai-thich-slide.md#slide-9--khoảng-trống-và-câu-hỏi-nghiên-cứu) | Bằng chứng lấy từ slide 7–8 |

## Cấu trúc repo

```
README.md                 ← file này
giai-thich-slide.md       ← giải thích từng slide + lời nói mẫu + hỏi đáp
bai-bao-lien-quan.md      ← các bài liên quan, các bài chấm lại SAGE (slide 3)
fmb/                      ← slide 4: audit FMB, ảnh rò, manifest train/dev/test
semanticrt/               ← slide 4b: kiểm SemanticRT, gom góc máy, script
cham_b3/                  ← slide 5–8: báo cáo chấm SegFormer-B3, cấu hình, code, kết quả 12 lần chạy
```

## Quy ước

- Số nào nhóm chưa tự đo thì ghi **"theo bài"**.
- mIoU chính: 13 lớp, bỏ pixel chưa gán nhãn, 273 ảnh test (bỏ 7 ảnh rò), trung bình 3 seed. Slide 8 dùng 280 ảnh để so với bài.
- `[a; b]` = khoảng tin cậy 95% (bootstrap theo khối ảnh liền nhau).

## Không có trong repo

- Dữ liệu gốc FMB, SemanticRT (tải theo link trong `fmb/README.md`, `semanticrt/README.md`).
- Checkpoint SegFormer và ma trận nhầm lẫn từng ảnh: trên Kaggle, riêng tư (xem [`cham_b3/README.md`](cham_b3/README.md) mục 10.2), xin quyền Mân.
- Bản gốc phần B3 trong repo nhóm: https://github.com/quan14333/xulianh/tree/main/reports/experiments/b3_fmb_seg
