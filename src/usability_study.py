"""Analisis uji usability: success rate, task time, dan skor SUS.

Membandingkan dua rancangan dasbor:
  - "Lama"  : dasbor padat tanpa pengelompokan dan tanpa filter
  - "UCD"   : dasbor pada repositori ini (Overview First, Zoom and Filter, Details-on-Demand)

PENTING: data/usability_results.csv dan data/sus_responses.csv yang dibuat otomatis
adalah DATA CONTOH (simulasi) agar skrip bisa dijalankan. Ganti dengan hasil uji nyata
(8 sampai 10 partisipan sudah cukup untuk uji usability kualitatif) dengan kolom sama.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TASKS = {
    "T1": "Lihat status terkini kelembapan tanah",
    "T2": "Temukan zona yang bermasalah",
    "T3": "Saring 24 jam terakhir untuk zona B",
    "T4": "Ekspor data ke CSV",
}
RES, SUS = "data/usability_results.csv", "data/sus_responses.csv"


def simulate(seed=11, n=8):
    rng = np.random.default_rng(seed)
    rows, sus = [], []
    base = {"Lama": {"T1": (22, .85), "T2": (48, .65), "T3": (70, .45), "T4": (55, .55)},
            "UCD":  {"T1": (9, .98),  "T2": (15, .95), "T3": (21, .93), "T4": (14, .95)}}
    for p in range(1, n + 1):
        for d in base:
            for t, (sec, ok) in base[d].items():
                rows.append((f"P{p:02d}", d, t, round(max(4, rng.normal(sec, sec * .2)), 1),
                             int(rng.random() < ok)))
            # 10 butir SUS (skala 1-5): butir ganjil positif, genap negatif
            good = 4.3 if d == "UCD" else 3.0
            ans = [int(np.clip(round(rng.normal(good if i % 2 == 0 else 6 - good, .7)), 1, 5))
                   for i in range(10)]
            sus.append((f"P{p:02d}", d, *ans))
    pd.DataFrame(rows, columns=["partisipan", "rancangan", "tugas", "waktu_detik", "berhasil"]).to_csv(RES, index=False)
    pd.DataFrame(sus, columns=["partisipan", "rancangan"] + [f"q{i}" for i in range(1, 11)]).to_csv(SUS, index=False)


def sus_score(r):
    q = [r[f"q{i}"] for i in range(1, 11)]
    return sum((v - 1) if i % 2 == 0 else (5 - v) for i, v in enumerate(q)) * 2.5


if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    if not (os.path.exists(RES) and os.path.exists(SUS)):
        simulate()
    r, s = pd.read_csv(RES), pd.read_csv(SUS)
    s["sus"] = s.apply(sus_score, axis=1)

    ringkas = r.groupby(["tugas", "rancangan"]).agg(
        success_rate=("berhasil", "mean"), waktu_rata2=("waktu_detik", "mean")).round(2).unstack()
    lines = ["RINGKASAN UJI USABILITY (data contoh/simulasi bila belum diganti data nyata)", "",
             "Per tugas:", ringkas.to_string(), "",
             "Keseluruhan:",
             r.groupby("rancangan").agg(success_rate=("berhasil", "mean"),
                                        waktu_rata2_detik=("waktu_detik", "mean")).round(2).to_string(), "",
             "Skor SUS (0-100; di atas 68 dianggap di atas rata-rata):",
             s.groupby("rancangan")["sus"].agg(["mean", "std"]).round(1).to_string()]
    out = "\n".join(lines)
    print(out)
    open("results/usability_summary.txt", "w", encoding="utf-8").write(out)

    fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
    for a, (col, ttl, df) in zip(ax, [("berhasil", "Success rate", r), ("waktu_detik", "Waktu tugas rata-rata (detik)", r)]):
        df.groupby(["tugas", "rancangan"])[col].mean().unstack().plot.bar(ax=a, rot=0, color=["#8a8f98", "#0b5cad"])
        a.set_title(ttl); a.set_xlabel("")
    s.groupby("rancangan")["sus"].mean().plot.bar(ax=ax[2], rot=0, color=["#8a8f98", "#0b5cad"])
    ax[2].axhline(68, ls="--", c="k", lw=1); ax[2].set_title("Skor SUS (garis = 68)"); ax[2].set_xlabel("")
    plt.tight_layout(); plt.savefig("results/usability_comparison.png", dpi=130)
