# Pages

This folder contains the different pages that will appear when you launch the Streamlit application.

There are a few things that you should note about the naming convention of the pages, and how they affect the order
in which pages are arranged in your application.

## Page

`Page`s are the foundation of a Streamlit application. They allow you to create complex applications with multiple
screens.

A `Page` is contained entirely in a Python file that follows the naming convention as specified above.

Since Streamlit follows a relatively low-code approach to UI element creation and arrangement, `Page`s are merely a
collection of Streamlit `elements` that are read and arranged from top to bottom.

It is hence important to think about the flow of your application first from top to bottom, and then from left to right.

## Naming Convention

All pages should be prefixed with a number. This number determines the overall order in which your pages will appear
on your application.

The number should then be immediately followed by an underscore `_`. The underscore helps to signal the end of
the page order number, and the beginning of your page name.

The name of the page should then be specified right after the underscore. The names of your pages should be UTF-8
encoded (emojis are allowed!).

> 🚨 Failure to prepend a number with the name of your file may result in your pages appearing out of order compared
> to how they were declared/arranged in this `pages` folder!

## Creating a Page

Create a new Python file following the naming convention as detailed above.

Paste this code at the top of your new Python file:

```python
import streamlit as st

from .core.system.logger import Logger
from .utils.streamlit_utils import init

init()
LOGGER = Logger("<YOUR PAGE NAME HERE>")

st.set_page_config(page_title="<YOUR PAGE NAME HERE>")

```

The code imports the `streamlit` library into your code and gives it the alias `st`. It also imports a utility function
`init()` that helps to set up the necessary [session states](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
for your application.

You may alter `init()` as you see fit, but make sure to **only append to the list of session state variables**, the core
list of session state variables **should not be altered**!

`LOGGER` represents an instance of a Logger that helps you to log actions taken within your application. You are highly
advised to use the Logger to debug your applications!

`st.set_page_config` helps to set up some basic information and metadata about your page.

Make sure to change `<YOUR PAGE NAME HERE>` entirely with the name of your page. You may also specify a page icon by
using the argument `page_icon` in `st.set_page_config`.

After pasting in the base code, you may import other libraries, use other Streamlit `elements`, etc. as you see fit.
Refer to the [API reference for Streamlit](https://docs.streamlit.io/develop/api-reference) for more information
about the different `elements` available to use.

## Updating a Page

To update the page details or content, simply modify the Python file that contains the page of interest. The changes
should appear immediately after the application is rerun (if the application is already in the running state prior
to the modification of the code).

## Deleting a Page

To delete a page, simply delete the Python file containing the page. Streamlit will automatically handle the removal
of that page from the application after the application is rerun (if the application is already in the running state prior
to the modification of the code).
