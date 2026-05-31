#!/bin/bash


# Quantum ESPRESSO 実行設定
QEBIN="/yourdir/espresso-7.1-1/bin"

# 実行
# SCF cal
$QEBIN/pw.x  < pw_BCC_Li_SCF.in > pw_BCC_Li_SCF.out
# cal eigenvalues at each kpoints for band calculation 
$QEBIN/pw.x   < pw_BCC_Li_BAND.in > pw_BCC_Li_BAND.out
# band plot
$QEBIN/bands.x   < bands.in > bands.out
# "$QEBIN/plotbands.x"   < plotbands.in 
# non SCF cal for fermi_velocity cal
$QEBIN/pw.x    < pw_BCC_Li_NSCF.in > pw_BCC_Li_NSCF.out
$QEBIN/fermi_velocity.x  < pw_BCC_Li_NSCF.in > pw_BCC_Li_NSCF_fermiv.out
