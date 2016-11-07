#!/usr/bin/env python
import unittest

from deploy import generate_versioned_tags, split_image_tag


class TestSplitImageTag(unittest.TestCase):
    def test_image_tag(self):
        image, tag = split_image_tag('foo:bar')
        self.assertEqual(image, 'foo')
        self.assertEqual(tag, 'bar')

    def test_image(self):
        image, tag = split_image_tag('foo')
        self.assertEqual(image, 'foo')
        self.assertIsNone(tag)


class TestGenerateVersionTag(unittest.TestCase):
    def test_name_tag(self):
        versioned_tags = generate_versioned_tags('foo', '5.4.1')
        self.assertEqual(versioned_tags, ['5.4.1-foo', '5.4-foo', '5-foo'])

    def test_version_and_name_tag(self):
        versioned_tags = generate_versioned_tags('5.4-foo', '5.4.1')
        self.assertEqual(versioned_tags, ['5.4.1-foo', '5.4-foo', '5-foo'])

    def test_other_version_tag(self):
        versioned_tags = generate_versioned_tags('2.7-foo', '5.4.1')
        self.assertEqual(versioned_tags,
                         ['5.4.1-2.7-foo', '5.4-2.7-foo', '5-2.7-foo'])

    def test_version_tag(self):
        versioned_tags = generate_versioned_tags('5.4', '5.4.1')
        self.assertEqual(versioned_tags, ['5.4.1', '5.4', '5'])

    def test_nont_tag(self):
        versioned_tags = generate_versioned_tags(None, '5.4.1')
        self.assertEqual(versioned_tags, ['5.4.1', '5.4', '5'])

if __name__ == '__main__':
    unittest.main()
