import cv2
import time

def measure_camera_resolution(camera_index=0):
    """
    Opens the camera, measures default resolution, and checks for common resolutions.
    
    Args:
        camera_index (int): Index of the camera to use (usually 0 for the default camera).
    """
    print(f"Attempting to access camera with index: {camera_index}...")
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not access camera {camera_index}. Please check connection or camera index.")
        return

    print("Camera opened successfully.")

    # Get default resolution
    default_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    default_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"\nDefault camera resolution: {default_width}x{default_height}")

    # List of common resolutions to check
    common_resolutions = [
        (640, 480),   # VGA
        (800, 600),   # SVGA
        (1024, 768),  # XGA
        (1280, 720),  # HD 720p
        (1920, 1080), # Full HD 1080p
        (2560, 1440), # 2K (QHD)
        (3840, 2160)  # 4K (UHD)
    ]

    print("\nChecking resolution support:")
    supported_resolutions = []
    for width, height in common_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        # Read values again after attempting to set
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if actual_width == width and actual_height == height:
            print(f"  - {width}x{height}: Supported")
            supported_resolutions.append(f"{width}x{height}")
        else:
            print(f"  - {width}x{height}: Not Supported (actual: {actual_width}x{actual_height})")

    if not supported_resolutions:
        print("No common supported resolutions found other than default.")
    
    # --- IMPORTANT FIX: Release and re-initialize the camera for a clean start ---
    cap.release()
    print("\nRe-initializing camera for video stream display...")
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not re-access camera {camera_index} for video stream. Exiting.")
        return
    
    # Set the camera to its default resolution (or a known supported resolution) for the display loop
    # This prevents issues if the last resolution tested was problematic.
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, default_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, default_height)
    print(f"Camera re-initialized to default resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    # --- END IMPORTANT FIX ---

    print("\nStarting video stream display (press 'q' to quit)...")
    
    prev_frame_time = 0 # Variable for FPS calculation
    new_frame_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break

        # Calculate and display FPS
        new_frame_time = time.time()
        fps = 0.0
        if prev_frame_time != 0:
            delta_time = new_frame_time - prev_frame_time
            if delta_time > 0:
                fps = 1.0 / delta_time
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        prev_frame_time = new_frame_time

        # Display current frame resolution
        current_res_text = f"Current Res: {frame.shape[1]}x{frame.shape[0]}"
        cv2.putText(frame, current_res_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Camera Resolution Test - Press Q to Quit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\nCamera resolution measurement program exited.")

if __name__ == "__main__":
    measure_camera_resolution(camera_index=0) # You can change the camera index if needed
