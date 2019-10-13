import numpy as np
import os
import tensorflow as tf

from distutils.version import StrictVersion
from matplotlib import pyplot as plt
from PIL import Image
from io import BytesIO

from tensorflow.models.research.object_detection.utils import ops as utils_ops
from tensorflow.models.research.object_detection.utils import label_map_util
from tensorflow.models.research.object_detection.utils import visualization_utils as vis_util

if StrictVersion(tf.__version__) < StrictVersion('1.12.0'):
    raise ImportError('Please upgrade your TensorFlow installation to v1.12.*.')


# Model name.
MODEL_NAME = 'ssd_mobilenet_v2_oid_v4_2018_12_12'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = 'object_detection/models/' + MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('object_detection/labels', 'oid_v4_label_map.pbtxt')

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[1], image.shape[2])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict, feed_dict={image_tensor: image})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.int64)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict


def detect_object(image_path="", output_size=(24, 14), output_path='result'):
    # If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
    # TEST_IMAGE_PATHS = [os.path.join(input_path, file_name)]
    figure = BytesIO()
    # Size, in inches, of the output images.
    IMAGE_SIZE = output_size
    image = Image.open(image_path)
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Actual detection.
    output_dict = run_inference_for_single_image(image_np_expanded, detection_graph)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks'),
        use_normalized_coordinates=True,
        line_thickness=4,
        min_score_thresh=0.2
    )
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(image_np)

    categories = []
    for i in range(len(output_dict['detection_scores'])):
        score = output_dict['detection_scores'][i]
        if score != 0:
            categories.append({
                'score': round(score, 2),
                'ymin': round(output_dict['detection_boxes'][i][0], 2),
                'xmin': round(output_dict['detection_boxes'][i][1], 2),
                'ymax': round(output_dict['detection_boxes'][i][2], 2),
                'xmax': round(output_dict['detection_boxes'][i][3], 2),
                'area': round((output_dict['detection_boxes'][i][2] - output_dict['detection_boxes'][i][0])
                        * (output_dict['detection_boxes'][i][3] - output_dict['detection_boxes'][i][1]), 2),
                'class_id': output_dict['detection_classes'][i],
                'class_name': category_index[output_dict['detection_classes'][i]]['name'],
            })
    # detection_mask => [ymin, xmin, ymax, xmax] => [left, right, top, bottom]
    # plt.savefig(os.path.join(output_path, 'media'), bbox_inches='tight')
    plt.savefig(figure)
    return figure, categories
