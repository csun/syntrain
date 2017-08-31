This is the code from a small project I worked on during the summer of 2017. It explored the generation of image semantic segmentation training data from 3D renders. You can read about it [here](http://www.csun.io/2017/08/31/synthetic-cv-dataset.html).

# Training the Model
1. Download the NYU V2 labelled dataset and save it somewhere.
2. `cd src` and `pip3 install -r requirements.txt`
3. `cd ..` and run `python3 src/convert_nyu_v2.py <PATH TO NYU DATASET>`. This will populate model/nyu_data with the baseline data in the correct format.
4. Install `model/caffe-segnet-cudnn5` by following the instructions that are somewhere online :)
5. Create a symlink from `/SegNet` to the `model/` folder. Alternatively, you can go through all files and replace instances of `/SegNet` with the path to the model folder. Sorry, I know this isn't ideal, but it's how caffe-segnet wanted things to be installed.
6. Run `/SegNet/caffe-segnet-cudnn5/build/tools/caffe train -gpu <GPU_ID> -solver <SOLVER_PROTOTXT>`, where SOLVER_PROTOTXT is either `/SegNet/models/nyu_segnet_solver.prototxt` or `/SegNet/models/combined_segnet_solver.prototxt` based on whether or not you want to exclude the synthetic images I've generated already.
7. Wait for a long time depending on how good your gpu is. You may need to fiddle with batch size to get it to run more effectively - look at the [caffe-segnet tutorial](http://mi.eng.cam.ac.uk/projects/segnet/tutorial.html) for help here.
8. Run `python3 src/compute_bn_statistics.py` to generate your final .caffemodel file. I think that you can find info on this in the caffe-segnet tutorial.
9. Run `python3 src/score_model.py` on the images you want to test your model with.

# Generating Synthetic Examples
If you just want to see some synthetic examples I've already generated, look in `model/syn_data/images`. Otherwise, you can follow these steps to make your own.

1. Fire up [Blender](http://blender.org) and model and light a scene of your choosing (cycles rendering engine only).
2. Change your Blender scripts directory to point to `blender_scripts/`
3. Select relevant objects and use the `Label Selected (syntrain)` addon to apply a label to them.
4. Open `src/setup_blender_nodes.py` in your script editor. This will set up the compositor nodes to output the labels and images from your scene to a folder named `render/` in the same directory as your .blend file. If you make changes to labels after running this script, you need to delete these created compositor nodes and run it again. Again, not ideal, but it doesn't take that long.
5. Render your scene and check the `render/` folder for output.
6. Note that if you plan on using these images to train this model, you'll need to update the relevant `train.txt` file and recalculate the class weights using `python3 src/calculate_class_weighting.py`.
