import unittest

import build


class MarkdownTests(unittest.TestCase):
    def test_duplicate_heading_ids_are_unique_and_toc_tracks_them(self):
        _, html, toc = build.convert("# Guide\n\n## Repeat\n\n## Repeat")
        self.assertIn('id="repeat-2"', html)
        self.assertEqual([item[1] for item in toc], ["repeat", "repeat-2"])

    def test_code_stays_literal_and_links_convert(self):
        _, html, _ = build.convert('# Guide\n\n[Read](getting-started.md#requirements)\n\n```csharp\nif (a < b) { Call("[x](bad.md)"); }\n```')
        self.assertIn('href="getting-started.html#requirements"', html)
        self.assertIn('a &lt; b', html)
        self.assertIn('[x](bad.md)', html)
        self.assertNotIn('href="bad.html"', html)

    def test_image_has_caption_alt_dimensions_and_full_size_link(self):
        _, html, _ = build.convert('# Guide\n\n![Product](assets/media/product-icon.png "The product icon")')
        self.assertIn('alt="Product"', html)
        self.assertIn('width="160"', html)
        self.assertIn('<figcaption>The product icon', html)

    def test_callout_and_nested_list_structure(self):
        _, html, _ = build.convert('# Guide\n\n::: warning Target\nCheck identity.\n:::\n\n- Parent\n  - Child')
        self.assertIn('class="callout warning"', html)
        self.assertIn('<li>Parent<ul>', html.replace('\n', ''))
        self.assertIn('<li>Child</li>', html)

    def test_rejects_unfinished_content(self):
        for text in ('# Guide\n\n```\nunfinished', '# Guide\n\n:::cards\n- A | B | C', '# Guide\n\n::: note Test\nText', '# Guide\n\n[SCREENSHOT: later]'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                build.convert(text)

    def test_rejects_second_h1_and_unsafe_url(self):
        with self.assertRaises(ValueError):
            build.convert('# One\n\n# Two')
        with self.assertRaises(ValueError):
            build.inline('[bad](javascript:alert)')

    def test_table_is_keyboard_scrollable_with_column_headers(self):
        _, html, _ = build.convert('# Guide\n\n| Name | Type |\n| --- | --- |\n| Target | GameObject |')
        self.assertIn('tabindex="0"', html)
        self.assertIn('<th scope="col">Name</th>', html)

    def test_flow_and_cards_link_to_generated_pages(self):
        _, html, _ = build.convert('# Guide\n\n:::flow\n- 01 | Request | Send it.\n:::\n\n:::cards\n- X | Start | Read this. | getting-started.md\n:::')
        self.assertIn('aria-label="Integration flow"', html)
        self.assertIn('href="getting-started.html"', html)


if __name__ == '__main__':
    unittest.main()
