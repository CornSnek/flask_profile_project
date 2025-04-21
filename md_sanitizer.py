from html_sanitizer import Sanitizer
from html_sanitizer.sanitizer import sanitize_href, tag_replacer, target_blank_noopener
sanitizer = Sanitizer({
    "tags": {
        "a", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "p", "ul", "ol",
        "li", "br", "sub", "sup", "hr",
    },
    "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
    "empty": {"hr", "a", "br"},
    "separate": {"a", "p", "li"},
    "whitespace": {"br"},
    "sanitize_href": sanitize_href,
    "keep_typographic_whitespace": True,
    "add_nofollow": True,
    "autolink": False,
    "element_postprocessors": [
        tag_replacer("form", "p"),
        target_blank_noopener,
    ],
    "is_mergeable": lambda e1, e2: True,
})