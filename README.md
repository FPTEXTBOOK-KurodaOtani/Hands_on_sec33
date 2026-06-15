# Hands_on_sec33

This directory contains input files for hands-on DFT calculations using Quantum ESPRESSO (QE).

The purpose of this hands-on section is to practice basic QE calculations and to confirm several topics discussed in the book through actual input files and calculations.

For the detailed procedure of each exercise, please refer to the `README.md` file and `run.sh` script in each subdirectory.

## References and required programs

Before running the calculations, please install Quantum ESPRESSO and prepare the external programs required for some exercises.

### Quantum ESPRESSO installation and compilation

Quantum ESPRESSO can be downloaded and compiled by following the official documentation.

Useful references are:

- Quantum ESPRESSO official web page:  
  https://www.quantum-espresso.org/
- Quantum ESPRESSO installation guide:  
  https://www.quantum-espresso.org/Doc/user_guide/node7.html
- Quantum ESPRESSO installation FAQ:  
  https://www.quantum-espresso.org/faq/installation/

The installation guide explains download, required libraries, CMake-based compilation, `make`-based compilation, MPI setup, BLAS/LAPACK, FFT libraries, and related build options.

### Quantum ESPRESSO input-variable documentation

The QE input files in this hands-on section mainly use the following executables:

```text
pw.x
pp.x
projwfc.x
```

The input variables for these programs are described in the official QE documentation:

- `pw.x` input variables:  
  https://www.quantum-espresso.org/Doc/INPUT_PW.html
- `pp.x` input variables:  
  https://www.quantum-espresso.org/Doc/INPUT_PP.html
- `projwfc.x` input variables:  
  https://www.quantum-espresso.org/Doc/INPUT_PROJWFC.html

Please refer to these pages when you want to check the meaning of variables in `pw_**.in`, post-processing input files, or projected-DOS input files.

### Materials Cloud online tools

The following online tools are not actively used in the present hands-on exercises, but they are useful for preparing and checking first-principles calculations:

https://www.materialscloud.org/work/tools

For example, Materials Cloud provides tools such as:

- a Quantum ESPRESSO input generator,
- structure visualization tools,
- SeeK-path for finding and visualizing high-symmetry k-point paths.

These tools can be helpful when checking crystal structures, generating input files, or confirming the k-point path used for band-structure calculations.

### FermiSurfer

Some exercises may use FermiSurfer to visualize Fermi surfaces.

Useful references are:

- FermiSurfer official page:  
  https://mitsuaki1987.github.io/fermisurfer/
- FermiSurfer documentation page:  
  https://mitsuaki1987.github.io/fermisurfer/html/index.html

FermiSurfer is a visualization tool for Fermi surfaces and can color the Fermi surface using quantities such as Fermi velocity or other band-dependent scalar quantities.

### Bader charge analysis

Some exercises use Bader charge analysis.

Useful references are:

- Bader charge analysis program:  
  https://theory.cm.utexas.edu/bader/
- Henkelman group Bader analysis page:  
  https://theory.cm.utexas.edu/henkelman/research/bader/

The Bader program reads charge-density files, such as Gaussian CUBE files, and outputs the charge associated with each atom and the Bader volumes.

## Pseudopotential files

QE input files require pseudopotential files.

The pseudopotential files used in this hands-on section are stored in:

```text
PSPOT/
```

In the present hands-on examples, the pseudopotentials are mainly taken from the GBRV pseudopotential library:

https://www.physics.rutgers.edu/gbrv/

The GBRV library provides pseudopotential files for Quantum ESPRESSO and was designed for accurate and computationally efficient high-throughput DFT calculations.

When choosing pseudopotentials for production calculations, it is important to check their accuracy and convergence behavior. A useful reference for pseudopotential validation is the SSSP efficiency table:

```text
https://legacy.materialscloud.org/discover/sssp/table/efficiency
```

The SSSP table provides benchmark information that is helpful when selecting pseudopotentials and cutoff energies.

The pseudopotentials included in `PSPOT/` are prepared for this hands-on exercise. For research calculations, the pseudopotential choice and convergence with respect to cutoff energies should be checked carefully.

In the QE input files, such as `pw_**.in`, the pseudopotential directory is specified by the variable `pseudo_dir`.

For example:

```fortran
pseudo_dir = '/yourdir/PSPOT'
```

Here, `/yourdir` must be replaced by the actual absolute path to the `Hands_on_sec33` directory on your computer or cluster.

## How to check the absolute path

You can check the absolute path of the current directory using the `pwd` command.

```bash
pwd
```

For example, if you are in the `Hands_on_sec33` directory and `pwd` returns:

```text
/home/user/Hands_on_sec33
```

then the `pseudo_dir` variable in the QE input files should be set as:

```fortran
pseudo_dir = '/home/user/Hands_on_sec33/PSPOT'
```

## Replacing `/yourdir/PSPOT`

The string `/yourdir/PSPOT` in the QE input files should be replaced by the actual absolute path to the `PSPOT` directory.

For example, if the absolute path of this directory is:

```text
/home/user/Hands_on_sec33
```

then replace:

```fortran
pseudo_dir = '/yourdir/PSPOT'
```

with:

```fortran
pseudo_dir = '/home/user/Hands_on_sec33/PSPOT'
```

This replacement can be done manually using a text editor.

After the replacement, check that `pseudo_dir` correctly points to the `PSPOT` directory and that the required pseudopotential files exist there.

## Running calculations

Move into each exercise directory and check the README and run script.

For example:

```bash
cd Al_Si_BAND
cat README.md
cat run.sh
```

The execution procedure depends on each exercise. In many cases, the calculation can be run with:

```bash
./run.sh
```

### Setting `QEBIN`

In the `run.sh` scripts, commands are often written using the variable `$QEBIN`, for example:

```bash
$QEBIN/pw.x < pw_*.in > pw_*.out
```

Here, `QEBIN` should be set to the `bin` directory where the compiled Quantum ESPRESSO executables are located.

For example:

```bash
QEBIN=/yourdir/qe-7.1/bin
```

or:

```bash
export QEBIN=/yourdir/qe-7.1/bin
```

In this case, the executables are assumed to be located as:

```text
/yourdir/qe-7.1/bin/pw.x
/yourdir/qe-7.1/bin/pp.x
/yourdir/qe-7.1/bin/projwfc.x
```

Please modify `/yourdir/qe-7.1/bin` according to your own installation path.

### Running QE manually

If you run QE manually, a typical command is:

```bash
$QEBIN/pw.x < pw_*.in > pw_*.out
```

Here, `$QEBIN` should point to the directory containing the Quantum ESPRESSO executables.

### Parallel execution

If parallel execution is available in your environment, QE can be executed with MPI.

For example:

```bash
mpirun -np 16 $QEBIN/pw.x < pw_*.in > pw_*.out
```

or, on a system using Slurm:

```bash
srun $QEBIN/pw.x < pw_*.in > pw_*.out
```

For calculations with many k points, k-point parallelization can be used by adding the `-nk` option.

For example:

```bash
mpirun -np 16 $QEBIN/pw.x -nk 4 < pw_*.in > pw_*.out
```

or:

```bash
srun $QEBIN/pw.x -nk 4 < pw_*.in > pw_*.out
```

The `-nk` option specifies the number of k-point pools. This distributes k points over multiple pools and can improve parallel efficiency when the calculation contains many k points.

The appropriate value of `-nk` depends on the number of MPI processes, the number of k points, and the computing environment. It should be chosen so that the parallel calculation remains efficient.

## Notes

Before running the calculations, check the following points:

1. Quantum ESPRESSO is available in your environment.
2. `$QEBIN/pw.x`, `$QEBIN/pp.x`, and other required executables can be run.
3. The `QEBIN` variable points to the correct `bin` directory of the Quantum ESPRESSO installation.
4. The `pseudo_dir` variable points to the correct `PSPOT` directory.
5. The pseudopotential files specified in each QE input file exist in `PSPOT/`.
6. The `README.md` and `run.sh` files in each exercise directory have been checked.
7. If an exercise uses FermiSurfer or the Bader program, confirm that the corresponding executable is available in your environment.
8. Materials Cloud online tools can be used as optional references for checking structures, QE inputs, and k-point paths.
9. For parallel calculations, consider using the `-nk` option when k-point parallelization is useful.
10. For research-level calculations, convergence with respect to pseudopotentials and cutoff energies should be tested.
