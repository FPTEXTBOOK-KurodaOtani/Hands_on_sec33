# BCC Li and Na Band Structure and Fermi Surface Calculation with Quantum ESPRESSO

This directory contains input files and a shell script for calculating the electronic band structure and Fermi surface of BCC Li using Quantum ESPRESSO.
The BCC Na also can be calculated using the same workflow.


The workflow consists of:

1. SCF calculation
2. Band-structure calculation along a high-symmetry k-path
3. Band post-processing using `bands.x`
4. NSCF calculation on a dense automatic k-point mesh
5. Fermi-velocity file generation using `fermi_velocity.x`
6. Visualization of `vfermi.frmsf` with FermiSurfer

Quantum ESPRESSO provides `fermi_velocity.x` to generate FermiSurfer input files from `pw.x` results, and the generated file is typically named `vfermi.frmsf`. ([Quantum Espresso][1])

## Required Files

Prepare the following input files:

```text
pw_BCC_Li_SCF.in
pw_BCC_Li_BAND.in
bands.in
pw_BCC_Li_NSCF.in
```

## Run Script

Create a shell script, for example `run_BCC_Li.sh`.

```bash
#!/bin/bash

# Quantum ESPRESSO executable directory
QEBIN="/yourdir/espresso-7.1-1/bin"

# =========================
# 1. SCF calculation
# =========================
$QEBIN/pw.x < pw_BCC_Li_SCF.in > pw_BCC_Li_SCF.out

# =========================
# 2. Band calculation
# =========================
# Calculate eigenvalues along the high-symmetry k-path.
$QEBIN/pw.x < pw_BCC_Li_BAND.in > pw_BCC_Li_BAND.out

# =========================
# 3. Band post-processing
# =========================
# This generates band data files such as *.dat and *.gnu.
$QEBIN/bands.x < bands.in > bands.out


# =========================
# 4. NSCF calculation for Fermi-surface analysis
# =========================
# The NSCF calculation should be performed using an automatic dense k-point mesh.
$QEBIN/pw.x < pw_BCC_Li_NSCF.in > pw_BCC_Li_NSCF.out

# =========================
# 5. Generate Fermi velocity file for FermiSurfer
# =========================
# This creates vfermi.frmsf.
$QEBIN/fermi_velocity.x -in pw_BCC_Li_NSCF.in > pw_BCC_Li_NSCF_fermiv.out
```

Run it with:

```bash
bash run_BCC_Li.sh
```

or submit it through your SLURM job script.

## Important Notes

The `SCF` calculation determines the self-consistent charge density.

The `BAND` calculation uses the SCF charge density and calculates eigenvalues along the selected high-symmetry path.

The `bands.x` post-processing step reads the band calculation results and generates files for plotting the band structure.

The `NSCF` calculation for Fermi-surface visualization should use a dense `K_POINTS automatic` mesh, not the line-mode k-path used for the band plot. QE documentation states that `fermi_velocity.x` should be used after a `pw.x` calculation with automatic k-points. ([Quantum Espresso][1])

For `fermi_velocity.x`, the number of k-point parallelization pools should be 1 or unspecified. The FermiSurfer tutorial also shows execution with `-npool 1` and states that `vfermi.frmsf` is generated afterward. ([mitsuaki1987.github.io][2])

## Band Plot

After running:

```bash
$QEBIN/bands.x < bands.in > bands.out
```

the band data can be plotted using gnuplot or Python. For example, `bands.x` may generate a file such as:

```text
Li.bands.dat.gnu
```

This file can be used directly for band plotting.
It can be plotted by using band_plot.py.

## Fermi Surface Plot with FermiSurfer

After running:

```bash
$QEBIN/fermi_velocity.x -in pw_BCC_Li_NSCF.in > pw_BCC_Li_NSCF_fermiv.out
```

the following file should be generated:

```text
vfermi.frmsf
```

This file can be opened with FermiSurfer:

```bash
fermisurfer vfermi.frmsf
```

FermiSurfer is a visualization tool for Fermi surfaces and can display Fermi surfaces colored by scalar quantities such as the magnitude of the Fermi velocity. ([mitsuaki1987.github.io][3])

## Online Visualization

The file `vfermi.frmsf` can also be visualized using FermiSurfer on Web. The web version allows users to select a local FRMSF file from the browser and display the Fermi surface online. Note that the online version supports local FRMSF files, while BXSF is not supported in the web interface. ([mitsuaki1987.github.io][4])

Therefore, after generating:

```text
vfermi.frmsf
```

you can either:

```bash
fermisurfer vfermi.frmsf
```

or upload/open the file in FermiSurfer on Web.

## Expected Output Files

Typical output files are (in reference):

```text
pw_BCC_Li_SCF.out
pw_BCC_Li_BAND.out
bands.out
pw_BCC_Li_NSCF.out
pw_BCC_Li_NSCF_fermiv.out
vfermi.frmsf
```

The most important file for the Fermi-surface plot is:

```text
vfermi.frmsf
```

Open this file with FermiSurfer to visualize the BCC Li Fermi surface.



[1]: https://www.quantum-espresso.org/Doc/pp_user_guide/node10.html "4.5 Color plot of the Fermi velocity and the orbital character on Fermi surfaces"
[2]: https://mitsuaki1987.github.io/fermisurfer/en/_build/html/qe.html "Tutorial with Quantum ESPRESSO — fermisurfer 2.4.0 documentation"
[3]: https://mitsuaki1987.github.io/fermisurfer/ "FermiSurfer Web page"
[4]: https://mitsuaki1987.github.io/fermisurfer/en/_build/html/onweb.html "FermiSurfer on Web — fermisurfer 2.4.0 documentation"