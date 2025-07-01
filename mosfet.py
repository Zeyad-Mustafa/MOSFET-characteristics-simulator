import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

class MOSFET:
    def __init__(self, Vth=1.0, k=0.5, lambda_param=0.02):
        """
        Initialize MOSFET parameters
        :param Vth: Threshold voltage (V)
        :param k: Transconductance parameter (A/V^2)
        :param lambda_param: Channel-length modulation parameter (1/V)
        """
        self.Vth = Vth
        self.k = k
        self.lambda_param = lambda_param

    def calculate_id(self, Vgs, Vds):
        """
        Calculate drain current using simplified MOSFET equations
        :param Vgs: Gate-to-source voltage (V)
        :param Vds: Drain-to-source voltage (V)
        :return: Drain current (A)
        """
        if Vgs < self.Vth:
            # Cut-off region
            return 0.0
        elif Vds < (Vgs - self.Vth):
            # Linear region
            return self.k * ((Vgs - self.Vth) * Vds - 0.5 * Vds**2) * (1 + self.lambda_param * Vds)
        else:
            # Saturation region
            return 0.5 * self.k * (Vgs - self.Vth)**2 * (1 + self.lambda_param * Vds)

def plot_characteristics(mosfet, Vgs_values, Vds_range):
    """
    Plot the output characteristics of the MOSFET
    :param mosfet: MOSFET instance
    :param Vgs_values: List of Vgs values to plot
    :param Vds_range: Range of Vds values (start, stop, num_points)
    """
    plt.figure(figsize=(10, 6))
    
    Vds = np.linspace(*Vds_range)
    
    for Vgs in Vgs_values:
        Id = [mosfet.calculate_id(Vgs, vds) for vds in Vds]
        plt.plot(Vds, Id, label=f'Vgs = {Vgs} V')
    
    plt.title('MOSFET Output Characteristics')
    plt.xlabel('Drain-to-Source Voltage (Vds) [V]')
    plt.ylabel('Drain Current (Id) [A]')
    plt.grid(True)
    plt.legend()
    plt.savefig('mosfet_characteristics.png')
    plt.show()

def main():
    parser = ArgumentParser(description='MOSFET Output Characteristics Simulator')
    parser.add_argument('--Vth', type=float, default=1.0, help='Threshold voltage (V)')
    parser.add_argument('--k', type=float, default=0.5, help='Transconductance parameter (A/V^2)')
    parser.add_argument('--lambda_param', type=float, default=0.02, help='Channel-length modulation parameter (1/V)')
    parser.add_argument('--Vgs', type=float, nargs='+', default=[1.5, 2.0, 2.5, 3.0], help='Gate-to-source voltages (V)')
    parser.add_argument('--Vds_max', type=float, default=5.0, help='Maximum drain-to-source voltage (V)')
    
    args = parser.parse_args()
    
    mosfet = MOSFET(Vth=args.Vth, k=args.k, lambda_param=args.lambda_param)
    plot_characteristics(mosfet, args.Vgs, (0, args.Vds_max, 100))

if __name__ == "__main__":
    main()