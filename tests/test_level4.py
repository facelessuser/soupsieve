"""
Test selectors level 4.

```
[foo='bar' i]
:nth-child(an+b [of S]?)
:is(s1, s2, ...) / :matches(s1, s2, ...)
:where(s1, s2, ...) allowed, but due to our environment, works like `:is()`
:not(s1, s2, ...)
:has(> s1, ...)
```

Likely to be implemented:

- `:nth-col(n)` / `:nth-last-col(n)`: This needs further understanding before implementing and would likely only be
  implemented for HTML, XHTML, and HTML5. This would not be implemented for XML.

- `E || F`: This would need more understanding before implementation. This would likely only be implemented for HTML,
  XHTML, and HTML5. This would not be implemented for XML.

Not supported (with current opinions or plans the matter):

- `:blank`: This applies to inputs with empty or otherwise null input. Currently, there is no plans to implement this.

- `:dir(ltr)`: This applies to direction of text. This direction can be inherited from parents. Due to the way Soup
  Sieve process things, it would have to scan the parents and evaluate what is inherited. it doesn't account for the CSS
  `direction` value, which is a good thing. It is doable, but not sure worth the effort. In addition, it seems there is
  reference to being able to do something like `[dir=auto]` which would select either `ltr` or `rtl`. This seems to add
  additional logic in to attribute selections which would complicate things, but still technically doable. There are
  currently no plans to implement this.

- `:lang(en-*)`: As mentioned in level 2 tests, in documents, `:lang()` can take into considerations information in
  `meta` and other things in the header. At this point, there are no plans to implement this. If a reasonable proposal
  was introduced on how to support this, it may be considered.

- `:local-link`: In our environment, there is no document URL. This isn't currently practical. This will not be
  implemented.

- `:read-only` / `:read-write`: There are no plans to implement this at this time.

- `:required` / `:optional`: There are no plans to implement this at this time.

- `:placeholder-shown`: There are no plans to implement this at this time.

- `:indeterminate`: There are no plans to implement this at this time.

- `:valid` / `:invalid`: We currently to not validate values, so this doesn't make sense at this time.

- `:user-invalid`: User cannot alter things in our environment because there is no user interaction (we are not a
  browser). This will not be implemented.

- `:scope`: I'm not sure what this means or if it is even useful in our context. More information would be needed. It
  seems in an HTML document, this would normally just be `:root` as there is no way to specify a different reference at
  this time. I'm not sure it makes sense to bother implementing this.

- `:in-range` / `:out-of-range`: This applies to form elements only. You'd have to evaluate `value`, `min`, and `max`. I
  guess you can have numerical ranges and alphabetic ranges. Currently, there are no plans to implement this.

- `:current` / `:past` / `:future`: I believe this requires a live, in browser state to determine what is current, to
  then determine what is past and future. I don't think this is applicable to our environment.

- `:default`: This is in the same vain as `:checked`. If we ever implemented that, we'd probably implement this, but
  there are no plans to do so at this time.

- `:focus-within` / `:focus-visible`: There is no focus in our environment, so this will not be implemented.

- `:target-within`: Elements cannot be "targeted" in our environment, so this will not be implemented.

- `:playing` / `:paused`: Elements cannot be played or paused in our environment, so this will not be implemented.
"""
