from collections import OrderedDict
import uuid

from django.core.exceptions import ValidationError
from django.db import models

from pkg_resources import SetuptoolsVersion


class Package(models.Model):
    name = models.CharField(blank=False, max_length=200)
    name_lower = models.CharField(blank=True, unique=True, max_length=200)
    changelog_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name_lower', )

    def prep_list(self, t):
        # XXX sort using pkg_resources.parse_version for comparison
        return [
            pv.version
            for pv in self.packageversion_set.filter(type=t)
        ]

    def as_dict(self):
        """
        :return: dictionary of data for this package, other than the name
        """
        return OrderedDict((
            ('changelog_url', self.changelog_url),
            ('bug_fix_releases', self.prep_list(PackageVersion.BUG_FIX)),
            ('compatibility_releases', self.prep_list(PackageVersion.COMPAT)),
            ('feature_releases', self.prep_list(PackageVersion.FEATURE)),
            ('ignored_releases', self.prep_list(PackageVersion.IGNORED)),
            ('security_releases', self.prep_list(PackageVersion.SECURITY)),
            ('lts_releases', self.prep_list(PackageVersion.LTS)),
        ))

    @classmethod
    def import_from_dict(cls, name, d):
        package = Package(
            name=name,
            changelog_url=d['changelog_url']
        )
        package.full_clean()
        package.save()

        mappings = (
            ('bug_fix_releases', PackageVersion.BUG_FIX),
            ('compatibility_releases', PackageVersion.COMPAT),
            ('feature_releases', PackageVersion.FEATURE),
            ('ignored_releases', PackageVersion.IGNORED),
            ('security_releases', PackageVersion.SECURITY),
            ('lts_releases', PackageVersion.LTS),
        )
        for attr, t in mappings:
            for version in d[attr]:
                pv = PackageVersion(
                    package=package,
                    type=t,
                    version=version
                )
                pv.full_clean()
                pv.save()

    @classmethod
    def export(cls):
        data = OrderedDict()
        for p in cls.objects.all():
            data[p.name] = p.as_dict()
        return data


def validate_version(value):
    # LTS form of version string?  (e.g., '1.11.')
    if value[-1] == '.':
        value = value + '0'  # Add 0 to get, e.g., '1.11.0'
    try:
        SetuptoolsVersion(value)
    # XXX can't manage to import InvalidVersion, which inherits from ValueError
    except ValueError as e:
        raise ValidationError(str(e))


class PackageVersion(models.Model):
    SECURITY = 1
    BUG_FIX = 3
    COMPAT = 4
    FEATURE = 5
    IGNORED = 6
    LTS = 7

    TYPE_CHOICES = (
        (SECURITY, 'contains security fixes'),
        (BUG_FIX, 'contains non-security bug fixes'),
        (COMPAT, 'contains fixes for compatibility with some other software'),
        (FEATURE, 'contains only new features'),
        (IGNORED, 'version should be ignored'),
        (LTS, 'LTS release'),
    )

    package = models.ForeignKey(Package)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    version = models.CharField(max_length=20, validators=[validate_version])

    class Meta:
        ordering = ('type', )
        unique_together = ('package', 'version')


class PackageDBAccess(models.Model):
    """
    Bearer of this token can export the package database
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    notes = models.TextField('Description of client')

    def __str__(self):
        return self.notes

    class Meta:
        verbose_name_plural = 'package DB accesses'
