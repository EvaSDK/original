1.1.0 (unreleased)
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

