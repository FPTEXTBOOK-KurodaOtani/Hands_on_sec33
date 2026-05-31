#!/bin/bash

# Quantum ESPRESSO 実行設定
QEBIN="/yourdir/espresso-7.1-1/bin"

# 実行
$QEBIN/pw.x   < pw_BCC_Na_SCF.in > pw_BCC_Na_SCF.out
$QEBIN/pw.x   < pw_BCC_Na_BAND.in > pw_BCC_Na_BAND.out
$QEBIN/bands.x   < bands.in > bands.out
#$QEBIN/plotbands.x   < plotbands.in 
$QEBIN/pw.x    < pw_BCC_Na_NSCF.in > pw_BCC_Na_NSCF.out
$QEBIN/fermi_velocity.x  < pw_BCC_Na_NSCF.in > pw_BCC_Na_NSCF_fermiv.out
