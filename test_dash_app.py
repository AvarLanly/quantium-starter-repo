"""
Test suite for Pink Morsel Sales Visualiser Dash app.
Tests verify that key UI components are present and functioning correctly.
Uses unit testing approach without requiring a browser.
"""

import pytest
from dash import Dash


def test_app_imports():
    """
    Test that the Dash app module can be imported successfully.
    Verifies the app instance is created without errors.
    """
    from dash_app import app
    assert app is not None
    assert isinstance(app, Dash)


def find_component_by_id(layout, target_id, _found=None):
    """
    Recursively search for a component with the given id in the layout tree.
    
    Args:
        layout: The Dash layout component to search within
        target_id: The id of the component to find
        _found: Internal parameter to track found component
    
    Returns:
        The component with the matching id, or None if not found
    """
    if _found is None:
        _found = [None]
    
    # Check if this component has the target id
    if hasattr(layout, 'id') and layout.id == target_id:
        _found[0] = layout
        return _found[0]
    
    # Recursively search through children
    if hasattr(layout, 'children'):
        children = layout.children
        if isinstance(children, list):
            for child in children:
                if _found[0] is None:
                    find_component_by_id(child, target_id, _found)
        elif _found[0] is None and children is not None:
            find_component_by_id(children, target_id, _found)
    
    return _found[0]


def find_text_in_layout(layout, search_text):
    """
    Recursively search for text content within the layout tree.
    
    Args:
        layout: The Dash layout component to search within
        search_text: The text string to search for
    
    Returns:
        True if the text is found, False otherwise
    """
    found = False
    
    # Recursively search through children
    if hasattr(layout, 'children'):
        children = layout.children
        if isinstance(children, list):
            for child in children:
                if find_text_in_layout(child, search_text):
                    found = True
                    break
        elif children is not None:
            if find_text_in_layout(children, search_text):
                found = True
    
    # Check if this component contains the text
    if hasattr(layout, 'children'):
        if isinstance(layout.children, str) and search_text in layout.children:
            found = True
        elif hasattr(layout, 'value') and layout.value and search_text in str(layout.value):
            found = True
    
    return found


def test_header_present():
    """
    Test that the header is present in the app layout.
    Verifies the main H1 title 'Pink Morsel Sales Visualiser' is displayed.
    """
    from dash_app import app
    
    # Check the app has a layout
    assert app.layout is not None
    
    # Search for the header text
    header_found = find_text_in_layout(app.layout, 'Pink Morsel Sales Visualiser')
    assert header_found, "Header 'Pink Morsel Sales Visualiser' not found in layout"


def test_visualisation_present():
    """
    Test that the line chart visualisation is present.
    Verifies the dcc.Graph component with id 'sales-line-chart' is rendered.
    """
    from dash_app import app
    
    # Find the graph component by searching recursively
    graph_component = find_component_by_id(app.layout, 'sales-line-chart')
    assert graph_component is not None, "Sales line chart component not found in layout"


def test_region_picker_present():
    """
    Test that the region picker radio buttons are present.
    Verifies the dcc.RadioItems component with all five region options:
    'all', 'north', 'east', 'south', 'west'.
    """
    from dash_app import app
    
    # Find the region selector component
    region_selector = find_component_by_id(app.layout, 'region-selector')
    assert region_selector is not None, "Region selector component not found in layout"
    
    # Check that it has the expected options
    assert hasattr(region_selector, 'options'), "Region selector has no options"
    option_values = [opt['value'] for opt in region_selector.options]
    assert 'all' in option_values, "'all' option not found"
    assert 'north' in option_values, "'north' option not found"
    assert 'east' in option_values, "'east' option not found"
    assert 'south' in option_values, "'south' option not found"
    assert 'west' in option_values, "'west' option not found"
