# ModelAnimation
Render animated network diagrams from (simple) TensorFlow models.

This is an early stage commit.  Documentaiton is sparse. 

When calling `create_animation`, the options are as follows:

| Option    | Default     |
|-----------|------------|
|margin| 200|
|size|[1920, 1080]|
|node_size|90|
|node_gap| 40|
|background_rgba| (32, 32, 32, 0)|
|node_rgb| (248, 167, 3)|
|node_stroke| 5|
|conn_rgb| (81, 181, 237)|
|conn_max_width| 20|
|frame_numbers| False|
|frame_numbers_title| 'epoch'|
|frame_numbers_font| 'OpenSans-Regular.ttf'|
|frame_numbers_size| 50|
|frame_numbers_xy| (100,100)|
|frame_numbers_rgb| (50,50,50)|
|gif| False|
|gif_name| 'animation.gif'|
|fps| 5 |

See the example notebook to get you going.  More docs in the future...