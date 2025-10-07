from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageEnhance, ImageFilter
import io


app = FastAPI(title="MedTech Image Processor")


# Autoriser le frontend (pour démo on autorise tout)
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)




@app.get("/health")
async def health():
return {"status": "ok"}




@app.post("/process")
async def process_image(phase: str = Form(...), file: UploadFile = File(...)):
"""
Receives an uploaded image (form-data) and a phase ("arterial" or "venous").
Returns the processed image bytes (PNG).
"""
phase = phase.lower().strip()
if phase not in ("arterial", "venous"):
raise HTTPException(status_code=400, detail="phase must be 'arterial' or 'venous'")


contents = await file.read()
try:
img = Image.open(io.BytesIO(contents)).convert('RGB')
except Exception as e:
raise HTTPException(status_code=400, detail=f"Invalid image: {e}")


# --- Simulated processing ---
if phase == 'arterial':
# Increase contrast then slightly sharpen
enhancer = ImageEnhance.Contrast(img)
processed = enhancer.enhance(1.6) # 1.0 = original, >1 more contrast
# optional small sharpen by unsharp mask
processed = processed.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))
else: # venous
# Apply gaussian blur (smoothing). Pillow's GaussianBlur uses radius.
processed = img.filter(ImageFilter.GaussianBlur(radius=2.5))


# Return as PNG bytes
out_buf = io.BytesIO()
processed.save(out_buf, format='PNG')
out_buf.seek(0)
return Response(content=out_buf.read(), media_type='image/png')