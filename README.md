# FieldShift — Agricultural Digital Twin (Prototype)

A farmer-centered decision-support prototype inspired by NASA Space Apps Challenge:
- Earth Memory: climate history charts
- Soil Debt: experimental environmental-pressure proxy
- What If Lab: rotation scenario comparison
- Farm Time Machine: past / present / future scenario tabs
- Why Not?: transparent assumptions and limitations

## Run locally
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. `python -m venv .venv`
4. Activate it:
   - Windows: `.venv\\Scripts\\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. `streamlit run app.py`

## NASA data
Enable **Fetch live NASA POWER data** in the sidebar. The app requests monthly:
- T2M (2-meter air temperature)
- PRECTOTCORR (corrected precipitation)
- ALLSKY_SFC_SW_DWN (solar radiation)

If internet/API access fails, it falls back to clearly labeled illustrative synthetic data.
No API key is required for NASA POWER point API.

## Important scientific limitations
This is an MVP/demo, not a validated agronomic model.
- Demo climate values are synthetic and must never be described as NASA observations.
- The Soil Debt / environmental pressure index is an experimental proxy, not soil health.
- Rotation scores are transparent heuristics, not calibrated yield forecasts or recommendations.
- SMAP/Landsat/SoilGrids are described in project plans but not yet integrated in this code.
- Crop attributes and weights must be validated by Moroccan agronomists and local sources.
- Satellite and gridded products do not replace field measurements or soil tests.

## Next integrations
1. NASA SMAP soil-moisture time series (Earthdata access/product selection).
2. Landsat surface reflectance → cloud masking → NDVI time series.
3. SoilGrids/WCS or local soil laboratory data.
4. Local crop calendars, water requirements, rotation constraints, market and pest data.
5. Calibrated multi-criteria scoring and uncertainty reporting.

## Project narrative
**FieldShift** gives farms a memory and farmers a sandbox: inspect environmental history, understand pressure signals, and compare rotation scenarios with transparent evidence and limitations.
