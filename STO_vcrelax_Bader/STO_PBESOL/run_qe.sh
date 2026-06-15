
# Quantum ESPRESSO 実行設定
QEBIN="/home/issp/materiapps/intel/espresso/espresso-7.1-1/bin"

# 実行
$QEBIN/pw.x < pw_STO.in > pw_STO.out
$QEBIN/pw.x < pw_STO_bader.in > pw_STO_bader.out
$QEBIN/pp.x < STO_all_pp.in > STO_all_pp.out
$QEBIN/pp.x < STO_val_pp.in > STO_val_pp.out
/yourdir/bader  STO_valence.cube -ref STO_all.cube > BADER.out
