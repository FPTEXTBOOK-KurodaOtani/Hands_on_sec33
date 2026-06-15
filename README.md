# Hands_on_sec33

This directory contains input files for hands-on DFT calculations using Quantum ESPRESSO (QE).

The purpose of this hands-on section is to practice basic QE calculations and to confirm several topics discussed in the book through actual input files and calculations.

For the detailed procedure of each exercise, please refer to the `README.md` file and `run.sh` script in each subdirectory.

## Pseudopotential files

QE input files require pseudopotential files.

The pseudopotential files used in this hands-on section are stored in:

```text
PSPOT/
```

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

On Linux, you can replace `/yourdir/PSPOT` in all `pw_*.in` files under the current directory using:

```bash
find . -type f -name "pw_*.in" -exec sed -i "s|/yourdir/PSPOT|$(pwd)/PSPOT|g" {} \;
```

On macOS, use:

```bash
find . -type f -name "pw_*.in" -exec sed -i '' "s|/yourdir/PSPOT|$(pwd)/PSPOT|g" {} \;
```

After replacement, check that the path was correctly set:

```bash
grep -r "pseudo_dir" .
```

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

If you run QE manually, a typical command is:

```bash
$QEBIN/pw.x < pw_*.in > pw_*.out
```

Here, `$QEBIN` should point to the directory containing the Quantum ESPRESSO executables.

## Notes

Before running the calculations, check the following points:

1. Quantum ESPRESSO is available in your environment.
2. `$QEBIN/pw.x`, `$QEBIN/pp.x`, and other required executables can be run.
3. The `pseudo_dir` variable points to the correct `PSPOT` directory.
4. The pseudopotential files specified in each QE input file exist in `PSPOT/`.
5. The `README.md` and `run.sh` files in each exercise directory have been checked.
