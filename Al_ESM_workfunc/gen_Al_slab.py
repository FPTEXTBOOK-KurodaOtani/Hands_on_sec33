from ase.build import fcc111
import numpy as np
from ase.io import write

# Define lattice constant for FCC Al in Angstroms
a = 4.044

# Build a 4-layer slab of the (111) surface for FCC Al.
# Here, size=(1, 1, 4) means minimal periodicity in the surface plane and 3 atomic layers in the z direction.
# No vacuum is added here (vacuum=0.0), as per the requirement.
slab = fcc111("Al", size=(1, 1, 4), a=a, vacuum=15.0)

# Shift the slab so that its center in the z direction is at z = 0.
# Calculate the midpoint of the z coordinates.
z_positions = slab.positions[:, 2]
z_center = (z_positions.max() + z_positions.min()) / 2.0
# Translate the slab so that z_center becomes 0.
slab.translate([0, 0, -z_center])

# Write the resulting slab structure to an output file (XYZ format is used here; choose as needed)
write("fcc111_4layer_slab.cif", slab)

pseudopotentials={"Al":"al_pbe_v1.uspp.F.UPF"}
pseudo_dir="/yourdir/PSPOT/"
input_data = {
        'control': {
            'calculation': 'scf',
            'restart_mode': 'from_scratch',
            'prefix': 'Al4',
            'outdir': './tmp/',
        },
        'system': {
            'ibrav': 0,  # Use explicit cell information
            'ecutwfc': 40,
            'ecutrho': 400,
            'occupations': 'smearing',
            'smearing': 'mp',
            'degauss': 0.01,
            'assume_isolated':'esm',
            'esm_bc':'bc1',
            'nosym':True
        },
        'electrons': {
            'conv_thr': 1e-8,
        }
}
    
fname = f'pw_Al_111_4_layers.in'
write(fname,slab, format='espresso-in',
input_data=input_data,
pseudopotentials=pseudopotentials,
pseudo_dir=pseudo_dir,
kpts=(12, 12, 1))
