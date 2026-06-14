

# Quantum ESPRESSO 実行設定
QEBIN="/yourdir/espresso-7.1-1/bin"

# 実行
$QEBIN/pw.x -nk 7 < pw_Al_111_4_layers.in > pw_Al_111_4_layers.out
