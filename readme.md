# CVFIGHT

CVFIGHT maps human pose landmarks (via MediaPipe) to keyboard events (via pynput) using OpenCV for video capture/visualization. It is a prototype to control applications or games by body movements — e.g., pressing keys when wrists or knees enter a dynamically computed bounding box.

---

## Repository structure (key files)

- `main.py` — Primary realtime script. Captures webcam or video, runs MediaPipe Pose, computes a dynamic bounding box relative to head and knee, and emits keyboard events when selected landmarks enter that box.
- `newTest.py` — Alternate/earlier variant of the main loop with similar detection + keyboard logic.
- `testWrite.py` — Extracts frames from a video into `frames/frame{i}.jpg` (flips frames before saving).
- `testImage_bbox.py` — Runs pose detection on a single saved frame and visualizes the dynamic bounding box; useful for tuning box parameters.
- `testkeyboard.py` — Simple script that sends repeated key events for testing `pynput`.
- `requirements.txt` — Pinned Python dependencies used for development.
- `frames/` — (not committed) directory for saved frames used during testing.

---

## Requirements

- Python 3.8+ (tested with 3.11)
- Windows recommended (scripts use OS-level key events and examples assume Windows keyboard navigation).
- Install dependencies:

Windows (recommended)

```powershell
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
```

macOS / Linux

```bash
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

Important packages: mediapipe, opencv-python, pynput, numpy, matplotlib.

---

## How it works (overview)

1. Capture frames from a video file or webcam using OpenCV.
2. Use MediaPipe Pose to detect 33 pose landmarks per frame.
3. Convert normalized landmarks to pixel coordinates.
4. Compute a dynamic bounding box relative to the detected head (landmark 0) and knee (landmark 25) positions.
5. Track a set of "selected" indices (wrists and knees by default). When a tracked landmark enters the bounding box, emit a corresponding key press with `pynput`.
6. `hit_status` flags prevent repeated press events while a landmark remains inside the box; the key is released when the landmark leaves.

---

## Usage

- Realtime webcam:

```powershell
python main.py
```

- Use a video file:

  - Open `main.py` or `newTest.py` and set `VideoPath` to the path of your MP4 file (remove any accidental leading spaces).
  - Then run the script as above.

- Controls:
  - Press ESC in the OpenCV window to quit (scripts check `cv2.waitKey(1) == 27`).
  - The scripts may perform window switching (Alt+Tab / cmd navigation) at startup—be prepared.

---

## Configuration (what to edit)

- `VideoPath` — Set to `0` for webcam or to a file path for offline testing.
- `selected_indices` — Landmarks to monitor (default: [15, 16, 25, 26] for wrists and knees).
- `part_names` — Map landmark indices to [label, key] pairs. Example:
  - `16: ["left_wrist",'a']`
  - `15: ["right_wrist",'s']`
  - `25: ["right_knee",'x']`
  - `26: ["left_knee",'z']`
- Bounding box multipliers — Located near head/knee calculations in `main.py` / `newTest.py`. Tweak `int(0.129*h)`, `int(0.49*h)`, `int(0.03*w)`, `int(0.1*w)` to fit your camera and subject size.

---

## Safety & Important Notes

- The scripts generate OS-level synthetic key events using `pynput`. This can interact with other applications unexpectedly. Run in a controlled environment and be ready to regain control (Alt+Tab or use Task Manager if needed).
- Window switching is performed in some scripts at startup — they will change window focus.
- Make sure the target application is ready to receive key input (has focus).
- Press ESC to close the OpenCV window and stop the program.

---

## Troubleshooting

- No landmarks detected: ensure subject is fully visible, well-lit, and not occluded. MediaPipe expects a clear view of the body.
- Keys not received by target application: ensure the target has focus and OS doesn't block synthetic input. On some systems, accessibility/input protections can prevent synthetic events.
- Frames not saving with `testWrite.py`: ensure `frames/` folder exists or create it manually and check write permissions.
- If MediaPipe or OpenCV errors occur: confirm installed package versions match `requirements.txt` or update to compatible versions.

---

## Development ideas / next steps

- Add CLI arguments to choose video source, toggle keyboard-emulation, or change key mappings at runtime.
- Add a safety confirmation prompt before emitting OS-level key events.
- Provide an "emulation-free" debug mode that only draws on-screen indicators (no `pynput` usage).
- Create unit tests for landmark-to-pixel conversion and bounding-box logic (separate logic from I/O for testability).
- Add logging and a configuration file (JSON/YAML) for key mappings and box parameters.

---

## License & Attribution

- This project uses Google MediaPipe and OpenCV, which are subject to their respective licenses.

---
