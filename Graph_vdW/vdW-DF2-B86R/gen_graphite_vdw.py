import os
import numpy as np

from ase import Atoms
from ase.io import write
from ase.geometry import cellpar_to_cell


# =========================
# User settings
# =========================

a = 2.46772
b = 2.46772
alpha = 90.0
beta = 90.0
gamma = 120.0

# reference c = 8.68504 A
# interlayer distance = c / 2 = 4.34252 A
d_list = [
    2.60,
    2.80,
    3.00,
    3.20,
    3.40,
    3.60,
    3.80,
    4.00,
    4.20,
    4.50,
    4.80,
    5.00,
    5.50,
    6.00,
    7.00,
    8.00,
    10.00,
]

graphene_vacuum = 30.0

pseudo_dir = "/yourdir/PSPOT/"

pseudopotentials = {
    "C": "c_pbe_v1.2.uspp.F.UPF",
}

kpts_graphite = (12, 12, 8)
kpts_graphene = (12, 12, 1)

output_root = "graphite_c_scan"


# =========================
# Structures
# =========================

def make_graphite_ab(d):
    c = 2.0 * d

    cell = cellpar_to_cell([
        a,
        b,
        c,
        alpha,
        beta,
        gamma,
    ])

    scaled_positions = [
        [0.00000, 0.00000, 0.75000],
        [0.00000, 0.00000, 0.25000],
        [0.33333, 0.66667, 0.75000],
        [0.66667, 0.33333, 0.25000],
    ]

    atoms = Atoms(
        symbols=["C", "C", "C", "C"],
        scaled_positions=scaled_positions,
        cell=cell,
        pbc=True,
    )

    return atoms


def make_graphene(vacuum=30.0):
    cell = cellpar_to_cell([
        a,
        b,
        vacuum,
        alpha,
        beta,
        gamma,
    ])

    scaled_positions = [
        [0.00000, 0.00000, 0.50000],
        [0.33333, 0.66667, 0.50000],
    ]

    atoms = Atoms(
        symbols=["C", "C"],
        scaled_positions=scaled_positions,
        cell=cell,
        pbc=True,
    )

    return atoms


# =========================
# QE input
# =========================

def make_input_data(prefix):
    input_data = {
        "control": {
            "calculation": "scf",
            "prefix": prefix,
            "pseudo_dir": pseudo_dir,
            "outdir": "./tmp",
            "tstress": True,
            "tprnfor": True,
            "disk_io": "low",
        },
        "system": {
            "ecutwfc": 40.0,
            "ecutrho": 400.0,
            "occupations": "smearing",
            "smearing": "mv",
            "degauss": 0.01,
            "input_dft": "vdW-DF2-B86R",
        },
        "electrons": {
            "conv_thr": 1.0e-8,
            "mixing_beta": 0.3,
        },
    }

    return input_data


def write_qe_input(atoms, workdir, prefix, kpts):
    os.makedirs(workdir, exist_ok=True)

    input_data = make_input_data(prefix=prefix)

    write(os.path.join(workdir, "structure.cif"), atoms)

    write(
        os.path.join(workdir, "pw.in"),
        atoms,
        format="espresso-in",
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        kpts=kpts,
        crystal_coordinates=True,
    )


# =========================
# Main
# =========================

def main():
    os.makedirs(output_root, exist_ok=True)

    graphene_dir = os.path.join(output_root, "graphene_iso")
    graphene = make_graphene(vacuum=graphene_vacuum)

    write_qe_input(
        atoms=graphene,
        workdir=graphene_dir,
        prefix="graphene_iso",
        kpts=kpts_graphene,
    )

    summary_lines = []
    summary_lines.append("# d[A]   c[A]   directory")

    for d in d_list:
        c = 2.0 * d

        dirname = f"d_{d:.5f}A".replace(".", "p")
        workdir = os.path.join(output_root, dirname)
        prefix = f"graphite_d_{d:.5f}".replace(".", "p")

        graphite = make_graphite_ab(d=d)

        write_qe_input(
            atoms=graphite,
            workdir=workdir,
            prefix=prefix,
            kpts=kpts_graphite,
        )

        summary_lines.append(f"{d:12.5f}  {c:12.5f}  {workdir}")

    with open(os.path.join(output_root, "summary.dat"), "w") as f:
        f.write("\n".join(summary_lines) + "\n")

    print("Generated graphite and graphene QE inputs.")
    print(f"Reference structure: a = {a}, b = {b}, gamma = {gamma}")
    print("Reference c = 8.68504 A corresponds to d = 4.34252 A")


if __name__ == "__main__":
    main()
