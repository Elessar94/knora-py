[![PyPI version](https://badge.fury.io/py/knora.svg)](https://badge.fury.io/py/knora)

# knora-py
knora-py is a python package containing a command line tool for data model (ontology) creation, a library allowing creation of single resources and mass upload using the bulk import of data into the Knora framework.

The package consists of:
- `Knora` Python modules for accessing Knora using the API (ontology creation, data import/export etc.)
- `knora-create-ontology` A command line program to create an ontology out of a simple JSON description
- `knora-reset-triplestore` A command line program to reset the content of the ontology. Does not require
   a restart of the Knora-Stack.

## Contents
- [Install](#install)
- [Creating an ontology `knora-create-ontology](#creating-an-ontology-with-knora-create-ontology)
  - [Usage](#usage)
- [JSON ontology definition format](#json-ontology-definitionformat)
  - [Prefixes](#prefixes)
  - [Project data](#project-data)
  - [Lists](#lists)
  - [Ontology](#ontology)
  - [Resources](#resources)
  - [Properties](#properties)
  - [A complete example for a full ontology](#a-complete-example-for-a-full-ontology)
- [JSON for lists](#json-for-lists)
  - [A full example for creating lists only](#a-full-example-for-creating-lists-only)
- [Importing data into the triple store](#importing-data-into-the-triple-store)
  - [Creating a Knora access instance](#creating-a-knora-access-instance)
  - [Getting the ontology schema](#getting-the-ontology-schema)
  - [Creating Resources](#creating-resources)
  - [Creating resources with attached images](#creating-resources-with-attached-images)
  - [Complete example](#complete-example)
- [Reseting the triplestore with `knora-reset-triplestore`](#reseting-the-triplestore-with-knora-reset-triplestore)
  - [Usage](#usage)
- [Bulk data import](#bulk-data-import)
  - [Requirements](#requirements)
  

## Install

To install the latest version published on PyPI run:
```
$ pip3 install knora
```

To update to the latest version run:
```
$ pip3 install --upgrade knora
```

To install from source, i.e. this repository run:
```
$ python3 setup.py install
```

## Creating an ontology with `knora-create-ontology`
This script reads a JSON file containing the data model (ontology) definition,
connects to the Knora server and creates the data model.

### Usage:

```bash
$ knora-create-ontology data_model_definition.json
```
It supports the foloowing options:

- _"-s server" | "--server server"_: The URl of the Knora server [default: localhost:3333]
- _"-u username" | "--user username"_: Username to log into Knora [default: root@example.com]
- _"-p password" | "--password password"_: The password for login to the Knora server [default: test]
- _"-v" | "--validate"_: If this flag is set, only the validation of the json is run
- _"-l" | "--lists"_: Only create the lists using [simplyfied schema](#json-for-lists). Please note
  that in this case the project __must__ exist.

## JSON ontology definition format

The JSON file contains a first object an object with the ```prefixes``` for
external ontologies that are being used, followed by the definition of
the project wic h includes all resources and properties:

### Prefixes

```json
{
  "prefixes": {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dcterms": "http://purl.org/dc/terms/"
  },
  "project": {}
}
```

### Project data
The project definitions requires

- _"shortcode"_: A hexadecimal string in the range between "0000" and "FFFF" uniquely identifying the project. 
- _"shortname"_: A short name (string)
- a _"longname"_: A longer string giving the full name for the project
- _descriptions_: Strings describing the projects content. These
  descriptions can be supplied in several languages (currently _"en"_, _"de"_, _"fr"_ and _"it"_ are supported).
  The descriptions have to be given as JSON object with the language as key
  and the description as value. At least one description in one language is required.
- _keywords_: An array of keywords describing the project.
- _lists_: The definition of flat or hierarchical list (thesauri, controlled vocabularies)
- _ontology_: The definition of the data model (ontology)

This a project definition lokks like follows:
  
```json
"project": {
   "shortcode": "0809",
   "shortname": "test"
   "longname": "Test Example",
   "descriptions": {
     "en": "This is a simple example project with no value.",
     "de": "Dies ist ein einfaches, wertloses Beispielproject"
   }
   "keywords": ["example", "senseless"],
   "lists": [],
   "ontology": {}
}
```

### Lists
A List consists of a root node identifing the list and an array of subnodes.
Each subnode may contain again subnodes (hierarchical list).
A node has the following elements:

- _name_: Name of the node. Should be unique for the given list
- _labels_: Language dependent labels
- _comments_: language dependent comments (optional)
- _nodes_: Array of subnodes (optional – leave out if there are no subnodes)

The _lists_ object contains an array of lists. Here an example:

```json
    "lists": [
      {
        "name": "orgtpye",
        "labels": { "de": "Organisationsart", "en": "Organization Type" },
        "nodes": [
          {
            "name": "business",
            "labels": { "en": "Commerce", "de": "Handel" },
            "comments": { "en": "no comment", "de": "kein Kommentar" },
            "nodes": [
              {
                "name": "transport",
                "labels": { "en": "Transportation", "de": "Transport" }
              },
              {
                "name": "finances",
                "labels": { "en": "Finances", "de": "Finanzen" }
              }
            ]
          },
          {
            "name": "society",
            "labels": { "en": "Society", "de": "Gesellschaft" }
          }
        ]
      }
    ]
```
the _lists_ element is optional.

### Ontology

The _ontology_ object contains the definition of the data model. The ontology has
the following elemens:

- _name_: The name of the ontology. This has to be a CNAME conformant name that can be use as prefix!
- _label_: Human readable and understandable name of the ontology
- _resources_: Array defining the resources (entities) of the data model

```json
    "ontology": {
      "name": "teimp",
      "label": "Test import ontology",
      "resources": []
    }
```

### Resources
The resource classes are the primary entities of the data model. A resource class
is a template for the representation of a real object that is represented in
the DaSCh database. A resource class defines properties (aka _data fields_). For each of
these properties a data type as well as the cardinality have to defined.

A resource consists of the following definitions:

- _name_: A name for the resource
- _label_: The string displayed of the resource is being accessed
- _super_: A resource class is always derived from an other resource. The
  most generic resource class Knora offers is _"Resource"_. The following
  parent predefined resources are provided by knora:
  - _Resource_: A generic "thing" that represents an item from the reral world
  - _StillImageRepresentation_: An object that is connected to a still image
  - _TextRepresentation_: An object that is connected to an (external) text (Not Yet Implemented)
  - _AudioRepresentation_: An object representing audio data (Not Yet Implemented)
  - _DDDRepresentation_: An object representing a 3d representation (Not Yet Implemented)
  - _DocumentRepresentation_: An object representing a opaque document (e.g. a PDF)
  - _MovingImageRepresentation_: An object representing a moving image (video, film)
  - _Annotation_: A predefined annotation object. It has the following properties
  defined:
    - _hasComment_ (1-n), _isAnnotationOf_ (1)
  - _LinkObj_: An resource class linking together several other, generic, resource classes. The class
  has the following properties: _hasComment_ (1-n), _hasLinkTo_ (1-n)
  - _Region_: Represents a simple region. The class has the following properties:
  _hasColor_ (1), _isRegionOf_ (1) _hasGeometry_ (1), _isRegionOf_ (1), _hasComment_ (0-n)
  
  However, a resource my be derived from a resource class in another ontology within the same project or
  from another resource class in the same ontology. In this case the reference
  has to have the form _prefix_:_resourceclassname_.
- _labels_: Language dependent, human readable names
- _comments_: Language dependend comments (optional)
- _properties_: Array of property definition for this resource class.

Example:

```json
     "resources": [
        {
          "name": "person",
          "super": "Resource",
          "labels": { "en": "Person", "de": "Person" },
          "comments": {
            "en": "Represents a human being",
            "de": "Repräsentiert eine Person/Menschen"
          },
          "properties": […]
        }
```

#### Properties
Properties are the definition of the data fields a resource class may or must have.
The properties object has the following fields:

- _name_: A name for the property
- _super_: A property has to be derived from at least one base property. The most generic base property
  Knora offers is _hasValue_. In addition the property may by als a subproperty of
  properties defined in external ontologies. In this case the qualified name including
  the prefix has to be given.
  The following base properties are definied by Knora:
  - _hasValue_: This is the most generic base.
  - _hasLinkTo_: This value represents a link to another resource. You have to indicate the
    the "_object_" as a prefixed IRI that identifies the resource class this link points to.
  - _hasColor_: Defines a color value (_ColorValue_)
  - _hasComment_: Defines a "standard" comment
  - _hasGeometry_: Defines a geometry value (a JSON describing a polygon, circle or rectangle), see _ColorValue_
  - _isPartOf_: A special variant of _hasLinkTo_. It says that an instance of the given resource class
    is an integral part of another resource class. E.g. a "page" is a prt of a "book".
  - _isRegionOf_: A special variant of _hasLinkTo_. It means that the given resource class
    is a "region" of another resource class. This is typically used to describe regions
    of interest in images.
  - _isAnnotationOf_: A special variant of _hasLinkTo_.  It denotes the given resource class
    as an annotation to another resource class.
  - _seqnum_: An integer that is used to define a sequence number in an ordered set of
    instances.
- _object_: The "object" defines the type of the value that the property will store.
  The following object types are allowed:
  - _TextValue_: Represents a text that may contain standoff markup
  - _ColorValue_: A string in the form "#rrggbb" (standard web color format)
  - _DateValue_: represents a date. It is a string having the format "_calendar":"start":"end"
    - _calender_ is either _GREGORIAN_ or _JULIAN_
    - _start_ has the form _yyyy_-_mm_-_dd_. If only the year is given, the precision
      is to the year, of only the year and month are given, the precision is to a month.
    - _end_ is optional if the date represents a clearely defined period or uncertainty.
    In total, a DateValue has the following form: "GREGORIAN:1925:1927-03-22"
    which means antime in between 1925 and the 22nd March 1927.
  - _DecimalValue_: a number with decimal point
  - _GeomValue_: Represents a geometrical shape as JSON.
  - _GeonameValue_: Represents a location ID in geonames.org
  - _IntValue_: Represents an integer value
  - _BooleanValue_: Represents a Boolean ("true" or "false)
  - _UriValue_: : Represents an URI
  - _IntervalValue_: Represents a time-interval
  - _ListValue_: Represents a node of a (possibly hierarchical) list
- _labels_: Language dependent, human readable names
- _gui_element_: The gui_element is – strictly seen – not part of the data. It gives the
  generic GUI a hint about how the property should be presented to the used. Each gui_element
  may have associated gui_attributes which contain further hints.
  There are the following gui_elements available:
  - _Colorpicker_: The only GUI element for _ColorValue_. Let's You pick a color. It requires the attribute "ncolors=integer"
  - _Date_: The only GUI element for _DateValue_. A date picker gui. No attributes
  - _Geometry_: Not Yet Implemented.
  - _Geonames_: The only GUI element for _GeonameValue_. Interfaces with geonames.org and allows to select a location
  - _Interval_: Not Yet Implemented.
  - _List_: A list of values. The Attribute "hlist=<list-iri>" is mandatory!
  - _Pulldown_: A GUI element for _ListValue_. Pulldown for list values. Works also for hierarchical lists. The Attribute "hlist=<list-iri>" is mandatory!
  - _Radio_: A GUI element for _ListValue_. A set of radio buttons. The Attribute "hlist=<list-iri>" is mandatory!
  - _SimpleText_: A GUI element for _TextValue_. A simple text entry box (one line only). The attributes "maxlength=integer" and "size=integer" are optional.
  - _Textarea_: A GUI element for _TextValue_. Presents a multiline textentry box. Optional attributes are "cols=integer",  "rows=integer", "width=percent" and "wrap=soft|hard".
  - _Richtext_: A GUI element for _TextValue_. Provides a richtext editor.
  - _Searchbox_: Must be used with _hasLinkTo_ properties. Allows to search and enter a resource that the given resource should link to. The Attribute "numprops=integer"
     indicates how many properties of the found resources should be indicated. It's mandatory!
  - _Slider_: A GUI element for _DecimalValue_. Provides a slider to select a decimal value. The attributes "max=decimal" and "min=decimal" are mandatory!
  - _Spinbox_: A GUI element for _IntegerValue_. A text field with and "up"- and "down"-button for increment/decrement. The attributes "max=decimal" and "min=decimal" are optional.
  - _Checkbox_: A GUI element for _BooleanValue_. 
  - _Fileupload_: not yet documented!
- _gui_attributes_: See above
- _cardinality_: The cardinality indicates how often a given property may occur. The possible values
  are:
  - "1": Exactly once (mandatory one value and only one)
  - "0-1": The value may be omitted, but can occur only once
  - "1-n": At least one value must be present. But multiple values may be present.
  - "0-n": The value may be omitted, but may also occur multiple times.

### A complete example for a full ontology

```json
{
  "prefixes": {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dcterms": "http://purl.org/dc/terms/"
  },
  "project": {
    "shortcode": "0170",
    "shortname": "teimp",
    "longname": "Test Import",
    "descriptions": {
      "en": "This is a project for testing the creation of ontologies and data",
      "de": "Dies ist ein Projekt, um die Erstellung von Ontologien und Datenimport zu testen"
    },
    "keywords": ["test", "import"],
    "lists": [
      {
        "name": "orgtpye",
        "labels": {
          "de": "Roganisationsart",
          "en": "Organization Type"
        },
        "nodes": [
          {
            "name": "business",
            "labels": {
              "en": "Commerce",
              "de": "Handel"
            },
            "comments": {
              "en": "no comment",
              "de": "kein Kommentar"
            },
            "nodes": [
              {
                "name": "transport",
                "labels": {
                  "en": "Transportation",
                  "de": "Transport"
                }
              },
              {
                "name": "finances",
                "labels": {
                  "en": "Finances",
                  "de": "Finanzen"
                }
              }
            ]
          },
          {
            "name": "society",
            "labels": {
              "en": "Society",
              "de": "Gesellschaft"
            }
          }
        ]
      }
    ],
    "ontology": {
      "name": "teimp",
      "label": "Test import ontology",
      "resources": [
        {
          "name": "person",
          "super": "Resource",
          "labels": {
            "en": "Person",
            "de": "Person"
          },
          "comments": {
            "en": "Represents a human being",
            "de": "Repräsentiert eine Person/Menschen"
          },
          "properties": [
            {
              "name": "firstname",
              "super": ["hasValue", "foaf:givenName"],
              "object": "TextValue",
              "labels": {
                "en": "Firstname",
                "de": "Vorname"
              },
              "gui_element": "SimpleText",
              "gui_attributes": ["size=24", "maxlength=32"],
              "cardinality": "1"
            },
            {
              "name": "lastname",
              "super": ["hasValue", "foaf:familyName"],
              "object": "TextValue",
              "labels": {
                "en": "Lastname",
                "de": "Nachname"
              },
              "gui_element": "SimpleText",
              "gui_attributes": ["size=24", "maxlength=64"],
              "cardinality": "1"
            },
            {
              "name": "member",
              "super": ["hasLinkTo"],
              "object": "teimp:organization",
              "labels": {
                "en": "member of",
                "de": "Mitglied von"
              },
              "gui_element": "Searchbox",
              "cardinality": "0-n"
            }
          ]
        },
        {
          "name": "organization",
          "super": "Resource",
          "labels": {
            "en": "Organization",
            "de": "Organisation"
          },
          "comments": {
            "en": "Denotes an organizational unit",
            "de": "Eine Institution oder Trägerschaft"
          },
          "properties": [
            {
              "name": "name",
              "super": ["hasValue"],
              "object": "TextValue",
              "labels": {
                "en": "Name",
                "de": "Name"
              },
              "gui_element": "SimpleText",
              "gui_attributes": ["size=64", "maxlength=64"],
              "cardinality": "1-n"
            },
            {
              "name": "orgtype",
              "super": ["hasValue"],
              "object": "ListValue",
              "labels": {
                "en": "Organizationtype",
                "de": "Organisationstyp"
              },
              "comments": {
                "en": "Type of organization",
                "de": "Art der Organisation"
              },
              "gui_element": "Pulldown",
              "gui_attributes": ["hlist=orgtype"],
              "cardinality": "1-n"
            }
          ]
        }
      ]
    }
  }
}
```

## JSON for lists

The JSON schema for uploading hierarchical lists only is simplyfied:
```json
{
  "project": {
    "shortcode": "abcd",
    "lists": []
  }
}
```
The definition of the lists is the same as in the full upload of an ontology!

### A full example for creating lists only
The following JSON definition assumes that there is a project with the shortcode _0808_.

```json
{
  "project": {
    "shortcode": "0808",
    "lists": [
      {
        "name": "test1",
        "labels": {
          "de": "TEST1"
        },
        "nodes": [
          {
            "name": "A",
            "labels": {
              "de": "_A_"
            }
          },
          {
            "name": "B",
            "labels": {
              "de": "_B_"
            },
            "nodes": [
              {
                "name": "BA",
                "labels": {
                  "de": "_BA_"
                }
              },
              {
                "name": "BB",
                "labels": {
                  "de": "_BB_"
                }
              }
            ]
          },
          {
            "name": "C",
            "labels": {
              "de": "_C_"
            }
          }
        ]
      }
    ]
  }
}
```
`
## Importing data into the triple store
In order to import data, the data has to be read and reformatted. Reading the data
depends on the dta source and has to be developed by the user. However Knora offers some
simple methods to add the resource by resource to the Knora backend. Basically You need
- to create a _Knora()_ access instance
- get the Ontology schema with a method provided by the Knora instance
- call repeatedly the method _create_resource()_.

### Creating a Knora access instance
First You have to import some libraries:
```python
from typing import List, Set, Dict, Tuple, Optional
import json
from jsonschema import validate
from knora import KnoraError, KnoraStandoffXml, Knora, Sipi

```
Then You are ready to create the Knora access isntance. You need to know the server URL of Knora and the login credentials to do so:
```python
con = Knora(args.server) #  Create the Knora access instance
con.login(args.user, args.password) #  Perform a login

```

### Getting the ontology schema
The next step is to fetch the ontology (data model) from the Knora server. You need to know
the project code (usually a _string_ in the form XXXX, where X are characters 0-9, A-F) and
the name of the ontology.  
_Note_: This works only with projects that use a single ontology. Support for projects using
several user defined ontologies has not yet been implemented.
```python
schema = con.create_schema(args.projectcode, args.ontoname)
```

### Creating resources
Now You are ready to create the resources (see [create_resource()](#https://github.com/dhlab-basel/knora-py/tree/master/knora#create_resource) for details of using this method):
```python
inst1_info = con.create_resource(schema, "object1", "obj1_inst1", {
    "textprop": "Dies ist ein Text!",
    "intprop": 7,
    "listprop": "options:opt2",
    "dateprop": "1966:CE:1967-05-21",
    "decimalprop": {'value': "3.14159", 'comment': "Die Zahl PI"},
    "geonameprop": "2661604",
    "richtextprop": {
        'value': KnoraStandoffXml("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text><p><strong>this is</strong> text</p> with standoff</text>"),
        'comment': "Text mit markup"
    },
    "intervalprop": "13.57:15.88"
})
```
THe call to _create_resource()_ returns a python Dict as follows:
```python
{
  'ark': 'http://0.0.0.0:3336/ark:/72163/1/00FE/HJD5LCVFS=qzUPK2=LgX1wZ',
  'iri': 'http://rdfh.ch/00FE/HJD5LCVFS-qzUPK2-LgX1w',
  'vark': 'http://0.0.0.0:3336/ark:/72163/1/00FE/HJD5LCVFS=qzUPK2=LgX1wZ.20190620T221223429441Z'
}
```
The `iri` can be used to reference this newly created resource in later calls.

### Creating resources with attached images

In order to create a StillImageRepresentation, that is a resource that is connected to an image,
YOu first have to upload the image usiing Sipi. For this YOu create first an instance of Sipi:
```python
sipi = Sipi(args.sipi, con.get_token())
```
The access token is taken from the Knora access instance using the method _get_tokeen()_. The Sipi
instance is then able to upload images:
```python
res = sipi.upload_image('example.tif')
```
The parameter to _upload_image()_ is the path to the image file. Currently J2K, TIF, PNG and JPG-imges are supported.

Now You are read to create the resource:
```python
fileref = res['uploadedFiles'][0]['internalFilename']
inst2_info = con.create_resource(
  schema,
  "object2",
  "obj2_inst1", {
    "titleprop": "Stained glass",
    "linkprop": inst1_info['iri']
  },
  fileref)
```
Please note that above example creates a resource that has a link to another resource. It
uses a link property defined in this example ontology as _linkprop_.

### Complete example

The complete example looks as follows:
```python
import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, KnoraStandoffXml, Knora, Sipi


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="http://0.0.0.0:3333", help="URL of the Knora server")
parser.add_argument("-S", "--sipi", type=str, default="http://0.0.0.0:1024", help="URL of SIPI server")
parser.add_argument("-u", "--user", default="root@example.com", help="Username for Knora")
parser.add_argument("-p", "--password", default="test", help="The password for login")
parser.add_argument("-P", "--projectcode", default="00FE", help="Project short code")
parser.add_argument("-O", "--ontoname", default="kpt", help="Shortname of ontology")

args = parser.parse_args()


con = Knora(args.server)
con.login(args.user, args.password)

schema = con.create_schema(args.projectcode, args.ontoname)

inst1_info = con.create_resource(
  schema,
  "object1",
  "obj1_inst1", {
  "textprop": "Dies ist ein Text!",
  "intprop": 7,
  "listprop": "options:opt2",
  "dateprop": "1966:CE:1967-05-21",
  "decimalprop": {'value': "3.14159", 'comment': "Die Zahl PI"},
  "geonameprop": "2661604",
  "richtextprop": {
    'value': KnoraStandoffXml("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<text><p><strong>this is</strong> text</p> with standoff</text>"),
    'comment': "Text mit markup"
  },
  "intervalprop": "13.57:15.88"
})
pprint(inst1_info)

#first upload image to SIPI
sipi = Sipi(args.sipi, con.get_token())
res = sipi.upload_image('example.tif')
pprint(res)

fileref = res['uploadedFiles'][0]['internalFilename']
inst2_info = con.create_resource(
  schema,
  "object2",
  "obj2_inst1", {
    "titleprop": "Stained glass",
    "linkprop": inst1_info['iri']
  },
  fileref)
pprint(inst2_info)
```

## Resetting the triplestore with `knora-reset-triplestore`
This script reads a JSON file containing the data model (ontology) definition,
connects to the Knora server and creates the data model.

### Usage:

```bash
$ knora-reset-triplestore
```
It supports the following options:

- _"-s server" | "--server server"_: The URl of the Knora server [default: localhost:3333]
- _"-u username" | "--user username"_: Username to log into Knora [default: root@example.com]
- _"-p password" | "--password password"_: The password for login to the Knora server [default: test]

For resetting of the triplestore through Knora-API to work, it is necessary to start the Knora-API server
with a configuration parameter allowing this operation (e.g., `KNORA_WEBAPI_ALLOW_RELOAD_OVER_HTTP`
environment variable or the corresponding setting in `application.conf`).

## Bulk data import
In order to make a bulk data import, a properly formatted XML file has to be created. The python module "knora" contains
classes and methods to facilitate the creation of such a XML file.

## Requirements

To install the requirements:

```bash
$ pip3 install -r requirements.txt
```


To generate a "requirements" file (usually requirements.txt), that you commit with your project, do:

```bash
$ pip3 freeze > requirements.txt
```

## Publishing

Generate distribution package. Make sure you have the latest versions of `setuptools` and `wheel` installed:

```bash
$ python3 -m pip install --upgrade pip setuptools wheel
$ python3 setup.py sdist bdist_wheel
```

You can install the package locally from the dist:

```bash
$ python3 -m pip ./dist/some_name.whl
```

Upload package with `twine`,

first create `~/.pypirc`:

```bash
[distutils] 
index-servers=pypi
[pypi] 
repository = https://upload.pypi.org/legacy/ 
username =your_username_on_pypi
```

then upload:

```bash
$ python3 -m pip install --upgrade tqdm twine
$ python3 -m twine upload dist/*
```

For local development:

```bash
$ python3 setup.py develop
```

## Testing

```bash
$ pip3 install pytest
$ pip3 install --editable .
$ pytest
```

## Requirements

To install the requirements:

```bash
$ pip3 install -r requirements.txt
```


To generate a "requirements" file (usually requirements.txt), that you commit with your project, do:

```bash
$ pip3 freeze > requirements.txt
```

