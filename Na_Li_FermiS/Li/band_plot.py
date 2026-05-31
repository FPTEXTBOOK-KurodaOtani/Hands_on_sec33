import numpy as np
import matplotlib.pyplot as plt

fermi = 0.9452  # grep "Fermi energ" scf.out

data = np.loadtxt("bccLi.bands.dat.gnu")
x = data[:, 0]
e = data[:, 1] - fermi

breaks = [0]
for i in range(1, len(x)):
    if x[i] < x[i - 1]:
        breaks.append(i)
breaks.append(len(x))

fig, ax = plt.subplots(figsize=(5.0, 6.0))

for i in range(len(breaks) - 1):
    s = breaks[i]
    t = breaks[i + 1]
    ax.plot(x[s:t], e[s:t], linewidth=1.2,color="black")

ax.axhline(0.0, linestyle="--", linewidth=0.8, color="blue")

ax.set_ylabel(r"$E - E_{\mathrm{F}}$ (eV)", fontsize=18)


# =========================
# High-symmetry points
# from bands.out
# =========================
k_nodes = [0.0000, 0.7500, 1.3624, 1.9747, 2.8408]
k_labels = ["P", r"$\Gamma$", "N", "H", r"$\Gamma$"]

ax.set_xticks(k_nodes)
ax.set_xticklabels(k_labels, fontsize=16)

for k in k_nodes:
    ax.axvline(k, color="black", linewidth=0.8)

plt.ylim(-5,15)

plt.tight_layout()
plt.savefig("bcc_band.pdf", dpi=300)
plt.show()
