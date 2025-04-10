from pyppeteer import launch

async def html_to_png(html_content, output_image_path, **kwargs):
    """
    Provide html string, and export as png file.
    Will return a dict of element positions and sizes of elements given by the element_ids kwarg.
    Will fit the element given by wrapper id, if not given, fits body.
    To render transparently, use rgba.

    Must be run asynchronously:
    ```python
    import asyncio
    positions = asyncio.run(html_to_png())
    ```

    kwargs:
    - max_width
    - max_height
    - element_ids
    - wrapper_id
    """
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()

    await page.setViewport({'width': kwargs.get("max_width", 1920), 'height': kwargs.get("max_height", 1080)})
    await page.setContent(html_content)
    await page.waitForSelector('body')

    if kwargs.get("wrapper_id", None) != None:
        wrapper_el = await page.querySelector(f'#wrapper')
    else:
        wrapper_el = await page.querySelector(f'body')
    wrapper_el_bb = await wrapper_el.boundingBox()

    await page.screenshot({'path': output_image_path, 'clip': wrapper_el_bb, 'omitBackground': True})

    element_positions = {}
    if kwargs.get("element_ids", None):
        for elem_id in kwargs.get("element_ids"):
            try:
                element = await page.querySelector(f'#{elem_id}')
                if element:
                    bounding_box = await element.boundingBox()
                    element_positions[elem_id] = bounding_box
            except Exception as e:
                print(f"Error while retrieving position for {elem_id}: {e}")

    await browser.close()

    return element_positions