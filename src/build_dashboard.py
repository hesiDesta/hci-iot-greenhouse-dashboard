"""Menyisipkan data CSV ke src/template.html -> docs/index.html (satu berkas, offline)."""
import json
import pandas as pd

df = pd.read_csv("data/sensor_log.csv")
data = df.to_dict(orient="records")
html = open("src/template.html", encoding="utf-8").read()
html = html.replace("/*__DATA__*/[]", json.dumps(data, ensure_ascii=False))
open("docs/index.html", "w", encoding="utf-8").write(html)
print(f"docs/index.html dibuat dari {len(data)} baris data.")
