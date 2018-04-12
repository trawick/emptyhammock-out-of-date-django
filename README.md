# emptyhammock-out-of-date-django

## Overview

This is a companion package to [emptyhammock-out-of-date](https://github.com/trawick/emptyhammock-out-of-date)
which supports maintenance of a package release database in the Django admin,
and delivery to clients which will pass it to emptyhammock-out-of-date.

The database can be exported to YAML from admin.  Additionally, a "package DB
access" UUID can be generated from admin, and clients specifying that UUID in
the URL can access a YAML export of the database on demand.

You should understand emptyhammock-out-of-date and the meaning of its
package release database before considering this package.

![Sample view in Django admin](/docs/Django-admin-image.png?raw=true "Sample view")
