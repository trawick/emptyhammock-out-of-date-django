# Changes and migration requirements

## Version 0.0.9

* Support Django 4.2.  Django versions < 4.2 are no longer supported.

## Version 0.0.8

* Support Django 3.2 by setting default_auto_field .

## Version 0.0.7

* Fix import error with Django 2.2.

## Version 0.0.6

* Add support for Django 2.2.

## Version 0.0.5

* Use `packaging` package instead of `setuptools` for validating package
  versions, to resolve a load failure with `setuptools` version 39.0.0 or
  later.  **`packaging` is a new requirement of this package.**

# Version 0.0.4

* Add admin interface for exporting the package db.
* Improve field names and make other minor improvements in admin.

## Version 0.0.3

* Trivial admin improvements

## Version 0.0.2

* Packaging fixes

## Version 0.0.1

* Initial version
