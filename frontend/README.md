# Introduction

Scientific articles, especially Wikipedia articles, often have formulas that cannot be processed by search engines without annotations. In order to improve the annotation process in the editing of Wikipedia articles, suggestions for potential Wikidata QIDs are loaded using the script stored here. For this purpose, the script uses the MathWikiLink API, which returns QIDs for passed identifiers or formula concepts.

### Definitions

##### Identifiers
Identifiers in mathematical formulae are the meanings attached to symbols contained within a formula. For example, the identifier *E* means "*energy*" in the formula *E=mc^2*.

##### Formula Concept
The concept of a formula is the name or meaning (semantics) that can be associated with it. 
For example, a possible concept name annotation for the formula *E=mc2* would be "*mass-energy equivalence*".


## Getting Started

### Prerequisites

Mediawiki container for Docker. 

See here:
[https://hub.docker.com/_/mediawiki](https://hub.docker.com/_/mediawiki)


### Installing

Download the script from this git and paste it into the wikipedia site for your individual user scripts:

[https://de.wikipedia.org/wiki/user:**USERNAME**/common.js](https://www.youtube.com/watch?v=xvFZjo5PgG0)
(Change the username in this link!)

## Usage

When implemented correctly, you can go to a formula on wikipedia and open it in the extended formula visual editor. (Note: Does not work in the quick editor due to space restrictions)
When going to the options tab, the script will automatically show up to three suggestions from multiple sources in the backend .json-file for the identifier or formula string beneath the QID-text field. 

<!-------- ToDo: SCREENSHOT or GIF of showcase --------->

Suggestions are presented with their name and correlating wikidata QID. Copy the appropriate QID or wikidata item name into the QID text field to correctly annotate the identifier or formula.

## Authors

* Fabian Wolz
* Johannes Christians
* Antonin Königsfeld

## Acknowledgments

We thank the MathWikiLink backend team for hosting the .json-files for identifier and formula QID [suggestions](https://github.com/gipplab/MathWikiLink/tree/master/dataset).
