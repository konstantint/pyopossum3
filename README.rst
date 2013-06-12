=====================================================================================
SQLAlchemy-based interface to the oPOSSUM3 transcription factor binding site database
=====================================================================================

The package provides an object-oriented access interface to the `oPOSSUM3 <http://opossum.cisreg.ca/oPOSSUM3/>`_ raw database tables.

Installation
------------

The simplest way to install the package is via ``easy_install`` or ``pip``::

    $ easy_install pyopossum3

Dependencies
------------

- ``SQLAlchemy``
- ``MySQL-Python``

Usage
-----
A usage example is the following::

   from pyopossum3 import Opossum
   o = Opossum("mysql://opossum_r:@opossum.cmmt.ubc.ca/oPOSSUM3_human")
   o.ConservedTfbs.query.first().gene
   o.ExternalGeneId.query.filter(o.ExternalGeneId.external_id.in_(['TSPAN6'])).filter(o.ExternalGeneId.gene.has(chr='X')).first().gene
   ... etc ...

The second line creates a connection to the oPOSSUM server, and the third/fourth query the ``conserved_tfbss`` and ``external_gene_ids`` tables using SQLAlchemy syntax.

Naturally, for heavy analyses, you are suggested to set up your own copy of the database.
See `here <http://opossum.cisreg.ca/oPOSSUM3/download.html>`_ for instructions on how to download the data.

You can get a feeling for the structure of the database by running the following::

    for cls in o.all_orm_classes:
        print cls.query.first()

The main table you should probably care about is ``ConservedTfbs``, which contains matches in the vicinity of each gene, annotated with match score and conservation level.

See also
--------

* Report issues and submit fixes at Github: https://github.com/konstantint/pyopossum3

