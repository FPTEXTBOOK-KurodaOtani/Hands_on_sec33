import os
import glob
import math
from ase.io import read


ROOT = "graphite_c_scan"
GRAPHENE_OUT = os.path.join(ROOT, "graphene_iso", "pw.out")
OUTFILE = os.path.join(ROOT, "interaction_energy.dat")

NC_GRAPHITE_CELL = 4.0


def get_d_from_dirname(dirname):
    base = os.path.basename(dirname)
    d_str = base.replace("d_", "").replace("A", "").replace("p", ".")
    return float(d_str)


def read_total_energy_by_ase(pw_out):
    atoms = read(pw_out, index=-1, format="espresso-out")
    energy_ev = atoms.get_potential_energy()
    return energy_ev


def fmt(x):
    if math.isnan(x):
        return "nan"
    return f"{x:.12f}"


def main():
    if not os.path.isfile(GRAPHENE_OUT):
        raise FileNotFoundError(f"{GRAPHENE_OUT} not found")

    e_graphene = read_total_energy_by_ase(GRAPHENE_OUT)

    results = []

    dirs = sorted(glob.glob(os.path.join(ROOT, "d_*A")))

    for dpath in dirs:
        if not os.path.isdir(dpath):
            continue

        try:
            d = get_d_from_dirname(dpath)
        except ValueError:
            continue

        c = 2.0 * d
        pw_out = os.path.join(dpath, "pw.out")

        if not os.path.isfile(pw_out):
            results.append(
                (
                    d,
                    c,
                    math.nan,
                    math.nan,
                    math.nan,
                    "NO_OUTPUT",
                    dpath,
                )
            )
            continue

        try:
            e_graphite = read_total_energy_by_ase(pw_out)

            # Interaction energy:
            # Eint = Egraphite - 2 * Egraphene
            # Stable binding gives Eint < 0.
            eint_ev = e_graphite - 2.0 * e_graphene

            # Positive binding energy in meV/C.
            # Around equilibrium, this should be about 50 meV/C.
            ebind_mev_per_c = eint_ev * 1000.0 / NC_GRAPHITE_CELL

            status = "OK"

        except Exception:
            e_graphite = math.nan
            eint_ev = math.nan
            ebind_mev_per_c = math.nan
            status = "ASE_READ_ERROR"

        results.append(
            (
                d,
                c,
                e_graphite,
                eint_ev,
                ebind_mev_per_c,
                status,
                dpath,
            )
        )

    results.sort(key=lambda x: x[0])

    valid = [r for r in results if not math.isnan(r[4])]

    if len(valid) > 0:
        best = min(valid, key=lambda x: x[4])
        best_d = best[0]
        best_ebind = best[4]
    else:
        best_d = math.nan
        best_ebind = math.nan

    with open(OUTFILE, "w") as f:
        f.write(f"# E_graphene[eV] = {e_graphene:.12f}\n")
        f.write("# Eint = Egraphite - 2 * Egraphene\n")
        f.write("# Ebind[meV/C] = Eint[eV] * 1000 / 4\n")
        f.write(f"# maximum_binding_distance[A] = {fmt(best_d)}\n")
        f.write(f"# maximum_binding_energy[meV/C] = {fmt(best_ebind)}\n")
        f.write(
            "# d[A]   c[A]   Egraphite[eV]   "
            "Eint[eV/cell]   Ebind[meV/C]   status   directory\n"
        )

        for d, c, e_graphite, eint_ev, ebind_mev_per_c, status, dpath in results:
            f.write(
                f"{d:.8f}  "
                f"{c:.8f}  "
                f"{fmt(e_graphite)}  "
                f"{fmt(eint_ev)}  "
                f"{fmt(ebind_mev_per_c)}  "
                f"{status}  "
                f"{dpath}\n"
            )

    print(f"E_graphene = {e_graphene:.12f} eV")
    print(f"maximum binding distance = {fmt(best_d)} A")
    print(f"maximum binding energy   = {fmt(best_ebind)} meV/C")
    print(f"Output: {OUTFILE}")


if __name__ == "__main__":
    main()
