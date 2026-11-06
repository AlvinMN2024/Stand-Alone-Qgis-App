# Stand-alone PyQGIS application

This is a small desktop example that opens a QGIS project and provides pan, zoom, and coordinate capture tools. The application code is updated for the QGIS 4.x Qt 6 bindings (`qgis.PyQt`). Run it with the Python interpreter and environment belonging to the QGIS installation; do not install a separate PyQt package into that environment.

## Requirements

- QGIS 4.2.3 (or another QGIS 4.x release with the same Qt 6 API)
- Python provided by that QGIS installation
- The `data.gpkg` GeoPackage referenced by `StandAloneApp/project1.qgz`

The downloaded archive does not include `StandAloneApp/data.gpkg`. The project references layers in that file (`MunicipalityCentroids`, `PalCstPoly`, `Roads`, and `munipol`), so copy the original GeoPackage into `StandAloneApp/` before running. Without it, the project will open with missing layers.

## Run on Linux

Use the Python environment configured by your QGIS package. If QGIS is installed with a nonstandard prefix, set `QGIS_PREFIX_PATH` to that prefix before launching. The default prefix in the sample is `/usr`.

```sh
python3 StandAloneApp/StandAloneAppSample.py
```

For distributions where QGIS provides a launcher or environment setup script, launch through that environment so the QGIS Python modules and Qt libraries are on the search paths.
