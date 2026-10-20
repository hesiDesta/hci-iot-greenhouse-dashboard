# Dokumen Perancangan (UCD)

## 1. User persona
**Pak Dedi, 45 tahun, pengelola greenhouse (contoh persona).**
- *Goals:* memastikan tanaman di setiap zona selalu dalam kondisi optimal dan mengetahui masalah sebelum tanaman rusak.
- *Pain points:* aplikasi lama menampilkan terlalu banyak angka sekaligus; sulit membedakan zona yang bermasalah; layar ponsel kecil; sering membuka dasbor saat berada di lapangan dengan cahaya terang.
- *Behaviors:* memeriksa kondisi 2 sampai 3 kali sehari lewat ponsel; hanya ingin tahu "ada masalah atau tidak"; jarang membuka detail kecuali ada peringatan.

> Persona ini contoh. Untuk penelitian sebenarnya, susun dari hasil wawancara, observasi, dan kuesioner pengguna.

## 2. Kebutuhan
**Fungsional**
- F1 Menampilkan ringkasan kondisi terkini tiap sensor.
- F2 Menyaring data berdasarkan zona, rentang waktu, dan sensor.
- F3 Menampilkan tren sensor dalam grafik garis dengan batas normal.
- F4 Menampilkan detail semua sensor pada waktu yang dipilih.
- F5 Menampilkan daftar peringatan di luar rentang normal.
- F6 Mengekspor data yang sedang ditampilkan ke CSV.

**Nonfungsional**
- N1 Memuat cepat dan dapat dibuka tanpa internet (satu berkas HTML).
- N2 Terbaca di layar kecil dan terang (tata letak responsif, kontras tinggi).
- N3 Memenuhi prinsip aksesibilitas POUR.
- N4 Mendukung mode gelap mengikuti pengaturan perangkat.

## 3. Pemetaan prinsip materi ke rancangan
| Prinsip dari materi | Penerapan pada dasbor |
|---|---|
| Overview First | Bagian 1: tiga kartu ringkasan kondisi terkini di bagian paling atas |
| Zoom and Filter | Bagian 2: filter zona, rentang waktu, sensor |
| Details-on-Demand | Bagian 4: detail muncul saat kursor/ketuk/panah pada grafik |
| Tufte, hindari chartjunk | Tanpa 3D, tanpa dekorasi; garis kisi tipis; label langsung di ujung garis; satu grafik satu pesan |
| Pemilihan jenis grafik | Grafik garis untuk data deret waktu; tabel untuk peringatan |
| Gestalt: proximity | Kartu, filter, grafik, dan tabel dikelompokkan per bagian bernomor |
| Gestalt: similarity | Satu zona selalu memakai warna dan pola garis yang sama |
| Memori kerja terbatas | Hanya satu sensor pada grafik dalam satu waktu; peringatan dibatasi 8 terbaru |
| Visibility dan feedback | Kartu terpilih diberi bingkai; kursor vertikal dan panel detail langsung berubah |
| Consistency | Format nilai, satuan, dan istilah status seragam di semua bagian |
| Affordance | Kartu sensor berupa tombol; kontrol berukuran minimal 44 px |
| WCAG Perceivable | Status tidak hanya warna (ada ikon dan teks), kontras tinggi, pola garis berbeda per zona, alternatif teks pada grafik |
| WCAG Operable | Semua dapat dioperasikan keyboard (Tab dan panah), fokus terlihat jelas, tautan lewati ke grafik |
| WCAG Understandable | Bahasa Indonesia sederhana, label formulir jelas, petunjuk penggunaan grafik |
| WCAG Robust | HTML semantik (heading, tabel dengan `th scope`, `aria-live`, `aria-pressed`) |
| Etika dan dark patterns | Tidak ada pelacak, iklan, atau pop-up; data tidak keluar dari perangkat |

## 4. Evaluasi usability
Empat tugas diuji (lihat `src/usability_study.py`): melihat status terkini, menemukan zona bermasalah, menyaring 24 jam untuk zona B, dan mengekspor data. Metrik: *success rate*, *task time*, dan skor SUS.
