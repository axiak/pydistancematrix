pydistancematrix
=================

pydistancematrix will partition a list of edges based on a hard limit of
nodes per graph.

Essentially, this module will take a graph and partition it into subgraphs
of a hard limit size, returning both the lists of nodes in each sub-graph,
and the list of edges that are 'cut' by the partitioning.

For example::

    >>> import distancematrix

    >>> distancematrix.matrix_calls([
        (1, 2),
        (2, 3),
        (7, 8),
        (9, 10)], limit=3)
    [[1, 2, 3], [7, 8], [9, 10]], []

License
--------

BSD

Author
-------

Mike Axiak
