## PDF Loader

`get_page_images(pno, full=False)`  
PDF only: Return a list of all images (directly or indirectly) referenced by the page.

PARAMETERS:
pno (int) – page number, 0-based, -∞ < pno < page_count.

full (bool) – whether to also include the referencer’s xref (which is zero if this is the page).

RETURN TYPE:
list

RETURNS:
a list of images referenced by this page. Each item looks like

(xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter, referencer)

Where

xref (int) is the image object number

smask (int) is the object number of its soft-mask image

width and height (ints) are the image dimensions

bpc (int) denotes the number of bits per component (normally 8)

colorspace (str) a string naming the colorspace (like DeviceRGB)

alt. colorspace (str) is any alternate colorspace depending on the value of colorspace

name (str) is the symbolic name by which the image is referenced

filter (str) is the decode filter of the image (Adobe PDF References, pp. 22).

referencer (int) the xref of the referencer. Zero if directly referenced by the page. Only present if full=True.

---

`extractBLOCKS()`  
Textpage content as a list of text lines grouped by block. Each list items looks like this:

(x0, y0, x1, y1, "lines in the block", block_no, block_type)
The first four entries are the block’s bbox coordinates, block_type is 1 for an image block, 0 for text. block_no is the block sequence number. Multiple text lines are joined via line breaks.

For an image block, its bbox and a text line with some image meta information is included – not the image content.

This is a high-speed method with just enough information to output plain text in desired reading sequence.

RETURN TYPE:
list
