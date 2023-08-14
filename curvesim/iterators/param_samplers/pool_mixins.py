"""
These mixins extend Curve pool classes for the purpose of generating iterables
of pool instances configured by different simulation parameters.

Each mixin defines a different pool type and a set of special attribute setters.
"""

from curvesim.pool.cryptoswap.calcs import newton_D
from curvesim.pool.sim_interface import (
    SimCurveCryptoPool,
    SimCurveMetaPool,
    SimCurvePool,
)


class CurvePoolMixin:
    """
    Parameter sampler mixin for Curve stableswap pools.
    Defines special attribute setters.
    """

    @property
    def _pool_type(self):
        return SimCurvePool

    @property
    def setters(self):
        """
        Returns
        -------
        dict
            A dictionary containing the special setters for the pool parameters.
        """
        return {"D": stableswap_D_to_balances}


class CurveMetaPoolMixin:
    """
    Parameter sampler mixin for Curve stableswap meta-pools.
    Defines special attribute setters.
    """

    @property
    def _pool_type(self):
        return SimCurveMetaPool

    @property
    def setters(self):
        """
        Returns
        -------
        dict
            A dictionary containing the special setters for the pool parameters.
        """
        return {"D": stableswap_D_to_balances, "D_base": stableswap_D_base_to_balances}


class CurveCryptoPoolMixin:
    """
    Parameter sampler mixin for Curve cryptoswap pools.
    Defines special attribute setters.
    """

    @property
    def _pool_type(self):
        return SimCurveCryptoPool

    @property
    def setters(self):
        """
        Returns
        -------
        dict
            A dictionary containing the special setters for the pool parameters.
        """
        return {
            "D": cryptoswap_D_to_balances,
            "A": set_cryptoswap_A,
        }


def set_cryptoswap_A(pool, A):
    xp = pool._xp()
    gamma = pool.gamma
    D = newton_D(A, gamma, xp)
    print("A setter, D value:", D)
    pool.D = D
    pool.A = A


def set_cryptoswap_gamma(pool, gamma):
    xp = pool._xp()
    A = pool.A
    D = newton_D(A, gamma, xp)
    pool.D = D
    pool.gamma = gamma


def stableswap_D_to_balances(pool, D):
    """
    Sets the balance for each token in the pool based on the provided
    invariant value.

    Parameters
    ----------
    pool : instance of _pool_type
    D : int
        The invariant value.
    """
    rates = pool.rates
    n = pool.n
    pool.balances = [D // n * 10**18 // r for r in rates]


def stableswap_D_base_to_balances(pool, D_base):
    """
    Sets the balance for each token in the basepool based on the provided
    invariant value.

    Parameters
    ----------
    pool : instance of _pool_type
    D_base : int
        The invariant value for the basepool.
    """
    basepool = pool.basepool
    rates = basepool.rates
    n = basepool.n
    basepool.balances = [D_base // n * 10**18 // r for r in rates]


def cryptoswap_D_to_balances(pool, D):
    """
    Sets the balance for each token in the pool based on the provided
    invariant value.

    Parameters
    ----------
    pool : instance of _pool_type
    D : int
        The invariant value.
    """
    pool.D = D
    pool.balances = pool._convert_D_to_balances(D)
