# Giải thích slide giữa kỳ – nhóm SAGE

Slide: 12 trang trên Canva (link gửi riêng trong nhóm). Mọi số là nhóm tự chạy, trừ chỗ ghi "theo bài".

Mỗi slide có 2 phần:
- **Ý chính:** những gì trên slide.
- **💡 Hiểu đơn giản:** giải thích vì sao, ý nghĩa con số.

**Một câu:** nhóm chấm lại SAGE thật công bằng trên FMB bằng đúng mạng chấm của bài (SegFormer-B3, 3 lần chạy). Kết quả: ảnh nhiệt giúp thật (nhất là lớp người), nhưng SAGE chỉ hơn ảnh thường +0,8, chưa tái lập được +12,1 của bài, và cách ghép trung bình đơn giản không thua SAGE. Từ đó nhóm đặt 3 câu hỏi nghiên cứu.

**Mạch trình bày:** vấn đề → SAGE → bài khác nói gì → dữ liệu → cách chấm → kết quả → so với bài → khoảng trống và câu hỏi.

**SegFormer là gì?** Một mạng phân đoạn ảnh: gán nhãn cho từng pixel (đường, người, xe…). Nhóm dùng nó làm **"giám khảo"** chấm ảnh ghép. B3 là bản cỡ vừa, đúng bản bài SAGE dùng.

Lời nói mẫu nằm ở **cuối file**.

---

## Trang 1 – Tiêu đề

"Hợp nhất ảnh hồng ngoại và ảnh thường phục vụ bài toán hiểu ngữ cảnh – Tái lập và đánh giá SAGE trên FMB." Tên nhóm, MSSV, GVHD.

---

## Slide 1 – Vấn đề và bài toán

**Ý chính**
- Ảnh thường (**VIS**) gần như không thấy gì khi trời tối, có sương hoặc khói. Ảnh hồng ngoại (**IR**) vẫn thấy người và xe, nhưng mất màu và chi tiết.
- **Input:** ảnh màu + ảnh nhiệt → **Ghép ảnh** → **Output:** 1 ảnh ghép màu.
- **Cách chấm:** ảnh ghép → mạng phân đoạn → đo mIoU (độ khớp với nhãn).
- **Thách thức:** không có ảnh ghép chuẩn để làm nhãn → chấm gián tiếp.
- Ảnh minh họa: FMB test 00089, khói che người ở VIS, IR vẫn thấy rõ.

**💡 Hiểu đơn giản**
- VIS giống mắt người: thấy màu, biển báo, nhưng tối là chịu. IR giống "mắt nhìn nhiệt": người và xe nóng nên sáng rõ, nhưng không có màu. Ghép lại để lấy cái tốt của cả hai.
- Không ai biết ảnh ghép "đúng" trông thế nào. Vì vậy nhóm chấm bằng câu hỏi: **ảnh ghép có giúp máy nhận ra vật thể tốt hơn không?** Máy nhận ra tốt hơn thì ảnh ghép tốt hơn.

---

## Slide 2 – Phương pháp SAGE (CVPR 2025)

**Ý chính**
- **Teacher:** dùng SAM (mô hình tách vật thể) để tạo ảnh ghép giữ rõ từng vật thể. Chỉ dùng khi train.
- **Student:** mạng nhỏ 0,136M tham số, chạy không cần SAM. Học lại từ Teacher qua 3 loss (L_fea + L_cont + L_cs). Nhanh: 10,47 ms/ảnh (theo bài).
- **Kết quả theo bài:** mIoU VIS 49,1 → SAGE 61,2 (tăng 12,1). Bỏ SAM: 61,2 → 56,5 (Bảng 3).
- **Câu hỏi đặt ra:** SAM có thật sự giúp nhận diện vật thể tốt hơn cách ghép đơn giản không?

**💡 Hiểu đơn giản**
- Giống **thầy và trò**:
  - Thầy (Teacher) có "sách tham khảo" là SAM, nên hiểu rõ "đâu là một vật", nhưng nặng và chậm.
  - Trò (Student) không có sách, chỉ học theo cách thầy làm.
  - Đi thi (chạy thật) chỉ có trò làm bài, nên rất nhanh.
- **SAM** là mô hình của Meta, tự khoanh vùng mọi vật (người, xe, nhà…) mà không cần biết tên lớp.
- **3 loss = 3 cách trò học thầy:**
  - **L_fea:** "nghĩ giống thầy", đặc trưng bên trong giống thầy.
  - **L_cont:** "bài làm trông giống thầy", cạnh và độ sáng giống ảnh mẫu.
  - **L_cs:** "hiểu vật thể giống thầy", dùng SAM làm thước đo.
- **Điểm cần nhớ cho phần sau:** chỉ Teacher có loss phân đoạn (L_seg). Student **không** được học trực tiếp từ nhãn phân đoạn, chỉ học gián tiếp qua thầy và SAM. Ý này dẫn tới RQ1.

---

## Slide 3 – Các nghiên cứu liên quan

**Ý chính – Các hướng ghép ảnh liên quan** (số theo từng bài)
- **SegMiF (ICCV 2023):** học ghép ảnh và phân đoạn cùng lúc; tạo bộ dữ liệu FMB. VIS 50,5 → 54,8 mIoU.
- **SAGE (CVPR 2025):** Teacher dùng SAM, rồi dạy lại Student nhỏ gọn. VIS 49,1 → 61,2.
- **PIAFusion (2022), AMFusion (2024):** tăng phần ảnh nhiệt khi cảnh tối. Bài gốc không đánh giá phân đoạn trên FMB (AMFusion chỉ đo phát hiện người).
- **SEA (2024):** đánh giá ảnh ghép bằng mạng phân đoạn có sẵn, không train lại. 30 cách ghép (FMB, MVSeg) đều không hơn chỉ dùng VIS; chưa có ghép trung bình.

**Ý chính – Các bài sau có đo SAGE trên FMB** (số theo từng bài)

| Bài | Mạng phân đoạn | mIoU SAGE |
|---|---|---|
| SSVIF (arXiv 2025) | SegFormer-B3 | 62,0 |
| AD-SRF (arXiv 2026) | OverLock-B | 61,4 |
| P2Fusion (arXiv 2026) | SegFormer-B5 | 56,5 |
| PCDFusion (NeurIPS 2026) | SegFormer-B2 | 56,3 |
| CLDyN (CVPR 2026) | SegFormer-B2 | 54,9 |

→ Cùng là SAGE, mIoU dao động 54,9 → 62,0 tùy cấu hình (dẫn sang slide 6). Không bài nào đo VIS → chưa ai kiểm lại +12,1 → nhóm tự đo (slide 7).

**💡 Hiểu đơn giản**
- Các bài sau SAGE chỉ dùng SAGE làm đối thủ để so với phương pháp mới của họ. **Không bài nào đo ảnh thường (VIS)**, nên chưa ai kiểm lại con số +12,1. Đây là lý do nhóm tự đo.
- Cùng một SAGE mà mỗi bài ra một số khác (lệch tới 7 điểm) → cấu hình đánh giá ảnh hưởng rất lớn → nhóm ghi đủ cấu hình (slide 6).
- Số trên slide này đều **theo từng bài**, nhóm chưa tự đo.
- ⚠ Bản trước (đến 16/11/2026) có cột ghi nhầm là "SAGE − VIS" (thật ra là "phương pháp của bài − SAGE"); đã đối chiếu bảng gốc và sửa.

---

## Slide 4 – Dataset FMB và cách chia dữ liệu

**Ý chính**
- Ảnh đường phố: cặp VIS–IR chụp cùng lúc + nhãn từng điểm ảnh.
- 1.500 cặp ảnh 800×600: 1.220 train, 280 test; 14 lớp vật thể.
- **Rò rỉ:** 7 ảnh test là khung hình kề ảnh train → bỏ ra, báo kết quả trên **273 ảnh**.
- **Chấm SAGE:** train SegFormer trên đủ 1.220 ảnh như bài. Tách 175 ảnh (**Dev**) để chỉnh phần cải tiến sau này.
- Xe đạp không có trong test → tính mIoU trên 13 lớp. Có lớp hiếm → dùng mIoU, mỗi lớp tính ngang nhau.
- Ảnh minh họa thật: đêm (train 00598), sương (train 01132), khói (test 00089), mỗi cảnh có VIS, IR, nhãn.

**💡 Hiểu đơn giản**
- **Rò dữ liệu là gì?** FMB cắt từ video, nên 2 ảnh liền nhau gần như giống hệt. Nếu ảnh này ở train còn ảnh kề nó ở test, mạng đã "thấy trước đề thi", kết quả sẽ đẹp giả. Nhóm bỏ 7 ảnh đó ra cho chắc.
- **Dev để làm gì?** Khi làm cải tiến phải chỉnh tham số. Chỉnh trên Dev, không nhìn tập test, để kết quả test vẫn công bằng. Dev cắt theo khối ảnh liền nhau, không bốc ngẫu nhiên, cùng lý do chống rò.
- **Sao 13 lớp?** Có 15 nhãn. Bỏ nhãn 0 (chưa gán nhãn) còn 14 lớp. Xe đạp không xuất hiện trong test thì không chấm được (0 chia 0), còn 13.
- **Sao dùng mIoU, không dùng độ chính xác pixel?** Đường, cây, nhà chiếm phần lớn pixel. Chỉ đoán đúng mấy lớp to là độ chính xác đã cao, dù sai hết lớp nhỏ. mIoU lấy trung bình **từng lớp**, nên người, biển báo cũng được tính ngang lớp to.

---

## Slide 4b – Dataset mở rộng: SemanticRT

**Ý chính**
- Ảnh đường phố, phần lớn chụp ban đêm. 11.371 cặp RGB–nhiệt, 1280×1024.
- 13 lớp, có nhãn từng điểm ảnh → đo được mIoU như FMB.
- Mô hình ghép chưa từng thấy dữ liệu này → dùng để **kiểm tra tổng quát**, không train lại mô hình ghép.
- **Split gốc chia ngẫu nhiên theo khung hình:** 347/2.836 ảnh test trùng y hệt ảnh train.
- Khoảng 22 góc máy, góc nào cũng có ảnh ở cả train và test → nhóm chia lại theo góc máy.
- Ảnh minh họa: test img_10729 và train img_00721 giống nhau từng điểm ảnh (cả VIS và IR).

**💡 Hiểu đơn giản**
- **Vì sao cần thêm dataset?** Nếu chỉ thử trên FMB, cải tiến có thể chỉ "hợp với FMB". Đem sang dữ liệu khác mà vẫn tốt thì mới chắc là cải tiến thật. Slide này phục vụ RQ3.
- **Vì sao không dùng LLVIP?** LLVIP chỉ có khung bao người (dùng cho phát hiện), không có nhãn từng pixel nên không đo được mIoU. SemanticRT có nhãn phân đoạn.
- **Phát hiện của nhóm:** bộ chia sẵn của tác giả bốc ngẫu nhiên từng khung hình. Có 347 ảnh test **trùng y hệt** ảnh train, giống lỗi rò ở FMB nhưng nặng hơn nhiều. Nhóm gom ảnh theo góc máy rồi chia train/test theo góc máy, để camera nào ở test thì không xuất hiện ở train.
- **"Không train lại mô hình ghép" nghĩa là gì?** Mô hình ghép (SAGE hoặc bản cải tiến) giữ nguyên trọng số đã train trên FMB. Chỉ có SegFormer (giám khảo) phải train mới, vì SemanticRT có bộ lớp khác FMB.
- Số "~22 góc máy" là ước lượng (gom tự động rồi xem bằng mắt), nên ghi dấu "~".

---

## Slide 5 – Baseline và cách đánh giá

**Ý chính – 4 loại ảnh, mọi thứ khác giữ nguyên**

| Loại | Là gì | Để kiểm điều gì |
|---|---|---|
| VIS | Chỉ ảnh thường | Mốc gốc: không ghép thì được bao nhiêu |
| IR | Chỉ ảnh nhiệt | Ảnh nhiệt một mình được bao nhiêu |
| Ghép TB | Độ sáng = (VIS + IR)/2 | Cách ghép **đơn giản nhất**: không học, không SAM |
| SAGE | Bản Student của tác giả | Phương pháp của bài |

**Ý chính – 2 mức chấm**
- **Mức 1 – chỉ số ghép (không cần nhãn):** SCD, MS-SSIM (tổng với 2 ảnh nguồn), Q_ABF.
- **Mức 2 – hiểu cảnh (cần nhãn):** train mới một SegFormer-B3 riêng cho mỗi loại ảnh, cùng cấu hình → mIoU 13 lớp, 273 ảnh.
- Khoảng tin cậy 95% (bootstrap theo cụm ảnh). Chạy 3 lần (3 seed). Bỏ 7 ảnh rò. Bài không ghi đủ cấu hình → nhóm tự chọn và ghi rõ.

**💡 Hiểu đơn giản**
- **Vì sao cần mức 2?** Mức 1 chỉ đo ảnh ghép "giống ảnh gốc" đến đâu. Mục đích ghép là để máy hiểu cảnh, nên nhóm cho máy "làm bài thi thật": phân đoạn từng pixel.
- **Như thi đấu công bằng:** 4 thí sinh (4 loại ảnh) được cùng một kiểu thầy (SegFormer-B3) dạy cùng giáo án (cùng cấu hình), rồi thi cùng đề (273 ảnh).
- **Ghép TB là "đối thủ tối thiểu":** một phương pháp tốn công như SAGE ít nhất phải hơn cách cộng hai ảnh chia đôi.
- **Vì sao chạy 3 lần và có khoảng tin cậy?** Train lại thì kết quả dao động khoảng 1 điểm. Chênh lệch nhỏ hơn mức dao động thì chưa kết luận được.

---

## Slide 6 – Cấu hình chấm SegFormer-B3

**Ý chính – Nhóm chọn gì, bài có ghi không**

| Mục | Nhóm chọn | Bài ghi? |
|---|---|---|
| Mạng | SegFormer-B3 | Có |
| Khởi tạo | Trọng số mit-b3 học sẵn trên ImageNet | Không |
| Số lớp khi train | 15 lớp (tính cả nền chưa gán nhãn) | Không |
| Dữ liệu train | Đủ 1.220 ảnh train chính thức | Có |
| Số vòng | 100 epoch (15.200 vòng), batch 8 | Chỉ epoch |
| Tối ưu | AdamW, lr 6e-5, warmup 1.500, poly | Không rõ (bài chỉ ghi chung "Adam is adopted for training", không rõ cho SegFormer) |
| Tăng cường | Phóng to/thu nhỏ, cắt 512, lật ngang | Không |
| Chọn mô hình | Lấy bản cuối, không chọn theo test | Không |
| Đánh giá | Nguyên ảnh 600×800, 273 ảnh, 13 lớp | Không |
| Số lần chạy | 3 seed, FP16, Kaggle T4 | Không |

**Ý chính – Đã kiểm lỗi**
- Ảnh SAGE nhóm tạo trùng ảnh mẫu của tác giả (tương quan 0,9999).
- Rò dữ liệu: train/test không trùng; báo cả 280 và 273 ảnh.
- mIoU: thử 3 cách tính, kết luận không đổi.
- Code chấm: viết riêng một bản để chấm lại, khớp 100%.
- Train đủ vòng, loss đã ổn định.
- Không do may rủi: chạy 3 lần + khoảng tin cậy.

**💡 Hiểu đơn giản**
- Bài SAGE không công bố code chấm phân đoạn, và chỉ ghi 2/10 mục cấu hình. Mục nào bài không ghi thì nhóm chọn theo cấu hình SegFormer gốc hoặc code SegMiF (cùng nhóm tác giả), và ghi rõ ra.
- **Cột "Đã kiểm lỗi" trả lời câu "có phải nhóm làm sai không?"** Nhóm đã loại từng khả năng: tạo ảnh sai, rò dữ liệu, cách tính mIoU, lỗi code, train chưa đủ, may rủi.

---

## Slide 7 – Kết quả trên 273 ảnh test

**Ý chính – Chỉ số ghép (cao hơn = tốt hơn)**

| Chỉ số | VIS | Ghép TB | SAGE |
|---|---|---|---|
| SCD | 0,55 | 1,39 | **1,71** |
| MS-SSIM (tổng) | 1,46 | **1,60** | 1,52 |
| Q_ABF | **0,76** | 0,40 | 0,67 |

**Ý chính – mIoU (%), trung bình 3 lần chạy**

| Ảnh đầu vào | Toàn bộ | Ảnh tối | Lớp người |
|---|---|---|---|
| VIS | 62,6 | 55,9 | 59,1 |
| IR | 56,4 | 57,6 | **70,9** |
| Ghép TB | **64,4** | **61,8** | 69,7 |
| SAGE | 63,4 | 58,4 | 70,0 |

"Ảnh tối" = 1/3 số ảnh tối nhất. [a; b] = khoảng tin cậy 95%.

**Ý chính – 3 ô kết luận**
1. **+0,8 – SAGE chỉ nhỉnh hơn VIS:** SAGE − VIS = +0,8 [−0,9; +3,0]. Khoảng tin cậy chứa 0 → chưa chắc. Bài ghi +12,1 → chưa tái lập được.
2. **+1,05 – Ghép TB hơn SAGE:** TB − SAGE = +1,05 [+0,08; +2,16]. Hơn ở cả 3 lần chạy, nhưng sát 0 → bằng chứng còn yếu.
3. **+10,9 – Lớp người nhờ ảnh nhiệt:** SAGE − VIS = +10,9 ở lớp người. IR 70,9 ≈ SAGE 70,0 ≈ TB 69,7 → lợi ích đến từ ảnh nhiệt.

**💡 Hiểu đơn giản**
- **Ảnh nhiệt giúp thật, nhưng không phải nhờ riêng SAGE.** Lớp người tăng gần 11 điểm vì người tỏa nhiệt. Nhưng chỉ dùng IR, hay cộng đơn giản, cũng được mức đó.
- **Tính trên toàn bộ ảnh thì SAGE gần như ngang VIS** (+0,8, chưa chắc). Lợi ích ở lớp người bị bù lại ở các lớp cần màu và chi tiết (biển báo, đèn…).
- **Cách cộng hai ảnh chia đôi lại tốt nhất** ở cả toàn bộ lẫn ảnh tối. Nhưng chỉ hơn SAGE khoảng 1 điểm, nên nói "**không thua, còn nhỉnh hơn**", không nói "tốt hơn hẳn".
- **Chỉ số ghép mỗi cái chọn một người thắng khác nhau:** SCD chọn SAGE, MS-SSIM chọn Ghép TB, Q_ABF chọn VIS. SAGE thắng SCD rõ nhưng không thắng mIoU → **chỉ số ghép tốt chưa chắc giúp máy hiểu cảnh tốt.**
- **Đọc khoảng tin cậy:** [−0,9; +3,0] chứa 0 nghĩa là chênh lệch có thể bằng 0, chưa kết luận được. [+0,08; +2,16] không chứa 0 nhưng mép dưới rất sát 0, nên bằng chứng còn yếu.

---

## Slide 8 – So với số của bài báo (7 lớp)

**Ý chính – IoU từng lớp (%)**

| Lớp | VIS bài | VIS nhóm | IR bài | IR nhóm | SAGE bài | SAGE nhóm |
|---|---|---|---|---|---|---|
| Đường | 84,8 | 88,4 | 83,7 | 86,4 | 89,0 | 87,7 |
| Nhà | 81,0 | 82,6 | 77,6 | 82,1 | 83,9 | 84,6 |
| Biển báo | 64,2 | 77,3 | 55,9 | 65,7 | 71,4 | 78,3 |
| Cây | 84,7 | 86,3 | 80,9 | 83,2 | 86,3 | 87,4 |
| Xe buýt | 46,8 | 34,5 | 38,1 | 37,6 | 66,7 | 32,1 |
| Người | 61,1 | 59,0 | 57,1 | 70,9 | 64,1 | 69,9 |
| Xe con | 77,1 | 79,4 | 74,2 | 75,7 | 81,7 | 78,4 |
| **TB 7 lớp** | **71,4** | **72,5** | **66,8** | **71,7** | **77,6** | **74,0** |

**Mức tăng SAGE − VIS:** trên 7 lớp bài +6,2, nhóm +1,6; mIoU chung bài +12,1, nhóm +0,8.

**Nhận xét**
- VIS khớp bài: 72,5 so với 71,4.
- SAGE thấp hơn bài: 74,0 so với 77,6.
- Lệch nhiều nhất ở xe buýt (32,1 so với 66,7). Đây là lớp hiếm, số thay đổi nhiều giữa các lần chạy.
- Bài không nói ảnh SAGE lấy từ Teacher hay Student → chưa rõ vì sao lệch.

**💡 Hiểu đơn giản**
- **Slide này dùng 280 ảnh** (đủ tập test như bài), không phải 273 như slide 7, để so với bài cho công bằng (chú thích cuối slide có ghi).
- **Vì sao chỉ so 7 lớp?** Bài chỉ in số của 7 lớp này, và không nói mIoU chung tính trên những lớp nào. Nên chỉ so trực tiếp được trên 7 lớp. Không so thẳng mIoU chung (49,1 của bài với 62,6 của nhóm) vì hai bên tính khác nhau.
- **VIS khớp bài** → cách chấm của nhóm đúng. **SAGE thấp hơn bài** → chỗ lệch nằm ở ảnh SAGE, không phải ở cách chấm.
- **Xe buýt kéo lệch nhiều nhất:** lớp hiếm, ít ảnh, nên số dao động mạnh giữa các lần chạy.
- **Giả thuyết:** bài có thể dùng ảnh của Teacher (mạng lớn, có SAM) chứ không phải Student. Bài không nói rõ, nên nhóm chỉ ghi "chưa rõ".

---

## Slide 9 – Khoảng trống và câu hỏi nghiên cứu

**Ý chính – Khoảng trống**
1. SAGE chưa tái lập được lợi ích +12,1 so với VIS.
2. Ghép trung bình đơn giản không thua SAGE.
3. Chưa rõ phần SAM đóng góp gì cho phân đoạn.

**Ý chính – Bằng chứng đã có**
- SAGE − VIS = +0,8 [−0,9; +3,0]; bài ghi +12,1.
- Trên 7 lớp: VIS khớp bài (72,5 so với 71,4), SAGE thấp hơn bài (74,0 so với 77,6).
- Ghép TB − SAGE = +1,05 [+0,08; +2,16].
- Lớp người: IR 70,9 ≈ SAGE 70,0 → lợi ích từ ảnh nhiệt.
- Bài báo: bỏ SAM thì 61,2 → 56,5, chưa ai kiểm lại.

**Ý chính – Câu hỏi nghiên cứu** (tạm thời, có thể đổi khi nghiên cứu thêm)
- **RQ1 (khoảng trống 1, 3):** SAGE chỉ được dẫn dắt gián tiếp qua SAM. Thêm tín hiệu phân đoạn trực tiếp (fine-tune SAGE bằng loss phân đoạn) có giúp mIoU FMB vượt Ghép TB và VIS không?
- **RQ2 (khoảng trống 2):** Phân đoạn cần phần nào của ảnh ghép: tần thấp (độ sáng, tương phản) hay tần cao (cạnh, chi tiết)?
- **RQ3 (kiểm tra RQ1):** Fine-tune trên FMB có thể chỉ học thuộc FMB. Cải thiện có giữ được trên SemanticRT không (không train lại mô hình ghép)?
- **Thành công khi:** RQ1 hơn cả Ghép TB và VIS; RQ3 vẫn hơn SAGE gốc trên SemanticRT.
- **Cách đo chung:** mIoU B3, 3 seed, khoảng tin cậy 95%; chỉnh trên Dev, không đụng test.

**💡 Hiểu đơn giản – 3 câu hỏi nối nhau thế nào**
- **Mạch:** SAGE chưa hơn rõ ràng → **thử cải thiện** (RQ1) → **hiểu vì sao** cách đơn giản lại tốt (RQ2) → **kiểm tra** cải thiện có thật không (RQ3).
- **RQ1:** ở SAGE, chỉ Teacher có loss phân đoạn. Student học gián tiếp qua thầy và SAM, mà phần SAM chưa ai kiểm lại. Nhóm thử cho Student học **thẳng** từ nhãn phân đoạn: lấy SegFormer đã train, đóng băng, rồi dùng loss của nó để chỉnh tiếp Student. Phải hơn cả Ghép TB, vì một phương pháp tốn công mà thua cách cộng đơn giản thì không có ý nghĩa.
- **RQ2:** tách ảnh thành hai phần. **Tần thấp** là mảng sáng tối lớn (vùng người sáng lên trong ảnh nhiệt). **Tần cao** là cạnh và chi tiết nhỏ (viền biển báo, chữ). Ghép TB giữ tần thấp rất tốt mà vẫn thắng, nên có thể phân đoạn cần tần thấp nhiều hơn. Kiểm bằng cách ghép tần thấp của ảnh này với tần cao của ảnh kia. Đây là phần xử lý ảnh, hợp với CS406.
- **RQ3:** dùng SemanticRT (slide 4b). Giữ nguyên mô hình ghép đã fine-tune trên FMB, không train lại, đem ghép ảnh SemanticRT rồi chấm. Vẫn hơn SAGE gốc thì cải thiện là thật. Còn kém đi thì là học thuộc FMB, và đó vẫn là một phát hiện có giá trị.
- **Vì sao "tạm thời"?** Giữa kỳ yêu cầu có số liệu thật rồi mới đề xuất. Các RQ đi ra từ số liệu ở slide 7–8, nhưng hướng làm cụ thể có thể chỉnh khi thử nghiệm.

---

## Trang cuối – Cảm ơn

---

## Chỉ số, hiểu nhanh

| Chỉ số | Hiểu đơn giản |
|---|---|
| **mIoU** | Độ trùng giữa vùng mạng khoanh và vùng đúng, lấy trung bình 13 lớp. Ví dụ IoU người = 70% nghĩa là vùng "người" mạng khoanh trùng 70% với người thật. Cao hơn là tốt hơn. |
| **SCD** | Ảnh ghép giữ được bao nhiêu phần **riêng** của mỗi ảnh (thứ IR có mà VIS không có, và ngược lại). Chỉ VIS thì thiếu phần của IR nên thấp (0,55). |
| **MS-SSIM (tổng)** | Giống cấu trúc VIS **cộng** giống cấu trúc IR. Mỗi phần tối đa 1, tổng tối đa 2. **Lớn hơn 1 là bình thường.** |
| **Q_ABF** | Cạnh, đường viền của ảnh nguồn được giữ lại bao nhiêu (0–1). VIS nhiều cạnh nhất nên "chỉ VIS" điểm cao nhất. |
| **Khoảng tin cậy 95%** | Bốc lại tập test nhiều lần (theo cụm ảnh liền nhau) để xem kết quả dao động bao nhiêu. **Không chứa 0** thì chênh lệch là thật. **Chứa 0** thì chưa kết luận được. |
| **Seed** | Train lại với khởi tạo ngẫu nhiên khác, kết quả hơi khác (khoảng 1 điểm). Lặp lại ở nhiều seed mới đáng tin. |
| **Fine-tune** | Lấy mô hình đã train sẵn, train tiếp một chút với mục tiêu mới. Ở RQ1: Student SAGE train tiếp bằng loss phân đoạn. |

---

## Thầy có thể hỏi

| Câu hỏi | Trả lời |
|---|---|
| Vậy bài báo sai à? | Không kết luận vậy. Nhóm chỉ chưa tái lập được +12,1 với cấu hình của mình. Bài không công bố code chấm và chỉ ghi 2/10 mục cấu hình. Các bài sau SAGE chưa ai đo lại VIS trên FMB, nên chưa ai kiểm được +12,1 (slide 3). |
| Sao chắc nhóm không làm sai? | Slide 6, cột "Đã kiểm lỗi": ảnh SAGE trùng ảnh tác giả (tương quan 0,9999), VIS khớp bài trên 7 lớp, code chấm viết 2 bản khớp 100%, 3 lần chạy. |
| Sao so công bằng? | Cùng mạng chấm B3, cùng cấu hình, cùng 273 ảnh, cùng 3 seed. Chỉ khác ảnh đầu vào. |
| Leakage xử lý thế nào? | FMB: bỏ 7 ảnh test rò, báo trên 273 ảnh (có báo cả 280). Dev cắt theo khối. SemanticRT: chia lại theo góc máy. |
| Sao MS-SSIM lớn hơn 1? | Vì là tổng của hai phần (với VIS và với IR), tối đa 2. Bài SAGE cũng dùng định nghĩa này. |
| Sao chưa có cải tiến? | Đề yêu cầu có số liệu thật rồi mới đề xuất. Giữa kỳ tìm đúng chỗ yếu và đặt câu hỏi, sau giữa kỳ mới làm cải tiến. |
| SemanticRT khác LLVIP thế nào? | LLVIP chỉ có khung bao người, không đo được mIoU. SemanticRT có nhãn từng pixel (13 lớp). |
| Sao không dùng split gốc của SemanticRT? | Split gốc bốc ngẫu nhiên từng khung hình: 347/2.836 ảnh test trùng y hệt ảnh train. Dùng thì mIoU bị thổi phồng. |
| RQ1 có giống SegMiF không? | SegMiF train ghép và phân đoạn cùng lúc từ đầu. RQ1 giữ nguyên SAGE, chỉ chỉnh tiếp Student nhỏ bằng loss phân đoạn, rồi kiểm có tổng quát sang dữ liệu khác không (RQ3). |
| Fine-tune bằng loss phân đoạn có làm ảnh ghép xấu đi? | Có thể. Nên ngoài mIoU nhóm vẫn đo chỉ số ghép (mức 1) để xem đánh đổi. |
| Tăng phần ảnh nhiệt khi tối thì PIAFusion làm rồi? | Đúng (slide 3), nhưng các bài đó chưa đo bằng mIoU. RQ2 hỏi khác: phân đoạn cần tần thấp hay tần cao, không chỉ là tỉ lệ IR. |

---

## Lời nói mẫu (1 người trình bày, khoảng 7 phút)

> Không cần đọc thuộc lòng. Nắm ý từng đoạn rồi nói bằng lời của mình. Số trong ngoặc là thời gian gợi ý.

**Tiêu đề (10 giây)**
"Em xin trình bày đề tài của nhóm: hợp nhất ảnh hồng ngoại và ảnh thường phục vụ hiểu ngữ cảnh. Giữa kỳ, nhóm tập trung tái lập và đánh giá lại phương pháp SAGE trên bộ dữ liệu FMB."

**Slide 1 – Vấn đề (35 giây)**
"Ảnh thường gần như không thấy gì khi trời tối, có sương hay khói. Như ảnh này, khói che kín người. Ảnh hồng ngoại đo nhiệt nên vẫn thấy rõ hai người, nhưng mất màu và chi tiết. Bài toán là ghép hai ảnh thành một. Cái khó là không có ảnh ghép chuẩn, nên nhóm chấm gián tiếp: đưa ảnh ghép vào mạng phân đoạn, máy nhận ra vật thể càng đúng thì ảnh ghép càng tốt."

**Slide 2 – SAGE (40 giây)**
"SAGE là bài CVPR 2025, hoạt động theo kiểu thầy và trò. Teacher dùng SAM để tạo ảnh ghép giữ rõ từng vật thể, rồi dạy lại cho Student nhỏ qua ba loss. Lúc chạy chỉ cần Student, rất nhanh, không cần SAM. Theo bài, SAGE tăng mIoU từ 49,1 lên 61,2, tức hơn ảnh thường 12,1 điểm, và bỏ SAM thì giảm còn 56,5. Câu hỏi của nhóm: SAM có thật sự giúp hơn cách ghép đơn giản không?"

**Slide 3 – Liên quan (35 giây)**
"Bên trái là các hướng gần nhất: SegMiF tạo ra bộ FMB, PIAFusion và AMFusion tăng phần ảnh nhiệt khi tối nhưng chưa đo bằng phân đoạn, SEA chấm bằng mạng có sẵn nhưng không có SAGE. Bên phải: các bài sau tự chấm lại SAGE trên FMB chỉ thấy SAGE hơn ảnh thường từ 0 đến 5,5 điểm, không ai gần 12,1. Vì vậy nhóm chấm lại bằng đúng mạng B3 như bài, chạy 3 lần."

**Slide 4 – FMB (35 giây)**
"FMB có 1.500 cặp ảnh đường phố, nhãn 14 lớp. Khi kiểm dữ liệu, nhóm thấy 7 ảnh test là khung hình kề ảnh train, nên bỏ ra và báo kết quả trên 273 ảnh. Nhóm tách thêm 175 ảnh Dev, cắt theo khối, để sau này chỉnh cải tiến mà không nhìn tập test. Xe đạp không có trong test nên mIoU tính trên 13 lớp."

**Slide 4b – SemanticRT (35 giây)**
"Để kiểm tra cải tiến có tổng quát không, nhóm thêm SemanticRT: 11.371 cặp ảnh, có nhãn từng pixel nên đo được mIoU. Khi kiểm, nhóm phát hiện bộ chia sẵn bốc ngẫu nhiên từng khung hình: 347 ảnh test trùng y hệt ảnh train, như cặp ảnh này. Vì vậy nhóm chia lại theo góc máy, khoảng 22 góc."

**Slide 5 – Cách đánh giá (40 giây)**
"Nhóm so 4 loại ảnh: chỉ ảnh thường, chỉ ảnh nhiệt, ghép trung bình là cách đơn giản nhất, và SAGE. Chấm hai mức. Mức một là các chỉ số ghép. Mức hai là hiểu cảnh: với mỗi loại ảnh, train riêng một SegFormer-B3 cùng cấu hình rồi đo mIoU. Chạy 3 lần và tính khoảng tin cậy 95% để biết chênh lệch có chắc không."

**Slide 6 – Cấu hình (30 giây)**
"Bài không công bố code chấm và chỉ ghi 2 trên 10 mục cấu hình, nên nhóm tự chọn theo SegFormer gốc và ghi rõ. Nhóm cũng kiểm từng khả năng làm sai: ảnh SAGE nhóm tạo trùng ảnh của tác giả, không rò dữ liệu, code chấm viết hai bản khớp nhau, và chạy 3 lần."

**Slide 7 – Kết quả (60 giây)** ← slide quan trọng nhất, nói chậm
"Có ba điểm. Thứ nhất, SAGE chỉ hơn ảnh thường 0,8 điểm, khoảng tin cậy chứa 0, nên chưa chắc; bài ghi 12,1. Thứ hai, ghép trung bình đơn giản lại hơn SAGE khoảng 1 điểm, ở cả 3 lần chạy, nhưng sát 0 nên bằng chứng còn yếu. Thứ ba, ở lớp người SAGE hơn ảnh thường gần 11 điểm, nhưng chỉ dùng ảnh nhiệt cũng được mức đó, nên lợi ích đến từ ảnh nhiệt. Thêm nữa, ở chỉ số ghép SAGE thắng SCD rõ, nhưng khi đo bằng hiểu cảnh thì không. Tức là chỉ số ghép tốt chưa chắc giúp máy hiểu cảnh tốt."

**Slide 8 – So với bài (35 giây)**
"Bài chỉ in số của 7 lớp, nên nhóm so trên 7 lớp đó. Ảnh thường của nhóm khớp bài, 72,5 so với 71,4, nên cách chấm đúng. Nhưng SAGE của nhóm thấp hơn bài, 74,0 so với 77,6, lệch nhiều nhất ở xe buýt là lớp hiếm. Bài không nói ảnh SAGE lấy từ Teacher hay Student, nên chưa rõ nguyên nhân."

**Slide 9 – Khoảng trống và câu hỏi (60 giây)**
"Từ số liệu, nhóm thấy ba khoảng trống: chưa tái lập được +12,1; ghép đơn giản không thua SAGE; và chưa rõ SAM đóng góp gì. Nhóm đặt ba câu hỏi nối nhau. RQ1: ở SAGE, Student chỉ học gián tiếp qua SAM; nếu cho Student học thẳng từ loss phân đoạn thì có vượt được ghép trung bình và ảnh thường không. RQ2: để hiểu vì sao cách đơn giản lại tốt, nhóm hỏi phân đoạn cần phần tần thấp, tức độ sáng và tương phản, hay tần cao, tức cạnh và chi tiết. RQ3: cải thiện của RQ1 có giữ được trên SemanticRT, dữ liệu chưa thấy, không. Mọi thứ đo bằng mIoU B3, 3 lần chạy, chỉnh trên Dev, không đụng tập test. Em xin hết, cảm ơn thầy và các bạn."

**Mẹo:**
- Hết giờ thì rút slide 3, 6 và 8 trước, **giữ nguyên slide 7 và 9**.
- Thầy hỏi khó thì dùng bảng "Thầy có thể hỏi" ở trên.
- Khi nói về Ghép TB: "**không thua, còn nhỉnh hơn**", không nói "tốt hơn hẳn".
- Khi nói về bài báo: "**chưa tái lập được**", không nói "bài sai".
