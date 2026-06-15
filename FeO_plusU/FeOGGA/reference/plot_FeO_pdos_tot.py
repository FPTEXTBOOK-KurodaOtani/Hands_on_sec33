import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# =========================
# User settings
# =========================

pdos_file = "FeO.pdos_tot"
output_png = "FeO_pdos_tot.png"

# Fermi energy [eV]
# Set this value from the QE output if needed.
fermi_energy = 13.7984

# x-axis range [eV]
# Energy is plotted as E - EF.
xmin = -10.0
xmax = 10.0

# y-axis range
# Down spin is plotted on the negative side.
# If ymin/ymax are None, matplotlib chooses the range automatically.
#
# Example:
ymin = -20.0
ymax = 20.0
#ymin = None
#ymax = None

# If True, y-axis tick labels are shown as positive values
# even for the negative down-spin side.
show_positive_y_ticks = True

# Use Times New Roman font
use_times_new_roman = True


# =========================
# Read PDOS
# =========================

def read_pdos_tot(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"{filename} was not found.")

    data = np.loadtxt(filename, comments="#")

    if data.ndim == 1:
        data = data.reshape(1, -1)

    return data


def positive_tick_formatter(y, pos):
    return f"{abs(y):g}"


def main():
    data = read_pdos_tot(pdos_file)

    energy = data[:, 0] - fermi_energy

    if use_times_new_roman:
        plt.rcParams["font.family"] = "Times New Roman"

    plt.figure(figsize=(6.0, 4.5))

    if data.shape[1] >= 5:
        # Typical spin-polarized QE projwfc.x pdos_tot format:
        # E(eV), dosup(E), dosdw(E)
        #
        # Down-spin components are multiplied by -1 only for plotting,
        # so that they appear as a mirror image of the up-spin components.
        # The y-axis tick labels can still be shown as positive values.
        dos_up = data[:, 1]
        dos_down = data[:, 2]

        plt.plot(energy, dos_up, label="DOS up")
        plt.plot(energy, -dos_down, label="DOS down")

        ylabel = "DOS / PDOS"

    elif data.shape[1] >= 3:
        # Typical non-spin-polarized format:
        # E(eV), dos(E), pdos(E)
        dos = data[:, 1]
        pdos = data[:, 2]

        plt.plot(energy, dos, label="DOS")

        ylabel = "DOS"

    else:
        raise ValueError(
            "Unsupported format. "
            "Expected at least 3 columns."
        )

    plt.axvline(0.0, linestyle=":", linewidth=1.0)
    plt.axhline(0.0, linewidth=0.8)

    plt.xlim(xmin, xmax)

    if ymin is not None or ymax is not None:
        plt.ylim(ymin, ymax)

    if show_positive_y_ticks:
        ax = plt.gca()
        ax.yaxis.set_major_formatter(FuncFormatter(positive_tick_formatter))

    plt.xlabel(r"$E - E_F$ (eV)", fontsize=14)
    plt.ylabel(ylabel, fontsize=14)

    plt.legend(frameon=False, fontsize=10)
    plt.tight_layout()

    plt.savefig(output_png, dpi=300)
    plt.show()

    print(f"Saved: {output_png}")


if __name__ == "__main__":
    main()
