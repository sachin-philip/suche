from elasticsearch import Elasticsearch
import pickle
import csv
import json
import os.path

__ver__ = '0.4.6'

"""
Suche - An Elasticsearch Export Framework
"""
class Suche(object):

    """
    init configuration
    ##PARAMS##

    address: elastic search address - not required field :
             default : localhost
    port   : port number of elasticsearch - not a required field :
             default :9200
    index  : index name for the process - required field
    """
    def __init__(self, address="localhost", port=9200, index=""):

        if not address or port:
            try:
                conf_string = open("suche_config.json", 'r').read()
                self.config = json.loads(conf_string)
            except (IOError, ValueError):
                self.config = {
                                "ELASTIC_ADDRESS": "localhost",
                                "ELASTIC_PORT": 9200,
                                "SUCHE_OUTPUT": ""
                                }

        self.address = address if address else self.config.get("ELASTIC_ADDRESS")
        self.port = port if port else self.config.get("ELASTIC_PORT")
        self.es_address = str(self.address)+ ":" + str(self.port)
        self.es = Elasticsearch(self.es_address)
        self.index = index


    def set_index(self, index):
        """
        function to set index/ change index after initializing
        """
        if type(index) == str:
            self.index = index
        else:
            print "enter a valid string"


    def _export_csv(self, list_out, header):
        """
        Export Csv function
        PARAM
        list_out : dict that contains data
        header : list that contains header
        """
        f_name = os.path.join(self.config.get("SUCHE_OUTPUT") + self.output_file + ".csv")
        with open(f_name, "w") as finalfile:
            output_file = csv.DictWriter(finalfile, header)
            output_file.writeheader()
            for dat in list_out:
                output_file.writerow(dat)
        print "output file can be found at %s" % f_name


    def _export_pkl(self, list_out):
        """
        Export in Pickle format
        """
        f_name = os.path.join(self.config.get("SUCHE_OUTPUT") + self.output_file + ".pkl")
        flick = open(f_name, 'wb')
        pickle.dump(list_out , flick)
        flick.close()
        print "output file can be found at %s" % f_name


    def allData(self, doc_type, fields, output_format=None, filename=None):
        """
        All Match data export
        """
        self.fields = fields
        self.output_format = output_format.lower() if output_format else None
        self.output_file = filename.lower() if filename else "suche_export"
        search = self.es.search(
            index = self.index,
            doc_type = doc_type,
            scroll = '2m',
            search_type = 'scan',
            size = 1000,
            body = {
                "query": {
                    "match_all" : {}
                    }, "fields" : self.fields
                })
        sid = search['_scroll_id']
        scroll_size = search['hits']['total']
        return self._preProcess(sid, scroll_size)


    def filterData(self, doc_type, match_json , fields, output_format=None, filename=None):
        """
        Filter Querying

        CHANGE PARAM
        match_json : json for the filtered quering

        """
        match_json_data = {match_json['key']: match_json['query']}
        self.fields = fields
        self.output_format = output_format.lower() if output_format else None
        self.output_file = filename.lower() if filename else "suche_export"
        search = self.es.search(
            index = self.index,
            doc_type = doc_type,
            scroll = '2m',
            search_type = 'scan',
            size = 1000,
            body = {
                "query": {
                    "match" : match_json_data
                    }, "fields" : self.fields
                })
        sid = search['_scroll_id']
        scroll_size = search['hits']['total']
        return self._preProcess(sid, scroll_size)


    def multiMatch(self, doc_type, multiple_match, fields, output_format=None, filename=None):
        """
        Multi match quering

        PARAMS
        multiple match = dict
        """
        string = self._frameJson(multiple_match)
        len_string = len(string)
        self.fields = fields
        self.output_format = output_format.lower() if output_format else None
        self.output_file = filename.lower() if filename else "suche_export"
        search = self.es.search(
            index = self.index,
            doc_type = doc_type,
            scroll = '2m',
            search_type = 'scan',
            size = 1000,
            body ={
                    "query" : {
                        "bool" : {
                            "should" : string,
                            "minimum_should_match" : len_string,
                        }
                    }
                })
        sid = search['_scroll_id']
        scroll_size = search['hits']['total']
        return self._preProcess(sid, scroll_size, multi=True)


    def _frameJson(self, dict_val, multi=False):
        """
        Frame json
        """
        rise_json = []
        if multi:
            val = json.loads(dict_val)
            rise_json.append({"match" : {val['key'] : val['query']}})
        else:     
            for val in dict_val:
                rise_json.append({"match" : {val['key'] : val['query']}})
        return rise_json


    def _preProcess(self, sid, scroll_size, multi=False):
        """
        Data Proprocessing Function
        Formats data in to clean list
        """

        temp_list = []
        while (scroll_size > 0):
            page = self.es.scroll(scroll_id = sid, scroll = '2m')
            # Update the scroll ID
            sid = page['_scroll_id']
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])
            data = page['hits']['hits']
            # print "scroll size: " + str(scroll_size)
            for dat in data:
                temp = {}
                for field in self.fields:
                    if multi:
                        try:
                            temp[field] = dat['_source'][field]
                        except :
                            temp[field] = "---"
                    else:
                        try:
                            temp[field] = dat['fields'][field][0]
                        except :
                            temp[field] = "---"
                try:
                    temp_list.append(temp)
                except Exception as e:
                    print e

        return self._exportProcess(temp_list)


    def _exportProcess(self, lists):
        """
        Export Data Function controller
        """
        if self.output_format == 'csv':
            self._export_csv(lists, self.fields)
        elif self.output_format == 'pkl':
            self._export_pkl(lists)
        else:
            return lists
