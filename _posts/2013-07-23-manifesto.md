---
layout: page
title: "Manifesto"
category: ref
date: 2013-07-23 16:37:59
---

### Complex Data Models
            
Handling _complex_ data models sounds more attractive, but even simple ones can benefit from a really good data access layer API.

#### Perceivably _flat_ data access layer

It is simpler to choose/search from a list of items than to attempt to traverse a relational data model or document store. Many times you simply _don't know_ what you're looking for or when you do, you don't (and shouldn't) know where to look.

#### Descriptive metadata (and domain specificity)

Merely having a data model and its constraints is not enough. The first barrier for users is figuring out what about the data they can search for. Humanize the data model by adding some descriptive love.

#### Free-text data model search

An intuitive and powerful search depends on the first two points mentioned above. The (highly descriptive) metadata as well as the structural metadata can be indexed and searched against directly. A match in this case would be particular data point whether it is for query or display purposes.

#### Expand the search by including the data itself

To make the search more robust, discreate data can be indexed and associated with each data point as well. As an example, if I type `male`, the available query or view options may result in `gender`. This enables users to find what they are looking for by directly searching for the a known data value. One caveat to this is regarding permissions. If certain end are not allowed to view certain data, a match occuring from typing `male` would potentially mean there are `male` data values.

#### Humans aren't constrained, databases schemas are (and for good reason)

Databases have _data types_ to allow for fast and effective search on data. For example, you cannot query the string `hello world` using a numerical operator (as least in a way that makes sense). For this reason, data are split up into multiple fields suting the needs of the data. For example when you view a cooking recipe, you would expect to read an ingredient such as _2 teaspoons of salt_. What would happen if you only knew the ingredient name i.e. _salt_? You wouldn't know _how much_ of the ingredient you need. Likewise if you only saw _teaspoons_ without _2_, you would not know the quantity of _salt_ to add.

The power of the database comes from storing and indexing discrete values which enables fast search and sorting capabilities. Humans however need to be able to view these discrete values in way that means something to them.

### Large Data Sets

Large data sets should _only_ benefit users in the sense that they have more data to explore.  Similar to the comment on complexity.. small data sets will work just fine here as well.

#### Usability must have an O(1) relationship to data size

The scale of the data must not tax its usability. Interfaces must be able to scale with the data transparently and not burden the user with too many options at once.

#### _Get a sense_ of the data by showing aggregate statistics

Most data should be looked at an aggregate level. If you choose the view _gender_ data, the appropriate view is a series aggregate counts for _male_, _female_ and _unknown_. This immediately gives the user a sense of the data. For example, if the are interesting in the _male_ population, but the data set only has a few, they can make the decision to continue or not.

These statistics can be thought of as another set of metadata. This time it's computed from the data itself.
            
#### Stats are good, visuals are better
            
This goes hand-in-hand with displaying aggregate statistics. Use visuals such as histograms to display the distribution of data. This is particularly important for continuous data where simply listing min, max, mean, mode, standard deviation and variance is not good enough. Again, at this stage the goal is for a user to _get a sense_ of the data before having to query or view it.

### Domain Specificity

It's simple. Humans are more comfortable with the language and concepts they know and understand.

#### Group data to produce information

In the example above, a recipe _ingredient_ was used as an example to convey the importance of context and being presented with _all_ the necessary information. In most cases, data stored in a structured and constrained database system can be thought of _raw_ data and does not lend itself well for presentation. This data needs to be grouped together (like the ingredient) and formatted appropriately for display. If the ingredient `name`, `quantity` and `unit` were displayed out of order, that would cause confusion.
