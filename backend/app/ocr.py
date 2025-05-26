
"""OCR pipeline for Sudoku grid extraction and digit recognition.

Requires:
  - opencv-python-headless
  - numpy
  - onnxruntime (model download during container build)
  - pyzbar (for QR token match)

Model:
  Default: MNIST‑style 28×28 digit classifier (10 classes 0‑9) located at
  /models/mnist.onnx. The Dockerfile fetches it automatically.
"""
from io import BytesIO
from typing import List, Tuple
import cv2, numpy as np
from PIL import Image
import onnxruntime as rt
import pyzbar.pyzbar as pyzbar

# Load ONNX model once
try:
    _sess = rt.InferenceSession("models/mnist.onnx", providers=["CPUExecutionProvider"])
    _input_name = _sess.get_inputs()[0].name
except Exception as e:
    _sess = None
    print("[OCR] Failed to load model:", e)

def decode_qr(
    """Decode qr."""image_bytes: bytes) -> str | None:
    img = Image.open(BytesIO(image_bytes))
    decoded = pyzbar.decode(img)
    if decoded:
        return decoded[0].data.decode()
    return None

def _extract_grid(
    """ extract grid."""image: np.ndarray) -> np.ndarray:
    """Warp the Sudoku grid to a square top‑down view."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV,11,2)
    contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if not contours:
        return image
    peri = cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], 0.02*peri, True)
    if len(approx)==4:
        pts = approx.reshape(4,2).astype(np.float32)
        # order points
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)
        tl, br = pts[np.argmin(s)], pts[np.argmax(s)]
        tr, bl = pts[np.argmin(diff)], pts[np.argmax(diff)]
        side = max([
            np.linalg.norm(br-tr),
            np.linalg.norm(tr-tl),
            np.linalg.norm(tl-bl),
            np.linalg.norm(bl-br)
        ])
        dst = np.array([[0,0],[side-1,0],[side-1,side-1],[0,side-1]], np.float32)
        M = cv2.getPerspectiveTransform(np.array([tl,tr,br,bl]), dst)
        warped = cv2.warpPerspective(gray, M, (int(side), int(side)))
        return warped
    return gray

def _split_into_cells(
    """ split into cells."""grid_img: np.ndarray, size:int)->List[np.ndarray]:
    h,w = grid_img.shape
    cell_h, cell_w = h//size, w//size
    cells=[]
    for r in range(size):
        for c in range(size):
            cell = grid_img[r*cell_h:(r+1)*cell_h, c*cell_w:(c+1)*cell_w]
            cells.append(cell)
    return cells

def _prepare_digit(
    """ prepare digit."""cell: np.ndarray) -> np.ndarray:
    # threshold & center
    _,th = cv2.threshold(cell,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    h,w = th.shape
    # crop bounding box
    ys, xs = np.where(th>0)
    if len(xs)==0:
        return None
    x1,x2,y1,y2 = xs.min(), xs.max(), ys.min(), ys.max()
    digit = th[y1:y2+1,x1:x2+1]
    # resize to 28x28
    digit = cv2.resize(digit,(28,28), interpolation=cv2.INTER_AREA)
    digit = digit.astype("float32")/255.0
    digit = digit.reshape(1,1,28,28)
    return digit

def predict_digits_grid(
    """Predict digits grid."""image_bytes: bytes, size:int=9)->Tuple[List[List[int]], List[List[float]]]:
    if _sess is None:
        raise RuntimeError("ONNX model not loaded")
    img_np = cv2.imdecode(np.frombuffer(image_bytes,np.uint8), cv2.IMREAD_COLOR)
    grid = _extract_grid(img_np)
    cells=_split_into_cells(grid,size)
    board=[[0]*size for _ in range(size)]
    conf=[[0.0]*size for _ in range(size)]
    for idx,cell in enumerate(cells):
        digit_input = _prepare_digit(cell)
        r,c = divmod(idx,size)
        if digit_input is None:
            continue
        out = _sess.run(None, {_input_name: digit_input})[0]
        pred = int(out.argmax())
        probability = float(out.max())
        if pred!=0 and probability>0.8:   # threshold
            board[r][c]=pred
            conf[r][c]=probability
    return board, conf
