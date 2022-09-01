<p align="center">
  <img src="https://github.com/philsMINT/MathWikiLink/blob/master/media/MathWikiLink_logo.png"/>
</p>

# MathWikiLink

An Entity Linking System for Mathematical Formulae

## Introduction

MathWikiLink provides an API for the retrieval of mathematical entity linking recommendations based on various sources (mainly Wikidata) for the use in further projects.

Some content already exists as a dependency from the AnnoMathTex-Project. MathWikiLink runs as a service that can be queried via HTTP and delivers JSON-content in the form of a dictionary.

Queries can consist of identifiers or formulae. The API returns a dictionary containing the entities (corresponding QID for Wikidata) and a short description.

The efforts for providing a frontend integrated into Wikipedia can be found under [/frontend](https://github.com/gipplab/MathWikiLink/tree/master/frontend).

## Definitions (from [AnnoMathTex](https://github.com/gipplab/AnnoMathTex))

### Identifiers
Identifiers in mathematical formulae are the meanings attached to symbols contained within a formula. For example, the identifier *E* means "*energy*" in the formula $E=mc^2$.

### Formula Concept
The concept of a formula is the name or meaning (semantics) that can be associated with it. 
For example, a possible concept name annotation for the formula $E=mc^2$ would be "*mass-energy equivalence*".

# Installation

For compatibility reasons ***Python Version 3.6.15 is highly recommended***.

Clone the repository. 

    git clone https://github.com/gipplab/MathWikiLink

Set up a virtual environment (Python-Package "virtualenv" needed, be sure to use Python 3.6)

    python -m virtualenv mathwikilink_env

Activate the environment (Linux). 

    source mathwikilink_env/bin/activate

Activate the environment (Windows).

    mathwikilink_env\Scripts\activate

Install the requirements (due to compatibility issues it is possible that setuptools 56.2.0 need to be installed
before)

    cd MathWikiLink
    pip install setuptools==56.2.0
    pip install -r requirements.txt

Run the API by

    python api.py

The file backend/run/SECRET.key is needed to access the data repository.

Deactivate the environment by typing

    deactivate

within the environment (shell).

# Usage of API

`http://127.0.0.1:5000/api/v1/identifier_names?identifier=<IDENTIFIER>`
 
`http://127.0.0.1:5000/api/v1/formula_names?formula=<FORMULA>`

The formula parameter needs to be provided as complete formula with equality sign, single mathematical terms won't work.

The optional GET-parameter "limit" can be given, to get more or fewer results, default is 5.

With the optional "source" parameter, it can be chosen if the recommendations are retrieved from local indices, which 
can be updated (source=index, default) or by an inbuilt legacy AnnoMathTex instance (source=annomathtex) (see [Helper scripts](#helper-scripts)).

# Example

The following query for the identifier $E$ returns:

```http://127.0.0.1:5000/api/v1/identifier_names?identifier=E```

```yaml
{
    "arXivEvaluationItems": [
        {
            "name": "energy",
            "qid": "Q11379"
        },
        {
            "name": "bundle",
            "qid": "N/A"
        },
        {
            "name": "vector",
            "qid": "N/A"
        },
        {
            "name": "space",
            "qid": "Q472971"
        },
        {
            "name": "field",
            "qid": "Q185674"
        }
    ],
    "wikidata1Results": [
        {
            "name": "Erdős–Borwein constant",
            "qid": "Q1349661"
        },
        {
            "name": "energy",
            "qid": "Q11379"
        },
        {
            "name": "minimum explosive concentration",
            "qid": "Q77569705"
        },
        {
            "name": "half maximal effective concentration",
            "qid": "Q286136"
        }
    ],
    "wikipediaEvaluationItems": [
        {
            "name": "kinetic energy",
            "qid": "Q46276"
        },
        {
            "name": "vector bundle",
            "qid": "N/A"
        },
        {
            "name": "field",
            "qid": "Q185674"
        },
        {
            "name": "energy",
            "qid": "Q11379"
        },
        {
            "name": "modules",
            "qid": "N/A"
        }
    ]
}
```

# Helper scripts

## [create_identifier_index.py](https://github.com/gipplab/MathWikiLink/blob/master/backend/api/create_identifier_index.py)

The create-identifier-index script creates a JSON formatted recommendation identifier index from local source files by 
employing AnnoMathTex classes as well as postprocessing and reformatting, saving it to 
[/dataset/identifier_index.json](https://github.com/gipplab/MathWikiLink/blob/master/dataset/identifier_index.json).

## [formula_index_retrieval.py](https://github.com/gipplab/MathWikiLink/blob/master/backend/api/formula_index_retrieval.py)
The formula-index-retrieval script creates JSON formatted recommendation formulae and QID indices from a Wikidata SPARQL
queries saving it to 
[/dataset/formula_string_index.json](https://github.com/gipplab/MathWikiLink/blob/master/dataset/formula_string_index.json) 
and [/dataset/formula_qid_index.json](https://github.com/gipplab/MathWikiLink/blob/master/dataset/formula_qid_index.json).

## [update_identifier_index_SPARQL.py](https://github.com/gipplab/MathWikiLink/blob/master/backend/api/update_identifier_index.py)

The identifier-update script works without further parameters. By default the file dataset/identifier_index.json will be used.
The script takes each identifier, queries Wikidata via SPARQL and looks for new results. If new elements exist (key: QID) they will be added the the given local JSON-file.




# Helper classes

## [AnnoMathTexEvaluationHandler](https://github.com/gipplab/MathWikiLink/blob/master/backend/api/helper_classes/annomathtex_evaluation_handler.py)

The Class employs the inbuilt AnnoMathTex instance for recommendation retrieval via HTTP GET requests in api.py.

## [IndexEvaluationHandler](https://github.com/gipplab/MathWikiLink/blob/master/backend/api/helper_classes/index_evaluation_handler.py)

The class evaluates the identifier index provided in /dataset/identifier_index.json or formulae and QID indices via the
formula_index_retrieval.py helper script in /api for recommendation retrieval via HTTP GET requests in api.py.

# Open ToDos

- Create docker container for hosting MathWikiLink with integrated cronjob to enable frequent index update
- Provide forceupdate argument to api for index updates
- Identify potential to optimize QID retrieval for formulae by merging with name retrieval
- Compare performance Wikidata identifier parts (SPARQL) vs. fuzzy string (dump) retrieval


# Acknowledgments

This work heavily relies on and reuses code from [AnnoMathTex](https://github.com/gipplab/AnnoMathTex).
