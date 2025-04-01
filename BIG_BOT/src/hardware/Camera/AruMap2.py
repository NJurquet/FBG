import numpy as np
import cv2
import cv2.aruco as aruco

#This codes displays the position of the aruco marker 25 based on the defined position of markers 21 and 23.


def undistort_image(frame, K, D, DIM, balance=0.0, dim2=None, dim3=None):
    """
    Undistort a fisheye image.

    Args:
        frame: Input frame to undistort
        K: Camera matrix
        D: Distortion coefficients
        DIM: Dimensions of the image
        balance: Balance factor between 0 and 1 (default is 0.0)
        dim2, dim3: Additional dimensions for cropping (optional)

    Returns:
        Undistorted frame
    """
    dim1 = frame.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    assert dim1[0] / dim1[1] == DIM[0] / DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"

    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image.
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, 5)
    undistorted_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    return undistorted_frame

def create_coordinate_mapping(frame, aruco_dict_type=cv2.aruco.DICT_4X4_50):
    """
    Detect ArUco markers in a frame and create a coordinate mapping.

    Args:
        frame: Input frame where markers will be detected
        aruco_dict_type: ArUco dictionary type

    Returns:
        Dictionary mapping marker IDs to their pixel coordinates, corners, and IDs
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Set up ArUco detector
    aruco_dict = aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    # Detect markers
    corners, ids, rejected = detector.detectMarkers(gray)

    # Create mapping dictionary
    marker_positions = {}

    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            # Get the center of the marker
            marker_corners = corners[i][0]
            center_x = np.mean(marker_corners[:, 0])
            center_y = np.mean(marker_corners[:, 1])
            marker_positions[int(marker_id)] = (center_x, center_y)

    return marker_positions, corners, ids

def load_calibration(self, file_path):
    try:
        calibration_data = np.load(file_path)
        self.camera_matrix = calibration_data['camera_matrix']
        self.dist_coeffs = calibration_data['dist_coeffs']
        print("Camera calibration data loaded successfully.")
    except FileNotFoundError:
        print(f"Calibration file not found: {file_path}")
    except KeyError:
        print("Calibration file is missing required data.")

def compute_transformation_matrix(src_points, dst_points):
    """
    Compute the transformation matrix from source to destination points.

    Args:
        src_points: List of source points [(x1,y1), (x2,y2)]
        dst_points: List of destination points [(x1',y1'), (x2',y2')]

    Returns:
        Transformation matrix
    """
    # We need at least 2 points to compute the transformation
    if len(src_points) < 2 or len(dst_points) < 2:
        raise ValueError("Need at least 2 points to compute transformation")

    # Convert points to numpy arrays
    src = np.array(src_points, dtype=np.float32).reshape(-1, 1, 2)
    dst = np.array(dst_points, dtype=np.float32).reshape(-1, 1, 2)

    # Calculate affine transformation
    transform_matrix, _ = cv2.estimateAffinePartial2D(src, dst)

    return transform_matrix

def apply_transformation(point, transform_matrix):
    """
    Apply transformation matrix to a point.

    Args:
        point: (x,y) tuple representing the point
        transform_matrix: 2x3 transformation matrix

    Returns:
        Transformed point
    """
    x, y = point
    point_array = np.array([x, y, 1])

    # Apply transformation
    transformed = np.dot(transform_matrix, point_array)

    return (transformed[0], transformed[1])

def main():
    # Open camera
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set camera resolution (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    DIM = (1280, 720)
    K = np.array([[640, 0, 639.5],
                  [0, 640, 359.5],
                  [0, 0, 1]])
    D = np.array([[-0.047631], [0.020278], [-0.005686], [0.000986]]) #Those are taken at random. The real values I found are wrong

    # Define marker IDs
    marker_id1, marker_id2 = 21, 23  # Markers used to define the coordinate system
    target_marker_id = 25  # The marker whose coordinates we want to display

    # Define the desired positions for the coordinate system markers
    desired_positions = {
        marker_id1: (0, 0),       # First marker at origin
        marker_id2: (0, 100)      # Second marker at (0, 100)
    }

    # Virtual point (where the cans are)
    virtual_points = [
        (-20, 130),
        (-30, 125)
    ]

    print("Press 'q' to quit")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Undistort the fisheye image
        undistorted_frame = undistort_image(frame, K, D, DIM)

        # Detect ArUco markers
        marker_positions, corners, ids = create_coordinate_mapping(undistorted_frame)

        # Draw detected markers
        if ids is not None:
            undistorted_frame = aruco.drawDetectedMarkers(undistorted_frame, corners, ids)

            # Check if we have both required markers for the coordinate system
            if marker_id1 in marker_positions and marker_id2 in marker_positions:
                # Source points (detected pixel coordinates)
                src_points = [marker_positions[marker_id1], marker_positions[marker_id2]]

                # Destination points (desired coordinates)
                dst_points = [desired_positions[marker_id1], desired_positions[marker_id2]]

                try:
                    # Find transformation matrices
                    # From pixel to desired coordinates (direct transform)
                    direct_transform = compute_transformation_matrix(src_points, dst_points)
                    
                    # From desired to pixel coordinates (inverse transform)
                    inverse_transform = compute_transformation_matrix(dst_points, src_points)

                    # Draw virtual points
                    for i, virtual_point in enumerate(virtual_points):
                        transformed_point = apply_transformation(virtual_point, inverse_transform)
                        x, y = transformed_point
                        cv2.circle(undistorted_frame, (int(x), int(y)), 10, (0, 255, 0), -1)
                        cv2.putText(undistorted_frame, f"Virtual Point ({virtual_point[0]}, {virtual_point[1]})",
                                    (int(x) + 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Check if target marker 25 is detected
                    if target_marker_id in marker_positions:
                        # Get pixel coordinates of marker 25
                        marker25_pixel = marker_positions[target_marker_id]
                        
                        # Transform pixel coordinates to our coordinate system
                        marker25_coords = apply_transformation(marker25_pixel, direct_transform)
                        
                        # Draw marker 25 with its coordinates in our system
                        x, y = marker25_pixel
                        cv2.circle(undistorted_frame, (int(x), int(y)), 10, (0, 0, 255), -1)
                        cv2.putText(undistorted_frame, f"Marker 25: ({marker25_coords[0]:.1f}, {marker25_coords[1]:.1f})",
                                    (int(x) + 10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # Draw marker coordinates for coordinate system markers
                    for marker_id, (x, y) in marker_positions.items():
                        if marker_id in desired_positions:
                            pos = desired_positions[marker_id]
                            cv2.putText(undistorted_frame, f"({pos[0]}, {pos[1]})",
                                      (int(x), int(y) - 30), cv2.FONT_HERSHEY_SIMPLEX,
                                      0.5, (255, 0, 0), 2)
                except Exception as e:
                    # In case of numerical errors
                    cv2.putText(undistorted_frame, f"Error: {str(e)}", (10, 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display information
        cv2.putText(undistorted_frame, "Looking for markers 21, 23 and 25", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('ArUco Coordinate Mapping', undistorted_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()