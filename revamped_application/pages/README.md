# Pages

This folder contains the different pages that will appear when you launch the Streamlit application.

There are a few things that you should note about the naming convention of the pages, and how they affect the order
in which pages are arranged in your application.

## Page

`Page`s are the foundation of a Streamlit application. They allow you to create complex applications with multiple
screens.

A `Page` is contained entirely in a Python file that follows the naming convention as specified above.

Since Streamlit follows a what-you-code-is-what-you-get approach to UI element arrangement, `Page`s are merely a
collection of Streamlit `elements` that are read and arranged from top to bottom.

## Naming Convention

All pages should be prefixed with a number. This number determines the overall order in which your pages will appear
on your application.

The number should then be immediately followed by an underscore `_`. The underscore helps to signal the end of
the page order number, and the beginning of your page name.

The name of the page should then be specified right after the underscore. The names of your pages should be UTF-8 encoded
(emojis are allowed!).

## Creating a Page

Create a new Python file following the naming convention as detailed above.

Paste this code at the top of your new Python file:

```python
import streamlit as st

from utils.streamlit_utils import init

init()

st.set_page_config(page_title="<YOUR PAGE NAME HERE>")
```

The code imports the `streamlit` library into your code and gives it the alias `st`. It also imports a utility function
`init()` that helps to set up the necessary [session states](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
for your application.

You may alter `init()` as you see fit, but make sure to **only append to the list of session state variables**, the core
list of session state variables **should not be altered**!

`st.set_page_config` helps to set up some basic information and metadata about your page.

Make sure to change `<YOUR PAGE NAME HERE>` entirely with the name of your page. You may also specify a page icon by
using the argument `page_icon` in `st.set_page_config`.

After pasting in the base code, you may import other libraries, use other Streamlit `elements`, etc. as you see fit.
Refer to the [API reference for Streamlit](https://docs.streamlit.io/develop/api-reference) for more information
about the different `elements` available to use.

## Updating a Page

To update the page details or content, simply modify the Python file that contains the page of interest.

## Deleting a Page

To delete a page, simply delete the Python file containing the page. Streamlit will automatically handle the removal
of that page from the application.
