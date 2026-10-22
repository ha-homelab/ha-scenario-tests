# Maintaining guide translations

The installation, scope, scenario contract, troubleshooting and validation guides,
and the checked-in wiki home page are available in the 24 languages listed in
[`languages.json`](languages.json). The catalog follows the
[ha-homelab language reference](https://github.com/ha-homelab/.github/blob/main/languages.json).
Each page links to every language of the same guide. These are full translations;
the historical validation dates, unsuccessful macOS runtime result and hardware
limitations remain part of every translation. Documentation languages do not
change the CLI's supported languages.

English is the source for these families. Translations use `name.<language>.md`
beside `name.md`; Chinese variants are `zh-Hans` and `zh-Hant`. Arabic, Persian
and Hebrew prose uses explicit right-to-left containers, with left-to-right code
blocks and language navigation. Keep a blank line between HTML containers and
Markdown so GitHub renders the Markdown content correctly.

When changing a source guide:

1. Update the complete text in all 23 translations, including Russian. Preserve
   requirements, examples, error conditions, historical evidence and limitations.
2. Preserve fenced code, inline identifiers and external link destinations exactly.
   Links between translated families use the same language, including canonical
   GitHub main-branch links to these guides. Keep fragment links and pinned
   external references unchanged. Preserve translated headings, steps and lists.
3. Keep the `language-navigation:start` / `language-navigation:end` block on every
   page. It must link to all entries in the catalog, including the current page.
4. Update the source digest in [`translations.json`](translations.json) only
   after reviewing the translations. It is SHA-256 of the UTF-8 English content,
   with the navigation block removed and leading/trailing whitespace stripped.
5. Stage new files, then run `python3 tools/check_docs.py` and
   `ruff check --select E4,E7,E9,F tools/check_docs.py`. The existing Check workflow
   runs the documentation check; no separate translation service is involved.
6. Preview representative pages on GitHub, including a right-to-left guide with
   code. Request a content review: structural checks cannot prove translation
   accuracy.

The checker verifies the catalog, source digests, presence of all pages,
navigation targets and direction attributes, fenced code, inline literals,
heading/list structure, Markdown destinations and existing local-link/SVG checks.
The digests stop a prose-only English edit from silently leaving these
translations stale. They are a review guard, not a substitute for human review.

Publishing checked-in pages to the separate GitHub wiki remains a separate
operation. This change does not alter application behavior, release criteria,
runtime versions or the historical test results.
