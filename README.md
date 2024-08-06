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
<iframe width="560" height="315" src="https://www.youtube.com/embed/PAVJtOw4m-c" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>