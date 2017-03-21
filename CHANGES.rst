1.3.2 (2017-03-21)
------------------

* Switch to flask-classful.
* Fix antispam code generation, closes #3.
* Move antispam code logic to a custom Field.
* Fix rendering of locked galleries, closes #2.

1.3.1 (2017-03-13)
------------------

* Add forgotten labels to translations.
* Fix thumbroll links.

1.3.0 (2017-03-13)
------------------

* Read EXIF data from pictures.
* Remove hard-coded links to endpoint serving files using a named endpoint.
* Move navigation build to base.html and fix URL to site root.
* Add missing quality argument when triggering resize task through browsing.
* Split view in gallery listing view and gallery detail view to allow easier
  templating or URLS.
* Use Flask-WTF to deal with comment form.
* Generate comment HTML content from template.
* Extend random number generation to 0-9999 instead of 1000-9999.

1.2.0 (2016-07-10)
------------------

* Move application creation to a dedicated module.
* Read configuration passed by Paste.
* Fix various typos.
* Add sample PasteDeploy configuration.
* Fix setuptools packaging.

1.1.0 (2016-02-07)
------------------

* Fix locked galleries credentials validation.
* Fix comment submission anti-spam validation.
* Fix bypassing of locked galleries via direct links.
* Fix typo in MQ picture check.
* Send pictures using Flask and kill all hardcoded domain name
  references.
* Add RQ based thumbnail generator.
* Automatically generate thumbnails of a gallery when HQ folder is
  found but not thumbs.
* Fix client-based locale selection.
* Add a PasteDeploy application factory entry-point.
* Fix BasicAuth on various browsers.
* Allow using any filename for pictures rather than sequantial numbers.
* Make all templates derive from base.html.

1.0.0 (2015-03-16)
------------------

* Initial release.

