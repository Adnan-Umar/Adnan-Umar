# Project Memory

**Project:** Md Adnan Umar — GitHub Profile  
**Format:** Append-only log of key facts, discoveries, and decisions  
**Last Updated:** 2026-07-22

---

## Environment

- **OS:** Windows 11
- **Python:** 3.13.2 at `C:\Python313\python.exe`
- **Always invoke as:** `& "C:\Python313\python.exe"` in PowerShell
- **Repo root:** `d:\AllProgram\LEARN\Github-Profile\Adnan-Umar\`
- **Git remote:** `https://github.com/Adnan-Umar/Adnan-Umar.git`
- **Branch:** `main`

---

## Key Discoveries

### GitHub SVG Rendering (2026-07-22)
GitHub serves SVGs through its Camo CDN proxy which:
- Strips `<script>`, `<style>`, and inline `style=` silently
- Blocks all external HTTP/HTTPS references inside SVGs
- Passes through: `<animate>`, `<animateTransform>`, SVG filters, masks, clipPaths
- Therefore: all animation → SMIL only; all images → base64 data URI

### rembg / onnxruntime (2026-07-22)
- `rembg` installed but missing `onnxruntime` backend
- Fixed by: `pip install "rembg[cpu]"` (installs onnxruntime automatically)
- First run downloads `u2net.onnx` (~176 MB) to `C:\Users\adnan\.u2net\`
- Subsequent runs are instant (model cached)

### Python PATH conflict (2026-07-22)
- `python` command in PowerShell resolves to Windows Store stub, not CPython 3.13
- `C:\Python313\python.exe` is the correct path for all scripts
- All workflow YAML must use `python` (GitHub runners resolve correctly)

### Contribution data all zeros (2026-07-22)
- `fetch_contributions.py` (old version) returned all zeros
- Root cause: GitHub HTML changed; `td[data-date]` now needed instead of `rect[data-date]`
- Fixed in new `fetch_contributions.py` with multi-selector fallback strategy

### PowerShell multiline string limitation
- PowerShell cannot pass multiline strings to `-c` flag reliably
- Solution: always write to a `.py` file and run `python script.py`

---

## Profile Data

```
Name:      Md Adnan Umar
Role:      Software Engineer
Location:  India
Education: B.Tech CSE, Final Year
Email:     adnanmd0786@gmail.com
Portfolio: https://adnan-portfolio-lykp.onrender.com/
LinkedIn:  https://linkedin.com/in/adnan--umar
GitHub:    https://github.com/Adnan-Umar
X:         https://x.com/Adnan__Umar
Instagram: https://instagram.com/_adnan__umar_
```

---

## Asset Sizes (current)

| File | Size |
|:---|:---|
| `dark.svg` | 141.7 KB |
| `light.svg` | 141.7 KB |
| `info-card.svg` | 133.2 KB |
| `contrib-heatmap.svg` | 65.9 KB |
| `scripts/pic-b64.txt` | 114 KB |

---

## Important File Notes

- `scripts/pic-b64.txt` is 116,706 chars — reading it takes ~50ms; don't do it in a loop
- `make_info_card.py` reads `scripts/pic-b64.txt`; falls back to extracting base64 from existing `info-card.svg` if the txt file is missing
- `prep_photo.py` prepares photos for ASCII conversion only (not used by hero SVGs)
- `info-card.svg` is canonical; regenerate with `python scripts/make_info_card.py`

---

## Workflow Notes

- `update-profile.yml` uses `[skip ci]` in commit message — prevents infinite Action loops
- Snake workflow writes to an `output` branch, not `main`
- `GITHUB_TOKEN` is the only secret needed — no PAT required for this setup
