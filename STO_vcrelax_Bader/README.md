# 3-4. STO_vcrelax_Bader

This directory contains Quantum ESPRESSO calculations for SrTiO3 using variable-cell relaxation (`vc-relax`) and Bader charge analysis.

The calculations compare several exchange-correlation functionals:

- LDA
- GGA-PBE
- GGA-PBEsol

The directory is organized as:

```text
STO_vcrelax_Bader/
├── STO_LDA/
├── STO_PBE/
└── STO_PBESOL/
```

The Bader charge analysis is performed only for the GGA-PBE calculation in `STO_PBE`.

## Purpose

The purpose of this workflow is to:

1. optimize the lattice constant and internal atomic positions of SrTiO3 using `vc-relax`,
2. compare the relaxed structures obtained with LDA, GGA-PBE, and GGA-PBEsol,
3. check that the stress and atomic forces are sufficiently small after relaxation,
4. perform Bader charge analysis for the GGA-PBE result.

## Variable-cell relaxation

The first step is to perform a `vc-relax` calculation for SrTiO3.

The `vc-relax` calculation optimizes both:

- the unit-cell shape and volume,
- the atomic positions.

This calculation is performed separately in the following directories:

```text
STO_LDA/
STO_PBE/
STO_PBESOL/
```

Each directory corresponds to a different exchange-correlation functional.

## Important note on QE `vc-relax`

When using `vc-relax` in Quantum ESPRESSO, it is important to check the final output carefully.

After the structural optimization is judged to be converged, Quantum ESPRESSO performs an additional calculation using the final relaxed structure. Therefore, the total energy, stress, and atomic forces can change slightly after the convergence message.

For this reason, the final total energy, stress tensor, and atomic forces should be checked at the end of the output file, not only at the geometry-optimization convergence step.

In particular, confirm that:

- the stress is sufficiently small,
- the forces acting on atoms are sufficiently small,
- the final structure is physically reasonable,
- the final total energy corresponds to the final relaxed structure.

## Bader charge analysis

Bader charge analysis is performed only for the GGA-PBE calculation:

```text
STO_PBE/
```

Before performing the Bader analysis, install the Bader charge analysis program.


- Bader charge analysis program:
  https://theory.cm.utexas.edu/bader/
- Henkelman group Bader analysis page:
  https://theory.cm.utexas.edu/henkelman/research/bader/

The Bader program reads charge-density files, such as Gaussian CUBE files, and outputs the charge associated with each atom and the Bader volumes.


For example, after installing the executable, it can be called as:

```bash
/yourdir/bader
```

## Bader calculation workflow

The Bader charge analysis requires both the valence charge density and the reference total charge density.

The calculation is performed in the following order:

```bash
$QEBIN/pw.x < pw_STO.in > pw_STO.out
$QEBIN/pw.x < pw_STO_bader.in > pw_STO_bader.out
$QEBIN/pp.x < STO_all_pp.in > STO_all_pp.out
$QEBIN/pp.x < STO_val_pp.in > STO_val_pp.out
/yourdir/bader STO_valence.cube -ref STO_all.cube > BADER.out
```

The final command produces:

```text
ACF.dat
```

The `CHARGE` column in `ACF.dat` should be checked.

## Why both all-electron and valence charge densities are needed

In a pseudopotential calculation, the explicitly calculated charge density is usually the valence charge density. However, Bader charge analysis requires a reliable charge-density topology to define the atomic basins.

Therefore, two cube files are used:

```text
STO_valence.cube
STO_all.cube
```

The command

```bash
/yourdir/bader STO_valence.cube -ref STO_all.cube > BADER.out
```

means that the Bader volumes are determined using the reference charge density `STO_all.cube`, while the charge integrated in each Bader basin is taken from `STO_valence.cube`.

This is useful when using pseudopotentials because the valence charge can be analyzed while the reference density gives a better description of the atomic charge-density topology.

## Core-electron correction

The `CHARGE` column in `ACF.dat` corresponds to the integrated valence charge in each Bader basin.

To estimate the atomic charge state, the core-electron contribution must be considered.

The number of core electrons is estimated from the atomic number and the number of valence electrons included in the pseudopotential.

For SrTiO3, the core-electron numbers used here are:

```text
O   :  2   1s
Ti  : 10   1s + 2s + 2p
Sr  : 28   1s + 2s + 2p + 3s + 3p + 3d
```

These values are referred to as `CORE-ELECTRON`.

## Valence electrons from pseudopotentials

The number of valence electrons should be checked from the pseudopotential file.

For example, in the Ti pseudopotential file:

```text
ti_pbe_v1.4.uspp.F.UPF
```

the following valence states are included:

```text
nl pn  l   occ               Rcut            Rcut US             E pseu
3S  3  0  2.00      0.00000000000      1.80000000000     -5.55524566700
3P  3  1  6.00      0.00000000000      1.80000000000     -3.78919170400
4S  4  0  2.00      0.00000000000      1.80000000000     -0.87721941400
3D  3  2  1.00      0.00000000000      1.80000000000     -1.16623785300
</PP_INFO>
```

Therefore, the Ti pseudopotential includes:

```text
3s2 3p6 4s2 3d1
```

which gives 11 valence electrons.

Since the atomic number of Ti is 22, the number of core electrons is:

```text
22 - 11 = 10
```

## Charge evaluation

For each atom, the effective charge can be estimated using:

```text
CHARGE = ATOMIC_NUMBER - CORE_ELECTRON - BADER_VALENCE_CHARGE
```

where:

- `ATOMIC_NUMBER` is the nuclear charge,
- `CORE_ELECTRON` is the number of core electrons,
- `BADER_VALENCE_CHARGE` is the value from the `CHARGE` column in `ACF.dat`.

For Ti, an example is:

```text
# ACF.dat   CORE-ELECTRON      ATOMIC_NUMBER     CHARGE
Ti 9.912879 10 (1s+2s+2p)      22                2.087121
```

This means:

```text
CHARGE = 22 - 10 - 9.912879
       = 2.087121
```

Thus, the Bader charge analysis gives an effective Ti charge of approximately:

```text
Ti : +2.087
```

## Files used for Bader analysis

Typical files for the PBE Bader analysis are:

```text
pw_STO.in
pw_STO.out
pw_STO_bader.in
pw_STO_bader.out
STO_all_pp.in
STO_all_pp.out
STO_val_pp.in
STO_val_pp.out
STO_all.cube
STO_valence.cube
BADER.out
ACF.dat
```

## Checklist

Before discussing the Bader charges, check the following points:

1. The `vc-relax` calculation has converged.
2. The final stress is sufficiently small.
3. The final atomic forces are sufficiently small.
4. The final relaxed structure was used for the Bader calculation.
5. The SCF calculation for Bader analysis finished normally.
6. Both `STO_all.cube` and `STO_valence.cube` were generated by `pp.x`.
7. The Bader program generated `ACF.dat`.
8. The `CHARGE` column in `ACF.dat` was checked.
9. The core-electron correction was applied when estimating atomic charges.

## Summary

This workflow performs `vc-relax` calculations for SrTiO3 using LDA, GGA-PBE, and GGA-PBEsol.

The Bader charge analysis is performed only for the GGA-PBE calculation in `STO_PBE`.

The Bader charge is evaluated using the valence charge from `ACF.dat` together with the core-electron correction:

```text
CHARGE = ATOMIC_NUMBER - CORE_ELECTRON - BADER_VALENCE_CHARGE
```

The final stress, atomic forces, and total energy from the converged `vc-relax` output should always be checked carefully.
