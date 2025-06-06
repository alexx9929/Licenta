from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtCore import QObject
import DIContainer
from ResourcesManagement.SceneManager import SceneManager, Distribution
from ObjectBuilding.GameObject import GameObject
from threading import Thread
import time
from PySide6.QtGui import QVector3D, QQuaternion
import numpy as np
import ImageSearcher
from Utilities import MiscFunctions


class CameraController3D(Qt3DExtras.QFirstPersonCameraController):
    def __init__(self):
        super().__init__(DIContainer.scene)
        self.scene_manager = DIContainer.scene_manager
        self.camera_holder = DIContainer.scene.cameraHolder

        self.default_linear_speed = 50
        self.default_look_speed = 100

        self.setLinearSpeed(self.default_linear_speed)
        self.setLookSpeed(self.default_look_speed)
        self.setCamera(DIContainer.scene.cameraHolder.camera)

        # Focus parameters
        self.minimum_distance = 1
        self.initial_position = None
        self.initial_distance = None
        self.direction = None
        self.target = None
        self.target_position = None
        self.delta_rotation = None
        self.interpolation_factor = 0
        self.interpolation_step = 0.005
        self.released_control = False
        self.rotation_steps = None

        # Parallel camera control
        self.control_callback = None
        self.control_thread = Thread(target=self.control_camera)
        self.control_thread.start()

    def center_camera(self):
        if self.scene_manager.image_distribution == Distribution.planar:
            count = self.scene_manager.image_count
            images_per_row = self.scene_manager.imagesPerRow
            offset = self.scene_manager.imageOffset

            plane_size = GameObject.__DEFAULT__PLANE_LENGTH__()
            x_multiplier = (images_per_row / 2) if count >= images_per_row else count / 2
            y_multiplier = -(count / images_per_row) / 2

            if images_per_row % 2 != 0:
                x_multiplier -= 0.5

            if (images_per_row * images_per_row) % 2 != 0:
                y_multiplier += 0.5

            x_pos = (plane_size + offset) * x_multiplier
            y_pos = (plane_size + offset) * y_multiplier
            self.camera_holder.set_position(x_pos, y_pos, 10)

        if self.scene_manager.image_distribution == Distribution.normal:
            z_pos = self.scene_manager.normal_deviation[2] * 2
            DIContainer.scene.cameraHolder.set_position(0, 0, z_pos)

    def control_camera(self):
        """This function runs in a separate thread and controls the camera if there is a method for it"""
        while True:
            if self.control_callback:
                self.control_callback()
            else:
                time.sleep(0)

    def move_to_target(self):
        """This function moves and rotates the camera smoothly until it reaches its target
         while keeping the input inactive"""
        if self.interpolation_factor <= 1:
            delta = self.initial_distance * self.interpolation_factor * self.direction
            new_position = QVector3D(self.initial_position.x() + delta[0], self.initial_position.y() + delta[1],
                                     self.initial_position.z() + delta[2])
            self.interpolation_factor += self.interpolation_step
            self.camera_holder.set_position_vector(new_position)
            self.camera_holder.camera.rotate(self.rotation_steps)

            self.released_control = False
            DIContainer.main_window.repaint()

            self.camera_holder.print_rotation()
        else:
            if not self.released_control:
                DIContainer.input_handler.unblock_mouse_input()
                self.control_callback = None
                self.initial_position = None
                self.interpolation_factor = 0
                DIContainer.main_window.clicked_object = None
                self.released_control = True

    def start_movement_to_target(self, target_position: QVector3D):
        """Calculates the necessary parameters for a smooth transition to the target and starts
        the control thread that will move the camera"""
        self.initial_position = self.camera_holder.get_position()

        self.target_position = target_position
        self.calculate_initial_distance()

        if self.initial_distance < self.minimum_distance:
            self.target_position = None
            self.initial_position = None
            return

        self.calculate_direction()
        self.calculate_rotation_steps()

        # Starts movement
        DIContainer.input_handler.block_mouse_input()
        self.control_callback = self.move_to_target

    def start_movement_to_object(self, obj: GameObject):
        self.target = obj
        DIContainer.image_data_widget.set_data(obj)
        self.calculate_object_target_position(obj)
        self.start_movement_to_target(self.target_position)

    def start_movement_to_cluster(self, cluster_index: int):
        self.calculate_cluster_target_position(cluster_index)
        self.start_movement_to_target(self.target_position)

    def calculate_cluster_target_position(self, cluster_index: int):
        means = DIContainer.scene_manager.clusters_distributions[cluster_index][0]
        deviations = DIContainer.scene_manager.clusters_distributions[cluster_index][1]
        z_offset = 2
        x_pos = means[0]
        y_pos = means[1]
        z_pos = means[2] + deviations[2] * 3 + 2
        self.target_position = QVector3D(x_pos, y_pos, z_pos)

    def calculate_object_target_position(self, obj):
        """Calculates target position based on the position of the object"""
        z_offset = 2

        self.target_position = obj.transform.translation()
        self.target_position.setZ(self.target_position.z() + z_offset)

    def calculate_initial_distance(self):
        """Calculates the initial distance between the position of the camera and the target position"""
        p1 = [self.initial_position.x(), self.initial_position.y(), self.initial_position.z()]
        p2 = [self.target_position.x(), self.target_position.y(), self.target_position.z()]
        self.initial_distance = ImageSearcher.ImageSearcher.euclidian_distance(p1, p2)

    def calculate_direction(self):
        """Calculates the direction between initial and target position and normalizes it"""
        direction = self.target_position - self.camera_holder.get_position()
        direction_list = [direction.x(), direction.y(), direction.z()]
        self.direction = direction_list / np.linalg.norm(direction_list)

    def calculate_rotation_steps(self):
        """Divides the delta rotation into steps. Each iteration will rotate the
        camera by the same amount until the target rotation is reached"""
        target_rotation = QVector3D(0, 0, 0)
        number_of_steps = 1 / self.interpolation_step
        old_rotation = self.camera_holder.get_rotation()
        delta_rotation = target_rotation - old_rotation

        self.rotation_steps = QQuaternion.fromEulerAngles(delta_rotation.x() / number_of_steps,
                                                          delta_rotation.y() / number_of_steps,
                                                          delta_rotation.z() / number_of_steps)
