from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.blocks import PageChooserBlock
from wagtail_color_panel.blocks import NativeColorBlock

# --- CHOICES ---
RICH_TEXT_BLOCK_FEATURES = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "strikethrough",
    "superscript",
    "subscript",
    "blockquote",
    "code",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
    "styles",
    "colour",
]

FEATURE_LAYOUT_CHOICES = [
    ("side-by-side-right", "Image Right, Text Left"),
    ("side-by-side-left", "Image Left, Text Right"),
    ("stacked-center", "Image Top, Text Centered Bottom"),
]

TEXT_ALIGNMENT_CHOICES = [
    ("start", "Left (Start)"),
    ("end", "Right (End)"),
    ("center", "Center"),
]

LINE_HEIGHT_CHOICES = [
    ("", "Default Line Height (lh-base)"),
    ("lh-1", "No extra leading (Single)"),
    ("lh-sm", "Small Line Height"),
    ("lh-lg", "Large Line Height (Double)"),
]


class RawHTMLBlock(blocks.RawHTMLBlock):
    """A block specifically for pasting raw, unvalidated HTML content."""
    class Meta:
        icon = 'code'
        label = 'Raw HTML'
        template = 'home/blocks/raw_html_block.html'


class FeatureBlock(blocks.StructBlock):
    """
    A customizable block for featuring an image and associated text/CTA.
    Used for the main feature sections on the HomePage.
    """
    image = ImageChooserBlock(required=True)
    title = blocks.CharBlock(required=True, max_length=150)
    text = blocks.RichTextBlock(
        required=True, 
        features=RICH_TEXT_BLOCK_FEATURES,
        help_text="Detailed text content for the feature section."
    )
    
    # CTA fields
    link_text = blocks.CharBlock(
        required=False, 
        max_length=50, 
        help_text="Text for the call-to-action button (e.g., 'Explore Now')"
    )
    link_page = blocks.PageChooserBlock(
        required=False, 
        help_text="Target page for the CTA button."
    )

    # Style fields
    layout_style = blocks.ChoiceBlock(
        choices=FEATURE_LAYOUT_CHOICES,
        default='side-by-side-right',
        help_text="Choose the arrangement of the image and text."
    )
    background_color = NativeColorBlock(
        required=False, 
        help_text="Optional: Set a custom background color for this block."
    )
    text_color = NativeColorBlock(
        required=False, 
        help_text="Optional: Set a custom text color for this block."
    )
    
    # Fine-tuning options
    text_alignment = blocks.ChoiceBlock(
        choices=TEXT_ALIGNMENT_CHOICES,
        default='start',
        required=False,
        label="Text Alignment",
        help_text="Horizontal alignment for the text content."
    )

    line_height = blocks.ChoiceBlock(
        choices=LINE_HEIGHT_CHOICES,
        default='',
        required=False,
        label="Line Height",
        help_text="Bootstrap line height utility class for text spacing."
    )

    class Meta:
        template = 'home/blocks/feature_block.html'
        icon = 'laptop'
        label = 'Feature Block (Image & Text)'