#!/usr/bin/env python

import sys
from pynauty import autgrp, Graph, Version
import pytest

# List of graphs for testing
#
# Structure:
#   [[name, Graph, numorbit, grpsize, generators]]
#
# numorbit, grpsize, generators was calculated by dreadnut
#

def test_autgrp(graph):
    gname, g, numorbit, grpsize, gens = graph
    print(Version())
    print('%-17s ...' % gname, end=' ')
    sys.stdout.flush()
    generators, order, o2, orbits, orbit_no = autgrp(g)
    assert generators == gens and orbit_no == numorbit and order == grpsize


@pytest.mark.parametrize('n', [-1, 2**31, 2**32 + 16, 2**33 + 16, 2**64])
def test_autgrp_number_of_vertices_out_of_range(n):
    with pytest.raises(ValueError):
        autgrp(Graph(n))


def test_autgrp_adjacency_vertex_out_of_range():
    n = 2**33 + 16
    with pytest.raises(ValueError):
        autgrp(Graph(n, adjacency_dict={2**32 + 20: [0]}))
    with pytest.raises(ValueError):
        autgrp(Graph(n, adjacency_dict={0: [2**32 + 20]}))
    for adjacency_dict in ({20: [0]}, {0: [20]}, {0: [-1]}, {-1: [0]},
                           {0: [2**70]}):
        g = Graph(16)
        g.adjacency_dict.update(adjacency_dict)
        with pytest.raises(ValueError):
            autgrp(g)


def test_autgrp_vertex_coloring_too_many_vertices():
    g = Graph(4, vertex_coloring=[{0, 1}])
    g.vertex_coloring.append({0})
    with pytest.raises(ValueError):
        autgrp(g)
    g = Graph(4, vertex_coloring=[{0, 1}])
    g.vertex_coloring.append({50})
    with pytest.raises(ValueError):
        autgrp(g)
