
import numpy as np
from fractions import Fraction


def frac_to_float(x):
    """
    Convert fractional string such as '1/4', '5/8', '-3/8' to float.
    """
    return float(Fraction(str(x)))


def make_vec(values):
    """
    Make numpy vector from fractional strings or numbers.
    """
    return np.array([frac_to_float(v) for v in values], dtype=float)


def fcc_standard_to_cart(k_std):
    """
    Convert FCC standard fractional coordinates to Cartesian reciprocal coordinates.

    Standard FCC reciprocal basis:

        b1 = ( 1, -1,  1) / sqrt(2)
        b2 = (-1,  1,  1) / sqrt(2)
        b3 = ( 1,  1, -1) / sqrt(2)

    k_cart = k1*b1 + k2*b2 + k3*b3
    """
    b1 = np.array([ 1.0, -1.0,  1.0]) / np.sqrt(2.0)
    b2 = np.array([-1.0,  1.0,  1.0]) / np.sqrt(2.0)
    b3 = np.array([ 1.0,  1.0, -1.0]) / np.sqrt(2.0)

    bmat = np.column_stack([b1, b2, b3])

    return bmat @ k_std


def rotate_to_qe_orientation(k_cart):
    """
    Convert the standard Cartesian orientation to the orientation used
    in the present QE FCC band path.

    This gives the path:

        L -> Gamma -> X -> U -> Gamma

    with

        X = (0, -1/sqrt(2), 0)
        U = (-1/(4 sqrt(2)), -1/sqrt(2), 1/(4 sqrt(2)))
    """
    rotation = np.array([
        [-1.0,  0.0,  0.0],
        [ 0.0, -1.0,  0.0],
        [ 0.0,  0.0,  1.0],
    ])

    return rotation @ k_cart


def qe_crystal_b_to_cart(k_qe):
    """
    Convert QE crystal_b coordinates to Cartesian reciprocal coordinates.

    q = 1/sqrt(2) * (
        -h + k + l,
         h - k + l,
         h + k - l
    )
    """
    h, k, l = k_qe

    qx = -h + k + l
    qy =  h - k + l
    qz =  h + k - l

    return np.array([qx, qy, qz]) / np.sqrt(2.0)


def cart_to_qe_crystal_b(k_cart):
    """
    Convert Cartesian reciprocal coordinate to QE crystal_b coordinate.
    """
    b1 = np.array([-1.0,  1.0,  1.0]) / np.sqrt(2.0)
    b2 = np.array([ 1.0, -1.0,  1.0]) / np.sqrt(2.0)
    b3 = np.array([ 1.0,  1.0, -1.0]) / np.sqrt(2.0)

    bmat = np.column_stack([b1, b2, b3])

    k_qe = np.linalg.solve(bmat, k_cart)

    k_qe[np.abs(k_qe) < 1.0e-12] = 0.0

    return k_qe


def standard_to_qe_crystal_b(k_std):
    """
    Standard FCC fractional coordinate
    -> Cartesian reciprocal coordinate
    -> QE-oriented Cartesian coordinate
    -> QE crystal_b coordinate
    """
    k_cart_std = fcc_standard_to_cart(k_std)
    k_cart_qe = rotate_to_qe_orientation(k_cart_std)
    k_qe = cart_to_qe_crystal_b(k_cart_qe)

    return k_qe, k_cart_qe


def calc_xcoords(cart_points):
    """
    Calculate cumulative x coordinates for band plot.
    """
    xcoords = []
    x = 0.0

    for i in range(len(cart_points)):
        if i == 0:
            x = 0.0
        else:
            dx = np.linalg.norm(cart_points[i] - cart_points[i - 1])
            x += dx

        xcoords.append(x)

    return xcoords


def main():
    path = [
        {"label": "L", "std": ["0",   "1/2", "0"],   "npoint": 40},
        {"label": "G", "std": ["0",   "0",   "0"],   "npoint": 60},
        {"label": "X", "std": ["0",   "1/2", "1/2"], "npoint": 20},
        {"label": "U", "std": ["1/4", "5/8", "5/8"], "npoint": 60},
        {"label": "G", "std": ["1",   "1",   "1"],   "npoint": 40},
    ]

    qe_points = []
    cart_points = []

    for p in path:
        k_std = make_vec(p["std"])
        k_qe, k_cart_qe = standard_to_qe_crystal_b(k_std)

        qe_points.append(k_qe)
        cart_points.append(k_cart_qe)

    xcoords = calc_xcoords(cart_points)

    print()
    print("Converted FCC k-points")
    print()

    print(
        "{:>6s}  {:>18s}  {:>34s}  {:>34s}  {:>10s}".format(
            "label",
            "standard",
            "QE crystal_b",
            "QE Cartesian reciprocal",
            "x"
        )
    )

    for p, k_qe, k_cart, x in zip(path, qe_points, cart_points, xcoords):
        std_text = "(" + ", ".join(p["std"]) + ")"

        qe_text = "({: .6f}, {: .6f}, {: .6f})".format(
            k_qe[0], k_qe[1], k_qe[2]
        )

        cart_text = "({: .6f}, {: .6f}, {: .6f})".format(
            k_cart[0], k_cart[1], k_cart[2]
        )

        print(
            "{:>6s}  {:>18s}  {:>34s}  {:>34s}  {:10.4f}".format(
                p["label"],
                std_text,
                qe_text,
                cart_text,
                x
            )
        )

    print()
    print("QE K_POINTS crystal_b")
    print()
    print("K_POINTS crystal_b")
    print(len(path))

    for p, k_qe in zip(path, qe_points):
        print(
            "{: .6f} {: .6f} {: .6f} {:4d} ! {}".format(
                k_qe[0],
                k_qe[1],
                k_qe[2],
                p["npoint"],
                p["label"]
            )
        )

    print()
    print("Band plot xticks")
    print()

    print("xticks = [", end="")
    print(", ".join("{:.4f}".format(x) for x in xcoords), end="")
    print("]")

    xlabels = []
    for p in path:
        if p["label"] == "G":
            xlabels.append(r"r'$\\Gamma$'")
        else:
            xlabels.append("'" + p["label"] + "'")

    print("xlabels = [", end="")
    print(", ".join(xlabels), end="")
    print("]")


if __name__ == "__main__":
    main()
