QEBIN="/yourdir/espresso-7.1-1/bin"

# 実行
$QEBIN/pw.x < pw_FeO_SCF.in > pw_FeO_SCF.out
$QEBIN/pw.x < pw_FeO_NSCF.in > pw_FeO_NSCF.out
$QEBIN/projwfc.x < pdos.in > pdos.out
