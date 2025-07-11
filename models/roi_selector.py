import cv2
import pandas as pd

def select_roi(camera_index=0, resolution=(1280, 720), csv_file="roi_selector.csv"):
    """
    Opens the camera, displays the feed, allows ROI selection, and shuts down the camera afterward.
    Saves the top-left and bottom-right coordinates of the selected ROI into a CSV file.
    """
    global roi_x1, roi_y1, roi_x2, roi_y2, drawing

    # Variables for ROI selection
    roi_x1, roi_y1, roi_x2, roi_y2 = -1, -1, -1, -1
    drawing = False

    # Mouse callback function for drawing ROI
    def draw_roi(event, x, y, flags, param):
        global roi_x1, roi_y1, roi_x2, roi_y2, drawing
        if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing
            drawing = True
            roi_x1, roi_y1 = x, y
        elif event == cv2.EVENT_MOUSEMOVE and drawing:  # Update rectangle as mouse moves
            roi_x2, roi_y2 = x, y
        elif event == cv2.EVENT_LBUTTONUP:  # Finish drawing
            drawing = False
            roi_x2, roi_y2 = x, y

    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None, None, None, None

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # Verify resolution
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera resolution set to: {int(actual_width)}x{int(actual_height)}")

    # Create a window and set the mouse callback
    cv2.namedWindow("Select ROI", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select ROI", draw_roi)

    print("Press and drag to draw the ROI. Press 'q' to confirm selection and quit.")
    while True:
        success, frame = cap.read()
        if not success:
            print("Error: Could not read from the camera.")
            break

        # Draw the ROI rectangle on the frame
        if roi_x1 != -1 and roi_y1 != -1 and roi_x2 != -1 and roi_y2 != -1:
            cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("Select ROI", frame)

        # Break the loop on 'q' or when ROI is selected
        key = cv2.waitKey(1)
        if key == ord('q') or (roi_x1 != -1 and roi_y1 != -1 and roi_x2 != -1 and roi_y2 != -1 and not drawing):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

    # Save ROI to a CSV file
    if roi_x1 != -1 and roi_y1 != -1 and roi_x2 != -1 and roi_y2 != -1:
        print(f"Selected ROI: Top-left ({roi_x1}, {roi_y1}), Bottom-right ({roi_x2}, {roi_y2})")
        
        # Create a DataFrame with the ROI data
        roi_data = {
            "TopLeft_X": [roi_x1],
            "TopLeft_Y": [roi_y1],
            "BottomRight_X": [roi_x2],
            "BottomRight_Y": [roi_y2],
        }
        df = pd.DataFrame(roi_data)
        
        # Append to the CSV file if it exists, or create a new one
        try:
            df.to_csv(csv_file, mode="a", index=False, header=not pd.io.common.file_exists(csv_file))
            print(f"ROI saved to {csv_file}")
        except Exception as e:
            print(f"Error saving ROI to CSV: {e}")
        
        return roi_x1, roi_y1, roi_x2, roi_y2
    else:
        print("No ROI selected.")
        return None, None, None, None


# Test the ROI Selector
if __name__ == "__main__":
    select_roi(camera_index=0, resolution=(1920, 1080))
