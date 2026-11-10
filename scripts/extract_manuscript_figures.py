"""Extract embedded inline figure images in reading order from a local DOCX.

Figures are *manuscript images*, not regenerated experimental plots. Verify
caption-to-image mapping manually before making public claims.
"""
import argparse
from pathlib import Path
from docx import Document


def extract(src, out):
    doc=Document(src)
    out.mkdir(parents=True, exist_ok=True)
    for index, shape in enumerate(doc.inline_shapes, start=1):
        blips=shape._inline.xpath('.//a:blip')
        if len(blips)!=1:
            raise ValueError(f'Image {index}: expected one image resource')
        link=blips[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if not link:
            raise ValueError(f'Image {index}: no embedded rId')
        part=doc.part.related_parts[link]
        extension=Path(str(part.partname)).suffix.lower()
        if extension not in ('.png','.jpg','.jpeg','.webp','.tif','.tiff'):
            raise ValueError(f'Unexpected image extension: {extension}')
        destination=out/f'figure_{index:02d}{extension}'
        destination.write_bytes(part.blob)
        print(destination, len(part.blob), 'bytes')
    if len(doc.inline_shapes)!=16:
        print(f'WARNING: extracted {len(doc.inline_shapes)} inline images; expected 16; review source.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('manuscript',type=Path)
    p.add_argument('--out',type=Path,default=Path('figures/manuscript'))
    a=p.parse_args()
    extract(a.manuscript,a.out)
