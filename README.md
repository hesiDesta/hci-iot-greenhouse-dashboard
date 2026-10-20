# Dasbor Monitoring Greenhouse Cerdas: Studi Kasus HCI dan Visualisasi Data untuk IoT

Studi kasus ini diturunkan dari materi webinar *Human-Computer Interaction & Data Visualization*
(Informatics Practitioner Lecture Series, 19 Oktober 2026, narasumber Arafat Febriandirza, BRIN).
Materi diterapkan pada dasbor yang memantau sensor IoT di greenhouse.

**Demo:** setelah GitHub Pages diaktifkan (Settings, Pages, Branch `main`, folder `/docs`),
dasbor dapat dibuka dari `https://USERNAME.github.io/hci-iot-greenhouse-dashboard/`.
Atau cukup buka `docs/index.html` di browser.

## Skenario
Pengelola greenhouse memantau 3 zona (A, B, C) dengan sensor suhu udara, kelembapan udara,
dan kelembapan tanah. Dasbor harus membantu pengguna melihat kondisi dengan cepat dan
menemukan zona bermasalah tanpa kewalahan oleh angka.

Data simulasi memuat dua gangguan: irigasi zona B berhenti (kelembapan tanah turun di bawah batas)
dan pendingin zona C bermasalah (suhu melewati batas).

## Struktur
```
src/generate_data.py     simulasi data sensor -> data/sensor_log.csv
src/template.html       templat dasbor (HTML, CSS, JavaScript tanpa pustaka luar)
src/build_dashboard.py   menyisipkan data ke templat -> docs/index.html
src/usability_study.py   analisis success rate, task time, dan SUS
docs/perancangan.md      persona, kebutuhan fungsional/nonfungsional, pemetaan prinsip
results/                 hasil analisis usability dan tangkapan layar
```

## Cara menjalankan
```bash
pip install -r requirements.txt
python src/generate_data.py       # membuat data simulasi
python src/build_dashboard.py     # membangun docs/index.html
python src/usability_study.py     # analisis usability
```
Untuk data nyata dari ESP32 atau Arduino, simpan pembacaan ke `data/sensor_log.csv`
dengan kolom `waktu, zona, suhu, kelembapan_udara, kelembapan_tanah`, lalu jalankan ulang `build_dashboard.py`.

## Penerapan materi
| Materi | Penerapan |
|---|---|
| User-Centered Design dan persona | `docs/perancangan.md` |
| Kebutuhan fungsional dan nonfungsional | `docs/perancangan.md` |
| Overview First, Zoom and Filter, Details-on-Demand | Bagian 1 sampai 4 dasbor |
| Hindari chartjunk, pilih grafik yang sesuai | Grafik garis minimalis dengan label langsung |
| Prinsip Gestalt, visibility, feedback, consistency, affordance | Pengelompokan bagian, kartu interaktif, panel detail |
| WCAG (POUR) | Kontras tinggi, status bukan hanya warna, navigasi keyboard, HTML semantik, mode gelap |
| Evaluasi usability | `src/usability_study.py` |

## Tentang hasil uji usability
Berkas `data/usability_results.csv` dan `data/sus_responses.csv` yang disertakan adalah
**data contoh hasil simulasi**, hanya agar skrip dapat dijalankan dan format datanya jelas.
Angka pada `results/usability_summary.txt` **bukan** temuan penelitian. Untuk penelitian
sebenarnya, ajak 8 sampai 10 pengguna mencoba dua rancangan, catat hasilnya dengan kolom yang sama,
lalu jalankan ulang skrip.

## Keterbatasan
- Data sensor simulasi; belum terhubung ke perangkat keras maupun MQTT secara langsung.
- Dasbor statis (data disisipkan saat build), belum memperbarui data secara real time.
- Rancangan "Lama" pada uji usability hanya sebagai pembanding konseptual dan belum dibangun.

## Pengembangan lanjutan
- Ambil data langsung dari broker MQTT atau API.
- Tambahkan notifikasi saat nilai melewati batas.
- Lakukan audit aksesibilitas dengan WAVE atau Lighthouse dan uji dengan pengguna nyata.
