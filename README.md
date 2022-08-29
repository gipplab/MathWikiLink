<p align="center">
  <img src="https://github.com/philsMINT/MathWikiLink/blob/master/media/MathWikiLink_logo.png"/>
</p>

# MathWikiLink

An Entity Linking System for Mathematical Formulae

## Introduction

MathWikiLink provides an API for usage in further projects to provide entity linking recommendations based on various sources (mainly Wikidata).

Some content already exists as a dependency from the AnnoMathTex-Project. MathWikiLink runs as a service that can be queried via HTTP and delivers JSON-content in the form of a dictionary.

Queries can consist in identifiers or formulae. The API returns a dictionary containing the entities (corresponding QID for Wikidata) and a short description.

## Definitions (taken from the AnnoMathTex-README)

### Identifiers
Identifiers in mathematical formulae are the meanings attached to symbols contained within a formula. For example, the identifier *E* means "*energy*" in the formula *E=mc^2*.

### Formula Concept
The concept of a formula is the name or meaning (semantics) that can be associated with it. 
For example, a possible concept name annotation for the formula *E=mc2* would be "*mass-energy equivalence*".

# Installation

Clone the repository. 

    git clone https://github.com/gipplab/MathWikiLink

Set up a virtual environment (Python-Package "virtualenv" needed)

    virtualenv mathwikilink_env

Activate the environment. 

    source mathwikilink_env/bin/activate

Install the requirements

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
  
The optional GET-parameter "limit" can be given, to get more or fewer results, default is 10.


# Helper scripts

## create_identifier_index.py

## update_identifier_index_SPARQL.py

The identifier-update script works without further parameters. By default the file dataset/identifier_index.json will be used.
The script takes each identifier, queries Wikidata via SPARQL and looks for new results. If new elements exist (key: QID) they will be added the the given local JSON-file.

# Helper classes
