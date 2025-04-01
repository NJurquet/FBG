import cv2
import numpy as np
import glob


class ArucoDetector:
    def __init__(self):
        self.marker_size_cm = 10 # Change the marker size according to the arucode size!!!!!!
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50) #Change to Dict.4x4_50 for real arucodes
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, cv2.aruco.DetectorParameters())
        self.detected_markers = {}
        self.camera_matrix = None
        self.dist_coeffs = None


    
    def calibrate_camera(self, chessboard_imgpath, chessboard_size):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

        objpoints = []
        imgpoints = []

        images = glob.glob(chessboard_imgpath)
        gray = None
        for img in images:
            img = cv2.imread(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
        if gray is not None:
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
            if ret:
                self.camera_matrix = mtx
                self.dist_coeffs = dist
                print("Camera calibration successful.")
                print(mtx)
            else:
                print("Camera calibration failed.")
        else:
            print("No valid chessboard images found for calibration.")
        
    def calibrate_fisheye_camera(self, chessboard_imgpath, chessboard_size):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objp = np.zeros((chessboard_size[0] * chessboard_size[1], 1, 3), np.float32)
        objp[:, :, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 1, 2)

        objpoints = []
        imgpoints = []

        images = glob.glob(chessboard_imgpath)

        gray = None
        for img in images:
            img = cv2.imread(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

            if ret:
                print(f"Successfully found corners in {img}")  # Add this line
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
                # Debug: Draw and display the corners
                cv2.drawChessboardCorners(img, chessboard_size, corners2, ret)
                cv2.imshow('Chessboard Corners', img)
                cv2.waitKey(50)
            else:
                print(f"Could not find corners in {img}")  # Add this line

        cv2.destroyAllWindows()

        if not objpoints:
            print("No valid chessboard images found!")
            return

        if gray is not None:
            # Use fisheye calibration function
            K = np.zeros((3, 3))
            D = np.zeros((4, 1))
            rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(len(objpoints))]
            tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for _ in range(len(objpoints))]

            ret, mtx, dist, rvecs, tvecs = cv2.fisheye.calibrate(
                objpoints,
                imgpoints,
                gray.shape[::-1],
                K,
                D,
                rvecs,
                tvecs,
                cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC,
                criteria
            )

            if ret:
                self.camera_matrix = mtx
                self.dist_coeffs = dist
                print("Fisheye camera calibration successful.")
                print(mtx)

                # Save the camera matrix and distortion coefficients to a file
                np.savez('camera_calibration.npz', camera_matrix=mtx, dist_coeffs=dist)
            else:
                print("Fisheye camera calibration failed.")
        else:
            print("No valid chessboard images found for calibration.")



    def detect_markers(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.camera_matrix is not None and self.dist_coeffs is not None:
            gray = cv2.undistort(gray, self.camera_matrix, self.dist_coeffs)
        corners, ids, _ = self.detector.detectMarkers(gray)
        self.detected_markers.clear()

        if ids is not None:
            for i in range(len(ids)):
                M = cv2.moments(corners[i][0])
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    marker_info = {
                        'ID': ids[i][0],
                        'Centroid': (cX, cY),
                        'Corners': corners[i][0]
                    }
                    self.detected_markers[ids[i][0]] = marker_info
        return self.detected_markers

    def calculate_marker_distance(self, frame):
            """
            Calculate precise marker distance using pose estimation
            """
            if self.camera_matrix is None or self.dist_coeffs is None:
                print("Camera needs to be calibrated first!")
                return {}

            # Detect markers
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = self.detector.detectMarkers(gray)
            
            distances = {}
            if ids is not None:
                # Estimate pose for each marker
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners, 
                    self.marker_size_cm, 
                    self.camera_matrix, 
                    self.dist_coeffs
                )
                
                for i, marker_id in enumerate(ids):
                    # Extract translation vector
                    tvec = tvecs[i][0]
                    
                    # Calculate distance (magnitude of translation vector)
                    distance = np.linalg.norm(tvec)
                    
                    distances[marker_id[0]] = {
                        'distance_cm': distance,
                        'x': tvec[0],
                        'y': tvec[1],
                        'z': tvec[2]
                    }
            
            return distances



    def calculate_marker_distance_solvepnp(self, frame):
        """
        Calculate marker distances using SolvePnP method
        """
        if self.camera_matrix is None or self.dist_coeffs is None:
            print("Camera needs to be calibrated first!")
            return {}

        # Detect markers
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)
        
        distances = {}
        if ids is not None:
            # Marker points in 3D (assuming square marker)
            marker_points = np.array([
                [-self.marker_size_cm/2, self.marker_size_cm/2, 0],
                [self.marker_size_cm/2, self.marker_size_cm/2, 0],
                [self.marker_size_cm/2, -self.marker_size_cm/2, 0],
                [-self.marker_size_cm/2, -self.marker_size_cm/2, 0]
            ], dtype=np.float32)

            for i, marker_id in enumerate(ids):
                # Get marker corners
                marker_corners = corners[i][0]
                
                # Solve PnP
                ret, rvec, tvec = cv2.solvePnP(
                    marker_points, 
                    marker_corners, 
                    self.camera_matrix, 
                    self.dist_coeffs
                )

                if ret:
                    # Calculate distance (magnitude of translation vector)
                    distance = np.linalg.norm(tvec)
                    
                    distances[marker_id[0]] = {
                        'distance_cm': distance,
                        'x': tvec[0][0],
                        'y': tvec[1][0],
                        'z': tvec[2][0],
                        'rvec': rvec  # rotation vector if needed
                    }

                    # Optional: Draw axis for visualization
                    frame = cv2.drawFrameAxes(
                        frame, 
                        self.camera_matrix, 
                        self.dist_coeffs, 
                        rvec, 
                        tvec, 
                        self.marker_size_cm/2
                    )
        
        return distances, frame

    def draw_marker_distances(self, frame, distances):
        """
        Draw marker distances on the frame
        """
        for marker_id, info in distances.items():
            # Find marker in detected markers
            if marker_id in self.detected_markers:
                marker_info = self.detected_markers[marker_id]
                corners = marker_info['Corners']
                
                # Calculate marker center
                M = cv2.moments(corners)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    # Draw distance information
                    distance_text = f"Marker {marker_id}: {info['distance_cm']:.2f} cm"
                    cv2.putText(frame, distance_text, 
                                (cX - 100, cY + 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                                (0, 255, 255), 2)
        
        return frame

    def draw_markers(self, frame):
            if self.detected_markers:
                for marker_id, marker_info in self.detected_markers.items():
                    cX, cY = marker_info['Centroid']
                    cv2.circle(frame, (cX, cY), 5, (255, 0, 255), -1)
                    marker_size_pixels = np.mean([np.linalg.norm(marker_info['Corners'][j] - marker_info['Corners'][(j + 1) % 4]) for j in range(4)])
                    distance_to_marker_cm = self.calculate_distance(marker_size_pixels, frame.shape[1])
                    cv2.putText(frame, f"Dist. to Marker {marker_id}: {distance_to_marker_cm:.2f} cm",
                                (cX - 120, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1)


def main():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    acd = ArucoDetector()

    # Perform calibration (ensure this is done correctly)
    acd.calibrate_fisheye_camera('BIG_BOT\src\hardware\Camera\screenshots/*.png', chessboard_size=(8, 6))

    while True:
            ret, frame = cap.read()
            if not ret:
                
                print("stop")
                break

            # Detect markers first
            acd.detect_markers(frame)

            # Calculate distances using SolvePnP
            distances, frame_with_axis = acd.calculate_marker_distance_solvepnp(frame)
            
            if distances:
                # Draw distances on the frame
                frame = acd.draw_marker_distances(frame_with_axis, distances)

            cv2.imshow('Marker Distances', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
