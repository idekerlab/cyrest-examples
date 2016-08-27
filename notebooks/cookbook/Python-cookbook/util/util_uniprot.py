#-*- coding:utf-8 -*-
import pandas as pd
import requests

def uniprot_id_mapping_service(query=None, from_id=None, to_id=None):
    # Uniprot ID Mapping service
    url = 'http://www.uniprot.org/mapping/'
    payload = {
        'from': from_id,
        'to': to_id,
        'format':'tab',
        'query': query
    }

    res = requests.get(url, params=payload)

    df = pd.read_csv(res.url, sep='\t')
    res.close()
    return df
