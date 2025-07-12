
# 📦 Real-Time Production Line Monitoring System  



## 📌 Project Overview

This project implements a real-time monitoring system for assembly lines or production environments using **YOLOv8 object detection** and **ROI-based tracking**. The system captures video from a high-resolution camera (1920x1080), allows the user to select a **Region of Interest (ROI)**, and then tracks **people** and **products** inside that region. It logs how long each object remains in the ROI, useful for analyzing **operator activity**, **product handling**, and **assembly process timing**.

---

## 🎯 Main Objectives

- 🎥 Detect and track persons and products in real-time using YOLOv8.
- 🟩 Focus detection within a user-defined ROI to enhance accuracy and reduce noise.
- ⏱️ Measure how long each object remains in the ROI.
- 🧠 Maintain object identity using lightweight tracking (IoU + centroid distance).
- 📊 Log data for later analysis in `.csv` format.
- 🖼️ Display real-time results with annotated video feed.

---

## 🧰 Project Structure

```
Capstone-Project/
│
├── models/                  # YOLOv8 trained weights (.pt files)
├── rpi/                     # Raspberry Pi scripts (if applicable)
├── Interface/               # GUI/Front-end elements (future integration)
├── handdetection/           # Experimental hand detection modules
├── handtracking/            # Experimental hand tracking modules
├── roi_selector.py          # 🔍 Script for user to select ROI with mouse
├── roi_coordinates.csv      # Stores last selected ROI coordinates
├── roi_selector.csv         # Backup file for ROI
├── assembly_steps.csv       # Predefined steps or metadata for assembly
├── socket_test.py           # Simple socket test for remote communication
└── README.md                # 📘 Project documentation
```

---

## ⚙️ How It Works

### 🟩 ROI Selection

- The camera opens at **1920x1080** resolution.
- The user selects a rectangular region using the mouse (ROI).
- Only objects inside this ROI will be tracked.

### 🎯 Object Detection

- The system uses a YOLOv8 model trained on custom classes such as:
  - `person`
  - `product`
  - `backpack`, `handbag`, `bench`, etc.

### 🧠 Object Tracking + Timer

- Uses **IoU (Intersection over Union)** and **Euclidean distance** to maintain consistent tracking ID.
- Each object inside the ROI is assigned a unique ID.
- If the object is lost for less than **0.5 seconds**, it is retained (buffer logic).
- The timer runs for each object, displaying elapsed time on screen.

### 🗃️ Data Logging

- When an object leaves the ROI or disappears:
  - If it stayed longer than 10 seconds, its info is saved.
- Logs are saved as `Time_data.csv` with:
  - Object ID
  - Class
  - Start and End Time
  - Total Duration in seconds

---

## 🖥️ Technologies Used

| Technology | Purpose |
|------------|---------|
| 🐍 Python   | Main programming language |
| 🎯 YOLOv8 (Ultralytics) | Object detection |
| 🧠 OpenCV  | Computer vision & GUI display |
| 📊 Pandas  | Data logging and CSV handling |
| 📸 USB Camera | 1920x1080 resolution video input |
| 💻 VS Code / Jupyter | Development environment |

---

## 🧪 Example Use Cases

- 🔧 Track operator involvement at assembly stations.
- 🧾 Record duration of product inspection or packaging.
- 📈 Analyze process bottlenecks using presence duration logs.

---

## 🚀 How to Run

1. Clone or download the repo.
2. Make sure Python + dependencies are installed:
    ```bash
    pip install ultralytics opencv-python pandas
    ```
3. Place your YOLOv8 model in the `models/weights/` directory.
4. Run the main script:
    ```bash
    python main_tracking.py
    ```
5. Select ROI with your mouse.
6. Monitor, detect, and log!

---

## 📂 Output Example (Time_data.csv)

| ID | Class   | Start Time | End Time | Total Duration (s) |
|----|---------|------------|----------|---------------------|
| 1  | person  | 10:12:45 AM | 10:13:01 AM | 16.0 |
| 2  | product | 10:13:22 AM | 10:13:33 AM | 11.0 |

---


