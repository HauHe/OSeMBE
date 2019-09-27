# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:50:24 2019

@author: haukeh
"""

# -*- coding: utf-8 -*-

"""
Service functions for reeem_db

This file is part of project REEEM (https://github.com/ReeemProject/reeem_db).
It's copyrighted by the contributors recorded in the version control history:
ReeemProject/reeem_db/database_adapter/reeem_io.py

SPDX-License-Identifier: AGPL-3.0-or-later
"""

__copyright__ = "© Hauke Henke"
__license__ = "GNU Affero General Public License Version 3 (AGPL-3.0)"
__license_url__ = "https://www.gnu.org/licenses/agpl-3.0.en.html"
__author__ = "Hauke Henke"
__version__ = "v0.0.1"

import os
import time
import getpass
import logging
from sqlalchemy import * 
import configparser as cp
import pandas as pd
import oedialect

# parameter
config_file = 'oep_io_config.ini'
config_section = 'oep'
log_file = 'oep_adapter.log'
# sys.tracebacklimit = 0
cfg = cp.RawConfigParser()

#%% logger
def logger():
    """Configure logging in console and log file.
    
    Returns
    -------
    rl : logger
        Logging in console (ch) and file (fh).
    """

    # set root logger (rl)
    rl = logging.getLogger('REEEMLogger')
    rl.setLevel(logging.INFO)
    rl.propagate = False

    # set format
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # console handler (ch)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    rl.addHandler(ch)

    # file handler (fh)
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    rl.addHandler(fh)

    return rl

#%% Scenario log
def scenario_log(con, project, version, io, schema, table, script, comment):
    """Write an entry in scenario log table.

    Parameters
    ----------
    con : connection
        SQLAlchemy connection object.
    project : str
        Project name.
    version : str
        Version number.
    io : str
        IO-type (input, output, temp).
    schema : str
        Database schema.
    table : str
        Database table.
    script : str
        Script name.
    comment : str
        Comment.

    """

    sql_scenario_log_entry = text("""
        INSERT INTO OSeMBE-data.scenario_log
            (project,version,io,schema_name,table_name,script_name,entries,
            comment,user_name,timestamp,metadata)
        SELECT  '{0}' AS project,
                '{1}' AS version,
                '{2}' AS io,
                '{3}' AS schema_name,
                '{4}' AS table_name,
                '{5}' AS script_name,
                COUNT(*) AS entries,
                '{6}' AS comment,
                session_user AS user_name,
                NOW() AT TIME ZONE 'Europe/Berlin' AS timestamp,
                obj_description('{3}.{4}' ::regclass) ::json AS metadata
        FROM    {3}.{4};""".format(project,version, io, schema, table, script,
                                   comment))

    con.execute(sql_scenario_log_entry)

#%% Filename split following REEEM conventions
def reeem_filenamesplit(filename):
    """file name identification"""

    filenamesplit = filename.replace(".xlsx", "").replace(".csv", "").split("_")
    fns = {}
    fns['day'] = filenamesplit[0]
    fns['pathway'] = filenamesplit[1]
    fns['model'] = filenamesplit[2]
    fns['framework'] = filenamesplit[3]
    fns['version'] = filenamesplit[4]
    fns['io'] = filenamesplit[5]
    return fns

#%% Check if OEP db Table exists and if not create one
def oep_table(con, db_table, schema_name):
    if fns['io'] == "Input":
        if not engine.dialect.has_table(con, db_table, schema_name):
            reeem_osembe_input_table.create()
            print('Created table')
        else:
            print('Table already exists')
    else:
        if not engine.dialect.has_table(con, db_table, schema_name):
            reeem_osembe_output_table.create()
            print('Created table')
        else:
            print('Table already exists')

#%% Sending OSeMBE df to OEP db
def osembe_2_oep_db(filename, fns, empty_rows, schema_name, region, con):
    """read excel file and sheets, make dataframe and write to database"""

    # read file
    path = os.path.join('Model_Data', filename)
    xls = pd.ExcelFile(path)
    df = pd.read_excel(xls, region, header=empty_rows, index_col='ID')
    log.info('...read sheet: {}'.format(region))

    # make dataframe
    df.columns = ['indicator', 'unit',
                  '2015', '2016', '2017', '2018', '2019', '2020', '2021',
                  '2022', '2023', '2024',
                  '2025', '2026', '2027', '2028', '2029', '2030', '2031',
                  '2032', '2033', '2034',
                  '2035', '2036', '2037', '2038', '2039', '2040', '2041',
                  '2042', '2043', '2044',
                  '2045', '2046', '2047', '2048', '2049', '2050', 'category',
                  'aggregation']
    df.index.names = ['nid']
    # print(df.head())
    # print(df.dtypes)

    # seperate columns
    dfunit = df[['category', 'indicator', 'unit', 'aggregation']].copy().dropna()
    dfunit.index.names = ['nid']
    dfunit.columns = ['category', 'indicator', 'unit', 'aggregation']
    # print(dfunit.head())
    # print(dfunit.dtypes)

    # drop seperated columns
    dfclean = df.drop(['category', 'indicator', 'unit', 'aggregation'],
                      axis=1).dropna()
    # print(dfclean.head())
    # print(dfclean)

    # stack dataframe
    dfstack = dfclean.stack().reset_index()
    dfstack.columns = ['nid', 'year', 'value']
    # dfstack.set_index(['nid','year'], inplace=True)
    dfstack.index.names = ['id']
    # print(dfstack)

    # join dataframe for database
    dfdb = dfstack.join(dfunit, on='nid')
    dfdb.index.names = ['dfid']
    dfdb['pathway'] = fns['pathway']
    dfdb['framework'] = fns['framework']
    dfdb['version'] = fns['version']
    dfdb['region'] = region
    dfdb['updated'] = fns['day']
#    print(dfdb)
    # dfdb['updated'] = (datetime.datetime.fromtimestamp(time.time())
    #     .strftime('%Y-%m-%d %H:%M:%S'))
    # print(dfdb.head())

    # copy dataframe to database
    dfdb.to_sql(con=con,
                schema=schema_name,
                name=db_table,
                if_exists='append',
                index=True)
    log.info('......sheet {} sucessfully imported...'.format(region))

#%% Input
filenames = [
            '2019-07-29_B0C0T0E0_OSeMBE_FrameworkNA_DataV2_Input.xlsx',
            '2019-07-29_B0C0T0E0_OSeMBE_FrameworkNA_DataV2_Output.xlsx' ]

regions = ['EU+CH+NO', 'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 
           'ES', 'FI', 'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 
           'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 
           'UK']

empty_rows = 5

# database table
schema_name = 'OSeMBE-data'
db_table_input = 'reeem_osembe_input'
db_table_output = 'reeem_osembe_output'

#%%
if __name__ == '__main__':
    
    # logging
    log = logger()
    start_time = time.time()
    log.info('script started...')
    
    # OEP session
    user = input('Enter OEP-username:')
    token = getpass.getpass('Token:')

    OEP_URL = 'openenergy-platform.org'
    OED_STRING = f'postgresql+oedialect://{user}:{token}@{OEP_URL}'
    
    engine = create_engine(OED_STRING)
    metadata = MetaData(bind=engine)
    print(metadata)
    
    reeem_osembe_input_table = Table (
            db_table_input,
            metadata,
            Column('nid', FLOAT(50)),
            Column('year', INTEGER),
            Column('value', FLOAT(50)),
            Column('category', VARCHAR(50)),
            Column('indicator', VARCHAR(50)),
            Column('unit', VARCHAR(50)),
            Column('aggregation', VARCHAR(50)),
            Column('pathway', VARCHAR(50)),
            Column('framework', VARCHAR(50)),
            Column('version', VARCHAR(50)),
            Column('region', VARCHAR(50)),
            Column('updated', VARCHAR(50)),
            schema=schema_name
            )
    
    reeem_osembe_output_table = Table (
            db_table_output,
            metadata,
            Column('nid', FLOAT(50)),
            Column('year', INTEGER),
            Column('value', FLOAT(50)),
            Column('category', VARCHAR(50)),
            Column('indicator', VARCHAR(50)),
            Column('unit', VARCHAR(50)),
            Column('aggregation', VARCHAR(50)),
            Column('pathway', VARCHAR(50)),
            Column('framework', VARCHAR(50)),
            Column('version', VARCHAR(50)),
            Column('region', VARCHAR(50)),
            Column('updated', VARCHAR(50)),
            schema=schema_name
            )
        
    con = engine.connect()
    print('Connection established')
    
    log.info('...read file(s)...')
    
    # import files
    for filename in filenames:
    
        # file and table
        fns = reeem_filenamesplit(filename)
        
        # i/o
        if fns['io'] == "Input":
            db_table = db_table_input
        else:
            db_table = db_table_output
        
        oep_table(con, db_table, schema_name)
        # log files
        log.info('read file: {}'.format(filename))
        log.info('...model: {}'.format(fns['model']))
        log.info('...pathway: {}'.format(fns['pathway']))
        log.info('...framework: {}'.format(fns['framework']))
        log.info('...version: {}'.format(fns['version']))
        log.info('...i/o: {}'.format(fns['io']))
        log.info('...regions: {}'.format(regions))
        log.info('...database table: OSeMBE-data.{}'.format(db_table))

        # import
        for region in regions:
            osembe_2_oep_db(filename, fns, empty_rows,
                            schema_name, region, con)

        # scenario log
        #scenario_log(con, 'REEEM', __version__, 'import', schema_name, db_table,
         #           os.path.basename(__file__), filename)


    # close connection
    con.close()
    log.info('...script successfully executed in {:.2f} seconds...'
             .format(time.time() - start_time))
    log.info('...database connection closed. Goodbye!')
