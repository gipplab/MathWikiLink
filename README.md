<p align="center">
  <img src="https://github.com/philsMINT/MathWikiLink/blob/master/media/MathWikiLink_logo.png"/>
</p>

# MathWikiLink
An Entity Linking System for Mathematical Formulae

# Installation

TODO - clean installation process needed

# Usage of API

http://127.0.0.1:5000/api/v1/identifier_names?identifier=<IDENTIFIER>
  
http://127.0.0.1:5000/api/v1/formula_names?formula=<IDENTIFIER>
  
The optional GET-parameter "limit" can be given, to get more or fewer results, default is 10.


# Helper scripts

## create_identifier_index.py

## update_identifier_index_SPARQL.py

The identifier-update script works without further parameters. By default the file dataset/identifier_index.json will be used.
The script takes each identifier, queries Wikidata via SPARQL and looks for new results. If new elements exist (key: QID) they will be added the the given local JSON-file.

# Helper classes
