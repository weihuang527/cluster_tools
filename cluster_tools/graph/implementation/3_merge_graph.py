import argparse

import z5py
import nifty
import nifty.distributed as ndist


def graph_step3(graph_path, last_scale, initial_block_shape, n_threads):
    factor = 2**last_scale
    block_shape = [factor * bs for bs in initial_block_shape]

    f_graph = z5py.File(graph_path)
    # TODO write shape attribute
    shape = f_graph.attrs['shape']
    blocking = nifty.tools.blocking(roiBegin=[0, 0, 0],
                                    roiEnd=list(shape),
                                    blockShape=block_shape)

    input_key = 'sub_graphs/s%i' % last_scale
    output_key = 'graph'
    block_list = range(blocking.numberOfBlocks)
    # TODO implement n_threads
    ndist.mergeSubgraphs(graph_path,
                         input_key,
                         blockPrefix="block_",
                         blockIds=block_list,
                         outKey=output_key,
                         numberOfThreads=n_threads)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("graph_path", type=str)
    parser.add_argument("last_scale", type=int)
    parser.add_argument("--block_file", type=str)
    parser.add_argument("--initial_block_shape", nargs=3, type=int)
    parser.add_argument("--n_threads", type=int)
    args = parser.parse_args()

    graph_step3(args.graph_path, args.last_scale,
                list(args.initial_block_shape), args.n_threads)
