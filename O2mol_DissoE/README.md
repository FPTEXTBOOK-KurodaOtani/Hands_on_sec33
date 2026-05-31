# O2 Molecular Dissociation Energy Calculation with Quantum ESPRESSO

This directory contains Quantum ESPRESSO input files for calculating the dissociation energy of an oxygen molecule, `O2`.

Calculations are performed for three exchange-correlation functionals:

```text
O_LDA
O_PBE
O_PBEsol
```

Each directory contains input files for:

```text
pw_O.in     # isolated oxygen atom
pw_O2.in    # oxygen molecule
```

The dissociation energy of the oxygen molecule is evaluated from the total energies as:

```math
D_{O_2} = 2E_O - E_{O_2}
```

where `E_O` is the total energy of an isolated oxygen atom and `E_O2` is the total energy of the oxygen molecule.

## Important Note for the Isolated Oxygen Atom

When calculating the isolated oxygen atom, the size and symmetry of the simulation cell must be chosen carefully.

The oxygen atom should be placed in a sufficiently large unit cell to avoid artificial interaction between periodic images. In this calculation, the following non-cubic cell is used:

```pw
CELL_PARAMETERS angstrom
7.0 0.0 0.0
0.0 7.5 0.0
0.0 0.0 8.0
```

This large cell helps reduce spurious interactions between neighboring oxygen atoms caused by periodic boundary conditions.

In addition, the unit cell is intentionally chosen to have lower symmetry. This is done to avoid convergence to an artificial local solution caused by the high symmetry of the cell. By slightly lowering the cell symmetry, the electronic structure calculation has more freedom to converge to a physically reasonable solution for the isolated oxygen atom.

## Spin-Polarized Calculation for O2

The oxygen molecule has a magnetic ground state, so spin-polarized calculations should be used.

For the `O2` calculation, the following settings are used:

```pw
nspin = 2,
starting_magnetization(1) = 0.8,
starting_magnetization(2) = 0.8,
```

Here, `nspin = 2` enables a spin-polarized calculation. The `starting_magnetization` values give initial magnetic moments to the oxygen atoms, which helps the calculation converge to the correct spin-polarized state.

If the two oxygen atoms are defined as separate atomic species, for example `O1` and `O2`, both species can be assigned the same oxygen pseudopotential while using separate starting magnetizations:

```pw
ATOMIC_SPECIES
O1  15.999  O.pz-n-kjpaw_psl.1.0.0.UPF
O2  15.999  O.pz-n-kjpaw_psl.1.0.0.UPF
```

Then the input can use:

```pw
starting_magnetization(1) = 0.8,
starting_magnetization(2) = 0.8,
```

## Run Script

The calculations can be executed using the following shell script:

```bash
#!/bin/sh

QEBIN="/yourdir/q-e/bin"

# Isolated oxygen atom calculation
$QEBIN/pw.x < pw_O.in > pw_O.out

# Oxygen molecule calculation
$QEBIN/pw.x < pw_O2.in > pw_O2.out
```

Save the script, for example, as:

```text
run.sh
```

and execute it:

```bash
sh run.sh
```

## Output Files

After running the script, the following output files are generated:

```text
pw_O.out
pw_O2.out
```

The total energies can be extracted from the output files using:

```bash
grep "!    total energy" pw_O.out
grep "!    total energy" pw_O2.out
```

The dissociation energy can then be calculated as:

```math
D_{O_2} = 2E_O - E_{O_2}
```

The same procedure should be repeated for `O_LDA`, `O_PBE`, and `O_PBEsol` to compare the functional dependence of the oxygen molecule dissociation energy.
