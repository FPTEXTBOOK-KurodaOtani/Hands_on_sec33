# FeO_plusU

This directory contains Quantum ESPRESSO calculations for antiferromagnetic FeO with and without the Hubbard \(+U\) correction.

The purpose of this exercise is to understand how DFT+\(U\) calculations are performed for FeO and why the initial occupation of the Hubbard manifold must be controlled carefully.

## Directory structure

The directory contains the following subdirectories:

```text
FeO_plusU/
├── FeOGGA/
├── FeOpU/
└── FeOpU_false/
```

The intended meaning is:

- `FeOGGA`: GGA calculation without \(+U\).
- `FeOpU`: GGA+\(U\) calculation with a controlled initial Hubbard occupation.
- `FeOpU_false`: GGA+\(U\) calculation without the desired initial occupation control, or with an intentionally different setting, used for comparison.

## Purpose

FeO is an antiferromagnetic transition-metal oxide. The Fe \(3d\) states are localized and are not always described well by a standard GGA calculation.

Therefore, a Hubbard \(+U\) correction is introduced for the Fe \(3d\) states.

However, FeO is a difficult case because different local minima can appear depending on the initial occupation of the Fe \(3d\) orbitals. If the initial occupation is not controlled, the self-consistent calculation can converge to an undesired metastable state.

## Important note on the FeO occupation state

Antiferromagnetic FeO has \(D_{3d}\) symmetry because of the magnetic ordering.

Under this symmetry, the Fe \(3d\) levels are split, and a singly degenerate \(a_{\rm 1g}\) orbital becomes the occupied state.

This system is special: if the initial occupation is not specified properly, the calculation may converge to another unstable or metastable electronic state instead of the desired antiferromagnetic insulating state.

For this reason, the initial occupation of the Hubbard occupation matrix is explicitly specified in the \(+U\) calculation.

## DFT+\(U\) syntax in Quantum ESPRESSO version 7.0 and later

In Quantum ESPRESSO version 7.0 and later, the recommended syntax for DFT+\(U\) uses the `HUBBARD` card.

For example:

```text
HUBBARD (ortho-atomic)
 U Fe1-3d 4.0
 U Fe2-3d 4.0
```

Here:

- `Fe1` and `Fe2` are two different Fe atomic species used to represent the two antiferromagnetic sublattices.
- `3d` specifies that the Hubbard correction is applied to the Fe \(3d\) manifold.
- `4.0` is the Hubbard \(U\) value in eV.

The `ortho-atomic` Hubbard projector uses Lowdin-orthogonalized atomic orbitals. This option is recommended when possible because it avoids applying the Hubbard correction twice in the orbital-overlap region.

## Initial Hubbard occupation

The following input variables are used to control the initial Hubbard occupation:

```fortran
starting_ns_eigenvalue(3,2,2)=1.0,
starting_ns_eigenvalue(3,1,3)=1.0,
```

The meaning of

```fortran
starting_ns_eigenvalue(m, ispin, ityp)
```

is:

- `m`: index of the eigenvalue of the Hubbard occupation matrix,
- `ispin`: spin index,
  - `1` = spin up,
  - `2` = spin down,
- `ityp`: atomic species index as defined in `ATOMIC_SPECIES`.

Therefore,

```fortran
starting_ns_eigenvalue(3,2,2)=1.0
```

sets the third eigenvalue of the Hubbard occupation matrix to 1.0 for spin down of atomic species 2.

Similarly,

```fortran
starting_ns_eigenvalue(3,1,3)=1.0
```

sets the third eigenvalue of the Hubbard occupation matrix to 1.0 for spin up of atomic species 3.

In a typical antiferromagnetic FeO setup, species 2 and species 3 correspond to two inequivalent Fe atoms with opposite spin directions. Therefore, these settings are used to initialize the desired orbital occupation on the two antiferromagnetic Fe sublattices.

This does not directly fix one matrix element of the occupation matrix. Instead, it modifies an eigenvalue of the initial Hubbard occupation matrix in the first iteration. The final occupation matrix should always be checked from the output.

## Order of the \(d\)-orbital occupation matrix

The Fe \(3d\) occupation matrix is printed as a \(5 \times 5\) matrix.

In this example, the order of the real \(d\)-orbital basis is:

```text
1: dz2
2: dzx
3: dzy
4: dx2-y2
5: dxy
```

The printed eigenvectors are expressed as columns in this basis.

For example, if the fifth eigenvector has components mainly in the `dzx`, `dzy`, and `dxy` rows, that eigenstate is a linear combination of those real \(d\) orbitals.

The diagonal entries of the occupation matrix before diagonalization approximately represent the occupations projected onto these real \(d\)-orbital basis functions. The off-diagonal entries represent orbital mixing.

## Example: Hubbard occupation output

A typical output block is:

```text
=================== HUBBARD OCCUPATIONS ===================
------------------------ ATOM    3 ------------------------
Tr[ns(  3)] (up, down, total) =   4.91218  1.23018  6.14236
Atomic magnetic moment for atom   3 =   3.68199
SPIN  1
eigenvalues:
  0.977  0.977  0.977  0.990  0.990
eigenvectors (columns):
 -0.000 -0.021 -0.005 -0.571 -0.821
  0.577 -0.571  0.583 -0.008  0.016
  0.577 -0.219 -0.786  0.018 -0.002
  0.000 -0.005  0.021  0.821 -0.571
 -0.577 -0.791 -0.203  0.010  0.015
occupation matrix ns (before diag.):
  0.990 -0.000 -0.000  0.000 -0.000
 -0.000  0.977 -0.000 -0.000  0.000
 -0.000 -0.000  0.977  0.000  0.000
  0.000 -0.000  0.000  0.990 -0.000
 -0.000  0.000  0.000 -0.000  0.977
SPIN  2
eigenvalues:
  0.047  0.047  0.068  0.068  1.000
eigenvectors (columns):
 -0.216 -0.910 -0.346 -0.076  0.000
  0.210 -0.199  0.232  0.728 -0.577
 -0.277 -0.083  0.514 -0.564 -0.577
  0.910 -0.216  0.076 -0.346 -0.000
 -0.067 -0.281  0.746  0.163  0.577
occupation matrix ns (before diag.):
  0.049 -0.003 -0.003  0.000 -0.006
 -0.003  0.377  0.311 -0.005 -0.311
 -0.003  0.311  0.377  0.005 -0.311
  0.000 -0.005  0.005  0.049 -0.000
 -0.006 -0.311 -0.311 -0.000  0.377
```

This block should be checked carefully.

### Trace of the occupation matrix

```text
Tr[ns(3)] (up, down, total) = 4.91218  1.23018  6.14236
```

This line gives the number of electrons in the Fe \(3d\) Hubbard manifold for atom 3.

The spin-up channel has approximately 4.91 electrons, and the spin-down channel has approximately 1.23 electrons.

### Atomic magnetic moment

```text
Atomic magnetic moment for atom 3 = 3.68199
```

This value is approximately the difference between the spin-up and spin-down occupations:

```text
4.91218 - 1.23018 = 3.68199
```

This confirms that atom 3 carries a large local magnetic moment.

### Eigenvalues

The eigenvalues of the occupation matrix represent the occupation numbers of the natural localized \(d\)-like states.

For example, in spin 2:

```text
0.047  0.047  0.068  0.068  1.000
```

one state is almost fully occupied, while the other four states are nearly empty.

This is the expected minority-spin occupation pattern for the desired FeO \(+U\) solution.

### Eigenvectors

The eigenvectors show the orbital character of each natural localized state.

Each column corresponds to one eigenvalue, and each row corresponds to one real \(d\)-orbital basis function in the order:

```text
dz2, dzx, dzy, dx2-y2, dxy
```

Thus, the eigenvector associated with the eigenvalue `1.000` indicates the orbital character of the occupied minority-spin state.

## PDOS calculation

After the SCF or \(+U\) calculation, a non-self-consistent calculation is performed for PDOS analysis:

```bash
$QEBIN/pw.x < pw_FeO_NSCF.in > pw_FeO_NSCF.out
```

Then projected DOS is calculated using `projwfc.x`:

```bash
$QEBIN/projwfc.x < pdos.in > pdos.out
```

The total projected DOS file is:

```text
FeO.pdos_tot
```

A plotting script is provided:

```text
plot_FeO_pdos_tot.py
```

Run it as:

```bash
python3 plot_FeO_pdos_tot.py
```

The script reads `FeO.pdos_tot` and generates a plot of the total DOS.

## Checklist

Before discussing the final \(+U\) result, check the following points:

1. The antiferromagnetic Fe sublattices are defined using different Fe species, such as `Fe1` and `Fe2`.
2. The Hubbard \(U\) is applied to both Fe sublattices.
3. For QE 7.0 or later, the `HUBBARD (ortho-atomic)` syntax is used.
4. The initial occupation is controlled using `starting_ns_eigenvalue`.
5. The `HUBBARD OCCUPATIONS` block is inspected after convergence.
6. The desired minority-spin occupation pattern is obtained.
7. The local magnetic moments are consistent with the antiferromagnetic state.
8. The PDOS calculation is performed using `pw_FeO_NSCF.in` and `projwfc.x`.
9. `FeO.pdos_tot` is plotted using the provided Python script.
