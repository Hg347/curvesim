"""
  Polygon curve pool simulation

"""

import time

import curvesim


def polygon_simulation():

    # stMatic/WMatic on polygon chain (Crypto V2 Factory Pool)
    testPoolId = "0xfb6fe7802ba9290ef8b00ca16af4bc26eb663a28"

    test = curvesim.pool.get_pool(testPoolId, "matic", normalize=True)
    test.A = 4000000
    test.gamma = 25000000000000
    test.mid_fee = 1542000
    test.out_fee = 298650000
    test.fee_gamma = 89560000000000000
    test.allowed_extra_profit = 2500000000000
    # test.balances = [361385319858769000000000000, 361385319858769000000000000]

    t = time.time()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    res = curvesim.autosim(
        testPoolId,
        chain="matic",
        A=[4850000, 50000000],
        mid_fee=[6541100, 39842100],
        fee_gamma=[89560000000000000, 50000000000000000],
        ncpu=1,
    )
    elapsed = time.time() - t
    print("Elapsed time:", elapsed)

    print("results are exported into results folder")
    res.plot(save_as=f"results/results_{timestr}.html")

    return res


res = polygon_simulation()
