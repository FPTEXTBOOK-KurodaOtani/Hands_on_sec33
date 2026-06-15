# 3-2. Al_Si_BAND

This directory contains example band-structure calculations for simple semiconductors and metals using Quantum ESPRESSO.

The current examples are organized into three directories:

```text
Al/
Si/
GaAs/
```

The main purpose of this section is to confirm the standard procedure for band-structure calculations in Quantum ESPRESSO and to check the k-point path used for band plotting.

## Purpose

This workflow performs band calculations for:

- FCC Al,
- diamond-structure Si,
- GaAs (appendix).

For the FCC cases, the script `fcc_bandspass.py` is used to check and generate the high-symmetry k-point path used in the band-structure calculation.

The basic Quantum ESPRESSO workflow is:

1. SCF calculation,
2. band calculation along a high-symmetry k-path,
3. post-processing using `bands.x`,
4. plotting using a Python script.

The Al example is used as the main reference workflow. The Si and GaAs examples follow the same basic procedure as the Al example.

## FCC k-path check

The script

```bash
python3 fcc_bandspass.py
```

is used to check the FCC band path.

This script converts standard FCC fractional k-point coordinates into the `crystal_b` coordinates used in the present Quantum ESPRESSO input.

The target path is:

```text
L -> Gamma -> X -> U -> Gamma
```

The script performs the following operations:

1. Defines high-symmetry points in the standard FCC convention.
2. Converts fractional values such as `1/4`, `1/2`, and `5/8` into floating-point values.
3. Converts the standard FCC fractional coordinates to Cartesian reciprocal coordinates.
4. Rotates the Cartesian coordinates to match the orientation used in the present QE input.
5. Converts the rotated Cartesian coordinates into QE `crystal_b` coordinates.
6. Calculates cumulative x coordinates for band plotting.
7. Prints the `K_POINTS crystal_b` block for the QE band calculation.
8. Prints the `xticks` and `xlabels` used for plotting the band structure.


The last Gamma point is set to `(1, 1, 1)`. This is an equivalent Gamma point `(0, 0, 0)` translated by a reciprocal lattice vector. It is used to represent the final U -> Gamma segment continuously in the extended-zone scheme.

The important output from this script is the `K_POINTS crystal_b` section, for example:

```text
K_POINTS crystal_b
...
```

This section should be copied or compared with the `K_POINTS` section in the QE band input file.

The script also prints the x-axis positions for plotting:

```python
xticks = [...]
xlabels = [...]
```

These values are used in the band-plotting script.

## Quantum ESPRESSO band calculation workflow



### 1. SCF calculation

```bash
$QEBIN/pw.x < pw_al_SCF.in > pw_al_SCF.out
```

The SCF calculation determines the self-consistent charge density.

After this calculation, the Fermi energy should be checked from `pw_al_SCF.out`.

For example:

```bash
grep -i "Fermi" pw_al_SCF.out
```

The Fermi energy is required when plotting the band structure relative to the Fermi level.

### 2. Band calculation

```bash
$QEBIN/pw.x < pw_al_BANDS.in > pw_al_BANDS.out
```

This calculation uses the charge density obtained from the SCF calculation and evaluates the Kohn-Sham eigenvalues along the selected high-symmetry k-point path.

The k-point path should be checked using `fcc_bandspass.py`.

### 3. Post-processing with `bands.x`

```bash
$QEBIN/bands.x < bands.in > bands.out
```

The `bands.x` post-processing program reads the band calculation result and generates the band data file.


Please note that bands.out fails to find 
the U point as high symmetric point.


For the Al example, the generated file is:

```text
Al.band.gnu
```

This file is used for plotting the band structure.

### 4. Band plotting

The band structure is plotted using:

```bash
python3 band_plot_FCC.py
```

The script reads:

```text
Al.band.gnu
```

and generates the band diagram.

The Fermi energy obtained from `pw_al_SCF.out` should be used to shift the energy axis so that the Fermi level is located at 0 eV.

## Expected directory structure

A typical directory structure is:

```text
Al_Si_BAND/
├── Al/
│   ├── fcc_bandspass.py
│   ├── pw_al_SCF.in
│   ├── pw_al_SCF.out
│   ├── pw_al_BANDS.in
│   ├── pw_al_BANDS.out
│   ├── bands.in
│   ├── bands.out
│   ├── Al.band.gnu
│   └── band_plot_FCC.py
├── Si/
│   └── ...
└── GaAs/
    └── ...
```

## Notes for FCC Al

For FCC, the band path should be carefully checked because the coordinates depend on the reciprocal-lattice convention and on the orientation used in the QE input.

The script `fcc_bandspass.py` explicitly handles this conversion.

The main functions are:

- `frac_to_float(x)`: converts fractional strings such as `1/4` into floating-point numbers.
- `make_vec(values)`: creates a NumPy vector from fractional strings or numbers.
- `fcc_standard_to_cart(k_std)`: converts standard FCC fractional coordinates into Cartesian reciprocal coordinates.
- `rotate_to_qe_orientation(k_cart)`: rotates the standard Cartesian orientation into the orientation used in the present QE input.
- `cart_to_qe_crystal_b(k_cart)`: converts Cartesian reciprocal coordinates into QE `crystal_b` coordinates.
- `standard_to_qe_crystal_b(k_std)`: performs the full conversion from standard FCC coordinates to QE `crystal_b` coordinates.
- `calc_xcoords(cart_points)`: calculates the cumulative x-axis coordinates for band plotting.

The resulting path is:

```text
L -> Gamma -> X -> U -> Gamma
```

where `Gamma` is the Brillouin-zone center.

## Checklist

Before plotting the band structure, check the following points:

1. The SCF calculation finished normally.
2. The band calculation finished normally.
3. `bands.x` generated `Al.band.gnu`.
4. The Fermi energy was obtained from `pw_al_SCF.out`.
5. The k-point path in `pw_al_BANDS.in` is consistent with the output of `fcc_bandspass.py`.
6. The x-axis labels in `band_plot_FCC.py` are consistent with the path:
   ```text
   L -> Gamma -> X -> U -> Gamma
   ```

## Summary

The complete workflow for the Al band calculation is:

```bash
$QEBIN/pw.x    < pw_al_SCF.in   > pw_al_SCF.out
$QEBIN/pw.x    < pw_al_BANDS.in > pw_al_BANDS.out
$QEBIN/bands.x < bands.in       > bands.out
python3 band_plot_FCC.py
```

The file `Al.band.gnu` generated by `bands.x` is used for plotting.

The Fermi energy should be checked from `pw_al_SCF.out` and used as the reference energy for the band diagram.
