
# financial_analysis/quant_methods/tvm_calculator.py

class TVMCalculator:
    """Performs Time Value of Money calculations (based on CFA curriculum)"""

    def __init__(self, n=None, r=None, pv=None, fv=None, pmt=0, compounding=1):
        """
        Args:
            n (float): Number of periods
            r (float): Interest rate per period (as a decimal, e.g. 0.08 for 8%)
            pv (float): Present Value
            fv (float): Future Value
            pmt (float): Payment per period (default = 0)
            compounding (int): Compounding frequency per year (default = 1 for annual)
        """
        self.n = n
        self.r = r
        self.pv = pv
        self.fv = fv
        self.pmt = pmt
        self.compounding = compounding

    def calculate_fv(self):
        """FV = PV*(1+r)^n + PMT*((1+r)^n - 1)/r"""
        r, n = self.r, self.n
        if r is None or n is None:
            raise ValueError("Rate and periods are required for FV calculation")
        fv_lump = self.pv * (1 + r) ** n if self.pv is not None else 0
        fv_annuity = self.pmt * (((1 + r) ** n - 1) / r)
        return fv_lump + fv_annuity

    def calculate_pv(self):
        """PV = FV / (1+r)^n + PMT * [1 - 1/(1+r)^n] / r"""
        r, n = self.r, self.n
        if r is None or n is None:
            raise ValueError("Rate and periods are required for PV calculation")
        pv_lump = self.fv / (1 + r) ** n if self.fv is not None else 0
        pv_annuity = self.pmt * (1 - (1 / (1 + r) ** n)) / r
        return pv_lump + pv_annuity

    def calculate_n(self):
        """n = log(FV/PV) / log(1+r)"""
        import math
        if self.r is None or self.pv is None or self.fv is None:
            raise ValueError("Rate, PV, and FV are required for n calculation")
        return math.log(self.fv / self.pv) / math.log(1 + self.r)

    def calculate_r(self):
        """Solves r using iterative method (only for FV with PV and PMT = 0)"""
        from scipy.optimize import fsolve

        if self.n is None or self.pv is None or self.fv is None:
            raise ValueError("n, PV, and FV are required to calculate r")

        def f(r):
            return self.pv * (1 + r) ** self.n - self.fv

        r_guess = 0.1
        return float(fsolve(f, r_guess)[0])
