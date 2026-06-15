
# Quantum ESPRESSO 実行設定
QEBIN="/yourdir/espresso-7.1-1/bin"


# run_graphite_c_scan.sh

set -e

# =========================
# User settings
# =========================

PWX="${QEBIN}/pw.x"

ROOT="graphite_c_scan"

#MPI_CMD="mpirun"
MPI_CMD=""


# =========================
# Run all calculations
# =========================

run_pw_dir () {
    dir="$1"

    if [ ! -d "${dir}" ]; then
        echo "skip: ${dir} not found"
        return
    fi

    if [ ! -f "${dir}/pw.in" ]; then
        echo "skip: ${dir}/pw.in not found"
        return
    fi

    echo "========================================"
    echo "Running ${dir}"
    echo "========================================"

    cd "${dir}"

    mkdir -p tmp

    if [ -f DONE ]; then
        echo "skip: already DONE"
        cd - > /dev/null
        return
    fi

    if [ -f FAILED ]; then
        rm FAILED
    fi

    if [ -f pw.out ]; then
        cp pw.out pw.out.bak
    fi

    if ${MPI_CMD} ${PWX} < pw.in > pw.out
    then
        qe_status="OK"
    else
        qe_status="QE_ERROR"
    fi

    if grep -q "JOB DONE" pw.out
    then
        echo "DONE: ${dir}"
        touch DONE
        rm -f FAILED
    else
        echo "FAILED: ${dir}"
        touch FAILED
    fi

    cd - > /dev/null
}


# =========================
# Run isolated graphene first
# =========================

run_pw_dir "${ROOT}/graphene_iso"


# =========================
# Run graphite c-scan
# =========================

for dir in ${ROOT}/d_*A
do
    run_pw_dir "${dir}"
done


echo "All calculations finished."
