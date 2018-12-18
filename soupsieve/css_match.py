"""CSS matcher."""
from . import util
import re
from .util import deprecated
from .import css_types as ct

# Empty tag pattern (whitespace okay)
RE_NOT_EMPTY = re.compile('[^ \t\r\n\f]')

# Relationships
REL_PARENT = ' '
REL_CLOSE_PARENT = '>'
REL_SIBLING = '~'
REL_CLOSE_SIBLING = '+'

# Relationships for :has() (forward looking)
REL_HAS_PARENT = ': '
REL_HAS_CLOSE_PARENT = ':>'
REL_HAS_SIBLING = ':~'
REL_HAS_CLOSE_SIBLING = ':+'

NS_XHTML = 'http://www.w3.org/1999/xhtml'


class CSSMatch:
    """Perform CSS matching."""

    def __init__(self, selectors, namespaces, flags):
        """Initialize."""

        self.meta_lang = None
        self.default_forms = []
        self.indeterminate_forms = []
        self.selectors = selectors
        self.namespaces = namespaces
        self.flags = flags

    def get_namespace(self, el):
        """Get the namespace for the element."""

        namespace = ''
        ns = el.namespace
        if ns:
            namespace = ns
        return namespace

    def supports_namespaces(self):
        """Check if namespaces are supported in the HTML type."""

        return self.is_xml or self.html_namespace

    def get_attribute(self, el, attr, prefix):
        """Get attribute from element if it exists."""

        value = None
        if self.supports_namespaces():
            value = None
            # If we have not defined namespaces, we can't very well find them, so don't bother trying.
            if prefix and prefix not in self.namespaces and prefix != '*':
                return None

            for k, v in el.attrs.items():
                parts = k.split(':', 1)
                if len(parts) > 1:
                    if not parts[0]:
                        a = k
                        p = ''
                    else:
                        p = parts[0]
                        a = parts[1]
                else:
                    p = ''
                    a = k
                # Can't match a prefix attribute as we haven't specified one to match
                # Try to match it normally as a whole `p:a` as selector may be trying `p\:a`.
                if not prefix and p:
                    if (self.is_xml and attr == k) or (not self.is_xml and util.lower(attr) == util.lower(k)):
                        value = v
                        break
                    # Coverage is not finding this even though it is executed.
                    # Adding a print statement before this (and erasing coverage) causes coverage to find the line.
                    # Ignore the false positive message.
                    continue  # pragma: no cover
                # We can't match our desired prefix attribute as the attribute doesn't have a prefix
                if prefix and not p and prefix != '*':
                    continue
                if self.is_xml:
                    # The prefix doesn't match
                    if prefix and p and prefix != '*' and prefix != p:
                        continue
                    # The attribute doesn't match.
                    if attr != a:
                        continue
                else:
                    # The prefix doesn't match
                    if prefix and p and prefix != '*' and util.lower(prefix) != util.lower(p):
                        continue
                    # The attribute doesn't match.
                    if util.lower(attr) != util.lower(a):
                        continue
                value = v
                break
        else:
            for k, v in el.attrs.items():
                if util.lower(attr) != util.lower(k):
                    continue
                value = v
                break
        return value

    def get_classes(self, el):
        """Get classes."""

        classes = el.attrs.get('class', [])
        if isinstance(classes, str):
            classes = [c for c in classes.strip().split(' ') if c]
        return classes

    def match_namespace(self, el, tag):
        """Match the namespace of the element."""

        match = True
        namespace = self.get_namespace(el)
        default_namespace = self.namespaces.get('')
        # We must match the default namespace if one is not provided
        if tag.prefix is None and (default_namespace is not None and namespace != default_namespace):
            match = False
        # If we specified `|tag`, we must not have a namespace.
        elif (tag.prefix is not None and tag.prefix == '' and namespace):
            match = False
        # Verify prefix matches
        elif (
            tag.prefix and
            tag.prefix != '*' and namespace != self.namespaces.get(tag.prefix, '')
        ):
            match = False
        return match

    def match_attributes(self, el, attributes):
        """Match attributes."""

        match = True
        if attributes:
            for a in attributes:
                value = self.get_attribute(el, a.attribute, a.prefix)
                pattern = a.xml_type_pattern if not self.html_namespace and a.xml_type_pattern else a.pattern
                if isinstance(value, list):
                    value = ' '.join(value)
                if value is None:
                    match = False
                    break
                elif pattern is None:
                    continue
                elif pattern.match(value) is None:
                    match = False
                    break
        return match

    def match_tagname(self, el, tag):
        """Match tag name."""

        return not (
            tag.name and
            tag.name not in ((util.lower(el.name) if not self.is_xml else el.name), '*')
        )

    def match_tag(self, el, tag):
        """Match the tag."""

        has_ns = self.supports_namespaces()
        match = True
        if tag is not None:
            # Verify namespace
            if has_ns and not self.match_namespace(el, tag):
                match = False
            if not self.match_tagname(el, tag):
                match = False
        return match

    def match_past_relations(self, el, relation):
        """Match past relationship."""

        found = False
        if relation[0].rel_type == REL_PARENT:
            parent = el.parent
            while not found and parent:
                found = self.match_selectors(parent, relation)
                parent = parent.parent
        elif relation[0].rel_type == REL_CLOSE_PARENT:
            parent = el.parent
            if parent:
                found = self.match_selectors(parent, relation)
        elif relation[0].rel_type == REL_SIBLING:
            sibling = el.previous_sibling
            while not found and sibling:
                if not util.is_tag(sibling):
                    sibling = sibling.previous_sibling
                    continue
                found = self.match_selectors(sibling, relation)
                sibling = sibling.previous_sibling
        elif relation[0].rel_type == REL_CLOSE_SIBLING:
            sibling = el.previous_sibling
            while sibling and not util.is_tag(sibling):
                sibling = sibling.previous_sibling
            if sibling and util.is_tag(sibling):
                found = self.match_selectors(sibling, relation)
        return found

    def match_future_child(self, parent, relation, recursive=False):
        """Match future child."""

        match = False
        for child in (parent.descendants if recursive else parent.children):
            if not util.is_tag(child):
                continue
            match = self.match_selectors(child, relation)
            if match:
                break
        return match

    def match_future_relations(self, el, relation):
        """Match future relationship."""

        found = False
        if relation[0].rel_type == REL_HAS_PARENT:
            found = self.match_future_child(el, relation, True)
        elif relation[0].rel_type == REL_HAS_CLOSE_PARENT:
            found = self.match_future_child(el, relation)
        elif relation[0].rel_type == REL_HAS_SIBLING:
            sibling = el.next_sibling
            while not found and sibling:
                if not util.is_tag(sibling):
                    sibling = sibling.next_sibling
                    continue
                found = self.match_selectors(sibling, relation)
                sibling = sibling.next_sibling
        elif relation[0].rel_type == REL_HAS_CLOSE_SIBLING:
            sibling = el.next_sibling
            while sibling and not util.is_tag(sibling):
                sibling = sibling.next_sibling
            if sibling and util.is_tag(sibling):
                found = self.match_selectors(sibling, relation)
        return found

    def match_relations(self, el, relation):
        """Match relationship to other elements."""

        found = False

        if relation[0].rel_type.startswith(':'):
            found = self.match_future_relations(el, relation)
        else:
            found = self.match_past_relations(el, relation)

        return found

    def match_id(self, el, ids):
        """Match element's ID."""

        found = True
        for i in ids:
            if i != el.attrs.get('id', ''):
                found = False
                break
        return found

    def match_classes(self, el, classes):
        """Match element's classes."""

        current_classes = self.get_classes(el)
        found = True
        for c in classes:
            if c not in current_classes:
                found = False
                break
        return found

    def match_root(self, el):
        """Match element as root."""

        parent = el.parent
        return parent and not parent.parent

    def match_nth_tag_type(self, el, child):
        """Match tag type for `nth` matches."""

        return(
            (child.name == (util.lower(el.name) if not self.is_xml else el.name)) and
            (not self.supports_namespaces() or self.get_namespace(child) == self.get_namespace(el))
        )

    def match_nth(self, el, nth):
        """Match `nth` elements."""

        matched = True

        for n in nth:
            matched = False
            if n.selectors and not self.match_selectors(el, n.selectors):
                break
            parent = el.parent
            last = n.last
            last_index = len(parent.contents) - 1
            relative_index = 0
            a = n.a
            b = n.b
            var = n.n
            count = 0
            count_incr = 1
            factor = -1 if last else 1
            index = len(parent.contents) - 1 if last else 0
            idx = last_idx = a * count + b if var else a

            # We can only adjust bounds within a variable index
            if var:
                # Abort if our nth index is out of bounds and only getting further out of bounds as we increment.
                # Otherwise, increment to try to get in bounds.
                adjust = None
                while idx < 1 or idx > last_index:
                    if idx < 0:
                        diff_low = 0 - idx
                        if adjust is not None and adjust == 1:
                            break
                        adjust = -1
                        count += count_incr
                        idx = last_idx = a * count + b if var else a
                        diff = 0 - idx
                        if diff >= diff_low:
                            break
                    else:
                        diff_high = idx - last_index
                        if adjust is not None and adjust == -1:
                            break
                        adjust = 1
                        count += count_incr
                        idx = last_idx = a * count + b if var else a
                        diff = idx - last_index
                        if diff >= diff_high:
                            break
                        diff_high = diff

                # If a < 0, our count is working backwards, so floor the index by increasing the count.
                # Find the count that yields the lowest, in bound value and use that.
                # Lastly reverse count increment so that we'll increase our index.
                lowest = count
                if a < 0:
                    while idx >= 1:
                        lowest = count
                        count += count_incr
                        idx = last_idx = a * count + b if var else a
                    count_incr = -1
                count = lowest
                idx = last_idx = a * count + b if var else a

            # Evaluate elements while our calculated nth index is still in range
            while 1 <= idx <= last_index:
                child = None
                # Evaluate while our child index is still range.
                while 0 <= index <= last_index:
                    child = parent.contents[index]
                    index += factor
                    if not util.is_tag(child):
                        continue
                    # Handle `of S` in `nth-child`
                    if n.selectors and not self.match_selectors(child, n.selectors):
                        continue
                    # Handle `of-type`
                    if n.of_type and not self.match_nth_tag_type(el, child):
                        continue
                    relative_index += 1
                    if relative_index == idx:
                        if child is el:
                            matched = True
                        else:
                            break
                    if child is el:
                        break
                if child is el:
                    break
                last_idx = idx
                count += count_incr
                if count < 0:
                    # Count is counting down and has now ventured into invalid territory.
                    break
                idx = a * count + b if var else a
                if last_idx == idx:
                    break
            if not matched:
                break
        return matched

    def match_empty(self, el):
        """Check if element is empty (if requested)."""

        is_empty = True
        for child in el.children:
            if util.is_tag(child):
                is_empty = False
                break
            elif (
                (util.is_navigable_string(child) and not util.is_special_string(child)) and
                RE_NOT_EMPTY.search(child)
            ):
                is_empty = False
                break
        return is_empty

    def match_subselectors(self, el, selectors):
        """Match selectors."""

        match = True
        for sel in selectors:
            if not self.match_selectors(el, sel):
                match = False
        return match

    def match_contains(self, el, contains):
        """Match element if it contains text."""

        types = (util.get_navigable_string_type(el),)
        match = True
        for c in contains:
            if c not in el.get_text(types=types):
                match = False
                break
        return match

    def match_default(self, el):
        """Match default."""

        match = False

        # Find this input's form
        form = None
        parent = el.parent
        while parent and form is None:
            if util.lower(parent.name) == 'form':
                form = parent
            else:
                parent = parent.parent

        # Look in form cache to see if we've already located its default button
        found_form = False
        for f, t in self.default_forms:
            if f is form:
                found_form = True
                if t is el:
                    match = True
                break

        # We didn't have the form cached, so look for its default button
        if not found_form:
            child_found = False
            for child in form.descendants:
                if not util.is_tag(child):
                    continue
                name = util.lower(child.name)
                # Can't do nested forms (haven't figured out why we never hit this)
                if name == 'form':  # pragma: no cover
                    break
                if name in ('input', 'button'):
                    for k, v in child.attrs.items():
                        if util.lower(k) == 'type' and util.lower(v) == 'submit':
                            child_found = True
                            self.default_forms.append([form, child])
                            if el is child:
                                match = True
                            break
                if child_found:
                    break
        return match

    def match_indeterminate(self, el):
        """Match default."""

        match = False
        name = el.attrs.get('name')

        def get_parent_form(el):
            """Find this input's form."""
            form = None
            parent = el.parent
            while form is None:
                if util.lower(parent.name) == 'form':
                    form = parent
                    break
                elif parent.parent:
                    parent = parent.parent
                else:
                    form = parent
                    break
            return form

        form = get_parent_form(el)

        # Look in form cache to see if we've already evaluated that its fellow radio buttons are indeterminate
        found_form = False
        for f, n, i in self.indeterminate_forms:
            if f is form and n == name:
                found_form = True
                if i is True:
                    match = True
                break

        # We didn't have the form cached, so validate that the radio button is indeterminate
        if not found_form:
            checked = False
            for child in form.descendants:
                if not util.is_tag(child) or child is el:
                    continue
                tag_name = util.lower(child.name)
                if tag_name == 'input':
                    is_radio = False
                    check = False
                    has_name = False
                    for k, v in child.attrs.items():
                        if util.lower(k) == 'type' and util.lower(v) == 'radio':
                            is_radio = True
                        elif util.lower(k) == 'name' and v == name:
                            has_name = True
                        elif util.lower(k) == 'checked':
                            check = True
                        if is_radio and check and has_name and get_parent_form(child) is form:
                            checked = True
                            break
                if checked:
                    break
            if not checked:
                match = True
            self.indeterminate_forms.append([form, name, match])

        return match

    def match_lang(self, el, langs):
        """Match languages."""

        match = False
        has_ns = self.supports_namespaces()

        # Walk parents looking for `lang` (HTML) or `xml:lang` XML property.
        parent = el
        found_lang = None
        while parent.parent and not found_lang:
            ns = self.is_html_ns(parent)
            for k, v in parent.attrs.items():
                if (
                    (self.is_xml and k == 'xml:lang') or
                    (
                        not self.is_xml and (
                            ((not has_ns or ns) and util.lower(k) == 'lang') or
                            (has_ns and not ns and util.lower(k) == 'xml:lang')
                        )
                    )
                ):
                    found_lang = v
                    break
            parent = parent.parent

        # Use cached meta language.
        if not found_lang and self.meta_lang:
            found_lang = self.meta_lang

        # If we couldn't find a language, and the document is HTML, look to meta to determine language.
        if not found_lang and not self.is_xml:
            found = False
            for tag in ('html', 'head'):
                found = False
                for child in parent.children:
                    if util.is_tag(child) and util.lower(child.name) == tag:
                        found = True
                        parent = child
                        break
                if not found:  # pragma: no cover
                    break

            if found:
                for child in parent:
                    if util.is_tag(child) and util.lower(child.name) == 'meta':
                        c_lang = False
                        content = None
                        for k, v in child.attrs.items():
                            if util.lower(k) == 'http-equiv' and util.lower(v) == 'content-language':
                                c_lang = True
                            if util.lower(k) == 'content':
                                content = v
                            if c_lang and content:
                                found_lang = content
                                self.meta_lang = found_lang
                                break
                    if found_lang:
                        break

        # If we determined a language, compare.
        if found_lang:
            for patterns in langs:
                match = False
                for pattern in patterns:
                    # print('PATTERN: ', pattern)
                    if pattern.match(found_lang):
                        # print('MATCHED')
                        match = True
                if not match:
                    break

        return match

    def match_selectors(self, el, selectors):
        """Check if element matches one of the selectors."""

        match = False
        is_not = selectors.is_not
        is_html = selectors.is_html
        if not (is_html and self.is_xml):
            for selector in selectors:
                match = is_not
                # We have a un-matchable situation (like `:focus` as you can focus an element in this environment)
                if isinstance(selector, ct.NullSelector):
                    continue
                # Verify tag matches
                if not self.match_tag(el, selector.tag):
                    continue
                # Verify `nth` matches
                if not self.match_nth(el, selector.nth):
                    continue
                if selector.flags & ct.SEL_EMPTY and not self.match_empty(el):
                    continue
                # Verify id matches
                if selector.ids and not self.match_id(el, selector.ids):
                    continue
                # Verify classes match
                if selector.classes and not self.match_classes(el, selector.classes):
                    continue
                # Verify attribute(s) match
                if not self.match_attributes(el, selector.attributes):
                    continue
                # Verify element is root
                if selector.flags & ct.SEL_ROOT and not self.match_root(el):
                    continue
                # Verify language patterns
                if selector.lang and not self.match_lang(el, selector.lang):
                    continue
                # Verify pseudo selector patterns
                if selector.selectors and not self.match_subselectors(el, selector.selectors):
                    continue
                # Verify relationship selectors
                if selector.relation and not self.match_relations(el, selector.relation):
                    continue
                # Validate that the current default selector match corresponds to the first submit button in the form
                if selector.flags & ct.SEL_DEFAULT and not self.match_default(el):
                    continue
                # Validate that the unset radio button is among radio buttons with the same name in a form that are
                # also not set.
                if selector.flags & ct.SEL_INDETERMINATE and not self.match_indeterminate(el):
                    continue
                if not self.match_contains(el, selector.contains):
                    continue
                match = not is_not
                break

        return match

    def is_html_ns(self, el):
        """Check if in HTML namespace."""

        ns = getattr(el, 'namespace') if el else None
        return ns and ns == NS_XHTML

    def match(self, el):
        """Match."""

        doc = el
        while doc.parent:
            doc = doc.parent
        root = None
        for child in doc.children:
            if util.is_tag(child):
                root = child
                break
        self.html_namespace = self.is_html_ns(root)
        self.is_xml = doc.is_xml and not self.html_namespace

        return util.is_tag(el) and el.parent and self.match_selectors(el, self.selectors)


class SoupSieve(ct.Immutable):
    """Match tags in Beautiful Soup with CSS selectors."""

    __slots__ = ("pattern", "selectors", "namespaces", "flags", "_hash")

    def __init__(self, pattern, selectors, namespaces, flags):
        """Initialize."""

        super().__init__(
            pattern=pattern,
            selectors=selectors,
            namespaces=namespaces,
            flags=flags
        )

    def _walk(self, node, capture=True, comments=False):
        """Recursively return selected tags."""

        match = CSSMatch(self.selectors, self.namespaces, self.flags).match

        # Walk children
        for child in node.descendants:
            if capture and util.is_tag(child) and match(child):
                yield child
            elif comments and util.is_comment(child):
                yield child

    def _sieve(self, node, capture=True, comments=False, limit=0):
        """Sieve."""

        if limit < 1:
            limit = None

        for child in self._walk(node, capture, comments):
            yield child
            if limit is not None:
                limit -= 1
                if limit < 1:
                    break

    def match(self, node):
        """Match."""

        return CSSMatch(self.selectors, self.namespaces, self.flags).match(node)

    def filter(self, nodes):  # noqa A001
        """Filter."""

        if util.is_tag(nodes):
            return [node for node in nodes.children if util.is_tag(node) and self.match(node)]
        else:
            return [node for node in nodes if self.match(node)]

    def comments(self, node, limit=0):
        """Get comments only."""

        return list(self.icomments(node, limit))

    def icomments(self, node, limit=0):
        """Iterate comments only."""

        yield from self._sieve(node, capture=False, comments=True, limit=limit)

    def select(self, node, limit=0):
        """Select the specified tags."""

        return list(self.iselect(node, limit))

    def iselect(self, node, limit=0):
        """Iterate the specified tags."""

        yield from self._sieve(node, limit=limit)

    def __repr__(self):  # pragma: no cover
        """Representation."""

        return "SoupSieve(pattern=%r, namespaces=%s, flags=%s)" % (self.pattern, self.namespaces, self.flags)

    __str__ = __repr__

    # ====== Deprecated ======
    @deprecated("Use 'SoupSieve.icomments' instead.")
    def commentsiter(self, node, limit=0):
        """Iterate comments only."""

        yield from self.icomments(node, limit)

    @deprecated("Use 'SoupSieve.iselect' instead.")
    def selectiter(self, node, limit=0):
        """Iterate the specified tags."""

        yield from self.iselect(node, limit)


ct.pickle_register(SoupSieve)
