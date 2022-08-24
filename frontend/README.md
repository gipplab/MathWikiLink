# Introduction

Scientific articles, especially Wikipedia articles, often have formulae that cannot be processed by search engines without annotations. In order to improve the annotation process in the editing of Wikipedia articles, suggestions for potential Wikidata QIDs are loaded using the script stored here. For this purpose, the script uses the .json files provided by the MathWikiLink API, which return QIDs for passed identifiers or formula concepts.

### Definitions

##### Identifiers
Identifiers in mathematical formulae are the meanings attached to symbols contained within a formula. For example, the identifier *E* means "*energy*" in the formula *E=mc²*.

##### Formula Concept
The concept of a formula is the name or meaning (semantics) that can be associated with it. 
For example, a possible concept name annotation for the formula *E=mc²* would be "*mass-energy equivalence*".

## Previous Work in Preperation for the Script Usage

We changed the MediaWiki Code (that Wikipedia uses for its site) multiple times to add the funcionality of changing the QID Value for formulae and identifiers inside the Visual Editor Formula Quick editor as well as the full-fledged editor.
You can read through the changes in detail [here](https://gerrit.wikimedia.org/r/c/mediawiki/extensions/Math/+/798804) and [here](https://gerrit.wikimedia.org/r/c/mediawiki/extensions/Math/+/807527).

We will change the MediaWiki Code again soon, since the JS Script is build upon a JS Hook inside the *ve.ui.MwLatexDialog* file that activates whenever the user clicks on the formula editor. This Hook, however, is not yet implemented inside the live Wikipedia Version.


## Getting Started

### Prerequisites

Download/copy the JavaScript file from this [github branch](https://github.com/gipplab/MathWikiLink/blob/master/frontend/script.js).


### Installing

Paste the Script into the wikipedia site for your individual user scripts:

[https://de.wikipedia.org/wiki/user:**USERNAME**/common.js](https://www.youtube.com/watch?v=xvFZjo5PgG0)
(Change the username in this link!)

## Usage

**---- NOTE: This Script does not work yet, since the neccessary JS Hook is missing inside the Wikipedia files. ----**

When implemented correctly, you can go to a formula concept or identifier on wikipedia and open it in the extended formula visual editor. (Note: Does not work in the quick editor due to space restrictions)
When going to the options tab, the script will automatically show up to three suggestions from multiple sources in the backend .json-file for the identifier or formula string beneath the QID-text field. 

<!-------- ToDo: SCREENSHOT or GIF of showcase --------->

Suggestions are presented with their name and correlating wikidata QID. Copy the appropriate QID or wikidata item name into the QID text field to correctly annotate the identifier or formula concept.

## Known Bugs | Open ToDos

Currently, the script produces suggestions when opening up the formula editor. When changing the Formula/Identifier, users have to close the editor and reopen it to get the new suggestions. Since this is quite tedious, we are looking for ways to embed the JS Hook in another place, preferably when the Input changes or the user switches to the Options tab inside the editor.


## Authors

* Fabian Wolz
* Johannes Christians
* Antonin Königsfeld

## Acknowledgments

We thank the MathWikiLink backend team for hosting the .json-files for [identifier and formula QID suggestions](https://github.com/gipplab/MathWikiLink/tree/master/dataset).
