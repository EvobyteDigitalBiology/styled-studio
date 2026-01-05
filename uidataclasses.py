from pydantic import BaseModel
from typing import List, Dict

class StyledComponent(BaseModel):

    name: str
    preview_description: str
    description: str
    usage_pattern: str
    docs_url: str
    category: str
    version: str
    preview_image_url: str
    main_image_url: str
    code_examples: List[Dict]
    code_copy_template: str

