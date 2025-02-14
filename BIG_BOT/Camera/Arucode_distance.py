import cv2
import numpy as np
import glob


class ArucoDetector:
    def __init__(self):
        self.marker_size = 6.7 # Change the marker size according to the arucode size!!!!!!
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL) #Change to Dict.4x4_50 for real arucodes
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, cv2.aruco.DetectorParameters())
        self.detected_markers = {}
        self.camera_matrix = None
        self.dist_coeffs = None


    
    def calibrate_cam(self, chessboard_imgpath, chessboard_size):
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
            else:
                print("Camera calibration failed.")
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

    def calculate_distance(self, marker_size_pixels, cap_width):
        return self.marker_size_cm * cap_width / marker_size_pixels

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
    cap = cv2.VideoCapture(0)
    acd = ArucoDetector()

    # Perform camera calibration
    acd.calibrate_camera('chessboards/*.png', chessboard_size=(9, 6)) #Il faut rajouter des chessboards dedans

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detected_markers = acd.detect_markers(frame)
        if detected_markers:
            acd.draw_markers(frame)
            acd.draw_connections(frame)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
