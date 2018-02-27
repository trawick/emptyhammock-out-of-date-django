from django.core.exceptions import ValidationError
from django.test import TestCase

from e_ood_django.models import Package, PackageVersion


class TestPackage(TestCase):

    def test_export_simplest(self):
        foo = Package.objects.create(
            name='Foo',
            changelog_url='https://emptyhammock.com/CHANGES.md',
        )
        self.assertEqual('foo', foo.name_lower)
        foo.packageversion_set.create(
            type=PackageVersion.LTS, version='1.11.'
        )
        foo.packageversion_set.create(
            type=PackageVersion.COMPAT, version='2.0.0',
        )
        foo.packageversion_set.create(
            type=PackageVersion.COMPAT, version='3.0.0',
        )
        foo.packageversion_set.create(
            type=PackageVersion.COMPAT, version='4.0.0',
        )
        bar = Package.objects.create(
            name='Bar',
        )
        self.assertEqual('bar', bar.name_lower)
        bar.packageversion_set.create(
            type=PackageVersion.FEATURE, version='1.5.0',
        )
        bar.packageversion_set.create(
            type=PackageVersion.FEATURE, version='1.6.0',
        )
        bar.packageversion_set.create(
            type=PackageVersion.FEATURE, version='1.7.0',
        )
        bar.packageversion_set.create(
            type=PackageVersion.SECURITY, version='1.5.1',
        )
        bar.packageversion_set.create(
            type=PackageVersion.SECURITY, version='1.6.1',
        )
        bar.packageversion_set.create(
            type=PackageVersion.SECURITY, version='1.7.1',
        )
        exported = Package.export()
        expected = {
            'Foo': dict(
                bug_fix_releases=[],
                changelog_url='https://emptyhammock.com/CHANGES.md',
                compatibility_releases=['2.0.0', '3.0.0', '4.0.0'],
                feature_releases=[],
                ignored_releases=[],
                lts_releases=['1.11.'],
                security_releases=[]
            ),
            'Bar': dict(
                bug_fix_releases=[],
                changelog_url='',
                compatibility_releases=[],
                feature_releases=['1.5.0', '1.6.0', '1.7.0'],
                ignored_releases=[],
                lts_releases=[],
                security_releases=['1.5.1', '1.6.1', '1.7.1']
            )
        }
        self.assertEqual(
            expected,
            exported
        )

    def test_bad_version(self):
        foo = Package.objects.create(
            name='Foo',
            changelog_url='https://emptyhammock.com/CHANGES.md',
        )
        x = PackageVersion(
            package=foo,
            type=PackageVersion.SECURITY,
            version='abc',
        )
        with self.assertRaises(ValidationError):
            x.full_clean()

    def test_good_versions(self):
        foo = Package.objects.create(
            name='Foo',
            changelog_url='https://emptyhammock.com/CHANGES.md',
        )
        x = PackageVersion(
            package=foo,
            type=PackageVersion.SECURITY,
            version='1.11.1',
        )
        x.full_clean()
        x = PackageVersion(
            package=foo,
            type=PackageVersion.LTS,
            version='1.11.',
        )
        x.full_clean()

    def test_import_export(self):
        test_data = {
            'Foo': dict(
                bug_fix_releases=['4.0.2'],
                changelog_url='https://emptyhammock.com/CHANGES.md',
                compatibility_releases=['2.0.0', '3.0.0', '4.0.0'],
                feature_releases=['2.2.0'],
                ignored_releases=['2.2.8'],
                lts_releases=['1.11.'],
                security_releases=['4.0.1']
            ),
            'Bar': dict(
                bug_fix_releases=[],
                changelog_url='',
                compatibility_releases=[],
                feature_releases=['1.5.0', '1.6.0', '1.7.0'],
                ignored_releases=[],
                lts_releases=[],
                security_releases=['1.5.1', '1.6.1', '1.7.1']
            )
        }
        for k, v in test_data.items():
            Package.import_from_dict(k, v)
        exported = Package.export()
        self.assertEqual(test_data, exported)
