import cv2
import numpy as np
import os
import json

def calibrate_fisheye_camera(image_folder, chessboard_size=(6, 9), square_size=1.0, output_file="camera_calibration.json"):
    """
    Calibrates a fisheye camera using chessboard images and saves the result.
    
    :param image_folder: Folder containing chessboard images.
    :param chessboard_size: Tuple indicating the number of inner corners (rows, columns).
    :param square_size: Size of each square in real-world units.
    :param output_file: File to save calibration results.
    """
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[1], 0:chessboard_size[0]].T.reshape(-1, 2)
    objp *= square_size
    objp = objp.astype(np.float32)  # Ensure correct type
    
    objpoints = []  # 3D points in real-world space
    imgpoints = []  # 2D points in image plane
    
    images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    valid_images = 0
    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            print(f"Could not read image: {fname}")
            continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        
        if ret:
            valid_images += 1
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), criteria)
            
            objpoints.append(objp.reshape(-1, 1, 3))
            imgpoints.append(corners.astype(np.float32))
            
            cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
            cv2.imshow('Valid Chessboard', img)
            cv2.waitKey(100)
            print(f"Valid chessboard: {fname}")
        else:
            print(f"Invalid chessboard: {fname}")
    
    cv2.destroyAllWindows()
    
    print(f"Found {valid_images} valid chessboard images")
    
    if valid_images < 10:
        print("Not enough valid chessboards for calibration. Need at least 10.")
        return None
    
    img_shape = gray.shape[::-1]
    
    K = np.eye(3)
    D = np.zeros((4, 1))
    
    try:
        ret, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
            objpoints, imgpoints, img_shape, K, D, None, None,
            cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_FIX_SKEW
        )
        
        print("Calibration successful!")
        print("Camera Matrix (K):", K)
        print("Distortion Coefficients (D):", D)
        print("RMS error:", ret)
        
        # Save calibration data
        calibration_data = {
            "camera_matrix": K.tolist(),
            "distortion_coefficients": D.tolist(),
            "rms_error": ret
        }
        
        with open(output_file, "w") as f:
            json.dump(calibration_data, f, indent=4)
        
        print(f"Calibration data saved to {output_file}")
        return K, D
    except cv2.error as e:
        print(f"Calibration failed: {e}")
    
    return None

if __name__ == "__main__":
    folder = "BIG_BOT/src/hardware/Camera/screenshots"  # Change to your chessboard images folder
    calibrate_fisheye_camera(folder)
