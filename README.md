Suche
------

An Elasticsearch Export Framework
 
## Documentation

### Installation

```bash
pip install suche
```

You need to have ```elasticsearch``` installed and running. 
More info: [https://www.elastic.co/](https://www.elastic.co/) 
    
### Basic Usage

```python
from suche import Suche
suche = Suche(elastic_address, elastic_port, index)
```
**elastic_address:** address for elasticsearch (optional)

**elastic_port:** port number for elasticsearch (optional)

**index:** index name of elasticsearch


## Specific Functions

#### Change Index
```python
suche.set_index(index)
```
**index:** index name of elasticsearch


## Configuration Options


ELASTIC_ADDRESS: Address to elasticsearch

ELASTIC_PORT:  elasticsearch port

Either, create a configuration file with name ```suche_config.json``` 
in the pwd, like below

```json
{
  "ELASTIC_ADDRESS": "localhost",
  "ELASTIC_PORT": 9200,
  "SUCHE_OUTPUT": ""
}
```

or

create Suche objects with custom configuration options required 
as shown below

```python
suche = Suche(elastic_address="localhost", elastic_port=9300, 
    index="default")
```

## Input Format For query

####The query input should be on below json Format for FilterData.

```json
    {
        "key": "name",
        "query": "atm"
     }

```

####The query input should be on below json Format for MultiFilter Data.

```json
    [
        {
            "key": "name",
            "query": "atm"
        },
        {
            "key": "name",
            "query": "almy"
        }
     ]


```

## Advanced Features

#### AllData

```python
suche.allData(doc_type = "person", fields= ["email", "name"], output_format= 'csv')
```
Matches all data in the doc type ```doc_type``` and filter data 
in accordance to ```fields``` and return  ```output_format```

Currently available ```output_format``` : csv and pickle

#### FilterData

Filtering takes a single json string to process

```python
suche.filterData(doc_type="person", match_json = { "key": "is_custom_domain", "query": "false" }, 
                fields = ["email", "name", "current_location"], output_format= 'pkl')
```
* Follow input format

Matches data in the doc type ```doc_type```, ```match_json``` and filter data 
in accordance to ```fields``` and return ```output_format```


#### MultiFilter Data

multifiltering takes a dict with multiple json to process output

```python
suche.multiMatch(doc_type="person", multiple_match = [{ "key": "data", "query": "false" }, { "key": "country", "query": "India" }],
                fields = ["email", "name", "current_location"], output_format= 'pkl')
```
* Follow input format

Matches data in the doc type ```doc_type```, ```multiple_match``` and filter data 
in accordance to ```fields``` and return ```output_format```
