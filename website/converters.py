import bleach
import markdown
from bleach_whitelist import markdown_attrs, markdown_tags
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension


# https://python-markdown.github.io/extensions/
MARKDOWN_EXTENSIONS = (CodeHiliteExtension(), FencedCodeExtension(), TocExtension())


def markdownify(html: str) -> str:
    """
    Given a string of HTML, returns the string converted
    to markdown and run through a HTML sanitizer.
    Syntax highlighting and fenced code blocks are supported.
    Additionally, a table of contents can be inserted by using `[TOC]`.
    """

    return bleach.clean(
        markdown.markdown(html, extensions=MARKDOWN_EXTENSIONS),
        markdown_tags,
        markdown_attrs,
    )
