from abc import ABC, abstractmethod

from curvesim.logging import get_logger

logger = get_logger(__name__)


class SimPool(ABC):
    """
    The interface that must be implemented by pools used in simulations.

    See curvesim.pool.sim_interface for implementations.
    """

    def prepare_for_trades(self, timestamp):
        """
        Does any necessary preparation before computing and doing trades.

        The input timestamp can be used to fetch any auxiliary data
        needed to prep the state.

        Base implementation is a no-op.

        Parameters
        ----------
        timestamp : datetime.datetime
            the time to sample from
        """

    @abstractmethod
    def price(self, coin_in, coin_out, use_fee=True):
        """
        Returns the spot price of `coin_in` quoted in terms of `coin_out`,
        i.e. the ratio of output coin amount to input coin amount for
        an "infinitesimally" small trade.

        Coin IDs should be strings but as a legacy feature integer indices
        corresponding to the pool implementation are allowed (caveat lector).

        The indices are assumed to include base pool underlyer indices.

        Parameters
        ----------
        coin_in : str, int
            ID of coin to be priced; in a swapping context, this is
            the "in"-token.
        coin_out : str, int
            ID of quote currency; in a swapping context, this is the
            "out"-token.
        use_fee: bool, default=False
            Deduct fees.

        Returns
        -------
        float
            Price of `coin_in` quoted in `coin_out`
        """
        raise NotImplementedError

    @abstractmethod
    def trade(self, coin_in, coin_out, size):
        """
        Perform an exchange between two coins.

        Coin IDs should be strings but as a legacy feature integer indices
        corresponding to the pool implementation are allowed (caveat lector).

        Note that all amounts are normalized to be in the same units as
        pool value, e.g. for Curve Stableswap pools, the same units as `D`.
        This simplifies cross-token comparisons and creation of metrics.


        Parameters
        ----------
        coin_in : str, int
            ID of "in" coin.
        coin_out : str, int
            ID of "out" coin.
        size : int
            Amount of coin `i` being exchanged.

        Returns
        -------
        (int, int, int)
            (amount of coin `j` received, trading fee, volume)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def number_of_coins(self):
        """
        Return number of coins you are swapping between for the simulation.

        Note this quantity is used for understanding how many tradable pairs
        in the pool there are for the purpose of the simulation.  This doesn't
        necessarily mean the same thing as the number of assets in the pool.

        Returns
        --------
        int
            The number of coins you can swap between.
        """
        raise NotImplementedError

    @abstractmethod
    def get_in_amount(self, coin_in, coin_out, out_balance_perc):
        """
        Calculate the swap amount of the "in" coin needed to leave
        the specified percentage of the "out" coin.

        Parameters
        ----------
        coin_in : str, int
            ID of "in" coin.
        coin_out : str, int
            ID of "out" coin.
        out_balance_perc : float
            Percentage of the "out" coin balance that should remain
            after doing the swap.

        Returns
        -------
        int
            The amount of "in" coin needed.
        """
        raise NotImplementedError
