# 3-3. Fe_Ti_FormE

This directory contains Quantum ESPRESSO calculations for evaluating the formation energy of B2-structured FeTi.

The formation energy is calculated from reference calculations of elemental Fe and Ti and the total energy of B2 FeTi.

The main reference structures are:

- BCC Fe,
- HCP Ti,
- B2 FeTi.

## Directory structure

The directory is organized as follows:

```text
Fe_Ti_FormE/
├── Fe_BCC/
├── Fe_HCP/
├── FeTi_B2_PBE/
└── Ti_HCP_PBE/
```

The `Fe_BCC` directory contains calculations with different exchange-correlation functionals:

```text
Fe_BCC/
├── Fe_LDA/
├── Fe_PBE/
└── Fe_PBESOL/
```

For example:

```text
Fe_BCC/Fe_PBE/
└── pw_fe.in
```

## Purpose

The purpose of this workflow is to calculate the formation energy of B2 FeTi using first-principles total energies.

The basic idea is to compare the total energy of FeTi with the energies of elemental Fe and Ti in their reference structures:

```text
FeTi(B2) -> Fe(BCC) + Ti(HCP)
```

The formation energy is then evaluated from:

```text
Eform = E(FeTi_B2) - E(Fe_BCC) - E(Ti_HCP)
```

with proper normalization by the number of atoms or formula units.

## Important normalization note for BCC Fe

The input file

```text
Fe_BCC/Fe_PBE/pw_fe.in
```

uses a BCC Fe structure.

However, the BCC structure is written using the conventional cubic cell. Therefore, the calculation cell contains:

```text
2 Fe atoms
```

This point is important when calculating the formation energy.

The total energy obtained from this calculation is the energy of 2 Fe atoms. Therefore, the Fe reference energy per atom should be calculated as:

```text
E_Fe_per_atom = E_Fe_BCC_cell / 2
```

This per-atom energy must be used in the formation-energy calculation.

## Reference energies

### BCC Fe

For BCC Fe calculated with a conventional cell containing 2 atoms:

```text
E_Fe_per_atom = E_Fe_BCC_cell / 2
```

### HCP Ti

For HCP Ti, the number of atoms in the calculation cell must also be checked.

If the HCP Ti cell contains 2 atoms, then:

```text
E_Ti_per_atom = E_Ti_HCP_cell / 2
```

In general:

```text
E_Ti_per_atom = E_Ti_HCP_cell / N_Ti
```

where `N_Ti` is the number of Ti atoms in the HCP Ti calculation cell.

### B2 FeTi

The B2 FeTi structure contains one Fe atom and one Ti atom in the primitive CsCl-type cell.

If the FeTi calculation cell contains one FeTi formula unit, that is:

```text
1 Fe atom + 1 Ti atom
```

then:

```text
E_FeTi_per_formula_unit = E_FeTi_B2_cell
```

If a larger supercell is used, the total energy must be divided by the number of FeTi formula units:

```text
E_FeTi_per_formula_unit = E_FeTi_B2_cell / N_FeTi
```

where `N_FeTi` is the number of FeTi formula units in the cell.

## Formation energy formula

The formation energy per FeTi formula unit is:

```text
Eform = E_FeTi_per_formula_unit - E_Fe_per_atom - E_Ti_per_atom
```

Using the conventional BCC Fe cell with 2 atoms, this becomes:

```text
Eform = E_FeTi_per_formula_unit - E_Fe_BCC_cell / 2 - E_Ti_per_atom
```

If HCP Ti is also calculated using a 2-atom cell:

```text
Eform = E_FeTi_per_formula_unit - E_Fe_BCC_cell / 2 - E_Ti_HCP_cell / 2
```

The result is usually reported in:

```text
eV / formula unit
```

For FeTi, this is also equivalent to:

```text
eV / FeTi
```

## Example calculation flow

A typical workflow is:

1. Calculate BCC Fe.
2. Calculate HCP Ti.
3. Calculate B2 FeTi.
4. Extract the total energies from the Quantum ESPRESSO output files.
5. Normalize each total energy by the number of atoms or formula units.
6. Calculate the formation energy.

For example, for the PBE calculation:

```text
Fe_BCC/Fe_PBE/
Ti_HCP_PBE/
FeTi_B2_PBE/
```

The formation energy is evaluated as:

```text
Eform_PBE = E(FeTi_B2_PBE) - E(Fe_BCC_PBE per atom) - E(Ti_HCP_PBE per atom)
```

## Checking the total energies

After each Quantum ESPRESSO calculation, confirm that the SCF calculation has finished normally.

For example:

```bash
grep "JOB DONE" pw.out
```

The total energy can be checked using:

```bash
grep "!" pw.out
```

Quantum ESPRESSO reports the total energy in Ry. Convert it to eV if necessary:

```text
1 Ry = 13.605693122994 eV
```

However, for formation-energy calculations, it is better not to convert each large total energy directly from Ry to eV before taking the energy difference. Direct conversion of large total energies can lead to significant numerical errors due to loss of precision when subtracting nearly equal large numbers.
Therefore, the recommended procedure is:
calculate the formation energy using total energies in Ry,
take the energy difference in Ry,
convert only the final formation energy from Ry to eV.


## Notes on exchange-correlation functionals

The `Fe_BCC` directory includes:

```text
Fe_LDA/
Fe_PBE/
Fe_PBESOL/
```

These calculations can be used to compare how the reference energy of BCC Fe depends on the exchange-correlation functional.

For a consistent formation-energy calculation, all components should be calculated using the same exchange-correlation functional and compatible pseudopotentials.

For example, a PBE formation energy should use:

```text
Fe_BCC/Fe_PBE
Ti_HCP_PBE
FeTi_B2_PBE
```

## Appendix: Comparison between Fe_BCC and Fe_HCP

As an additional check, calculations are prepared for both `Fe_BCC` and `Fe_HCP` using different exchange-correlation functionals.

For example, the following functional-dependent calculations may be compared:

```text
Fe_BCC/Fe_LDA
Fe_BCC/Fe_PBE
Fe_BCC/Fe_PBESOL

Fe_HCP/Fe_LDA
Fe_HCP/Fe_PBE
Fe_HCP/Fe_PBESOL
```

It is useful to compare the total-energy difference between BCC Fe and HCP Fe for each functional.

The energy difference should be evaluated per Fe atom:

```text
Delta E = E_Fe_HCP_per_atom - E_Fe_BCC_per_atom
```

where:

```text
E_Fe_BCC_per_atom = E_Fe_BCC_cell / N_BCC
E_Fe_HCP_per_atom = E_Fe_HCP_cell / N_HCP
```

Here, `N_BCC` and `N_HCP` are the numbers of Fe atoms in the BCC and HCP calculation cells, respectively.

For the BCC Fe input used here, the structure is written as a conventional BCC cell and contains 2 Fe atoms:

```text
N_BCC = 2
```

Therefore:

```text
E_Fe_BCC_per_atom = E_Fe_BCC_cell / 2
```

E_Fe_BCC_per_atom  should be converted to eV unit if necessary:

```text
1 Ry = 13.605693122994 eV
```


The sign of `Delta E` indicates which phase is more stable within a given functional:

```text
Delta E > 0  : BCC Fe is lower in energy than HCP Fe
Delta E < 0  : HCP Fe is lower in energy than BCC Fe
```

This comparison is useful for checking how the functional affects the relative stability of Fe crystal structures.

## Checklist

Before reporting the formation energy, check the following points:

1. The Fe, Ti, and FeTi calculations finished normally.
2. The same exchange-correlation functional was used for all reference and compound calculations.
3. The same type of pseudopotential setup was used consistently.
4. The BCC Fe conventional cell contains 2 Fe atoms.
5. The Fe reference energy was divided by 2.
6. The number of atoms in the HCP Ti cell was checked.
7. The FeTi B2 energy was normalized by the number of FeTi formula units.
8. The final formation energy was reported in eV per FeTi formula unit.
9. The Fe_BCC and Fe_HCP total-energy difference was compared per atom for each functional.

## Summary

This workflow calculates the formation energy of B2 FeTi from BCC Fe and HCP Ti reference calculations.

The most important point is that the BCC Fe input file, such as:

```text
Fe_BCC/Fe_PBE/pw_fe.in
```

uses a conventional BCC cell containing 2 Fe atoms.

Therefore, the Fe reference energy must be normalized as:

```text
E_Fe_per_atom = E_Fe_BCC_cell / 2
```

The formation energy per FeTi formula unit is:

```text
Eform = E_FeTi_per_formula_unit - E_Fe_per_atom - E_Ti_per_atom
```

As an appendix check, the total-energy difference between Fe_BCC and Fe_HCP should also be compared for each functional:

```text
Delta E = E_Fe_HCP_per_atom - E_Fe_BCC_per_atom
```
