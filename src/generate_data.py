"""Simulasi data sensor IoT greenhouse (3 zona, 7 hari, per jam).

Sensor: suhu udara (C), kelembapan udara (%), kelembapan tanah (%).
Skenario gangguan agar dasbor punya hal yang perlu dilihat pengguna:
  - Zona B: irigasi berhenti pada hari ke-5 sehingga kelembapan tanah turun.
  - Zona C: pendingin bermasalah pada hari ke-6 sehingga suhu naik.
Ganti data/sensor_log.csv dengan data ESP32/MQTT asli (kolom sama) bila ada.
"""
import numpy as np
import pandas as pd


def generate(seed=7):
    rng = np.random.default_rng(seed)
    waktu = pd.date_range("2026-10-13 00:00", periods=168, freq="h")
    offset = {"A": (0.0, 0.0, 0.0), "B": (0.4, -2.0, -1.5), "C": (-0.3, 3.0, 1.0)}
    rows = []
    for zona, (dt, dh, ds) in offset.items():
        for i, t in enumerate(waktu):
            h = t.hour
            siklus = np.sin(2 * np.pi * (h - 9) / 24)  # puncak pukul 15.00
            suhu = 24.5 + 3.2 * siklus + dt + rng.normal(0, 0.35)
            udara = 68 - 8 * siklus + dh + rng.normal(0, 1.2)
            tanah = 63 - 0.8 * (h % 12) + ds + rng.normal(0, 0.6)  # irigasi tiap 12 jam
            if zona == "B" and i >= 96:  # irigasi berhenti
                tanah = 63 - 0.8 * (i - 96) * 0.5 + ds + rng.normal(0, 0.6) - 0.8 * (h % 12)
            if zona == "C" and 120 <= i <= 135:  # pendingin bermasalah
                suhu += 6 + 3 * np.sin(np.pi * (i - 120) / 15)
            rows.append((t.strftime("%Y-%m-%d %H:%M"), zona, round(suhu, 1),
                         round(udara, 1), round(tanah, 1)))
    return pd.DataFrame(rows, columns=["waktu", "zona", "suhu",
                                       "kelembapan_udara", "kelembapan_tanah"])


if __name__ == "__main__":
    df = generate()
    df.to_csv("data/sensor_log.csv", index=False)
    print("Tersimpan: data/sensor_log.csv", df.shape)
