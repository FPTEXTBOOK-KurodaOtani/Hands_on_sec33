# Quantum ESPRESSO 実行設定
QEBIN="/yourdir/espresso-7.1-1/bin"

# 実行
#srun "$QEBIN/pw.x" -nk 7 < pw_al_SCF.in > pw_al_SCF.out
srun "$QEBIN/pw.x" -nk 7 < pw_al_BANDS.in > pw_al_BANDS_.out
srun "$QEBIN/bands.x" < bands.in > bands.out
