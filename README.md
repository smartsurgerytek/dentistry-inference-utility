# Image Processing Project

## <a name="GettingStarted"></a>Getting Started
First download a [model checkpoint](#model-checkpoints). Then the model can be used in just a few lines to get masks from a given prompt:
```
from segment_anything import SamPredictor, sam_model_registry
sam = sam_model_registry["<model_type>"](checkpoint="<path/to/checkpoint>")
predictor = SamPredictor(sam)
predictor.set_image(<your_image>)
masks, _, _ = predictor.predict(<input_prompts>)
```
