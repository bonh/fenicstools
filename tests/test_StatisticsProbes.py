#!/usr/bin/env py.test

import pytest
from dolfin import FunctionSpace, UnitCubeMesh, UnitSquareMesh, interpolate, \
                   Expression, VectorFunctionSpace, MPI, mpi_comm_world
from fenicstools import StatisticsProbes
from numpy import array
from fixtures import *


def test_StatisticsProbes_segregated_2D(V2):
    u0 = interpolate(Expression('x[0]', degree=1), V2)
    v0 = interpolate(Expression('x[1]', degree=1), V2)
    x = array([[0.5, 0.25], [0.4, 0.4], [0.3, 0.3]])
    probes = StatisticsProbes(x.flatten(), V2, True)

    for i in range(5):
        probes(u0, v0)
        
    p = probes.array()
    if MPI.rank(mpi_comm_world()) == 0:
        assert round(p[0,0] - 2.5, 7) == 0
        assert round(p[0,4] - 0.625, 7) == 0


def test_StatisticsProbes_segregated_3D(V3):
    u0 = interpolate(Expression('x[0]', degree=1), V3)
    v0 = interpolate(Expression('x[1]', degree=1), V3)
    w0 = interpolate(Expression('x[2]', degree=1), V3)
    x = array([[0.5, 0.25, 0.25], [0.4, 0.4, 0.4], [0.3, 0.3, 0.3]])
    probes = StatisticsProbes(x.flatten(), V3, True)

    for i in range(5):
        probes(u0, v0, w0)
        
    p = probes.array()
    if MPI.rank(mpi_comm_world()) == 0:
        assert round(p[0,0] - 2.5, 7) == 0
        assert round(p[0,4] - 0.3125, 7) == 0


def test_StatisticsProbes_vector_2D(VF2):
    u0 = interpolate(Expression(('x[0]', 'x[1]'), degree=1), VF2)
    x = array([[0.5, 0.25], [0.4, 0.4], [0.3, 0.3]])
    probes = StatisticsProbes(x.flatten(), VF2)

    for i in range(5):
        probes(u0)
        
    p = probes.array()
    if MPI.rank(mpi_comm_world()) == 0:
        assert round(p[0,0] - 2.5, 7) == 0
        assert round(p[0,4] - 0.625, 7) == 0


def test_StatisticsProbes_vector_3D(VF3):
    u0 = interpolate(Expression(('x[0]', 'x[1]', 'x[2]'), degree=1), VF3)
    x = array([[0.5, 0.25, 0.25], [0.4, 0.4, 0.4], [0.3, 0.3, 0.3]])
    probes = StatisticsProbes(x.flatten(), VF3)

    for i in range(5):
        probes(u0)
        
    p = probes.array()
    if MPI.rank(mpi_comm_world()) == 0:
        assert round(p[0,0] - 2.5, 7) == 0
        assert round(p[0,4] - 0.3125, 7) == 0

if __name__=="__main__":
    test_StatisticsProbes_segregated_2D(V2(mesh_2D()))
