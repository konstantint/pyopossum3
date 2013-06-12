'''
SQLAlchemy-based access to the oPOSSUM3 TFBS database.

Copyright 2013, Konstantin Tretyakov.
http://kt.era.ee/

Licensed under MIT license.
'''
import shutil, cPickle, os, pytest
from pyopossum3 import Opossum
from sqlalchemy import create_engine

TEST_URL = "mysql://opossum_r:@opossum.cmmt.ubc.ca/oPOSSUM3_human"
TEST_DIR = "tmp_TestOpossumCacheDir"

def setup_module():
    if os.path.isfile(TEST_DIR):
        os.unlink(TEST_DIR)
    if os.path.isdir(TEST_DIR):
        shutil.rmtree(TEST_DIR)
teardown_module = setup_module

def test_cache():
    e = create_engine(TEST_URL)
    
    # Init metadata by reflection
    md = Opossum._init_metadata(e, None)
    assert md is not None
    assert 'conserved_tfbss' in md.tables
    
    # Check saving to cache
    assert not os.path.exists(TEST_DIR)
    md = Opossum._init_metadata(e, TEST_DIR)
    assert os.path.exists(TEST_DIR)
    assert os.path.exists(os.path.join(TEST_DIR, 'metadata.pickle'))
    with open(os.path.join(TEST_DIR, 'metadata.pickle'), 'rb') as f:
        md_test = cPickle.load(f)
    assert 'conserved_tfbss' in md_test
    
    # Check loading from cache
    md = Opossum._init_metadata(None, TEST_DIR)
    assert 'conserved_tfbss' in md
    
    # Check exception
    with pytest.raises(Exception):
        Opossum._init_metadata(None, None)

def test_opossum():
    o = Opossum(TEST_URL, cache_dir=TEST_DIR)
    assert 'conserved_tfbss' in o.metadata
    assert o.ConservationLevel.query.first().level == 1
    assert o.DbInfo.query.first().ucsc_db == 'hg19'
    assert o.ConservedTfbs.query.first().gene.chr == 'X'
