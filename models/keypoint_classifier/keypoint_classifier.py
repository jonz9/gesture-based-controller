import numpy as np
import tensorflow as tf


# Keypoint classifier class for classifying static gestures
class KeypointClassifier(object):
    def __init__(
        self, model_path="models/keypoint_classifier/keypoint_classifier.tflite"
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)

        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    # classifies the gesture as outputs a corresponding index integer
    def __call__(self, landmark_list):
        input_details_tensor_index = self.input_details[0]["index"]
        self.interpreter.set_tensor(
            input_details_tensor_index, np.array([landmark_list], dtype=np.float32)
        )
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]["index"]
        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index
