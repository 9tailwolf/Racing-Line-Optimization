'''
Copyright by 9tailwolf.
For more information, visit (https://9tailwolf.github.io/playground/f1/racingline)
'''


import argparse

from classes.TrackPlotter import TrackPlotter

def get_argparse():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--circuit', default='Spa', type=str,
                        help='Input circuit of race data that you want to get.')
    parser.add_argument('--node_size', default=13, type=int,
                        help='Number of each position node that can be specified in one state.')
    parser.add_argument('--max_velocity', default=50, type=int,
                        help='Size of maximum velocity with one movement.')
    parser.add_argument('--min_velocity', default=10, type=int,
                        help='Size of minimum velocity with one movement.')
    parser.add_argument('--velocity_interval', default=11, type=int,
                        help='- Number of speeds that can be specified in one movement. It is obtained by dividing the value between max velocity and min velocity into equal parts.')
    parser.add_argument('--max_theta', default=60, type=int,
                        help='Size of maximum degree with one movement. The max theta value is allocated for each direction.')
    parser.add_argument('--theta_interval', default=13, type=int,
                        help='Number of degree that can be specified in one movement. It is obtained by dividing the value between theta intervals into equal parts.')
    parser.add_argument('--save', default=True, type=bool,
                        help='Determine saving result file.')

    return parser

def main(args=None):
    trackPlotter = TrackPlotter(args.circuit)
    trackPlotter.optimization(args.node_size, args.max_velocity, args.min_velocity, args.velocity_interval,args.max_theta,args.theta_interval,args.save)

if __name__ == '__main__':
    args = get_argparse().parse_args()
    main(args)